# FFBOT Roster Viewer

A dynamic, auto-updating web roster for **FFBOT** (Final Fantasy chat game) that displays all players, their units, stats, recruited characters, awakenings, and more.

Live demo: https://llamatodd.github.io/ffbot-roster/

## Features

- **Search** by username
- **Player cards** with portraits, stats, preferred stat highlight, Asc, Awakening %
- **Detailed modal** when clicking a player:
  - All recruited characters with portraits
  - Level, Passive, Awakenings (with learned/unlearned styling)
  - Speed, Specialty, full Description
  - Role color coding (DPS, Tank, Healer, Support)
- **Sorting**:
  - A-Z / Z-A
  - Hi-Low / Low-Hi by level
  - Sort by Role
- **Auto-updates** every 30 minutes via GitHub Actions

## Files

- `update_roster.py` – Parses `playerdatabase.ini` + `character_list.csv` and generates `index.html`
- `update_and_push.bat` – Runs the updater and pushes to GitHub
- `character_list.csv` – Character metadata (Role, Stats, Awakenings, etc.)
- `portrait/` folder – Character sprites (must stay in repo root)
- `index.html` – The generated website (auto-updated)

## How to Set Up Your Own Copy

1. **Fork** this repo or create a new one
2. **Clone** it to your computer
3. Place your `playerdatabase.ini` in the correct path (edit the path in `update_roster.py`)
4. Make sure the `portrait` folder contains all character PNGs
5. Update `character_list.csv` if needed
6. Run `update_and_push.bat` once to test
7. Set up GitHub Pages (Settings → Pages → Deploy from main branch)

### Auto-Update (Recommended)
1. Open **Task Scheduler** (search for it in Start menu)
2. Right-click **Task Scheduler Library** → **Create Basic Task**
3. Name it "FFBOT Roster Update"
4. Set trigger to **Daily** → choose time (e.g., every 30 minutes)
5. Action → **Start a program**
   - Program/script: `C:\Users\YourUsername\Desktop\FFBOT-Roster\update_and_push.bat`
6. Finish and test the task

The site will update automatically every 30 minutes and push to GitHub Pages.

## Credits
- Built with ❤️ by Grok + llamatodd
- Powered by Python + HTML/CSS/JS

---

Enjoy your roster! Feel free to open issues or PRs.
