#!/bin/bash
source /home/pi/Projects/osm-transferlist-analyzer/venv/bin/activate
python3 src/get_data.py
python3 src/update_data.py
python3 src/message.py