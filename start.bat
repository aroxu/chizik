@echo off
pip install -r requirements.txt
pip install --no-binary :all: psutil
cls
uvicorn main:app --host 0.0.0.0 --port 11020 --reload
