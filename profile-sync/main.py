import asyncio
import os
import sys

from config import FEATURED_PROJECTS, INDEX_HTML
from exceptions import ProfileSyncError
from github import build_client, fetch_repository_stats
from models import ProjectCard
from rendering import inject_cards, render_cards


async def collect_cards() -> list[ProjectCard]:
    """Fetch every project's stats in parallel, keeping the configured order."""
    token = os.environ.get("GITHUB_TOKEN")
    async with build_client(token) as client:
        try:
            async with asyncio.TaskGroup() as group:
                tasks = [
                    group.create_task(fetch_repository_stats(client, project.full_name))
                    for project in FEATURED_PROJECTS
                ]
        except* ProfileSyncError as group_error:
            raise group_error.exceptions[0] from None

    return [
        ProjectCard(project=project, stats=task.result())
        for project, task in zip(FEATURED_PROJECTS, tasks, strict=True)
    ]


async def update_index_html() -> bool:
    """Rewrite the cards in index.html; return True if the file changed."""
    cards = await collect_cards()
    cards_html = await render_cards(cards)

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


async def run() -> int:
    """Run the update and return a process exit status."""
    try:
        changed = await update_index_html()
    except ProfileSyncError as error:
        print(f"error: {error}", file=sys.stderr)
        return 1

    if changed:
        print(f"Updated {len(FEATURED_PROJECTS)} project cards in index.html.")
    else:
        print("index.html is already up to date.")
    return 0


def main() -> int:
    """Run the program and return its exit code."""
    return asyncio.run(run())


if __name__ == "__main__":
    raise SystemExit(main())
