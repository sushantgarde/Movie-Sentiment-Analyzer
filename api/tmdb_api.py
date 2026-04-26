import requests
import sys
import os
import time

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app_logger import get_logger

log = get_logger("tmdb_api")

# ─────────────────────────────────────────────────────────────────────────────
#  🔑 Get your FREE key at: https://www.themoviedb.org/settings/api
# ─────────────────────────────────────────────────────────────────────────────
TMDB_API_KEY = os.environ.get("TMDB_API_KEY", "554e826839d8ab9d1b65e68d83c61b1d")
BASE_URL     = "https://api.themoviedb.org/3"
IMAGE_BASE   = "https://image.tmdb.org/t/p/w500"

HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/120.0.0.0 Safari/537.36"
    ),
    "Accept": "application/json",
}

# ── Tunable request settings ──────────────────────────────────────────────────
REQUEST_TIMEOUT = 15        # reduced from 30s → 15s for faster failure detection
MAX_RETRIES     = 2         # reduced from 3 → 2 to fail faster on bad networks
RETRY_DELAY     = 1         # seconds to wait between retries

# ── Proxy auto-detection (fixes VPN / corporate network issues) ───────────────
# Reads HTTP_PROXY / HTTPS_PROXY env vars automatically set by most VPNs/proxies
PROXIES = {
    "http":  os.environ.get("HTTP_PROXY")  or os.environ.get("http_proxy"),
    "https": os.environ.get("HTTPS_PROXY") or os.environ.get("https_proxy"),
}
# Remove None values so requests doesn't choke on them
PROXIES = {k: v for k, v in PROXIES.items() if v}


def _get_with_retry(url: str, params: dict, label: str = "") -> requests.Response | None:
    """
    Wrapper around requests.get() that retries on Timeout or ConnectionError.
    Automatically uses system proxy if HTTP_PROXY / HTTPS_PROXY env vars are set.

    Parameters
    ----------
    url    : Full URL to GET
    params : Query parameters dict
    label  : Short description for log messages (e.g. "search", "external_ids")

    Returns
    -------
    requests.Response on success, None on repeated failure
    """
    for attempt in range(1, MAX_RETRIES + 1):
        try:
            log.debug(f"[TMDB API] {label} attempt {attempt}/{MAX_RETRIES} → {url}")
            resp = requests.get(
                url,
                params=params,
                headers=HEADERS,
                timeout=REQUEST_TIMEOUT,
                proxies=PROXIES or None,
            )
            log.debug(f"[TMDB API] {label} status: {resp.status_code}")
            return resp

        except requests.exceptions.Timeout:
            log.warning(
                f"[TMDB API] {label} timed out (attempt {attempt}/{MAX_RETRIES}) "
                f"after {REQUEST_TIMEOUT}s"
            )
        except requests.exceptions.ConnectionError as e:
            log.warning(
                f"[TMDB API] {label} connection error (attempt {attempt}/{MAX_RETRIES}): {e}"
            )
        except Exception as e:
            log.exception(f"[TMDB API] {label} unexpected error: {e}")
            return None   # non-retryable

        if attempt < MAX_RETRIES:
            log.info(f"[TMDB API] Retrying in {RETRY_DELAY}s…")
            time.sleep(RETRY_DELAY)

    log.error(
        f"[TMDB API] {label} failed after {MAX_RETRIES} attempts. "
        f"Check your internet connection or firewall / VPN settings."
    )
    return None


# ─────────────────────────────────────────────────────────────────────────────
#  PRIVATE HELPER
# ─────────────────────────────────────────────────────────────────────────────

def _search_movie(movie_name: str) -> dict | None:
    """
    Search TMDB for a movie by name.
    Returns the first result dict from TMDB, or None if nothing found.
    """
    log.info(f"[TMDB API] Searching for movie: '{movie_name}'")

    url    = f"{BASE_URL}/search/movie"
    params = {
        "api_key":  TMDB_API_KEY,
        "query":    movie_name,
        "language": "en-US",
        "page":     1,
    }

    resp = _get_with_retry(url, params, label="search")
    if resp is None:
        log.error(
            "[TMDB API] Could not reach api.themoviedb.org. "
            "Possible causes: slow internet, firewall, or ISP blocking. "
            "Try using a VPN or check https://api.themoviedb.org/3/configuration "
            "in your browser."
        )
        return None

    if resp.status_code == 401:
        log.error("[TMDB API] Invalid API key (401). Check TMDB_API_KEY.")
        return None
    if resp.status_code != 200:
        log.warning(f"[TMDB API] Unexpected status {resp.status_code} for search.")
        return None

    data    = resp.json()
    results = data.get("results", [])

    if results:
        hit = results[0]
        log.info(
            f"[TMDB API] Found — TMDB ID: {hit['id']} | "
            f"Title: '{hit.get('title')}' | "
            f"Release: {hit.get('release_date', 'N/A')}"
        )
        return hit
    else:
        log.warning(f"[TMDB API] No results found for '{movie_name}'")
        return None


# ─────────────────────────────────────────────────────────────────────────────
#  PUBLIC FUNCTIONS  (called by app.py)
# ─────────────────────────────────────────────────────────────────────────────

