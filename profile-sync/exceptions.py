class ProfileSyncError(Exception):
    """Base class for the errors this tool raises."""


class GitHubError(ProfileSyncError):
    """A GitHub request failed or returned something unexpected."""


class RenderingError(ProfileSyncError):
    """The cards could not be rendered or written to index.html."""
