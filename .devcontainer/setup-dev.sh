#!/bin/bash

cd /workspaces/my_data
rm -rf .venv
poetry config virtualenvs.in-project true
poetry install --with dev --with doc
