#!/usr/bin/env bash
cd /home/taikun/workspace/strava-kudos-taikun
set -e
source .venv/bin/activate
nohup python3 mainFlask.py &
