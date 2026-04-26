"""
rt_scraper.py
-------------
Scrapes Rotten Tomatoes audience reviews directly from the RT website.
No API key required — uses requests + BeautifulSoup.

RT review URL pattern:
    https://www.rottentomatoes.com/m/{slug}/reviews?type=user

Lives in: Sentiment_Analyzer/scraper/rt_scraper.py
"""

import requests
import re
import sys
import os
import time

from bs4 import BeautifulSoup

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from app_logger import get_logger

log = get_logger("rt_scraper")

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
# review_aggregator.py runs RT, IMDb, and TMDB-scraper simultaneously via
# ThreadPoolExecutor — sharing one Session caused race conditions and
# intermittent connection errors. Each HTTP call now opens its own Session
# via a context manager, which is fully thread-safe.


def _get_headers(index: int = 0) -> dict:
    return {
        "User-Agent":      USER_AGENTS[index % len(USER_AGENTS)],
        "Accept-Language": "en-US,en;q=0.9",
        "Accept":          "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
        "Accept-Encoding": "gzip, deflate, br",
        "Referer":         "https://www.rottentomatoes.com/",
    }


def clean_review(text: str) -> str:
    """Strip whitespace and stray HTML."""
    text = str(text).strip()
    text = re.sub(r'\s+', ' ', text)
    text = re.sub(r'<.*?>', '', text)
    return text


def _search_rt_slug(movie_name: str) -> str | None:
    """
    Search RT for a movie and return its slug (e.g. 'inception').
    Uses RT's search endpoint: https://www.rottentomatoes.com/search?search={name}
    """
    log.info(f"[RT] Searching for: '{movie_name}'")
    try:
        url = "https://www.rottentomatoes.com/search"
        # BUG FIX #7 (cont.): use a fresh per-call session instead of the shared module-level one
        with requests.Session() as session:
            resp = session.get(
                url,
                params={"search": movie_name},
                headers=_get_headers(0),
                timeout=12,
            )
        log.debug(f"[RT] Search HTTP {resp.status_code}")

        if resp.status_code != 200:
            log.warning(f"[RT] Search returned {resp.status_code}")
            return None

        soup = BeautifulSoup(resp.text, "html.parser")

        # RT search results — movie links look like /m/movie_slug
        # New RT layout uses <search-page-result> web components
        # Fallback: find all <a> with href matching /m/...
        links = soup.select("a[href*='/m/']")
        for link in links:
            href = link.get("href", "")
            m    = re.match(r".*/m/([^/?#]+)", href)
            if m:
                slug = m.group(1)
                log.info(f"[RT] Found slug: '{slug}' from href: {href}")
                return slug

        # Try JSON-LD or meta tags as fallback
        canonical = soup.find("link", {"rel": "canonical"})
        if canonical:
            m = re.search(r"/m/([^/?#]+)", canonical.get("href", ""))
            if m:
                return m.group(1)

        log.warning(f"[RT] No slug found for '{movie_name}'")
        return None

    except Exception as e:
        log.exception(f"[RT] Search error: {e}")
        return None


def _build_slug_from_name(movie_name: str) -> str:
    """
    Fallback: construct a likely RT slug from the movie name.
    e.g. "The Dark Knight" → "the_dark_knight"
    """
    slug = movie_name.lower().strip()
    slug = re.sub(r"[^\w\s]", "", slug)      # remove punctuation
    slug = re.sub(r"\s+", "_", slug)          # spaces → underscores
    return slug


