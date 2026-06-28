"""Exception hierarchy for profile-sync.

A single base class (:class:`ProfileSyncError`) lets the entry point catch every
expected failure in one place and report it cleanly, while the subclasses keep
the origin of a failure obvious at the call site.
"""


class ProfileSyncError(Exception):
    """Base class for every error profile-sync raises intentionally."""


class GitHubError(ProfileSyncError):
    """The GitHub API could not be queried or returned an unexpected response."""


class RenderingError(ProfileSyncError):
    """The project cards could not be rendered or written into ``index.html``."""
