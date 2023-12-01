#!/bin/bash
set -x

asdf plugin add poetry
asdf plugin add python
asdf install

poetry config virtualenvs.in-project true
poetry env use python
poetry install
