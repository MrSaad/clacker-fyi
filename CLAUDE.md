# clacker-fyi

A catalog webapp for custom mechanical keyboard builds scraped from
r/CustomKeyboards. Express + SQLite on the server, React + Vite on the client.
Filtering and search run entirely client-side against an in-memory copy of the
dataset fetched at boot.

## Layout

- `client/` — React + Vite SPA. Sidebar filters and search are client-side.
- `server/` — Express API backed by SQLite.
  - `db.js` — the only module that talks to the DB. Exports `openDb`,
    `getAllKeyboards`, `getKeyboardById`, `getTaxonomy`, `countKeyboards`.
  - `index.js` — routes: `/api/keyboards`, `/api/keyboards/:id`,
    `/api/taxonomy`, `/api/health`.
- `data/keyboards.db` — SQLite file, checked in (private repo). Authoritative
  store. Adding a brand, attribute value, or keyboard is an INSERT, not a code
  change.
- `scratch/` — one-off Python scripts used to build the initial dataset from
  Reddit. Not part of the running app, kept for reference / future re-ingest.

## Running

```
npm run install:all
npm run dev      # server :3001, client :5173
```

## `scratch/` scripts

Pipeline that produced the seed dataset (83 posts):

1. **`fetch_posts.py`** — pulls the top 100 posts + top-level comments from
   r/customkeyboards via public JSON endpoints. Writes `raw_posts.json`.
2. **`build_evidence.py`** — reduces `raw_posts.json` to `evidence.txt`:
   title + OP comments + any comment mentioning a parts keyword. This is the
   text a human (or LLM) reads to hand-extract parts.
3. **`build_dataset.py`** — merges a hand-built `EXTRACTIONS` dict (inline in
   the script) with `raw_posts.json` metadata to produce `keyboards.json`.
4. **`process_images.py`** — downloads post images, resizes with ImageMagick,
   uploads to S3, emits `keyboards_s3.json` with CDN URLs + thumbnails.

The final `keyboards.json` / `keyboards_s3.json` is what originally seeded
`data/keyboards.db`. The DB is now the source of truth; re-running these
scripts to ingest more posts means writing a new loader that UPSERTs into the
DB directly.

## DB schema

Grows by INSERT, not ALTER. New brands, attributes, or attribute values are
pure data.

- **`keyboards`** — one row per post. Hot columns: `id` (reddit post id), `title`,
  `author`, `permalink`, `created_utc`, `score`, `thumbnail_url`, `confidence`.
- **`keyboard_raw`** — side table for `selftext` and `parts_source_text`. Split
  off so `SELECT * FROM keyboards` stays lean.
- **`images`** — `(keyboard_id, idx, url)`. Gallery images in order.
- **`component_types`** — the 10 part slots (switches, keycaps, case, plate,
  pcb, stabilizers, layout, mods, cable, deskmat). `key` is the API field name.
- **`keyboard_components`** — `(keyboard_id, component_type_id, text)`.
  Free-text description per slot.
- **`brand_tags`** — `(component_type_id, label, aliases)`. `aliases` is a JSON
  array of lowercase substrings; null means `[label.toLowerCase()]`. Drives the
  sidebar brand filters.
- **`keyboard_brand_tags`** — M:N. Pre-computed at ingest by substring-matching
  component text against brand aliases.
- **`attribute_types`** — inferred enums (sound_profile, build_tier,
  typing_feel, build_complexity, color, theme). `multi` flag distinguishes
  single-valued (sound_profile) from multi-valued (color, theme).
- **`attribute_values`** — `(attribute_type_id, value)`. Every allowed value.
- **`keyboard_attributes`** — M:N join. Uniform shape covers both single- and
  multi-valued attributes; single-value semantics enforced at the write layer.
- **`meta`** — key/value. Currently holds `schema_version`.

## API shape

`GET /api/keyboards` returns an array of:

```jsonc
{
  "id": "j8aqrn",
  "title": "...", "author": "...", "permalink": "...",
  "created_utc": 1602289520, "score": 2433,
  "thumbnail_url": "...", "image_urls": ["..."],
  "confidence": "medium",
  "components":        { "switches": "Sakurios ...", "case": "PAW", ... },
  "component_brands":  { "switches": ["Sakurios"], "case": ["PAW"], ... },
  "attributes":        { "sound_profile": ["thocky"], "color": ["pink"], "theme": ["minimal","themed"], ... },
  "raw":               { "selftext": "", "parts_source_text": "..." }
}
```

`GET /api/taxonomy` returns `{ attribute_types, component_types }` — the
filter ontology the sidebar renders from. The client is taxonomy-agnostic;
adding a filter is a DB write + server restart.
