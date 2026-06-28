from dataclasses import dataclass
from typing import TypedDict


@dataclass(frozen=True, slots=True)
class FeaturedProject:
    """A repository to feature, with a hand-written description."""

    full_name: str
    description: str

    @property
    def name(self) -> str:
        """The repository name without the owner."""
        return self.full_name.split("/", maxsplit=1)[1]

    @property
    def url(self) -> str:
        """The repository's URL on GitHub."""
        return f"https://github.com/{self.full_name}"


@dataclass(frozen=True, slots=True)
class RepositoryStats:
    """The numbers fetched from GitHub for one repository."""

    stars: int
    forks: int
    watchers: int
    language: str


@dataclass(frozen=True, slots=True)
class ProjectCard:
    """A featured project together with its fetched stats."""

    project: FeaturedProject
    stats: RepositoryStats


class GitHubRepositoryPayload(TypedDict):
    """The fields read from GET /repos/{owner}/{repo}."""

    stargazers_count: int
    forks_count: int
    subscribers_count: int
    language: str | None
