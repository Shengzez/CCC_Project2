#!/bin/sh

cd /CCC_Project2/TwitterStreamer/
python3 -m pip install -r stream_requirements.txt
python3 --version
python3 tweetStreamer.py
exec "$@"
