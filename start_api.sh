#!/usr/bin/env bash
set -e

conda activate llm
uvicorn api:app --reload
