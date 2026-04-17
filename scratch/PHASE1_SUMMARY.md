# Phase 1 Summary — Reddit r/CustomKeyboards Ingestion

## Goal

Build a "keyboard part picker" website. Visitors browse real custom keyboard builds from r/CustomKeyboards, click an image, and see the parts (case, PCB, switches, keycaps, etc.) plus a link to the original Reddit post.

Phase 1 (this document) is the **data layer**: pull posts, extract parts, save structured JSON.
Phase 2 (later) is the **presentation layer**: build the website on top of `keyboards.json`.

---

## What we did

### 1. Fetched the top 100 posts of all time from r/CustomKeyboards

Used Reddit's public JSON endpoint — **no API key required** at this scale. The unauthenticated endpoints (`reddit.com/r/customkeyboards/top.json` and `reddit.com/comments/{id}.json`) allow ~60 requests/minute, which is well above what we need.

- One listing fetch returned all 100 top posts (Reddit's per-page max).
- All 100 happened to be image posts (subreddit is image-heavy by nature).
- For each post we then fetched the comment tree (one request per post) to get the parts list, since r/CustomKeyboards posts have **zero selftext** — every parts list lives in a comment, almost always by the OP.
- 99 of 100 comment fetches succeeded. The very last one (`hdtj9x`) hit a 429 rate limit and we gave up retrying after a couple of attempts. Title-only extraction was used for that post.

Output: `raw_posts.json` (377 KB) — all the raw fields we need: id, title, author, permalink, image URLs, selftext (always empty for this sub), and the full top-comment thread for each post (1822 comments total).

### 2. Condensed the raw data into "evidence" for extraction

Reading 1822 comments was overkill. We built a smaller bundle (`evidence.txt`, 100 KB) that for each post contains:
- title, permalink, author
- all comments by the OP (always include — these are usually the parts list)
- any other comment that mentions a parts keyword (`switch`, `keycap`, `gmk`, `gateron`, etc.) — fallback for posts where the parts info is in a reply by someone else

This file was the input to the extraction step.

### 3. Extracted structured parts from each post

Claude (me, in this conversation) read the evidence file and produced a structured entry per post. The decision rule per the plan: **drop any post that yields zero extractable parts**.

Output of this step is hand-coded into `build_dataset.py` as a Python dict (`E`), keyed by Reddit post id. Each entry has `parts` (fixed categories) and `inferred` (community-lingo tags).

### 4. Merged extractions with raw metadata → `keyboards.json`

`build_dataset.py` joins the extraction dict with `raw_posts.json` (for image URLs, scores, timestamps, permalinks) and writes the final `keyboards.json` (109 KB, 83 entries).

---

## Final dataset: `keyboards.json`

**83 entries.** 17 of the top 100 were skipped — see "Skipped posts" below for the reasoning.

### Entry schema

```jsonc
{
  "id": "j8aqrn",
  "title": "The perfect keyboard for Among Us",
  "author": "TakumiYamamoto",
  "permalink": "https://reddit.com/r/CustomKeyboards/comments/j8aqrn/...",
  "created_utc": 1602...,
  "score": 2433,
  "image_urls": ["https://i.redd.it/xxx.jpg"],

  "parts": {
    "case":         "PAW",
    "pcb":          null,
    "plate":        null,
    "switches":     "Sakurios (60g TX springs, lubed Hoppes 9 + Krytox 205g0, filmed)",
    "keycaps":      null,
    "stabilizers":  null,
    "layout":       null,
    "mods":         null,
    "cable":        null,
    "deskmat":      null
  },

  "inferred": {
    "sound_profile":    "thocky",      // thocky | clacky | creamy | poppy | marbley | topre | null
    "build_tier":       "high-end",    // budget | mid | high-end | endgame
    "aesthetic":        ["minimal", "themed"],
    "typing_feel":      "linear",      // linear | tactile | clicky | silent-tactile | topre | null
    "build_complexity": "heavy-mod",   // stock | light-mod | heavy-mod | null
    "confidence":       "medium"       // low | medium | high
  },

  "raw": {
    "selftext": "",
    "parts_source_text": "PAW\n\nSakurios, 60g TX springs lubed with Hoppes 9..."
  }
}
```

The `raw.parts_source_text` field is critical: it's the original text I extracted from. If the schema needs to change later, we can re-run extraction without re-fetching from Reddit.

### Coverage statistics

| Field | Coverage |
|---|---|
| `case` | 83 / 83 (100%) |
| `keycaps` | 79 / 83 (95%) |
| `switches` | 77 / 83 (92%) |
| `stabilizers` | 45 / 83 (54%) |
| `plate` | 43 / 83 (51%) |
| `cable` | 12 / 83 (14%) |
| `pcb` | 10 / 83 (12%) |
| `deskmat` | 9 / 83 (10%) |
| `mods` | 2 / 83 (2%) |

### Inferred distributions

- **Sound profile:** 58 thocky · 12 clacky · 6 creamy · 3 marbley · 1 poppy · 1 topre · 2 unknown
- **Build tier:** 49 endgame · 28 high-end · 5 mid · 1 budget — heavily skewed because "top of all time" is a self-selecting filter for expensive builds
- **Confidence:** mostly `high` (extracted from clear OP parts list); `medium` or `low` for posts where I had to guess from titles or non-OP comments

### Skipped posts (17 of 100)

These posts were filtered out at extraction time. None had a clean single-keyboard parts list.

| Reason | Count | Post IDs |
|---|---|---|
| **Collection posts** (multiple keyboards in one post, OP lists parts for each) — these don't fit our one-keyboard-per-entry data model | 11 | `iknpsy`, `msumg1`, `ogfml5`, `lb13b2`, `l3qx9l`, `n1wvj7`, `ou2gss`, `lbzzu5`, `qx185z`, `nc9gnk`, `k08nk6`, `o3qmji` |
| **No parts info** (no OP comment, no keyword-mentioning comments) | 4 | `l6sul1`, `hmjdiu`, `gz27wk`, `hlavay` |
| **Joke / meme posts** with no real build to catalog | 1 | `oigp34` (the "FR4 PCB on a Vans shoe" joke) |

> **Future fix:** the 11 "collection" posts contain ~30+ buildable keyboards collectively. If you want to recover them, extend the schema so a single post can produce **multiple** entries (e.g., add a `source_post_index` field, give them composite ids like `iknpsy_0`, `iknpsy_1`, etc.). Worth ~30 more entries.

### Known caveats / weak entries

- `hdtj9x` — comment fetch hit Reddit rate limit. Only title-based extraction (`Satisfaction 75 / GMK Oblivion`). Marked `confidence: low`.
- `i3smx4` — no OP comment. Parts pulled from a non-OP reply mentioning GMK WoB. Marked `confidence: low`.
- A few entries marked `confidence: medium` where parts came from titles only or had ambiguous wording.
- The `topre` value in `sound_profile` is an extension beyond the original enum (`thocky / clacky / creamy / poppy / marbley`). Topre boards behave nothing like MX, so it earned its own bucket. Update Phase 2 filters accordingly.

---

## Files in the workspace

| File | Size | Role |
|---|---|---|
| `fetch_posts.py` | 5 KB | Stdlib-only Reddit fetcher. One-shot script. Run with `uv run --no-project fetch_posts.py`. Idempotent — re-running re-fetches everything. |
| `raw_posts.json` | 377 KB | Raw fetched data: 100 posts + 1822 comments. The "source of truth" for re-extraction. Don't delete. |
| `build_evidence.py` | 2 KB | Reduces `raw_posts.json` → `evidence.txt`. Filters comments to OP-only + parts-keyword matches. |
| `evidence.txt` | 100 KB | Compact extraction input. Disposable — regenerable from `raw_posts.json`. |
| `build_dataset.py` | ~30 KB | Holds the hand-extracted parts data (the `E` dict, keyed by post id) and merges with `raw_posts.json` to write `keyboards.json`. **This is where extraction lives** — to fix a bad entry, edit this file and re-run. |
| `keyboards.json` | 109 KB | **The deliverable.** 83 structured entries. Input to Phase 2. |
| `PHASE1_SUMMARY.md` | (this file) | What you're reading. |

### How to re-run / regenerate

```bash
# Re-fetch from Reddit (only if you want fresh data — uses rate-limited public endpoints)
uv run --no-project fetch_posts.py

# Rebuild the condensed evidence file
uv run --no-project build_evidence.py

# Rebuild keyboards.json from extractions + raw metadata
uv run --no-project build_dataset.py
```

The fast iteration loop is **only** the third step — `build_dataset.py` reads `raw_posts.json` from disk and never touches Reddit.

---

## Verification we did

1. Confirmed every entry has at least one non-null `parts` field — **0 violations**.
2. Confirmed every entry has at least one URL in `image_urls` — **0 violations**.
3. Confirmed every entry has a `permalink` — **0 violations**.
4. Confirmed coverage stats look reasonable (case 100%, keycaps 95%, switches 92%).

What we **did not** do (recommended before Phase 2):
- **Manual spot-check.** Open 5–10 random entries' `permalink` URLs in a browser and confirm the extracted parts actually match what the post says. If you find systematic mistakes (e.g., I mis-attributed switches in some pattern), tell me and I'll fix the relevant entries in `build_dataset.py`.
- **Image URL liveness check.** We never actually loaded any of the `image_urls` to confirm they still resolve. Some i.redd.it links from 2020-era posts may have rotted. A simple curl loop on each URL would catch this — run that before building the website so we know which entries need a fallback.

---

## What's next: Phase 2 (the website)

Phase 2 was deliberately deferred. Here's what it needs to do, and the open questions to resolve before starting it.

### Core requirements (from the original brief)

1. Display all keyboards as a grid of images (the `image_urls[0]` of each entry).
2. Click an image → show full detail: all `parts`, all `inferred` fields, all `image_urls`, link to `permalink`.
3. Render straight from `keyboards.json` — no backend needed.

### Suggested approach (for when you pick this up)

A static SPA is the right shape. Options, in order of recommendation:

1. **Plain HTML + vanilla JS, single file.** Easiest. `index.html` fetches `keyboards.json` and renders. No build step, no framework. Probably ~200 lines of code total.
2. **Astro or 11ty.** If you want pretty static-site output with a real templating layer.
3. **Next.js / SvelteKit.** Overkill for 83 static entries, but worth it if you eventually want filters, search, faceted browsing.

### Open questions / things to think through before starting Phase 2

1. **Hosting.** GitHub Pages / Cloudflare Pages / Vercel — any static host works. Pick one before designing.
2. **Image hotlinking.** We chose to store URLs only, not download images. This means the site depends on i.redd.it / imgur staying up. For a portfolio site this is fine; for something more durable, add a step to mirror images to your host. Some imgur URLs may already be 403/410 — worth a one-time liveness check first (see "Verification we did").
3. **Filters / facets.** The `inferred` fields (`sound_profile`, `build_tier`, `aesthetic`, `typing_feel`) were designed exactly so you can offer filters like "show me all thocky endgame builds." Decide which facets you actually want before designing the UI — they'll drive the layout.
4. **Search.** For 83 entries, plain JS string search across `parts.*` is fine, no need for a search index.
5. **Sort order.** Default to `score` descending? `created_utc`? Random? User probably wants the high-score ones up top.
6. **Multiple images per post.** Some entries have galleries (up to 10 images). Decide how the detail view shows these — carousel? grid?
7. **Dataset growth.** Right now it's 83 entries. If you want it bigger, the answer is **not** "fetch more from r/CustomKeyboards" — you've already taken its top page. The answer is to:
   - Recover the 11 collection posts (~30+ entries) by extending the schema (see "Skipped posts" above)
   - Pull from `top?t=year`, `top?t=month`, `hot`, etc. (each is a separate page of 100)
   - Pull from related subs (r/MechanicalKeyboards, r/mk)
   - Do a Reddit OAuth registration so you can paginate past the first 100 posts of a listing
8. **Iteration on extractions.** If you spot bad entries while building the site, edit `build_dataset.py` and re-run — `keyboards.json` regenerates in <1 second.

### Recommended Phase 2 starting point

If you want my advice: start with the dumbest possible static `index.html` (50 lines) that just renders the grid + a modal. Don't overthink it. The data is the hard part and the data is done. Make it look right with 83 real entries on screen, **then** decide what filters and polish are worth adding.

### Things I'd defer until after Phase 2 v1 is up

- Image mirroring (only matters if Reddit images start rotting)
- Facet filters (only matters if browsing 83 things gets unwieldy — it probably won't)
- Recovering the 11 collection posts (only if you want a bigger dataset)
- OAuth + scaling beyond 100 posts (only if you want a much bigger dataset)
- Re-running extractions with different inferred categories (only if the current ones don't serve the website's UX)
