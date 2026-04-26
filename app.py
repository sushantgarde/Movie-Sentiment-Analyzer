import sys
import os
import re       # BUG FIX #2: moved re import to top-level (was buried inside parse_source_counts)
import time

# ✅ Correct project root (IMPORTANT for Render)
PROJECT_ROOT = os.path.dirname(os.path.abspath(__file__))

# BUG FIX #1: removed duplicate sys.path block — the second if-check was dead code
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

from flask import Flask, render_template, request
import joblib

from api.tmdb_api               import get_imdb_id, get_movie_data
from scraper.review_aggregator  import get_all_reviews
from app_logger                 import get_logger

log = get_logger("app")

# ── Load ML model ──────────────────────────────────────────────────────────────
MODEL_DIR = os.path.join(PROJECT_ROOT, 'model')

log.info("[STARTUP] Loading ML model and vectorizer...")
try:
    model      = joblib.load(os.path.join(MODEL_DIR, 'sentiment_model.pkl'))
    vectorizer = joblib.load(os.path.join(MODEL_DIR, 'vectorizer.pkl'))
    log.info("[STARTUP] Model and vectorizer loaded successfully.")
except FileNotFoundError as e:
    log.critical(f"[STARTUP] Model file not found: {e}")
    log.critical("[STARTUP] Run training.ipynb first to generate model files.")
    raise
except Exception as e:
    log.critical(f"[STARTUP] Failed to load model/vectorizer: {e}")
    raise

# BUG FIX #3: use absolute path for template_folder so it resolves correctly on Render/production
app = Flask(__name__, template_folder=os.path.join(PROJECT_ROOT, "templates"))


# ── Helpers ────────────────────────────────────────────────────────────────────

def predict_reviews(reviews: list) -> list:
    """
    Run the ML sentiment model on each review text.

    Returns
    -------
    list of int  →  1 = Positive, 0 = Negative
    """
    if not reviews:
        return []

    log.info(f"[ML] Running sentiment prediction on {len(reviews)} reviews")
    predictions = []

    for i, review in enumerate(reviews, 1):
        try:
            vec  = vectorizer.transform([review])
            pred = int(model.predict(vec)[0])
            predictions.append(pred)
            log.debug(
                f"[ML] Review #{i}/{len(reviews)} → "
                f"{'Positive' if pred == 1 else 'Negative'} | "
                f"Preview: '{review[:60].strip()}...'"
            )
        except Exception as e:
            log.error(f"[ML] Prediction failed for review #{i}: {e}")
            predictions.append(0)   # default to negative on error

    pos = sum(predictions)
    neg = len(predictions) - pos
    log.info(f"[ML] Done — Positive: {pos} | Negative: {neg} | Total: {len(predictions)}")
    return predictions


def rating_verdict(rating_str: str):
    """
    Convert a numeric rating string (0–10) into a 3-tier verdict.

    Returns  (verdict_label, css_class, score_float)
    """
    try:
        score = float(str(rating_str).split('/')[0])
        if score >= 7.0:
            verdict, cls = "Positive 😊", "positive"
        elif score >= 4.0:
            verdict, cls = "Mixed 😐",    "mixed"
        else:
            verdict, cls = "Negative 😞", "negative"
        log.debug(f"[RATING] Score {score} → {verdict}")
        return verdict, cls, score
    except Exception as e:
        log.warning(f"[RATING] Could not parse rating '{rating_str}': {e}")
        return None, "na", None


def parse_source_counts(source_summary: str | None) -> dict:
    """
    Parse the aggregator source summary string into a dict.

    e.g. "TMDB (30) · IMDb (25) · Rotten Tomatoes (18)"
         → {"TMDB": 30, "IMDb": 25, "Rotten Tomatoes": 18}
    """
    counts = {"TMDB": 0, "IMDb": 0, "Rotten Tomatoes": 0}
    if not source_summary:
        return counts
    # BUG FIX #2 (cont.): re is now imported at module level — no repeated import here
    for name in counts:
        m = re.search(rf"{re.escape(name)}\s*\((\d+)\)", source_summary)
        if m:
            counts[name] = int(m.group(1))
    return counts


