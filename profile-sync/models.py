"""Typed data structures shared across profile-sync.

These are deliberately small, immutable value objects. Keeping them free of any
behaviour (beyond trivial derived properties) makes the data flow easy to follow:
:mod:`github` produces :class:`RepositoryStats`, :mod:`config` owns the curated
:class:`FeaturedProject` list, and :mod:`rendering` consumes :class:`ProjectCard`.
"""

from dataclasses import dataclass
from typing import TypedDict


@dataclass(frozen=True, slots=True)
class FeaturedProject:
    """A GitHub repository to feature, paired with a hand-written description."""

    full_name: str
    """The ``owner/repo`` identifier, e.g. ``saadmk11/changelog-ci``."""

    description: str
    """A short, curated summary shown on the card (not the GitHub description)."""

    @property
    def name(self) -> str:
        """The repository name without its owner, e.g. ``changelog-ci``."""
        return self.full_name.split("/", maxsplit=1)[1]

    @property
    def url(self) -> str:
        """The canonical GitHub URL for the repository."""
        return f"https://github.com/{self.full_name}"


@dataclass(frozen=True, slots=True)
class RepositoryStats:
    """Live, periodically refreshed numbers for a single repository."""

    stars: int
    forks: int
    watchers: int
    language: str


@dataclass(frozen=True, slots=True)
class ProjectCard:
    """A featured project combined with its freshly fetched stats.

    This is the unit the Jinja template renders into a single card.
    """

    project: FeaturedProject
    stats: RepositoryStats


class GitHubRepositoryPayload(TypedDict):
    """The subset of GitHub's ``GET /repos/{owner}/{repo}`` response we read."""

    stargazers_count: int
    forks_count: int
    subscribers_count: int
    language: str | None
