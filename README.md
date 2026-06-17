# FFBOT Player Roster

A clean, searchable, auto-updating roster website for **FFBOT** (Final Fantasy chat game).

**Live Demo:** https://llamatodd.github.io/ffbot-roster/

## Features

- Real-time username search
- Click any player to see their recruited characters (level > 0 only)
- Proper character name capitalization
- Sort characters A-Z or by Level
- Auto-updates every 30 minutes
- Mobile-friendly dark theme

## How to Use

1. Visit the [live site](https://llamatodd.github.io/ffbot-roster/)
2. Search for a username
3. Click a player to see their full character roster and passives

## Setup For Your Own GitHub (Important!)

> ⚠️ **Do NOT skip this step** — otherwise it will try to push to llamatodd's repo.

1. Create your own GitHub repository (e.g. `ffbot-roster`)
2. Enable GitHub Pages (Settings → Pages → Deploy from main branch)
3. Download the files (`update_roster.py`, `update_and_push.bat`, etc.)
4. Place them in a folder with your `playerdatabase.ini`
5. **Change the Git remote** so it pushes to **your** repo:

   Open Command Prompt in the folder and run:
   ```cmd
   git remote set-url origin https://github.com/YOURUSERNAME/YOUR-REPO-NAME.git
