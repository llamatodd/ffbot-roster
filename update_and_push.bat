@echo off
setlocal enabledelayedexpansion

echo ========================================
echo     FFBOT Roster Auto Updater
echo ========================================

cd /d "%~dp0"

echo [%date% %time%] Running updater... >> roster_update.log
python update_roster.py

echo. >> roster_update.log
echo [%date% %time%] Committing and pushing... >> roster_update.log

git add index.html
git commit -m "Auto-update roster - %date% %time%" >> roster_update.log 2>&1
git push >> roster_update.log 2>&1

echo [%date% %time%] Done! >> roster_update.log
echo. >> roster_update.log