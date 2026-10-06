$DesktopPath = [System.Environment]::GetFolderPath([System.Environment+SpecialFolder]::Desktop)
$ShortcutPath = Join-Path $DesktopPath "J.A.R.V.I.S..lnk"
$TargetExe = "C:\Users\spect\JARVIS\venv\Scripts\pythonw.exe"
$AppScript = "C:\Users\spect\JARVIS\desktop_app.py"
$WorkingDir = "C:\Users\spect\JARVIS"

$WshShell = New-Object -ComObject WScript.Shell
$Shortcut = $WshShell.CreateShortcut($ShortcutPath)
$Shortcut.TargetPath = $TargetExe
$Shortcut.Arguments = "`"$AppScript`""
$Shortcut.WorkingDirectory = $WorkingDir
$Shortcut.Description = "J.A.R.V.I.S. Tactical Neural Interface - Shiv Nadar University"
# Holographic Iron Man / Cybernetic Wireframe Icon
$Shortcut.IconLocation = "C:\Users\spect\JARVIS\static\jarvis_logo.ico,0"
$Shortcut.Save()


Write-Host "Created shortcut successfully at: $ShortcutPath"
