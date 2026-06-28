"""A tiny GitHub REST API client built on the standard-library ``urllib``.

Only one endpoint is needed -- ``GET /repos/{owner}/{repo}`` -- so this stays
deliberately small. Every failure mode (network, HTTP status, malformed body,
missing fields) is translated into a :class:`~exceptions.GitHubError` carrying a
human-readable message, so callers never have to know about ``urllib`` details.
"""

import json
import urllib.error
import urllib.request
from http import HTTPStatus

from config import GITHUB_API_URL, REQUEST_TIMEOUT_SECONDS
from exceptions import GitHubError
from models import GitHubRepositoryPayload, RepositoryStats

_USER_AGENT = "saadmk11-profile-sync"
_FALLBACK_LANGUAGE = "Code"


def fetch_repository_stats(full_name: str, token: str | None = None) -> RepositoryStats:
    """Fetch the live star, fork and watcher counts plus the primary language.

    Args:
        full_name: The ``owner/repo`` identifier, e.g. ``saadmk11/changelog-ci``.
        token: An optional GitHub token. Supplying one raises the (otherwise very
            low) unauthenticated rate limit.

    Returns:
        The repository's current :class:`~models.RepositoryStats`.

    Raises:
        GitHubError: If the repository cannot be reached, the response is not
            valid JSON, or an expected field is missing.
    """
    payload = _request_repository(full_name, token)
    try:
        return RepositoryStats(
            stars=payload["stargazers_count"],
            forks=payload["forks_count"],
            watchers=payload["subscribers_count"],
            language=payload["language"] or _FALLBACK_LANGUAGE,
        )
    except KeyError as error:
        raise GitHubError(
            f"unexpected GitHub response for {full_name}: missing field {error}"
        ) from error


def _request_repository(full_name: str, token: str | None) -> GitHubRepositoryPayload:
    """Perform the HTTP GET and decode the JSON body.

    All low-level ``urllib``/``json`` failures are re-raised as
    :class:`~exceptions.GitHubError` with an actionable message.
    """
    request = urllib.request.Request(GITHUB_API_URL.format(full_name=full_name))
    request.add_header("Accept", "application/vnd.github+json")
    request.add_header("X-GitHub-Api-Version", "2022-11-28")
    request.add_header("User-Agent", _USER_AGENT)
    if token:
        request.add_header("Authorization", f"Bearer {token}")

    try:
        with urllib.request.urlopen(request, timeout=REQUEST_TIMEOUT_SECONDS) as response:
            payload: GitHubRepositoryPayload = json.load(response)
    except urllib.error.HTTPError as error:
        raise GitHubError(_describe_http_error(full_name, error)) from error
    except urllib.error.URLError as error:
        raise GitHubError(f"could not reach GitHub for {full_name}: {error.reason}") from error
    except TimeoutError as error:
        raise GitHubError(
            f"timed out fetching {full_name} after {REQUEST_TIMEOUT_SECONDS}s"
        ) from error
    except json.JSONDecodeError as error:
        raise GitHubError(f"invalid JSON in GitHub response for {full_name}: {error}") from error
    return payload


def _describe_http_error(full_name: str, error: urllib.error.HTTPError) -> str:
    """Turn an :class:`~urllib.error.HTTPError` into a helpful message.

    The common rate-limit and not-found cases get tailored hints; everything else
    falls back to the raw status.
    """
    match error.code:
        case HTTPStatus.FORBIDDEN | HTTPStatus.TOO_MANY_REQUESTS if (
            error.headers.get("X-RateLimit-Remaining") == "0"
        ):
            return (
                f"GitHub API rate limit exceeded while fetching {full_name}; "
                "set the GITHUB_TOKEN environment variable to raise the limit"
            )
        case HTTPStatus.NOT_FOUND:
            return f"repository {full_name} not found (is the name correct?)"
        case _:
            return f"GitHub API returned {error.code} {error.reason} for {full_name}"
