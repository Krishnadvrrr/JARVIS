@echo off
cd /d "C:\Users\spect\JARVIS"
"C:\Users\spect\JARVIS\venv\Scripts\python.exe" "C:\Users\spect\JARVIS\zepto_agent.py" %* > "C:\Users\spect\JARVIS\debug.log" 2>&1
