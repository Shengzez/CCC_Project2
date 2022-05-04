#!/bin/sh

cd /CCC_Project2/Backend/
python3 -m pip install -r requirements.txt
python3 --version
python3 api.py
exec "$@"
