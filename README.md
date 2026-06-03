# AI Market Bot

Inflection Scanner research dashboard.

## Deploy

This folder is prepared for Vercel.

- `index.html` is the dashboard.
- `api/inflection.py` is the public API route.
- `api/inflection_snapshot.json` is the latest approved research snapshot.
- `vercel.json` wires the API route.

The public deployment uses snapshot mode so it can open without exposing local API keys.
The local backend in `server.py` can run live Alpaca scans on your computer.

## Local

```bash
python3 server.py
```

Open:

```text
http://127.0.0.1:4184/
```

## Important

This is a research and paper-trading prototype. Do not connect real-money execution until stricter point-in-time data tests are complete.
