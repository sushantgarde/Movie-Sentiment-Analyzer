import requests
import re
import sys
import os
import time

# Allow imports from the project root (where app_logger.py lives)
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app_logger import get_logger

log = get_logger("tmdb_scraper")

# ─────────────────────────────────────────────────────────────────────────────
#  🔑 Get your FREE key at: https://www.themoviedb.org/settings/api
# ─────────────────────────────────────────────────────────────────────────────
TMDB_API_KEY = os.environ.get("TMDB_API_KEY", "554e826839d8ab9d1b65e68d83c61b1d")

BASE_URL = "https://api.themoviedb.org/3"

HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/120.0.0.0 Safari/537.36"
    )
}

MAX_RETRIES     = 2   # reduced from 3 → 2 for faster failure
RETRY_DELAY     = 1   # seconds between retries
REQUEST_TIMEOUT = 15  # seconds per attempt

# ── Proxy auto-detection (fixes VPN / corporate network issues) ───────────────
PROXIES = {
    "http":  os.environ.get("HTTP_PROXY")  or os.environ.get("http_proxy"),
    "https": os.environ.get("HTTPS_PROXY") or os.environ.get("https_proxy"),
}
PROXIES = {k: v for k, v in PROXIES.items() if v}


def clean_review(text: str) -> str:
    """
    Basic cleaning of a raw review string:
      - Strip leading/trailing whitespace
      - Collapse multiple newlines/spaces into a single space
      - Remove stray HTML tags
    """
    text = str(text).strip()
    text = re.sub(r'\s+', ' ', text)
    text = re.sub(r'<.*?>', '', text)
    return text


def _get_with_retry(url: str, params: dict, label: str = "") -> requests.Response | None:
    """
    Retry wrapper — retries up to MAX_RETRIES times on Timeout or ConnectionError.
    Automatically uses system proxy if HTTP_PROXY / HTTPS_PROXY env vars are set.
    """
    for attempt in range(1, MAX_RETRIES + 1):
        try:
            log.debug(f"[TMDB SCRAPER] {label} attempt {attempt}/{MAX_RETRIES} → {url}")
            resp = requests.get(
                url,
                params=params,
                headers=HEADERS,
                timeout=REQUEST_TIMEOUT,
                proxies=PROXIES or None,
            )
            log.debug(f"[TMDB SCRAPER] {label} status: {resp.status_code}")
            return resp
        except requests.exceptions.Timeout:
            log.warning(f"[TMDB SCRAPER] {label} timed out (attempt {attempt}/{MAX_RETRIES})")
        except requests.exceptions.ConnectionError as e:
            log.warning(f"[TMDB SCRAPER] {label} connection error (attempt {attempt}/{MAX_RETRIES}): {e}")
        except Exception as e:
            log.exception(f"[TMDB SCRAPER] {label} unexpected error: {e}")
            return None  # non-retryable
        if attempt < MAX_RETRIES:
            log.info(f"[TMDB SCRAPER] Retrying in {RETRY_DELAY}s…")
            time.sleep(RETRY_DELAY)
    log.error(f"[TMDB SCRAPER] {label} failed after {MAX_RETRIES} attempts.")
    return None


def get_tmdb_id(movie_name: str) -> int | None:
    """
    Search TMDB for a movie by name and return its TMDB movie ID.
    """
    log.info(f"[TMDB SCRAPER] Searching TMDB for: '{movie_name}'")

    if not TMDB_API_KEY:
        log.warning("[TMDB SCRAPER] TMDB API key not set — skipping TMDB reviews")
        return None

    url    = f"{BASE_URL}/search/movie"
    params = {
        "api_key":  TMDB_API_KEY,
        "query":    movie_name,
        "language": "en-US",
        "page":     1,
    }

    resp = _get_with_retry(url, params, label="search")
    if resp is None:
        return None

    if resp.status_code == 401:
        log.error("[TMDB SCRAPER] Invalid TMDB API key (401).")
        return None
    if resp.status_code != 200:
        log.warning(f"[TMDB SCRAPER] Search returned {resp.status_code}")
        return None

    data    = resp.json()
    results = data.get("results", [])

    if results:
        tmdb_id    = results[0]["id"]
        tmdb_title = results[0].get("title", "Unknown")
        log.info(f"[TMDB SCRAPER] Found — TMDB ID: {tmdb_id} | Title: '{tmdb_title}'")
        return tmdb_id
    else:
        log.warning(f"[TMDB SCRAPER] No TMDB results for '{movie_name}'")
        return None


