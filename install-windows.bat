@echo off
setlocal
set "CEASY_EXE=%~dp0ceasy.exe"
if not exist "%CEASY_EXE%" (
  echo Ceasy.exe was not found.
  echo Download and extract the Windows bundle, then run this installer from that folder.
  pause
  exit /b 1
)
for %%E in (.ce .ceasy) do (
  reg add "HKCU\Software\Classes\%%E" /ve /d "CeasySourceFile" /f >nul
)
reg add "HKCU\Software\Classes\CeasySourceFile" /ve /d "Ceasy source file" /f >nul
reg add "HKCU\Software\Classes\CeasySourceFile\DefaultIcon" /ve /d "\"%CEASY_EXE%\",0" /f >nul
reg add "HKCU\Software\Classes\CeasySourceFile\shell\open\command" /ve /d "\"%CEASY_EXE%\" \"%%1\" --pause" /f >nul
if errorlevel 1 (
  echo Could not register Ceasy file types. Try running this file again.
  pause
  exit /b 1
)
echo Ceasy is installed for this Windows user.
echo You can now double-click .ce and .ceasy files to run them.
echo Keep ceasy.exe in this folder; the file association points to it.
pause
