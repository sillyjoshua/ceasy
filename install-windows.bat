@echo off
setlocal EnableExtensions

set "SOURCE_EXE=%~dp0ceasy.exe"
if not exist "%SOURCE_EXE%" (
  echo Ceasy.exe was not found.
  echo Download and extract the Windows bundle, then run this installer from that folder.
  pause
  exit /b 1
)

rem Install per-user in a stable location so moving the ZIP folder will not break Ceasy.
set "CEASY_INSTALL_DIR=%LOCALAPPDATA%\Programs\Ceasy"
if not exist "%CEASY_INSTALL_DIR%" mkdir "%CEASY_INSTALL_DIR%"
if errorlevel 1 (
  echo Could not create the Ceasy installation directory.
  pause
  exit /b 1
)

copy /y "%SOURCE_EXE%" "%CEASY_INSTALL_DIR%\ceasy.exe" >nul
if errorlevel 1 (
  echo Could not copy ceasy.exe into "%CEASY_INSTALL_DIR%".
  pause
  exit /b 1
)
set "CEASY_EXE=%CEASY_INSTALL_DIR%\ceasy.exe"

rem Update the user PATH through .NET, not SETX. SETX can truncate long PATH values.
powershell -NoProfile -ExecutionPolicy Bypass -Command "$d=$env:CEASY_INSTALL_DIR; $p=[Environment]::GetEnvironmentVariable('Path','User'); $found=$false; foreach($x in ($p -split ';')) { if($x.Trim().TrimEnd('\') -ieq $d.TrimEnd('\')) { $found=$true } }; if(-not $found) { if([string]::IsNullOrWhiteSpace($p)) { $p=$d } else { $p=$p.TrimEnd(';')+';'+$d }; [Environment]::SetEnvironmentVariable('Path',$p,'User') }"
if errorlevel 1 (
  echo Ceasy was copied, but Windows could not update your user PATH.
  echo Add this folder to your user PATH manually:
  echo %CEASY_INSTALL_DIR%
  pause
  exit /b 1
)

for %%E in (.ce .ceasy) do (
  reg add "HKCU\Software\Classes\%%E" /ve /d "CeasySourceFile" /f >nul
)
reg add "HKCU\Software\Classes\CeasySourceFile" /ve /d "Ceasy source file" /f >nul
reg add "HKCU\Software\Classes\CeasySourceFile\DefaultIcon" /ve /d "\"%CEASY_EXE%\",0" /f >nul
reg add "HKCU\Software\Classes\CeasySourceFile\shell\open\command" /ve /d "\"%CEASY_EXE%\" \"%1\" --pause" /f >nul
if errorlevel 1 (
  echo Ceasy was added to PATH, but Windows file associations could not be registered.
  pause
  exit /b 1
)

echo.
echo Ceasy is installed for your Windows user.
echo Executable: %CEASY_EXE%
echo The install folder has been added to your user PATH without overwriting or truncating it.
echo Open a NEW Command Prompt or PowerShell window, then run: ceasy yourfile.ceasy
echo You can also double-click .ce and .ceasy files.
echo.
pause
