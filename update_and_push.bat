@echo off
echo ========================================
echo     FFBOT Roster Auto Updater
echo ========================================

cd /d "%~dp0"

echo Updating roster...
python update_roster.py

if %errorlevel% neq 0 (
    echo.
    echo ❌ Python script failed. Check the path in update_roster.py
    pause
    exit /b
)

echo.
echo Committing and pushing to GitHub...

git add index.html
git commit -m "Auto-update roster - %date% %time%"
git push

echo.
echo ✅ Done! Site should update shortly on GitHub Pages.
echo.

pause
