from pathlib import Path

from models import FeaturedProject

PROJECT_DIR = Path(__file__).resolve().parent
REPO_ROOT = PROJECT_DIR.parent
INDEX_HTML = REPO_ROOT / "index.html"
TEMPLATES_DIR = PROJECT_DIR / "templates"

GITHUB_API_URL = "https://api.github.com/repos/{full_name}"
REQUEST_TIMEOUT_SECONDS = 15

MARKER_START = "<!-- projects:start (auto-generated, do not edit by hand) -->"
MARKER_END = "<!-- projects:end -->"

FEATURED_PROJECTS: tuple[FeaturedProject, ...] = (
    FeaturedProject(
        full_name="djangopackages/djangopackages",
        description=(
            "A directory of reusable apps, sites, tools, and more for your Django projects."
        ),
    ),
    FeaturedProject(
        full_name="readthedocs/readthedocs.org",
        description=(
            "The source code that powers readthedocs.org. Contributed to database "
            "normalization, improved Elasticsearch performance by 15%, and unified Django settings."
        ),
    ),
    FeaturedProject(
        full_name="saadmk11/django-newsfeed",
        description=(
            "A Django package to create a news curator and newsletter subscription application."
        ),
    ),
    FeaturedProject(
        full_name="saadmk11/changelog-ci",
        description=(
            "GitHub Action that automatically generates changelogs using merged pull "
            "requests or commit messages."
        ),
    ),
    FeaturedProject(
        full_name="saadmk11/redis-search-django",
        description=(
            "Django package that provides auto indexing and searching capabilities for "
            "Django models using RediSearch."
        ),
    ),
    FeaturedProject(
        full_name="saadmk11/github-actions-version-updater",
        description=(
            "A GitHub Action that updates all GitHub Actions in a repository and creates "
            "a Pull Request with the updates."
        ),
    ),
    FeaturedProject(
        full_name="saadmk11/drf-test-generator",
        description=(
            "Generates basic unittest and pytest style tests for Django REST Framework ViewSets."
        ),
    ),
    FeaturedProject(
        full_name="saadmk11/python-third-party-imports",
        description=(
            "A Python CLI tool (written in Rust) that finds all third-party packages "
            "imported in your Python project."
        ),
    ),
)
