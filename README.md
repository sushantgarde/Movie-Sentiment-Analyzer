<div align="center">

```
   ██████╗██╗███╗   ██╗███████╗███████╗ ██████╗ ██████╗ ██████╗ ███████╗
  ██╔════╝██║████╗  ██║██╔════╝██╔════╝██╔════╝██╔═══██╗██╔══██╗██╔════╝
  ██║     ██║██╔██╗ ██║█████╗  ███████╗██║     ██║   ██║██████╔╝█████╗
  ██║     ██║██║╚██╗██║██╔══╝  ╚════██║██║     ██║   ██║██╔═══╝ ██╔══╝
  ╚██████╗██║██║ ╚████║███████╗███████║╚██████╗╚██████╔╝██║     ███████╗
   ╚═════╝╚═╝╚═╝  ╚═══╝╚══════╝╚══════╝ ╚═════╝ ╚═════╝ ╚═╝     ╚══════╝
```

### 🎬 *"Where AI meets the silver screen"*

**An intelligent movie sentiment analysis engine that reads the crowd so you don't have to.**

---

![Python](https://img.shields.io/badge/Python-3.10+-3776AB?style=for-the-badge&logo=python&logoColor=white)
![Flask](https://img.shields.io/badge/Flask-2.3+-000000?style=for-the-badge&logo=flask&logoColor=white)
![scikit-learn](https://img.shields.io/badge/scikit--learn-1.2+-F7931E?style=for-the-badge&logo=scikit-learn&logoColor=white)
![BeautifulSoup](https://img.shields.io/badge/BeautifulSoup4-4.12+-59B37A?style=for-the-badge)
![Accuracy](https://img.shields.io/badge/Model%20Accuracy-89.43%25-brightgreen?style=for-the-badge)
![License](https://img.shields.io/badge/License-MIT-yellow?style=for-the-badge)
![Deployed on Render](https://img.shields.io/badge/Deployed%20on-Render-46E3B7?style=for-the-badge&logo=render&logoColor=white)

<br/>

[🚀 Live Demo](https://movie-sentiment-analyzer-p5h8.onrender.com/) &nbsp;•&nbsp; [📖 How It Works](#-how-it-works--the-full-pipeline) &nbsp;•&nbsp; [⚙️ Install](#%EF%B8%8F-installation) &nbsp;•&nbsp; [🐛 Troubleshooting](#-troubleshooting) &nbsp;•&nbsp; [👥 Team](#-contributors)

</div>

---

## 🌟 What is CineScope?

> *"Is this movie worth two hours of my life?"* — Everyone, before every movie.

CineScope answers that question with **real data**, not one critic's hot take.

It's a full-stack AI-powered web application that **scrapes hundreds of real user reviews** from TMDB, IMDb, and Rotten Tomatoes simultaneously, then passes each one through a **machine learning sentiment classifier** trained on 50,000 reviews. In seconds, you get a verdict backed by the collective voice of the internet.

```
You type:   "Inception"
CineScope:  Fetches 150 reviews → Classifies each → Returns "Positive 😊 (87.3%)"
```

No fluff. No paid subscriptions. Just raw crowd intelligence, distilled by AI.

---

## ✨ Features at a Glance

| Feature | Description |
|---|---|
| 🔍 **Smart Search** | Find any movie by name instantly |
| 📡 **Live Scraping** | Parallel review fetching from TMDB, IMDb & Rotten Tomatoes |
| 🤖 **ML Classifier** | TF-IDF + Logistic Regression — **89.43% accuracy** |
| 📊 **Visual Verdict** | Animated positive/negative percentage bar |
| 🎭 **Rich Metadata** | Poster, plot, cast, director, runtime, genres & rating |
| ⭐ **Smart Fallback** | TMDB audience score when reviews are unavailable |
| 🎨 **10 UI Themes** | Midnight · Crimson · Forest · Neon · Sunrise · Ocean · Galaxy · Obsidian · Cherry · Slate |
| 🏷️ **Source Badges** | Per-review labels — TMDB / IMDb / RT |
| 📝 **Review Cards** | Expandable individual reviews with per-card sentiment labels |
| 🔄 **Deduplication** | Fingerprint-based — same review from multiple sources counted once |
| 📁 **Structured Logs** | Daily-rotating log files + colorized console output |
| 🚀 **Deploy-Ready** | One-click deploy to Render |

---

## 🌐 Live Demo

> 🚀 **Try it now, no setup required:**
> ### [movie-sentiment-analyzer-p5h8.onrender.com](https://movie-sentiment-analyzer-p5h8.onrender.com/)

---

## 🎥 Demo Video

<!-- 
  📌 HOW TO ADD YOUR DEMO VIDEO:
  Option A — YouTube / Loom (recommended):
    Replace the URL below with your video link.
    The thumbnail image will be clickable and link to the video.

    [![CineScope Demo](https://img.youtube.com/vi/YOUR_VIDEO_ID/maxresdefault.jpg)](https://www.youtube.com/watch?v=YOUR_VIDEO_ID)

  Option B — GitHub-hosted video (MP4 under 100MB):
    Drag and drop your .mp4 into any GitHub issue/PR comment box,
    copy the generated URL, then paste it here:

    https://user-images.githubusercontent.com/YOUR_USER_ID/your-video.mp4

  Option C — GIF demo (under 10MB):
    ![CineScope Demo](assets/demo.gif)
-->

> 📹 *Drop your screen-recording or YouTube link here using the guide above.*

---

## 📸 Screenshots


### 🏠 Home — Search Screen
<!-- Replace with: ![Home Screen](assets/screenshot-home.png) -->

[<img width="1863" height="984" alt="CineScope 1" src="https://github.com/user-attachments/assets/42866911-f280-4df0-84f6-e3c119d9b658" />
 ]

### 🎬 Results — Positive Verdict
<!-- Replace with: ![Positive Verdict](assets/screenshot-positive.png) -->

[<img width="1863" height="2086" alt="positive" src="https://github.com/user-attachments/assets/c6e72059-7182-47eb-84de-52aed0f68fe5" />
]



### 😞 Results — Negative Verdict
<!-- Replace with: ![Negative Verdict](assets/screenshot-negative.png) -->

[ <img width="1863" height="1715" alt="negative" src="https://github.com/user-attachments/assets/7646b428-cc65-4159-9f98-f2c22b986fe0" />
]


### 🎨 Theme Switcher
<!-- Replace with: ![Themes](assets/screenshot-themes.png) -->

[ <img width="1863" height="1137" alt="theme switchers" src="https://github.com/user-attachments/assets/b3ab4fdc-2094-41c2-8eeb-07b54fe358a1" />
]


## 📸 ASCII UI Preview

```
┌─────────────────────────────────────────────────────────────────┐
│  CineScope                                    ● ● ● ● ● ● ● ● │
│  AI-powered movie sentiment analysis                            │
├─────────────────────────────────────────────────────────────────┤
│  ┌─────────────────────────────────────────┐  [ Analyze ]      │
│  │  Search any movie… e.g. Inception       │                   │
│  └─────────────────────────────────────────┘                   │
├─────────────────────────────────────────────────────────────────┤
│  OVERALL VERDICT                            ⭐ 8.4 / 10        │
│  Positive 😊                               ████████░░ 87.3%   │
│  ML model on 143 reviews · TMDB(30)·IMDb(25)·RT(18)           │
├──────────┬──────────────────────────────────────────────────────┤
│ [POSTER] │ Inception  📅 2010  ⏱ 148 min  Sci-Fi  Action      │
│          │ Director: Christopher Nolan                          │
│          │ Cast: Leonardo DiCaprio, Joseph Gordon-Levitt...     │
│          │ "Cobb, a skilled thief who commits corporate..."     │
├──────────┴──────────────────────────────────────────────────────┤
│  REVIEWS (143)   🎬 TMDB 30   ⭐ IMDb 25   🍅 RT 18           │
│  [ All ] [ 👍 Positive ] [ 👎 Negative ]                       │
│  ┌──────────────────────────────────────────────────────────┐  │
│  │ 👍 Pos │ "A masterpiece of modern cinema. The way Nolan  │  │
│  │        │  weaves multiple dream layers..."  [Read more]  │  │
│  └──────────────────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────────────────┘
```

---

## 🏗️ Project Architecture

```
Sentiment_Analyzer/
│
├── 📂 api/
│   └── tmdb_api.py              # TMDB REST API client
│                                #   → get_imdb_id()    — resolves IMDb ID
│                                #   → get_movie_data() — full metadata fetch
│
├── 📂 scraper/
│   ├── __init__.py              # Package marker (required!)
│   ├── imdb_scraper.py          # IMDb HTML scraper (BeautifulSoup)
│   │                            #   → 3 fallback CSS selectors for layout changes
│   │                            #   → pagination support via data-key
│   ├── rt_scraper.py            # Rotten Tomatoes scraper
│   │                            #   → slug discovery via RT search
│   │                            #   → constructed slug fallback
│   ├── tmdb_scraper.py          # TMDB reviews via API (paginated)
│   └── review_aggregator.py     # Orchestrator
│                                #   → ThreadPoolExecutor (3 workers)
│                                #   → merge + fingerprint deduplication
│
├── 📂 model/
│   ├── sentiment_model.pkl      # Trained LogisticRegression (joblib)
│   └── vectorizer.pkl           # Fitted TfidfVectorizer (joblib)
│
├── 📂 dataset/
│   └── imdbds.csv               # 50,000 IMDb reviews — training corpus
│
├── 📂 notebook/
│   └── training.ipynb           # End-to-end ML training pipeline
│
├── 📂 templates/
│   └── index.html               # Single-page Jinja2 template
│                                #   → 10 CSS themes via data-theme
│                                #   → vanilla JS (no framework)
│
├── 📂 logs/                     # Auto-created on first run
│   └── app_YYYY-MM-DD.log       # Daily rotating structured logs
│
├── app.py                       # Flask entry point + prediction pipeline
├── app_logger.py                # Shared logging (console INFO + file DEBUG)
└── requirements.txt             # Pinned Python dependencies
```

---

## 🧠 How It Works — The Full Pipeline

When you type a movie name and hit **Analyze**, here's what happens under the hood:

### Step 1 — IMDb ID Resolution

```
"Inception"
    │
    ▼
TMDB Search API (/search/movie)
    │
    ▼
TMDB movie ID: 27205
    │
    ▼
TMDB External IDs API (/movie/27205/external_ids)
    │
    ▼
IMDb ID: "tt1375666"
```

### Step 2 — Movie Metadata

```
TMDB /movie/27205?append_to_response=credits,external_ids
    │
    ├── Title, Year, Plot, Tagline
    ├── Genres, Runtime, Language, Country
    ├── Poster URL (image.tmdb.org/t/p/w500)
    ├── Vote average + vote count
    ├── Director (from crew where job == "Director")
    └── Top 4 cast members
```

### Step 3 — Parallel Review Scraping

```
                ThreadPoolExecutor (max_workers=3)
               ┌──────────┬──────────┬──────────┐
               │          │          │          │
          TMDB API    IMDb HTML    RT HTML
         (paginated)  (3 CSS      (slug search
          /reviews     selectors,  + page
          endpoint)    pagination) pagination)
               │          │          │
               └──────────┴──────────┘
                          │
                Merge in priority order:
                TMDB → IMDb → RT
                          │
                Fingerprint deduplication
                (first 120 chars, lowercased)
                          │
                Up to 150 unique reviews
```

### Step 4 — ML Sentiment Classification

```
For each review:
    raw text
       │
       ▼  TF-IDF vectorizer.transform()  →  sparse vector (5,000 features)
       │
       ▼  LogisticRegression.predict()   →  1 (Positive) or 0 (Negative)

After all reviews:
    pos_pct = (positive_count / total) × 100

    pos_pct >= 60%  →  "Positive 😊"
    pos_pct <= 40%  →  "Negative 😞"
    else            →  "Mixed 😐"
```

### Step 5 — Rating Fallback

```
If zero reviews were found across all 3 sources:

    TMDB vote_average
        >= 7.0  →  "Positive 😊"
        >= 4.0  →  "Mixed 😐"
        <  4.0  →  "Negative 😞"
```

### Step 6 — Response

```
Flask renders index.html via Jinja2 with full movie_info dict
    → Verdict banner + animated progress bar
    → Movie card (poster, metadata)
    → Filterable review list (All / Positive / Negative tabs)
    → Per-review expandable cards with sentiment badge
```

---

## 🤖 Machine Learning Model

### Dataset

The model is trained on the [IMDB Dataset of 50K Movie Reviews](https://www.kaggle.com/datasets/lakshmi25npathi/imdb-dataset-of-50k-movie-reviews) — a perfectly balanced binary classification dataset.

| Property | Value |
|---|---|
| Total samples | 50,000 reviews |
| Positive reviews | 25,000 |
| Negative reviews | 25,000 |
| Train split | 40,000 (80%) |
| Test split | 10,000 (20%) |
| Vectorizer | TF-IDF, `max_features=5000` |
| Model | Logistic Regression (sklearn defaults) |
| **Test Accuracy** | **89.43%** ✅ |

### Text Preprocessing Pipeline

```python
raw review
    │
    ▼  text.lower()
    │
    ▼  re.sub(r'<.*?>', '', text)        # strip HTML tags
    │
    ▼  re.sub(r'[^a-zA-Z]', ' ', text)  # keep letters only
    │
    ▼  TfidfVectorizer(max_features=5000)
    │
    ▼  dense numpy array → LogisticRegression.predict()
    │
    ▼  1 = Positive  |  0 = Negative
```

### Why Logistic Regression?

Despite being a "simple" model, Logistic Regression on TF-IDF features is remarkably effective for sentiment classification:

| Advantage | Detail |
|---|---|
| ⚡ **Fast inference** | Milliseconds per review — no GPU needed |
| 🪶 **Lightweight** | Tiny `.pkl` file, loads in seconds at startup |
| 🎯 **High accuracy** | 89.43% on the standard IMDb benchmark |
| 🔍 **Interpretable** | Feature weights reveal which words drive predictions |
| 🚀 **Production-ready** | No runtime dependencies beyond scikit-learn |

For a web app where inference must be near-instant across 150 reviews, it's the ideal choice. Upgrading to BERT is on the roadmap — but this baseline is already excellent.

---

## 🎨 UI Themes

CineScope ships with **10 hand-crafted themes** switchable with one click. Each theme is defined entirely in CSS custom properties — no JavaScript required to switch. Your preference is saved to `localStorage` and restored on every visit.

| Theme | Vibe | Background | Accent |
|---|---|---|---|
| 🌙 **Midnight** | Dark indigo — default | `#0a0c14` | `#6366f1` |
| 🩸 **Crimson** | Dark red — dramatic | `#0d0204` | `#e11d48` |
| 🌲 **Forest** | Dark green — calm | `#030a06` | `#16a34a` |
| ⚡ **Neon** | Cyberpunk teal/pink | `#03001a` | `#00ffcc` |
| 🌅 **Sunrise** | Light orange — warm | `#fff7ed` | `#ea580c` |
| 🌊 **Ocean** | Light blue — clean | `#f0f9ff` | `#0284c7` |
| 🌌 **Galaxy** | Deep purple — cosmic | `#050510` | `#c084fc` |
| 🖤 **Obsidian** | True black — minimal | `#09090b` | `#e4e4e7` |
| 🌸 **Cherry** | Light pink — playful | `#fdf2f8` | `#db2777` |
| 🪨 **Slate** | Light grey — professional | `#f8fafc` | `#334155` |

---

## 🔧 Scraper Technical Details

### IMDb Scraper

The IMDb scraper handles IMDb's frequently changing HTML layout with **3 fallback CSS selectors** in priority order:

```
1. div.ipc-html-content-inner-div     ← New layout (2023+)
2. div.text.show-more__control        ← Old layout
3. div.review-container div.content   ← Legacy layout
```

Pagination is handled via IMDb's `data-key` attribute on the load-more element. User-Agent strings are rotated across pages to reduce blocking risk.

### Rotten Tomatoes Scraper

The RT scraper first attempts to discover the movie's URL slug via RT's search endpoint, then constructs one as a fallback:

```python
"The Dark Knight"  →  "the_dark_knight"
```

Reviews are scraped from `p.audience-reviews__review` with 2 additional fallback selectors for layout changes.

### Thread Safety

All three scrapers use **per-request `requests.Session()` context managers** rather than a shared module-level session. This is critical because `review_aggregator.py` runs all three scrapers simultaneously via `ThreadPoolExecutor` — a shared session causes race conditions and intermittent connection resets.

### Deduplication Strategy

Reviews are deduplicated using a fingerprint of the first 120 characters (lowercased and stripped), stored in a Python `set`. This catches the same review appearing on multiple platforms without requiring expensive full-string comparison.

---

## 📋 Prerequisites

Before you begin, make sure you have the following:

- **Python 3.10+**
- **pip**
- **Git**
- A free [TMDB API key](https://www.themoviedb.org/settings/api)
- Open internet access *(see [Troubleshooting](#-troubleshooting) if on a restricted network)*

---

## ⚙️ Installation

### 1 · Clone the Repository

```bash
git clone https://github.com/yourusername/Sentiment_Analyzer.git
cd Sentiment_Analyzer
```

### 2 · Create a Virtual Environment

```bash
python -m venv .venv

# Windows
.venv\Scripts\activate

# macOS / Linux
source .venv/bin/activate
```

### 3 · Install Dependencies

```bash
pip install -r requirements.txt
```

### 4 · Train the ML Model

Open `notebook/training.ipynb` in Jupyter and run all cells. This reads `dataset/imdbds.csv` and saves two files:

```
model/sentiment_model.pkl
model/vectorizer.pkl
```

> ⚠️ The app will refuse to start without these files.

### 5 · Create the Scraper Package File

```bash
# Windows
type nul > scraper\__init__.py

# macOS / Linux
touch scraper/__init__.py
```

### 6 · Set Your TMDB API Key

Get a free key at [https://www.themoviedb.org/settings/api](https://www.themoviedb.org/settings/api).
Copy the **API Key (v3 auth)** — the 32-character hex string (**not** the long Bearer token).

```bash
# Windows PowerShell
$env:TMDB_API_KEY="your_32_char_key_here"

# macOS / Linux
export TMDB_API_KEY="your_32_char_key_here"
```

Or set it directly in `api/tmdb_api.py` and `scraper/tmdb_scraper.py`:

```python
TMDB_API_KEY = "your_32_char_key_here"
```

---

## 🚀 Running Locally

```bash
python app.py
```

Open **http://127.0.0.1:5000** in your browser. Type any movie name and click **Analyze**.

**Expected startup output:**

```
2026-04-26 13:00:00 | INFO | app | [STARTUP] Loading ML model and vectorizer...
2026-04-26 13:00:06 | INFO | app | [STARTUP] Model and vectorizer loaded successfully.
2026-04-26 13:00:06 | INFO | app | [STARTUP] Flask app starting on port 5000
 * Running on http://127.0.0.1:5000
```

---

## ☁️ Deployment on Render

CineScope is fully configured for zero-effort deployment on [Render](https://render.com) (free tier).

**1.** Push your project to GitHub — make sure `model/*.pkl` files are committed.

**2.** Go to [render.com](https://render.com) → **New → Web Service** and connect your repo.

**3.** Configure the service:

| Setting | Value |
|---|---|
| **Runtime** | Python 3 |
| **Build Command** | `pip install -r requirements.txt` |
| **Start Command** | `python app.py` |

**4.** Add environment variables:

| Key | Value |
|---|---|
| `TMDB_API_KEY` | `your_32_char_key_here` |

**5.** Click **Deploy**. Done. 🎉

> ✅ **CineScope is already live at:** [movie-sentiment-analyzer-p5h8.onrender.com](https://movie-sentiment-analyzer-p5h8.onrender.com/)
>
> Render's US servers have unrestricted internet access — TMDB works perfectly in production even if your local network blocks it.

---

## 🐛 Troubleshooting

A complete record of every issue encountered during development, with verified solutions.

---

### ❌ `ModuleNotFoundError: No module named 'tmdb_scraper'`

**Cause:** The `scraper/` folder is not registered as a Python package (missing `__init__.py`), and `review_aggregator.py` uses bare module names that don't resolve from the project root.

**Fix 1 — Create the package init file:**

```bash
# Windows
type nul > scraper\__init__.py

# macOS / Linux
touch scraper/__init__.py
```

**Fix 2 — Update imports in `scraper/review_aggregator.py`:**

```python
# ❌ Wrong — bare names don't resolve from project root
from tmdb_scraper import get_tmdb_reviews
from imdb_scraper import get_imdb_reviews
from rt_scraper   import get_rt_reviews

# ✅ Correct — full package path from project root
from scraper.tmdb_scraper import get_tmdb_reviews
from scraper.imdb_scraper import get_imdb_reviews
from scraper.rt_scraper   import get_rt_reviews
```

---

### ❌ `Connection to api.themoviedb.org timed out`

**Cause:** Your network (college WiFi, office, or some mobile carriers) is blocking outbound connections to TMDB at the DNS or IP level. Python's `requests` makes direct TCP connections — your browser may still work because it uses a system proxy or different DNS resolution.

**Quick diagnosis:**

```bash
# Test TMDB — should print 200
python -c "import requests; r = requests.get('https://api.themoviedb.org', timeout=10); print(r.status_code)"

# Test general internet — should always work
python -c "import requests; r = requests.get('https://google.com', timeout=10); print(r.status_code)"
```

If Google returns `200` but TMDB times out — your network is performing DNS-level domain blocking.

#### ✅ Solution 1 — Change DNS to Google DNS *(most reliable fix)*

1. Press `Win + R`, type `ncpa.cpl`, press Enter
2. Right-click your active network adapter → **Properties**
3. Double-click **Internet Protocol Version 4 (TCP/IPv4)**
4. Select **"Use the following DNS server addresses"** and enter:

```
Preferred DNS:  8.8.8.8
Alternate DNS:  8.8.4.4
```

If `8.8.8.8` still doesn't work, try **Cloudflare DNS**:

```
Preferred DNS:  1.1.1.1
Alternate DNS:  1.0.0.1
```

**Verify the fix:**

```bash
python -c "import requests; r = requests.get('https://api.themoviedb.org/3/search/movie', params={'api_key':'your_key','query':'inception'}, timeout=10); print(r.status_code)"
# Expected: 200
```

#### ✅ Solution 2 — Mobile Hotspot

Turn on hotspot on your phone, connect your laptop's WiFi to it, then run the app. If your carrier also blocks TMDB on hotspot, combine with Solution 1.

#### ✅ Solution 3 — VPN

Install a free VPN, connect to any server, then run `python app.py`.

Recommended free options:
- [ProtonVPN](https://protonvpn.com) — unlimited free tier
- [Windscribe](https://windscribe.com) — 10 GB/month free

#### ✅ Solution 4 — Deploy to Render

If you can't resolve local network access, deploy to Render. Render's US servers have no such blocks and the app will work perfectly in production.

---

### ❌ `Invalid API key (401)`

**Cause:** Wrong API key. The TMDB settings page shows two different credentials — many users accidentally use the long Bearer token instead of the short v3 key.

**How to get the correct key:**

1. Go to [https://www.themoviedb.org/settings/api](https://www.themoviedb.org/settings/api) while logged in
2. Copy **"API Key (v3 auth)"** — a 32-character hex string like `554e826839d8ab9d1b65e68d83c61b1d`
3. Do **NOT** use **"API Read Access Token (v4 auth)"** — that is the long `eyJhbGci...` Bearer token

**If you only have the Bearer token**, extract the v3 key from it:

```python
import base64, json
token = "eyJhbGci...your.bearer.token"
payload = token.split('.')[1]
payload += '=' * (4 - len(payload) % 4)  # fix base64 padding
print(json.loads(base64.b64decode(payload))['aud'])
# prints your v3 API key
```

---

### ❌ `FileNotFoundError: model/sentiment_model.pkl`

**Cause:** The ML model files haven't been generated yet.

**Fix:** Open `notebook/training.ipynb` and run all cells. The final two cells save:

```
model/sentiment_model.pkl
model/vectorizer.pkl
```

Training takes approximately **30–60 seconds** on a modern machine.

---

### ❌ Browser shows JSON but Python times out

**Cause:** Your browser routes through a system proxy or VPN browser extension that Python's `requests` library does not use. Python makes direct TCP connections and bypasses browser-level proxy settings.

**Fix — set proxy environment variables before running:**

```powershell
# Find your proxy in browser settings → use that address here
$env:HTTPS_PROXY="http://proxy.address:port"
$env:HTTP_PROXY="http://proxy.address:port"
python app.py
```

The DNS change (Solution 1 above) is the cleaner fix as it resolves the root cause.

---

### ❌ Reviews count is 0 for all sources

**Cause:** IMDb and RT block scraping occasionally or change their HTML layout. The app automatically falls back to TMDB rating for the verdict.

**Debug individual scrapers:**

```bash
python -c "
from scraper.imdb_scraper import get_imdb_reviews
reviews, label = get_imdb_reviews('tt1375666', max_reviews=5)
print('IMDb:', label, '|', reviews[0][:80] if reviews else 'EMPTY')
"

python -c "
from scraper.rt_scraper import get_rt_reviews
reviews, label = get_rt_reviews('Inception', max_reviews=5)
print('RT:', label, '|', reviews[0][:80] if reviews else 'EMPTY')
"
```

If consistently empty, the site may have updated its HTML. Update the CSS selectors in the respective scraper file.

---

## 📦 Dependencies

| Package | Version | Purpose |
|---|---|---|
| `flask` | ≥2.3.2 | Web framework and template rendering |
| `scikit-learn` | ≥1.2.2 | TF-IDF vectorizer + Logistic Regression |
| `pandas` | ≥1.5.3 | Dataset loading in training notebook |
| `numpy` | ≥1.23.5 | Numerical array operations |
| `joblib` | ≥1.3.2 | Model serialization / deserialization |
| `requests` | ≥2.31.0 | HTTP client for API calls and scraping |
| `beautifulsoup4` | ≥4.12.2 | HTML parsing for IMDb and RT scrapers |
| `lxml` | ≥4.9.3 | Fast HTML parser backend for BS4 |
| `nltk` | ≥3.8.1 | NLP utilities |
| `matplotlib` | ≥3.7.1 | Training visualization *(notebook only)* |
| `seaborn` | ≥0.12.2 | Training visualization *(notebook only)* |
| `tqdm` | ≥4.66.1 | Progress bars *(notebook only)* |

> 💡 `logging` and `concurrent.futures` are Python stdlib — do **NOT** `pip install` them.

---

## 📊 Logging System

CineScope uses a structured dual-output logging system defined in `app_logger.py`:

```
Console  →  INFO level and above   (clean, readable output)
File     →  DEBUG level and above  (full detail, daily rotation)
            saved to: logs/app_YYYY-MM-DD.log
```

**Log format:**

```
2026-04-26 13:04:04 | INFO  | app               | [STEP 1] Fetching IMDb ID for 'inception'
2026-04-26 13:04:05 | INFO  | tmdb_api          | [TMDB API] Found — TMDB ID: 27205 | Title: 'Inception'
2026-04-26 13:04:06 | INFO  | review_aggregator | [AGGREGATOR] ✓ 'TMDB' → 28 reviews
2026-04-26 13:04:07 | INFO  | review_aggregator | [AGGREGATOR] ✓ 'IMDb' → 25 reviews
2026-04-26 13:04:08 | INFO  | review_aggregator | [AGGREGATOR] ✓ 'Rotten Tomatoes' → 18 reviews
2026-04-26 13:04:09 | INFO  | app               | [STEP 4] Verdict: Positive 😊 | Positive: 87.3% | Negative: 12.7%
2026-04-26 13:04:09 | INFO  | app               | [REQUEST] Completed in 5.23s — 'inception' → Positive 😊
```

Each module has its own named logger (`tmdb_api`, `imdb_scraper`, `rt_scraper`, `review_aggregator`) for easy filtering and debugging.

---

## 👥 Contributors

<div align="center">

| | Name | Role | Contributions |
|---|---|---|---|
| 👨‍💻 | **Sushant Garde** | Project Lead & Backend | ML model training pipeline, Flask backend, prediction pipeline, `app.py`, `app_logger.py`, deployment config |
| 🎨 | **Bijo Salu** | Frontend Engineer | UI/UX design, 10-theme CSS system, vanilla JS interactions, loading animations, responsive layout |
| 🔧 | **Shree Shinde** | Data Engineer | Web scrapers (IMDb, RT, TMDB), `review_aggregator`, thread safety, deduplication logic |
|     | **Mayur Anap**  | Documentation | Making the reports and project documentation|

</div>

---

## 🗺️ Roadmap

- [ ] Add support for TV shows and web series
- [ ] Aspect-based sentiment (story, acting, direction, music scored separately)
- [ ] Historical sentiment trend chart over time
- [ ] Export results as PDF report
- [ ] REST API endpoint for programmatic access
- [ ] Upgrade model to BERT / DistilBERT for higher accuracy
- [ ] Docker containerization for easier deployment
- [ ] Add user review submission and community verdicts

---

## 📄 License

```
MIT License — Copyright (c) 2026 CineScope Contributors

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software to use, copy, modify, merge, publish, distribute, sublicense,
and/or sell copies of the Software, subject to the condition that the above
copyright notice appears in all copies.
```

---

<div align="center">

**Built with ❤️ and way too much ☕ by the CineScope team**

*"The best movies deserve the best analysis."*

⭐ **Star this repo if CineScope helped you pick a better movie!**

</div>
