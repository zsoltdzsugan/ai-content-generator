#!/bin/bash

if [ -z "$1" ]; then
	echo "Usage: ./build.sh <basepath>"
	exit 1

uv run src/main.py publish "$1"
