"""Render project cards with Jinja2 and inject them into ``index.html``.

The Jinja template emits a single card at column zero; this module indents the
combined output to match the surrounding markup and swaps it in between the
``MARKER_START`` / ``MARKER_END`` comments. Autoescaping is enabled, so every
dynamic value in the template is HTML-escaped automatically.
"""

import textwrap
from collections.abc import Sequence

from jinja2 import Environment, FileSystemLoader

from config import MARKER_END, MARKER_START, TEMPLATES_DIR
from exceptions import RenderingError
from models import ProjectCard

_CARD_TEMPLATE = "project_card.html.jinja"

# Indentation of a card inside ``<div id="openSourceRepos">`` in index.html.
_CARD_INDENT = " " * 24

# Tailwind badge classes keyed by GitHub's primary-language name.
_LANGUAGE_BADGES: dict[str, str] = {
    "Python": "bg-blue-100 text-blue-800 dark:bg-blue-900 dark:text-blue-200",
    "JavaScript": "bg-yellow-100 text-yellow-800 dark:bg-yellow-900 dark:text-yellow-200",
    "TypeScript": "bg-sky-100 text-sky-800 dark:bg-sky-900 dark:text-sky-200",
    "Rust": "bg-orange-100 text-orange-800 dark:bg-orange-900 dark:text-orange-200",
}
_DEFAULT_LANGUAGE_BADGE = "bg-slate-100 text-slate-700 dark:bg-slate-700 dark:text-slate-200"


def _language_badge(language: str) -> str:
    """Return the Tailwind badge classes for a programming language."""
    return _LANGUAGE_BADGES.get(language, _DEFAULT_LANGUAGE_BADGE)


def _build_environment() -> Environment:
    """Create a Jinja2 environment with HTML autoescaping for the card template."""
    environment = Environment(
        loader=FileSystemLoader(TEMPLATES_DIR),
        autoescape=True,
        trim_blocks=True,
        lstrip_blocks=True,
        keep_trailing_newline=False,
    )
    environment.filters["language_badge"] = _language_badge
    return environment


def render_cards(cards: Sequence[ProjectCard]) -> str:
    """Render every card into a single, correctly indented HTML block.

    Raises:
        RenderingError: If the template cannot be found or rendered.
    """
    try:
        template = _build_environment().get_template(_CARD_TEMPLATE)
        rendered = "\n".join(template.render(card=card).strip() for card in cards)
    except Exception as error:  # Jinja raises a few unrelated exception types.
        raise RenderingError(f"failed to render the project cards: {error}") from error
    return textwrap.indent(rendered, _CARD_INDENT)


def inject_cards(page: str, cards_html: str) -> str:
    """Return ``page`` with the content between the markers replaced by ``cards_html``.

    Raises:
        RenderingError: If either marker is missing or they appear out of order.
    """
    start = page.find(MARKER_START)
    end = page.find(MARKER_END)
    if start == -1 or end == -1 or end < start:
        raise RenderingError(
            "could not locate the projects markers in index.html "
            f"({MARKER_START!r} ... {MARKER_END!r})"
        )

    block = f"{MARKER_START}\n{cards_html}\n{_CARD_INDENT}{MARKER_END}"
    return page[:start] + block + page[end + len(MARKER_END) :]