def get_tmdb_reviews(imdb_id: str, movie_name: str, max_reviews: int = 50) -> tuple[list, str | None]:
    """
    Fetch up to `max_reviews` user reviews for a movie from TMDB (paginated).

    Parameters
    ----------
    imdb_id     : IMDb ID string (kept for API compatibility; TMDB ID resolved internally)
    movie_name  : Human-readable movie name used for TMDB search
    max_reviews : Maximum number of reviews to collect (default 50)

    Returns
    -------
    (reviews_list, source_label)
        reviews_list  : list of cleaned review strings
        source_label  : e.g. "TMDB (42)" or None
    """
    log.info(f"[TMDB SCRAPER] Starting fetch for '{movie_name}' | max={max_reviews}")

    if not TMDB_API_KEY:
        log.warning("[TMDB SCRAPER] TMDB API key not set — skipping TMDB reviews")
        return [], None

    # ── Step 1: Resolve TMDB ID ───────────────────────────────────────────────
    tmdb_id = get_tmdb_id(movie_name)
    if not tmdb_id:
        log.warning(f"[TMDB SCRAPER] Could not resolve TMDB ID for '{movie_name}'")
        return [], None

    # ── Step 2: Paginated review fetch ────────────────────────────────────────
    reviews = []
    page    = 1
    skipped = 0

    try:
        while len(reviews) < max_reviews:
            url    = f"{BASE_URL}/movie/{tmdb_id}/reviews"
            params = {
                "api_key":  TMDB_API_KEY,
                "language": "en-US",
                "page":     page,
            }
            log.debug(f"[TMDB SCRAPER] Fetching reviews page {page}")

            resp = _get_with_retry(url, params, label=f"reviews-page-{page}")
            if resp is None:
                log.error(f"[TMDB SCRAPER] Could not fetch page {page} after retries.")
                break

            if resp.status_code == 401:
                log.error("[TMDB SCRAPER] Invalid TMDB API key (401). Stopping.")
                break
            if resp.status_code != 200:
                log.warning(f"[TMDB SCRAPER] Non-200 ({resp.status_code}). Stopping.")
                break

            data        = resp.json()
            results     = data.get("results", [])
            total_pages = data.get("total_pages", 1)
            total_count = data.get("total_results", 0)

            log.info(
                f"[TMDB SCRAPER] Page {page}/{total_pages} — "
                f"{len(results)} reviews | total: {total_count}"
            )

            if not results:
                log.info(f"[TMDB SCRAPER] No more reviews on page {page}. Stopping.")
                break

            for r in results:
                raw_content = r.get("content", "")
                author      = r.get("author", "Anonymous")
                content     = clean_review(raw_content)

                if len(content) > 30:
                    reviews.append(content)
                    log.debug(
                        f"[TMDB SCRAPER] Review #{len(reviews)} | "
                        f"Author: '{author}' | Length: {len(content)} chars"
                    )
                else:
                    skipped += 1
                    log.debug(f"[TMDB SCRAPER] Skipped short review ({len(content)} chars)")

                if len(reviews) >= max_reviews:
                    log.info(f"[TMDB SCRAPER] Reached limit ({max_reviews}). Stopping.")
                    break

            if page >= total_pages:
                log.info(f"[TMDB SCRAPER] All {total_pages} pages fetched.")
                break

            page += 1

    except Exception as e:
        log.exception(f"[TMDB SCRAPER] Unexpected error: {e}")

    log.info(
        f"[TMDB SCRAPER] Done — collected: {len(reviews)} | "
        f"skipped: {skipped} | pages: {page}"
    )

    if reviews:
        return reviews, f"TMDB ({len(reviews)})"
    log.warning(f"[TMDB SCRAPER] No usable reviews for '{movie_name}'")
    return [], None