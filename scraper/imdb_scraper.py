"""
imdb_scraper.py
---------------
Scrapes IMDb user reviews directly from the IMDb website.
No API key required — uses requests + BeautifulSoup.

IMDb review URL pattern:
    https://www.imdb.com/title/{imdb_id}/reviews/

Lives in: Sentiment_Analyzer/scraper/imdb_scraper.py
"""

import requests
import re
import sys
import os
import time

from bs4 import BeautifulSoup

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from app_logger import get_logger

log = get_logger("imdb_scraper")

# Rotate user-agents to avoid blocks
USER_AGENTS = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
    "(KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 "
    "(KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36",
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 "
    "(KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36",
]

# BUG FIX #7: Removed module-level shared SESSION object.
# requests.Session is NOT thread-safe for concurrent use across threads.
# review_aggregator.py calls IMDb, TMDB-scraper, and RT simultaneously via
# ThreadPoolExecutor — sharing one Session caused race conditions and
# intermittent connection errors. Each request now creates its own Session
# (or uses requests.get directly), which is safe across threads.


def _get_headers(index: int = 0) -> dict:
    return {
        "User-Agent":      USER_AGENTS[index % len(USER_AGENTS)],
        "Accept-Language": "en-US,en;q=0.9",
        "Accept":          "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
        "Accept-Encoding": "gzip, deflate, br",
        "Referer":         "https://www.imdb.com/",
    }


def clean_review(text: str) -> str:
    """Strip whitespace and stray HTML."""
    text = str(text).strip()
    text = re.sub(r'\s+', ' ', text)
    text = re.sub(r'<.*?>', '', text)
    return text


def _scrape_page(imdb_id: str, pagination_key: str = None, page_index: int = 0) -> tuple[list, str | None]:
    """
    Scrape one page of IMDb reviews.

    Returns (reviews_on_this_page, next_pagination_key_or_None)
    """
    base_url = f"https://www.imdb.com/title/{imdb_id}/reviews/"
    params   = {"sort": "helpfulnessScore", "dir": "desc", "ratingFilter": "0"}
    if pagination_key:
        params["paginationKey"] = pagination_key

    try:
        # BUG FIX #7 (cont.): use a fresh per-call session instead of the shared module-level one
        with requests.Session() as session:
            resp = session.get(
                base_url,
                params=params,
                headers=_get_headers(page_index),
                timeout=15,
            )
        log.debug(f"[IMDb] Page {page_index + 1} → HTTP {resp.status_code} | URL: {resp.url}")

        if resp.status_code == 403:
            log.error("[IMDb] 403 — IMDb blocked the request. Stopping.")
            return [], None
        if resp.status_code == 404:
            log.warning(f"[IMDb] 404 — title {imdb_id} not found.")
            return [], None
        if resp.status_code != 200:
            log.warning(f"[IMDb] HTTP {resp.status_code}. Stopping.")
            return [], None

        soup = BeautifulSoup(resp.text, "html.parser")

        # ── Extract review texts ──────────────────────────────────────────────
        reviews = []

        # Method 1: New IMDb layout (2023+) — div.ipc-html-content-inner-div
        containers = soup.select("div.ipc-html-content-inner-div")
        if containers:
            for c in containers:
                text = clean_review(c.get_text(separator=" "))
                if len(text) > 50:
                    reviews.append(text)
            log.debug(f"[IMDb] Method 1 (ipc-html-content) → {len(reviews)} reviews")

        # Method 2: Old IMDb layout — div.text.show-more__control
        if not reviews:
            containers = soup.select("div.text.show-more__control")
            for c in containers:
                text = clean_review(c.get_text(separator=" "))
                if len(text) > 50:
                    reviews.append(text)
            log.debug(f"[IMDb] Method 2 (show-more__control) → {len(reviews)} reviews")

        # Method 3: Generic review content divs
        if not reviews:
            containers = soup.select("div.review-container div.content div.text")
            for c in containers:
                text = clean_review(c.get_text(separator=" "))
                if len(text) > 50:
                    reviews.append(text)
            log.debug(f"[IMDb] Method 3 (review-container) → {len(reviews)} reviews")

        # ── Extract pagination key for next page ──────────────────────────────
        next_key = None

        # New layout: data-testid="load-more-trigger" or similar
        load_more = soup.find("div", class_="load-more-data")
        if load_more and load_more.get("data-key"):
            next_key = load_more["data-key"]
        else:
            # Old layout: <div class="load-more-data" data-key="...">
            btn = soup.find(attrs={"data-key": True})
            if btn:
                next_key = btn["data-key"]

        return reviews, next_key

    except requests.exceptions.Timeout:
        log.error(f"[IMDb] Timeout on page {page_index + 1}")
    except requests.exceptions.ConnectionError as e:
        log.error(f"[IMDb] Connection error: {e}")
    except Exception as e:
        log.exception(f"[IMDb] Unexpected error: {e}")

    return [], None


def get_imdb_reviews(imdb_id: str, max_reviews: int = 50) -> tuple[list, str | None]:
    """
    Scrape user reviews from IMDb for the given title.

    Parameters
    ----------
    imdb_id     : e.g. 'tt1375666'
    max_reviews : cap on reviews (default 50)

    Returns
    -------
    (reviews_list, source_label)
    """
    log.info(f"[IMDb] Scraping reviews for {imdb_id} | max={max_reviews}")

    all_reviews    = []
    pagination_key = None
    page_index     = 0

    while len(all_reviews) < max_reviews:
        reviews, next_key = _scrape_page(imdb_id, pagination_key, page_index)

        if not reviews:
            log.info(f"[IMDb] No reviews on page {page_index + 1}. Stopping.")
            break

        for rev in reviews:
            if len(all_reviews) >= max_reviews:
                break
            all_reviews.append(rev)

        log.info(f"[IMDb] Page {page_index + 1} → +{len(reviews)} | total: {len(all_reviews)}")

        if not next_key or len(all_reviews) >= max_reviews:
            break

        pagination_key = next_key
        page_index    += 1
        time.sleep(1.0)   # Be polite — 1 second between pages

    log.info(f"[IMDb] Done — {len(all_reviews)} reviews collected")

    if all_reviews:
        return all_reviews, f"IMDb ({len(all_reviews)})"
    log.warning(f"[IMDb] No reviews scraped for {imdb_id}")
    return [], None