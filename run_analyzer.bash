#!/bin/bash
source /home/pi/Projects/osm-transferlist-analyzer/venv/bin/activate
python3 /home/pi/Projects/osm-transferlist-analyzer/src/get_data.py
python3 /home/pi/Projects/osm-transferlist-analyzer/src/update_data.py
python3 /home/pi/Projects/osm-transferlist-analyzer/src/message.py