#!/usr/bin/env python3
"""
Create a new patch release on GitHub.

A changelog will be automatically generated from your commits.

The creation of a new GitHub release will then trigger the publish workflow on
GitHub Actions to publish the release to PyPI.

Requires GitHub CLI: https://cli.github.com/

You can either run this locally or by manually triggering the release workflow
on GitHub Actions:
https://docs.github.com/en/actions/managing-workflow-runs/manually-running-a-workflow

If you're running this script locally it will create a new release using the
latest commit from the main branch *on GitHub*. It does not use whatever is in
your local copy.

You don't need to use this script to create a new release!
You can just create a release manually in the GitHub web interface or by
running GitHub CLI's `gh release create` command:
https://cli.github.com/manual/gh_release_create
The advantage of running *this* script is that it'll calculate the new version
number for you by bumping the patch number of the last release.
"""
import json
import subprocess


def last_version() -> str:
    """Return the version number of the last release."""

    json_string = (
        subprocess.run(
            ["gh", "release", "view", "--json", "tagName"],
            check=True,
            stdout=subprocess.PIPE,
        )
        .stdout.decode("utf8")
        .strip()
    )

    return json.loads(json_string)["tagName"]


def bump_patch_number(version_number: str) -> str:
    """Return a copy of version_number with the patch number incremented."""

    # This assumes that version_number is a simple "X.Y.Z" string,
    # it's not fully robust semantic version number parsing.
    major, minor, patch = version_number.split(".")
    return f"{major}.{minor}.{int(patch) + 1}"


def create_new_patch_release():
    """Create a new patch release on GitHub."""

    new_version_number = bump_patch_number(last_version())

    subprocess.run(
        ["gh", "release", "create", "--generate-notes", new_version_number],
        check=True,
    )


if __name__ == "__main__":
    create_new_patch_release()