def get_imdb_id(movie_name: str) -> str | None:
    """
    Fetch the IMDb ID for a given movie name via TMDB.

    Flow:
        1. Search TMDB  →  get TMDB movie ID
        2. Call /movie/{tmdb_id}/external_ids  →  get imdb_id field

    Returns:
        IMDb ID string  e.g. 'tt0111161'
        None if not found or on any error
    """
    log.info(f"[TMDB API] Fetching IMDb ID for: '{movie_name}'")

    hit = _search_movie(movie_name)
    if not hit:
        return None

    tmdb_id = hit["id"]

    url    = f"{BASE_URL}/movie/{tmdb_id}/external_ids"
    params = {"api_key": TMDB_API_KEY}

    resp = _get_with_retry(url, params, label="external_ids")
    if resp is None:
        return None

    if resp.status_code != 200:
        log.warning(f"[TMDB API] external_ids returned {resp.status_code} for TMDB ID {tmdb_id}")
        return None

    data    = resp.json()
    imdb_id = data.get("imdb_id")

    if imdb_id:
        log.info(f"[TMDB API] IMDb ID resolved: {imdb_id} for '{movie_name}'")
        return imdb_id
    else:
        log.warning(f"[TMDB API] No IMDb ID found for TMDB ID {tmdb_id}")
        return None


def get_movie_data(movie_name: str) -> dict | None:
    """
    Fetch full movie metadata for a given movie via TMDB.

    Makes ONE API call using append_to_response to get:
        - Core details  : title, year, genres, plot, runtime, rating, votes, poster
        - Credits       : director name, top-4 cast members
        - External IDs  : imdb_id

    Returns a dict with keys that match what app.py expects:
        Title, Year, Genre, Director, Actors, Plot,
        Poster, imdbRating, imdbVotes, Runtime

    Plus bonus TMDB-only keys (optional, used by templates):
        Tagline, Language, Country, tmdb_id, imdb_id
    """
    log.info(f"[TMDB API] Fetching full movie data for: '{movie_name}'")

    hit = _search_movie(movie_name)
    if not hit:
        return None

    tmdb_id = hit["id"]

    url    = f"{BASE_URL}/movie/{tmdb_id}"
    params = {
        "api_key":            TMDB_API_KEY,
        "language":           "en-US",
        "append_to_response": "credits,external_ids",
    }

    resp = _get_with_retry(url, params, label="movie_detail")
    if resp is None:
        return None

    if resp.status_code != 200:
        log.warning(f"[TMDB API] movie_detail returned {resp.status_code} for TMDB ID {tmdb_id}")
        return None

    d = resp.json()

    # ── Genres ────────────────────────────────────────────────────────────────
    genres = ", ".join(g["name"] for g in d.get("genres", [])) or "N/A"

    # ── Credits: director + top-4 actors ──────────────────────────────────────
    credits  = d.get("credits", {})
    crew     = credits.get("crew", [])
    cast     = credits.get("cast", [])

    director = next(
        (person["name"] for person in crew if person.get("job") == "Director"),
        "N/A"
    )
    actors = ", ".join(person["name"] for person in cast[:4]) or "N/A"

    # ── Poster ────────────────────────────────────────────────────────────────
    poster_path = d.get("poster_path")
    poster      = f"{IMAGE_BASE}{poster_path}" if poster_path else None

    # ── Rating & votes ────────────────────────────────────────────────────────
    vote_avg   = d.get("vote_average", 0)
    vote_count = d.get("vote_count", 0)

    # ── Runtime ───────────────────────────────────────────────────────────────
    runtime_min = d.get("runtime")
    runtime     = f"{runtime_min} min" if runtime_min else "N/A"

    # ── Release year ──────────────────────────────────────────────────────────
    release_date = d.get("release_date", "")
    year         = release_date[:4] if release_date else "N/A"

    # ── IMDb ID (from appended external_ids) ──────────────────────────────────
    ext_ids = d.get("external_ids", {})
    imdb_id = ext_ids.get("imdb_id", "N/A")

    # ── Spoken languages & production countries ────────────────────────────────
    language = ", ".join(
        lang["english_name"] for lang in d.get("spoken_languages", [])
    ) or "N/A"

    country = ", ".join(
        c["name"] for c in d.get("production_countries", [])
    ) or "N/A"

    # ── Build final dict ───────────────────────────────────────────────────────
    movie_data = {
        "Title":      d.get("title", movie_name),
        "Year":       year,
        "Genre":      genres,
        "Director":   director,
        "Actors":     actors,
        "Plot":       d.get("overview", "N/A"),
        "Poster":     poster,
        "imdbRating": str(round(vote_avg, 1)),
        "imdbVotes":  f"{vote_count:,}",
        "Runtime":    runtime,
        "tmdb_id":    tmdb_id,
        "imdb_id":    imdb_id,
        "Tagline":    d.get("tagline", ""),
        "Language":   language,
        "Country":    country,
    }

    log.info(
        f"[TMDB API] Movie data retrieved — "
        f"Title: '{movie_data['Title']}' | "
        f"Year: {movie_data['Year']} | "
        f"Rating: {movie_data['imdbRating']}/10 | "
        f"Votes: {movie_data['imdbVotes']} | "
        f"Director: {movie_data['Director']}"
    )
    return movie_data