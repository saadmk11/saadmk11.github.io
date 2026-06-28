import textwrap
from collections.abc import Sequence

from jinja2 import Environment, FileSystemLoader
from jinja2.exceptions import TemplateError

from config import MARKER_END, MARKER_START, TEMPLATES_DIR
from exceptions import RenderingError
from models import ProjectCard

_CARD_TEMPLATE = "project_card.html.jinja"
_CARD_INDENT = " " * 24

_LANGUAGE_BADGES: dict[str, str] = {
    "Python": "bg-blue-100 text-blue-800 dark:bg-blue-900 dark:text-blue-200",
    "JavaScript": "bg-yellow-100 text-yellow-800 dark:bg-yellow-900 dark:text-yellow-200",
    "TypeScript": "bg-sky-100 text-sky-800 dark:bg-sky-900 dark:text-sky-200",
    "Rust": "bg-orange-100 text-orange-800 dark:bg-orange-900 dark:text-orange-200",
}
_DEFAULT_LANGUAGE_BADGE = "bg-slate-100 text-slate-700 dark:bg-slate-700 dark:text-slate-200"


def _language_badge(language: str) -> str:
    """Return the badge CSS classes for a language."""
    return _LANGUAGE_BADGES.get(language, _DEFAULT_LANGUAGE_BADGE)


_environment = Environment(
    loader=FileSystemLoader(TEMPLATES_DIR),
    autoescape=True,
    enable_async=True,
)
_environment.filters["language_badge"] = _language_badge


async def render_cards(cards: Sequence[ProjectCard]) -> str:
    """Render every card and return one indented HTML block."""
    try:
        template = _environment.get_template(_CARD_TEMPLATE)
        rendered = "\n".join([(await template.render_async(card=card)).strip() for card in cards])
    except TemplateError as error:
        raise RenderingError(f"could not render the project cards: {error}") from error
    return textwrap.indent(rendered, _CARD_INDENT)


def inject_cards(page: str, cards_html: str) -> str:
    """Replace the content between the project markers with cards_html."""
    start = page.find(MARKER_START)
    end = page.find(MARKER_END)
    if start == -1 or end == -1 or end < start:
        raise RenderingError("could not find the project markers in index.html")
    block = f"{MARKER_START}\n{cards_html}\n{_CARD_INDENT}{MARKER_END}"
    return page[:start] + block + page[end + len(MARKER_END) :]
