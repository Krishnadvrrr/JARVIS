@echo off
set "TARGET=%~1"
if "%TARGET%"=="" set "TARGET=https://www.youtube.com"
start "" "C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe" --new-window "%TARGET%"
