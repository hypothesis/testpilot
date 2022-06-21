#!/usr/bin/env python3
import json
import os
from pathlib import Path

from cookiecutter.main import cookiecutter

COOKIECUTTER_JSON_PATH = ".cookiecutter/cookiecutter.json"

with open(COOKIECUTTER_JSON_PATH, "r", encoding="utf-8") as cookiecutter_json_file:
    config = json.loads(cookiecutter_json_file.read())

cookiecutter(
    template=config["template"],
    directory=config["directory"],
    extra_context=config["extra_context"],
    no_input=True,
    overwrite_if_exists=True,
    output_dir=Path(os.getcwd()).parent,
)
