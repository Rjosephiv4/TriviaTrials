# Trivia Trials — original Flask edition

The original daily trivia game: Flask, JavaScript, SQLite, account sessions, classic/mini rounds, and leaderboards. The historical generation pipeline combines a web scraper with OpenAI-generated questions.

**Current direction:** [`TriviaTrials-Version-2`](https://github.com/Rjosephiv4/TriviaTrials-Version-2) is the separate modernization project. This repository preserves the first version and provides a reproducible local setup; it should be presented as an earlier project, not a hardened production service.

[Original video demonstration](https://www.youtube.com/watch?v=KUnDT_yv-N0)

## Local demo

Requires Python 3.11+. No API key is needed to play the included question set.

```bash
python -m venv .venv
. .venv/bin/activate
pip install -r requirements.txt
python init_db.py
python -m flask --app app run
```

Open `http://127.0.0.1:5000`, register a local account, and try a mini round. `init_db.py` creates an empty database and refuses to replace an existing one. No user accounts or password hashes are bundled in the current checkout.

Optional environment settings: `TRIVIA_DATABASE`, `TRIVIA_SESSION_DIR`, and `TRIVIA_SECRET_KEY`. A randomly generated development secret is used if no secret is configured. Use a stable secret for persistent sessions. `.env.example` documents the settings; export them in your shell before running.

## Verify

```bash
python -m unittest discover -s tests -v
```

Smoke tests use an isolated empty database, cover registration/login and authentication boundaries, and check that importing the app starts no background jobs. The original interface is retained.

## Legacy generation pipeline

Generation is opt-in. Installing `requirements-generation.txt` adds the OpenAI SDK. Only setting `TRIVIA_ENABLE_SCHEDULER=1` starts the legacy midnight scheduler. It performs network requests and may incur API costs. This path is preserved for historical context and is not exercised by the local demo or CI. Run scheduled generation as a separate worker in a future production deployment.

## Architecture and lessons

[`app.py`](app.py) owns HTTP routes and SQLite queries; templates and static JavaScript render the game; [`schema.sql`](schema.sql) initializes the shared tables. Per-user statistics tables and client-submitted scores are limitations of this early design. The game exposes correct answers to the client and does not protect leaderboard integrity from crafted/replayed submissions. Use the local demo for exploration; address those boundaries before deploying it publicly.

The current cleanup removes the bundled runtime database from the latest revision, replaces the machine-wide dependency dump, disables import-time generation, and adds setup and smoke tests. Removing a database from the latest tree does not erase older public Git history.
