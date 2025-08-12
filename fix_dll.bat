@echo off
echo Fixing Python DLL loading issues...

set APP_DIR=%~dp0build\MinecraftSoundsApp\MinecraftSounds

if not exist "%APP_DIR%\_internal" (
    echo Error: Application directory not found, please make sure you have run build.bat
    pause
    exit /b 1
)

echo Copying DLL files from _internal directory to application root directory...

for %%f in ("%APP_DIR%\_internal\python*.dll" "%APP_DIR%\_internal\VCRUNTIME*.dll" "%APP_DIR%\_internal\ucrtbase.dll") do (
    echo Copying %%~nxf
    copy /Y "%%f" "%APP_DIR%\%%~nxf" > nul
)

echo.
echo DLL fix completed! Please try running the application again.
echo If you still encounter issues, please refer to README_PACKAGING.md file.

pause