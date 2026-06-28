# profile-sync

A small tool that keeps the **Featured Projects** section of the profile site
(`../index.html`) in sync with live GitHub stats.

For every repository listed in [`config.py`](config.py) it **concurrently** fetches
the current star, fork and watcher counts (plus the primary language) from the GitHub
REST API and rewrites the cards between the `projects:start` / `projects:end` markers
in `index.html`.

## Usage

```bash
# from this directory
uv run main.py
```

Set `GITHUB_TOKEN` to raise the GitHub API rate limit (GitHub Actions provides one
automatically):

```bash
GITHUB_TOKEN=ghp_... uv run main.py
```

To change which projects are shown, edit the `FEATURED_PROJECTS` tuple in
`config.py` and re-run.

## Layout

| Module          | Responsibility                                          |
| --------------- | ------------------------------------------------------- |
| `config.py`     | The curated project list + paths and constants          |
| `models.py`     | Immutable, typed data structures                        |
| `github.py`     | Async GitHub REST client (httpx) — parallel requests    |
| `rendering.py`  | Jinja2 rendering + injection into `index.html`          |
| `main.py`       | Orchestration, CLI entry point and error handling       |
| `templates/`    | The Jinja2 card template                                |

## Development

```bash
uv run ruff check .
uv run mypy .
```
