@echo off
if "%~1"=="" exit /b
if exist "C:\Program Files\Google\Chrome\Application\chrome.exe" (
    start "" "C:\Program Files\Google\Chrome\Application\chrome.exe" --new-window "%~1"
) else (
    start "" "C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe" --new-window "%~1"
)
