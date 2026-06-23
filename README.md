# FFBOT Roster Viewer

A dynamic, auto-updating web roster for **FFBOT** (Final Fantasy chat game) with a retro pixel-RPG look — player cards, recruited character breakdowns, awakening progress, and live search.

Live site: https://llamatodd.github.io/ffbot-roster/

## Features

**Player cards**
- Pixelated portrait of the currently active hero, with an **ACTIVE** tag confirming it's the one being leveled
- **ASC** (Ascension) badge over the portrait — the stat that actually matters long-term, since Level resets often and Ascension is what boosts Awakening %
- Large, color-coded **role badge** (DPS / Tank / Healer / Support) with a matching icon, top-right of the portrait
- **Awakening %** shown as a headline stat
- Stat grid (ATK/MAG/SPI/HP) labeled "post-ascension," with the player's preferred stat highlighted
- Wins shown as a quiet footer stat (nice to look at, but not the focus)

**Character cards** (in the player detail modal)
- Portrait with a large faded "cropped hero" sprite bleeding into the card background
- **LV** badge (= wins) overlapping the portrait corner
- Color-coded role badge, Passive, and stats
- **Awakening tracker** — three pips for the W100 / W200 / W500 win thresholds. Unlocked pips show the awakening's name; locked pips show a live "X wins to go" countdown
- Speed, Specialty, and full Description

**Search & sort**
- Live search by username
- Sort A-Z / Z-A, Level Hi-Low / Low-Hi
- Filter by role (with the same icon + color coding as the cards)

**Look & feel**
- Press Start 2P pixel font for names, levels, and badges; regular sans-serif for body text and descriptions so it stays readable
- Dark navy retro palette throughout

## Files

| File | Purpose |
|---|---|
| `update_roster.pyw` | Parses `playerdatabase.ini` + `character_list.csv` and generates `index.html`. Saved as `.pyw` so it can be double-clicked without a console window flashing up |
| `update_and_push.bat` | Runs the updater, then commits and pushes `index.html` to GitHub |
| `update_and_push_silent.vbs` | Launches `update_and_push.bat` completely hidden (no window, no stolen focus) — **point Task Scheduler at this, not the `.bat` directly** |
| `character_list.csv` | Character metadata (Role, Stats, Passive, Awakenings, Speed, Specialty, Description) |
| `portrait/` | Character sprites — must stay in the repo root |
| `index.html` | The generated site (auto-updated, don't hand-edit) |

## How to Set Up Your Own Copy

1. **Fork** this repo (or create a new one) and clone it locally
2. Make sure the `portrait/` folder has a PNG for every character in `character_list.csv` (filenames must match the title-cased character name, e.g. `Cloud AC` → `Cloud Ac.png`)
3. Edit the hardcoded `ini_path` near the bottom of `update_roster.pyw` to point at your own `playerdatabase.ini`
4. Update `update_and_push_silent.vbs`'s path to match your local folder location
5. Run `update_and_push.bat` once to test the full pipeline (generate → commit → push)
6. Enable GitHub Pages (Settings → Pages → Deploy from the `main` branch)

### Auto-Update via Task Scheduler

1. Open **Task Scheduler** → **Create Basic Task**
2. Name it something like "FFBOT Roster Update"
3. Set the trigger to repeat on whatever interval you want (e.g. every 30 minutes)
4. Action → **Start a program**, pointing at `update_and_push_silent.vbs` (not the `.bat`)
5. Finish and test — it should run silently with no console window or focus stealing

Your PC needs to be on and the scheduled task enabled for updates to keep flowing.

## Known Upcoming Work

The game's next major update is replacing the single equipped **Passive** with a **Materia system** (multiple learnable/equippable Materia per character). The dev mentioned the save file encodes Materia as a compact custom string format (not plain readable data) to save space, which means `update_roster.pyw` will need a small decoder for that format before Materia can show up on character cards. Waiting on the actual encode/decode spec (or sample strings) from the dev before building that out.

## Credits
- Built with Grok, llamatodd, and Claude
- Powered by Python + HTML/CSS/JS

---

Enjoy your roster! Feel free to open issues or PRs.