def _scrape_rt_page(slug: str, page: int = 1, page_index: int = 0) -> tuple[list, bool]:
    """
    Scrape one page of RT audience reviews.

    Returns (reviews_list, has_next_page)
    """
    url = f"https://www.rottentomatoes.com/m/{slug}/reviews"
    params = {"type": "user", "page": str(page)}

    try:
        # BUG FIX #7 (cont.): fresh session per page call — thread-safe
        with requests.Session() as session:
            resp = session.get(
                url,
                params=params,
                headers=_get_headers(page_index),
                timeout=15,
            )
        log.debug(f"[RT] Reviews page {page} → HTTP {resp.status_code} | URL: {resp.url}")

        if resp.status_code == 404:
            log.warning(f"[RT] 404 for slug '{slug}'")
            return [], False
        if resp.status_code == 403:
            log.error("[RT] 403 — RT blocked the request.")
            return [], False
        if resp.status_code != 200:
            log.warning(f"[RT] HTTP {resp.status_code}")
            return [], False

        soup    = BeautifulSoup(resp.text, "html.parser")
        reviews = []

        # Method 1: New RT layout (2023+) — p.audience-reviews__review
        containers = soup.select("p.audience-reviews__review")
        if containers:
            for c in containers:
                text = clean_review(c.get_text(separator=" "))
                if len(text) > 30:
                    reviews.append(text)
            log.debug(f"[RT] Method 1 (audience-reviews__review) → {len(reviews)}")

        # Method 2: review-text class
        if not reviews:
            containers = soup.select("div.review-text, p.review-text")
            for c in containers:
                text = clean_review(c.get_text(separator=" "))
                if len(text) > 30:
                    reviews.append(text)
            log.debug(f"[RT] Method 2 (review-text) → {len(reviews)}")

        # Method 3: Any <p> inside a review card
        if not reviews:
            containers = soup.select("div.audience-reviews__review-wrap p")
            for c in containers:
                text = clean_review(c.get_text(separator=" "))
                if len(text) > 30:
                    reviews.append(text)
            log.debug(f"[RT] Method 3 (review-wrap p) → {len(reviews)}")

        # Check for next page
        has_next = False
        next_btn = (
            soup.select_one("a.js-prev-next-paging-link[data-direction='next']")
            or soup.select_one("button[data-qa='next']")
            or soup.select_one("a[data-qa='pagination-next']")
        )
        if next_btn:
            has_next = True

        # Also check if page number param still has content
        if not has_next and reviews:
            # heuristic: if we got a full page (usually 20), assume next page exists
            if len(reviews) >= 15:
                has_next = True

        return reviews, has_next

    except requests.exceptions.Timeout:
        log.error(f"[RT] Timeout on page {page}")
    except Exception as e:
        log.exception(f"[RT] Unexpected error: {e}")

    return [], False


def get_rt_reviews(movie_name: str, max_reviews: int = 50) -> tuple[list, str | None]:
    """
    Scrape audience reviews from Rotten Tomatoes for a movie.

    Parameters
    ----------
    movie_name  : e.g. 'Inception'
    max_reviews : cap on reviews (default 50)

    Returns
    -------
    (reviews_list, source_label)
    """
    log.info(f"[RT] Starting scrape for '{movie_name}' | max={max_reviews}")

    # Step 1: Find slug via search
    slug = _search_rt_slug(movie_name)

    # Step 2: Fallback to constructed slug if search failed
    if not slug:
        slug = _build_slug_from_name(movie_name)
        log.info(f"[RT] Using constructed slug: '{slug}'")

    all_reviews = []
    page        = 1
    page_index  = 0

    while len(all_reviews) < max_reviews:
        reviews, has_next = _scrape_rt_page(slug, page, page_index)

        if not reviews:
            log.info(f"[RT] No reviews on page {page}. Stopping.")
            break

        for rev in reviews:
            if len(all_reviews) >= max_reviews:
                break
            all_reviews.append(rev)

        log.info(f"[RT] Page {page} → +{len(reviews)} | total: {len(all_reviews)}")

        if not has_next or len(all_reviews) >= max_reviews:
            break

        page       += 1
        page_index += 1
        time.sleep(1.0)   # Be polite

    log.info(f"[RT] Done — {len(all_reviews)} reviews collected")

    if all_reviews:
        return all_reviews, f"Rotten Tomatoes ({len(all_reviews)})"
    log.warning(f"[RT] No reviews scraped for '{movie_name}'")
    return [], None