# ── Core prediction pipeline ───────────────────────────────────────────────────

def predict_movie(movie_name: str):
    """
    Full prediction pipeline for a given movie name.

    Steps
    -----
    1. Resolve IMDb ID via TMDB
    2. Fetch full movie metadata via TMDB
    3. Fetch up to 150 reviews from TMDB + IMDb + Rotten Tomatoes (parallel)
    4. Run ML sentiment model
    5. Fall back to TMDB rating verdict if no reviews found
    6. Build and return movie_info dict for the template

    Returns
    -------
    (movie_info dict, None)  on success
    (None, error_str)        on failure
    """
    start_time = time.time()
    log.info("=" * 60)
    log.info(f"[REQUEST] New prediction request: '{movie_name}'")

    try:
        # ── Step 1: Resolve IMDb ID ───────────────────────────────────────────
        log.info(f"[STEP 1] Fetching IMDb ID for '{movie_name}'")
        imdb_id = get_imdb_id(movie_name)
        if not imdb_id:
            log.warning(f"[STEP 1] IMDb ID not found for '{movie_name}'")
            return None, "❌ Movie not found. Please check the movie name."
        log.info(f"[STEP 1] IMDb ID: {imdb_id}")

        # ── Step 2: Fetch movie metadata ──────────────────────────────────────
        log.info(f"[STEP 2] Fetching metadata for '{movie_name}'")
        data = get_movie_data(movie_name)
        if not data:
            log.error(f"[STEP 2] Could not fetch metadata for '{movie_name}'")
            return None, "❌ Could not fetch movie data. Please try again."
        log.info(
            f"[STEP 2] Metadata OK — '{data.get('Title')}' ({data.get('Year')}) | "
            f"Rating: {data.get('imdbRating')}/10"
        )

        # ── Step 3: Fetch reviews (parallel) ──────────────────────────────────
        log.info(f"[STEP 3] Fetching multi-source reviews (max 150)")
        reviews, source = get_all_reviews(imdb_id, movie_name, max_total=150)
        log.info(f"[STEP 3] Reviews: {len(reviews)} | Sources: {source or 'None'}")

        source_counts = parse_source_counts(source)

        # ── Step 4: ML sentiment prediction ───────────────────────────────────
        ml_verdict  = None
        ml_class    = None
        pos_pct     = None
        neg_pct     = None
        predictions = []

        if reviews:
            log.info(f"[STEP 4] Running ML model on {len(reviews)} reviews")
            predictions = predict_reviews(reviews)
            total       = len(predictions)

            if total > 0:   # ← guard against division by zero
                pos_count = sum(predictions)
                pos_pct   = round((pos_count / total) * 100, 1)
                neg_pct   = round(100 - pos_pct, 1)

                if pos_pct >= 60:
                    ml_verdict, ml_class = "Positive 😊", "positive"
                elif pos_pct <= 40:
                    ml_verdict, ml_class = "Negative 😞", "negative"
                else:
                    ml_verdict, ml_class = "Mixed 😐",    "mixed"

                log.info(
                    f"[STEP 4] Verdict: {ml_verdict} | "
                    f"Positive: {pos_pct}% | Negative: {neg_pct}%"
                )
            else:
                log.warning("[STEP 4] Predictions list empty after model run")
        else:
            log.warning("[STEP 4] No reviews — skipping ML prediction")

        # ── Step 5: TMDB rating fallback ──────────────────────────────────────
        tmdb_rating = data.get('imdbRating', 'N/A') or 'N/A'
        log.info(f"[STEP 5] TMDB rating: {tmdb_rating}")

        rating_label, rating_class, score = (
            rating_verdict(tmdb_rating)
            if tmdb_rating != 'N/A'
            else (None, 'na', None)
        )

        # ── Step 6: Choose final verdict ──────────────────────────────────────
        if ml_verdict:
            overall       = ml_verdict
            overall_class = ml_class
            overall_basis = (
                f"ML model on {len(reviews)} reviews · "
                f"TMDB ({source_counts['TMDB']}) · "
                f"IMDb ({source_counts['IMDb']}) · "
                f"RT ({source_counts['Rotten Tomatoes']})"
            )
            log.info(f"[STEP 6] Final verdict (ML): {overall}")

        elif rating_label:
            overall       = rating_label
            overall_class = rating_class
            overall_basis = f"TMDB rating fallback ({tmdb_rating}/10) — no reviews found"
            log.info(f"[STEP 6] Final verdict (rating fallback): {overall}")

        else:
            overall       = "Unknown"
            overall_class = "na"
            overall_basis = "Insufficient data"
            log.warning(f"[STEP 6] Could not determine verdict for '{movie_name}'")

        # ── Build template context dict ────────────────────────────────────────
        elapsed = round(time.time() - start_time, 2)
        log.info(f"[REQUEST] Completed in {elapsed}s — '{movie_name}' → {overall}")
        log.info("=" * 60)

        movie_info = {
            # Core details
            'title':         data.get('Title',     movie_name),
            'year':          data.get('Year',       'N/A'),
            'genre':         data.get('Genre',      'N/A'),
            'director':      data.get('Director',   'N/A'),
            'actors':        data.get('Actors',     'N/A'),
            'plot':          data.get('Plot',       'N/A'),
            'poster':        data.get('Poster',     None),
            'runtime':       data.get('Runtime',    'N/A'),
            # Rating
            'rating':        tmdb_rating,
            'score':         score,
            'votes':         data.get('imdbVotes',  'N/A'),
            'rating_label':  rating_label,
            'rating_class':  rating_class,
            # ML results
            'ml_verdict':    ml_verdict,
            'ml_class':      ml_class,
            'pos_pct':       pos_pct,
            'neg_pct':       neg_pct,
            'review_count':  len(reviews),
            'source':        source,
            'source_counts': source_counts,
            'reviews':       list(zip(reviews, predictions)),
            # Final verdict
            'overall':       overall,
            'overall_class': overall_class,
            'overall_basis': overall_basis,
            # Performance
            'elapsed':       elapsed,
            # Extra TMDB fields
            'tagline':       data.get('Tagline',  ''),
            'language':      data.get('Language', 'N/A'),
            'country':       data.get('Country',  'N/A'),
            'imdb_id':       data.get('imdb_id',  'N/A'),
            'tmdb_id':       data.get('tmdb_id',  'N/A'),
        }

        return movie_info, None

    except Exception as e:
        elapsed = round(time.time() - start_time, 2)
        log.exception(f"[REQUEST] Unhandled error after {elapsed}s for '{movie_name}': {e}")
        return None, f"⚠️ An unexpected error occurred: {str(e)}"


# ── Flask routes ───────────────────────────────────────────────────────────────

@app.route('/', methods=['GET', 'POST'])
def home():
    movie_info = None
    error      = None

    if request.method == 'POST':
        movie_name = request.form.get('movie', '').strip()
        client_ip  = request.remote_addr

        log.info(f"[HTTP] POST / | IP: {client_ip} | Movie: '{movie_name}'")

        if not movie_name:
            log.warning(f"[HTTP] Empty movie name from IP: {client_ip}")
            error = "❌ Please enter a movie name."
        else:
            movie_info, error = predict_movie(movie_name)

        if error:
            log.warning(f"[HTTP] Returning error to client: {error}")

    else:
        log.debug(f"[HTTP] GET / | IP: {request.remote_addr}")

    return render_template('index.html', movie=movie_info, error=error)


@app.errorhandler(404)
def not_found(e):
    log.warning(f"[HTTP] 404 — {request.url}")
    return "404 - Page not found", 404


@app.errorhandler(500)
def server_error(e):
    log.error(f"[HTTP] 500 — {request.url} | {e}")
    return "500 - Internal server error", 500


if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)