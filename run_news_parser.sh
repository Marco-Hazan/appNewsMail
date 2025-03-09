#!/bin/bash
exec > /home/ruckone/appNewsMail/postfix_script.log 2>&1
echo "Script started at $(date)"

# Activate the virtual environment
source /home/ruckone/appNewsMail/.venv/bin/activate

# Run the Python script
python3 /home/ruckone/appNewsMail/news_parser.py

echo "Script finished at $(date)"