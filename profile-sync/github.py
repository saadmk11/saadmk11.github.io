import json
from http import HTTPStatus

import httpx

from config import GITHUB_API_URL, REQUEST_TIMEOUT_SECONDS
from exceptions import GitHubError
from models import GitHubRepositoryPayload, RepositoryStats

_USER_AGENT = "saadmk11-profile-sync"
_FALLBACK_LANGUAGE = "Code"


def build_client(token: str | None = None) -> httpx.AsyncClient:
    """Build a shared client for the GitHub API.

    Use it as an async context manager so connections are reused. A token, if
    given, raises the rate limit.
    """
    headers = {
        "Accept": "application/vnd.github+json",
        "X-GitHub-Api-Version": "2022-11-28",
        "User-Agent": _USER_AGENT,
    }
    if token:
        headers["Authorization"] = f"Bearer {token}"
    return httpx.AsyncClient(headers=headers, timeout=REQUEST_TIMEOUT_SECONDS)


async def fetch_repository_stats(client: httpx.AsyncClient, full_name: str) -> RepositoryStats:
    """Fetch the current stats for a repository, e.g. "saadmk11/changelog-ci".

    Raises GitHubError if the request fails or the response is malformed.
    """
    try:
        response = await client.get(GITHUB_API_URL.format(full_name=full_name))
        response.raise_for_status()
        payload: GitHubRepositoryPayload = response.json()
        return RepositoryStats(
            stars=payload["stargazers_count"],
            forks=payload["forks_count"],
            watchers=payload["subscribers_count"],
            language=payload["language"] or _FALLBACK_LANGUAGE,
        )
    except httpx.HTTPStatusError as error:
        raise GitHubError(_describe_http_error(full_name, error)) from error
    except httpx.TimeoutException as error:
        raise GitHubError(
            f"timed out fetching {full_name} after {REQUEST_TIMEOUT_SECONDS}s"
        ) from error
    except httpx.RequestError as error:
        raise GitHubError(f"could not reach GitHub for {full_name}: {error}") from error
    except (json.JSONDecodeError, KeyError) as error:
        raise GitHubError(f"unexpected GitHub response for {full_name}: {error}") from error


def _describe_http_error(full_name: str, error: httpx.HTTPStatusError) -> str:
    """Turn an HTTP error from GitHub into a readable message."""
    response = error.response
    match response.status_code:
        case HTTPStatus.FORBIDDEN | HTTPStatus.TOO_MANY_REQUESTS if (
            response.headers.get("X-RateLimit-Remaining") == "0"
        ):
            return f"GitHub rate limit hit while fetching {full_name}; set GITHUB_TOKEN to raise it"
        case HTTPStatus.NOT_FOUND:
            return f"repository {full_name} not found"
        case _:
            return (
                f"GitHub returned {response.status_code} {response.reason_phrase} for {full_name}"
            )
