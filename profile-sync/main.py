"""Refresh the "Featured Projects" cards in ``index.html`` with live GitHub stats.

Run it from this directory with uv::

    uv run main.py

For every repository in :data:`config.FEATURED_PROJECTS` it fetches the current
star, fork and watcher counts (plus the primary language) and rewrites the cards
between the ``projects:start`` / ``projects:end`` markers in ``index.html``.

Set the ``GITHUB_TOKEN`` environment variable to raise the GitHub API rate limit;
GitHub Actions provides one automatically.
"""

import os
import sys

from config import FEATURED_PROJECTS, INDEX_HTML
from exceptions import ProfileSyncError
from github import fetch_repository_stats
from models import ProjectCard
from rendering import inject_cards, render_cards


def collect_cards() -> list[ProjectCard]:
    """Fetch live stats for every featured project and pair them together."""
    token = os.environ.get("GITHUB_TOKEN")
    return [
        ProjectCard(project=project, stats=fetch_repository_stats(project.full_name, token))
        for project in FEATURED_PROJECTS
    ]


def update_index_html() -> bool:
    """Refresh ``index.html`` in place. Returns ``True`` if the file changed.

    Raises:
        ProfileSyncError: On any GitHub, rendering or filesystem failure.
    """
    cards_html = render_cards(collect_cards())

    try:
        page = INDEX_HTML.read_text(encoding="utf-8")
    except OSError as error:
        raise ProfileSyncError(f"could not read {INDEX_HTML}: {error}") from error

    updated = inject_cards(page, cards_html)
    if updated == page:
        return False

    try:
        INDEX_HTML.write_text(updated, encoding="utf-8")
    except OSError as error:
        raise ProfileSyncError(f"could not write {INDEX_HTML}: {error}") from error
    return True


def main() -> int:
    """CLI entry point. Returns a process exit code (``0`` ok, ``1`` on error)."""
    try:
        changed = update_index_html()
    except ProfileSyncError as error:
        print(f"error: {error}", file=sys.stderr)
        return 1

    if changed:
        print(f"Updated {len(FEATURED_PROJECTS)} project cards in index.html.")
    else:
        print("index.html is already up to date.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
