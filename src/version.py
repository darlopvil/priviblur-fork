import hashlib
import os
import pathlib
import subprocess

CURRENT_VERSION = "v0.4.0-dev"

# Taken from the Invidious Project
# CURRENT_BRANCH = subprocess.run(
#     "git branch --show-current".split(),
#     stdout=subprocess.PIPE
# ).stdout.decode("utf-8").strip()


def _commit_from_environment():
    """Commit hash injected at build time, see docker/Dockerfile."""
    return os.environ.get("PRIVIBLUR_COMMIT", "").strip()


def _commit_from_git():
    """Commit hash from the working tree, for runs from a checkout.

    Returns an empty string when git is unavailable or this is not a
    repository, instead of crashing at import time.
    """
    try:
        result = subprocess.run(
            "git rev-list HEAD --max-count=1 --abbrev-commit".split(),
            stdout=subprocess.PIPE,
            stderr=subprocess.DEVNULL,
            check=True,
        )
    except (OSError, subprocess.CalledProcessError):
        return ""

    return result.stdout.decode("utf-8").strip()


# The environment wins so that container images do not need to ship .git/ just
# to know their own commit. See issue #16.
CURRENT_COMMIT = _commit_from_environment() or _commit_from_git() or "unknown"

PROJECT_VERSION = f"{CURRENT_VERSION}"
VERSION = f"{CURRENT_VERSION}-{CURRENT_COMMIT}"


def _compute_asset_version():
    """Fingerprint of everything under assets/, used for cache busting.

    Derived from the contents of the files rather than from the commit hash.
    A commit-based value meant that any change to a stylesheet was invisible to
    browsers until it was committed: the URL did not change, so the browser
    kept serving its cached copy. That turned every CSS iteration into a
    "why is my change not applying" hunt. See issue #16.

    assets/ is a handful of small files, so hashing them once at import costs
    nothing worth measuring.
    """
    assets_path = pathlib.Path(__file__).parent.parent / "assets"

    digest = hashlib.sha256()

    if not assets_path.is_dir():
        return "unknown"

    for path in sorted(assets_path.rglob("*")):
        if path.is_file():
            digest.update(path.relative_to(assets_path).as_posix().encode("utf-8"))
            digest.update(path.read_bytes())

    return digest.hexdigest()[:12]


ASSET_VERSION = _compute_asset_version()