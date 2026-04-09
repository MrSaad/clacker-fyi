# Keyboard Part Picker

A faceted browser for r/CustomKeyboards top builds. Express API + Vite/React/Tailwind frontend.

## Run it

```bash
npm run install:all
npm run dev
```

- Client (Vite): http://localhost:5173
- API (Express): http://localhost:3001

## Layout

```
keyboard-part-picker/
├── server/   Express, serves /api/keyboards from server/data/keyboards.json
├── client/   Vite + React + Tailwind
└── ingest/   Phase 1 data pipeline (Reddit fetch + extraction + keyboards.json)
```

`server/data/keyboards.json` is a copy of `ingest/keyboards.json`. To refresh it
after re-running the ingest pipeline:

```bash
npm run sync-data
```

## Re-running the ingest pipeline

```bash
cd ingest
uv run --no-project fetch_posts.py     # re-fetch from Reddit (rate-limited)
uv run --no-project build_evidence.py  # rebuild evidence.txt
uv run --no-project build_dataset.py   # rebuild keyboards.json
cd .. && npm run sync-data             # copy into the server
```

See `ingest/PHASE1_SUMMARY.md` for the full pipeline writeup.
