import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from concurrent.futures import ThreadPoolExecutor, as_completed
from app_logger import get_logger

from scraper.tmdb_scraper import get_tmdb_reviews
from scraper.imdb_scraper import get_imdb_reviews
from scraper.rt_scraper   import get_rt_reviews

log = get_logger("review_aggregator")

PER_SOURCE_MAX = 50


def get_all_reviews(
    imdb_id:    str,
    movie_name: str,
    max_total:  int = 150,
) -> tuple[list, str | None]:
    """
    Fetch reviews from TMDB, IMDb, and Rotten Tomatoes concurrently,
    then merge and deduplicate.

    Returns (reviews_list, source_summary_string)
    """
    log.info(
        f"[AGGREGATOR] Multi-source fetch — '{movie_name}' ({imdb_id}) "
        f"| max_total={max_total}"
    )

    sources = {
        "TMDB":            lambda: get_tmdb_reviews(imdb_id, movie_name, max_reviews=PER_SOURCE_MAX),
        "IMDb":            lambda: get_imdb_reviews(imdb_id,              max_reviews=PER_SOURCE_MAX),
        "Rotten Tomatoes": lambda: get_rt_reviews(movie_name,             max_reviews=PER_SOURCE_MAX),
    }

    raw_results: dict[str, tuple[list, str | None]] = {}
    errors: list[str] = []

    # ── Parallel fetch ────────────────────────────────────────────────────────
    with ThreadPoolExecutor(max_workers=3) as executor:
        future_map = {executor.submit(fn): name for name, fn in sources.items()}

        for future in as_completed(future_map):
            name = future_map[future]
            try:
                reviews, label    = future.result()
                raw_results[name] = (reviews or [], label)
                count = len(reviews or [])
                if count > 0:
                    log.info(f"[AGGREGATOR] ✓ '{name}' → {count} reviews")
                else:
                    log.warning(f"[AGGREGATOR] ✗ '{name}' → 0 reviews")
            except Exception as e:
                log.error(f"[AGGREGATOR] '{name}' raised exception: {e}")
                raw_results[name] = ([], None)
                errors.append(name)

    # ── Merge + deduplicate (TMDB → IMDb → RT) ───────────────────────────────
    all_reviews:   list[str]      = []
    seen:          set[str]       = set()
    source_counts: dict[str, int] = {}

    for name in ("TMDB", "IMDb", "Rotten Tomatoes"):
        revs, _ = raw_results.get(name, ([], None))
        added   = 0
        for rev in revs:
            fp = rev[:120].lower().strip()
            if fp and fp not in seen:
                seen.add(fp)
                all_reviews.append(rev)
                added += 1
            if len(all_reviews) >= max_total:
                break
        source_counts[name] = added
        if len(all_reviews) >= max_total:
            break

    parts = [
        f"{name} ({source_counts[name]})"
        for name in ("TMDB", "IMDb", "Rotten Tomatoes")
        if source_counts.get(name, 0) > 0
    ]
    source_summary = " · ".join(parts) if parts else None

    log.info(
        f"[AGGREGATOR] Done — total: {len(all_reviews)} | "
        f"breakdown: {source_summary or 'none'} | errors: {errors or 'none'}"
    )

    return all_reviews, source_summary