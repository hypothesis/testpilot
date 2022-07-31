import sys
from argparse import ArgumentParser
from importlib.metadata import version
from subprocess import DEVNULL, STDOUT, CalledProcessError

from testpilot import core


def cli(_argv=None):
    parser = ArgumentParser(
        description="Format, lint and test only the files that have changed on this branch.",
    )
    parser.add_argument("-d", "--debug", action="store_true")
    parser.add_argument("-v", "--version", action="store_true")
    parser.add_argument(
        "-t",
        "-s",
        "--tox",
        "--slower",
        action="store_true",
        help="run all commands in tox instead of directly",
    )

    args = parser.parse_args(_argv)

    if args.version:
        print(version("testpilot"))
        sys.exit()

    try:
        core.run(
            args.debug,
            ["git", "rev-parse", "--is-inside-work-tree"],
            stdout=DEVNULL,
            stderr=STDOUT,
        )
    except CalledProcessError:
        sys.exit("It looks like you aren't in a git repo")

    current_project = core.StandardProject(args.tox, args.debug)

    for project_class in [
        core.HProject,
        core.CheckmateProject,
        core.ViaProject,
        core.ViaHTMLProject,
        core.PythonPackageProject,
    ]:
        project = project_class(args.tox, args.debug)
        if project.is_current_project():
            current_project = project
            break

    if args.debug:
        core.log(f"Project class: {type(current_project)}")

    current_project.run_all()
