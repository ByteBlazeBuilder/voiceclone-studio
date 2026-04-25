@echo off
echo.
echo  VoiceClone Studio — XTTS-v2
echo  Starting...
echo  Open http://localhost:5000
echo.
call conda activate voiceclone
start "" http://localhost:5000
python app.py
