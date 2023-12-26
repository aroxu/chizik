@echo off
pip install -r requirements.txt
pip install --no-binary :all: psutil
cls
python main.py
