# FFBOT Roster Viewer

A dynamic, auto-updating web roster for **FFBOT** (Final Fantasy chat game) with a retro pixel-RPG look — player cards, recruited character breakdowns, a live Awakening % leaderboard, and Twitch chat integration.

Live site: https://llamatodd.github.io/ffbot-roster/

## Features

**Player cards**
- Pixelated portrait of the currently active hero, with an **ACTIVE** tag confirming it's the one being leveled
- **Rank badge** (top-left) based on Awakening % — gold/silver/bronze medal for the top 3, a plain white `#N` for everyone else. Tied players share a rank instead of having ties broken arbitrarily
- Top 10 cards get a gold glow border; top 20 get a cooler blue-silver glow, so the leaderboard's upper tier stands out at a glance
- **ASC** (Ascension) badge over the portrait — the stat that matters long-term, since Level resets often and Ascension is what boosts Awakening %
- Large, color-coded **role badge** (DPS / Tank / Healer / Support) with a matching icon, top-right of the portrait
- **Awakening %** shown as a headline stat
- Stat grid (ATK/MAG/SPI/HP) labeled "post-ascension," with the player's preferred stat highlighted
- Wins shown as a quiet footer stat

**Character cards** (in the player detail modal)
- Portrait with a large faded "cropped hero" sprite bleeding into the card background
- **LV** badge (= wins) overlapping the portrait corner
- Color-coded role badge, Passive, and stats — including multi-word character names (e.g. "Auron Young," "Cait Sith") whose Passives previously showed as `None` due to a quoting quirk in the game's save format; this is fixed
- **Awakening tracker** — three pips for the W100 / W200 / W500 win thresholds. Unlocked pips show the awakening's name; locked pips show a live "X wins to go" countdown
- Speed, Specialty, and full Description

**Search & sort**
- Live search by username
- Sort player grid by **Rank**, **A-Z**, or **Z-A** (defaults to Rank, so the leaderboard order is what you see first)
- Filter character grid by role (with the same icon + color coding as the cards)

**Look & feel**
- Press Start 2P pixel font for names, levels, and badges; regular sans-serif for body text and descriptions so it stays readable
- Dark navy retro palette throughout
- Pixel-font title with a retro glow + decorative divider, flanked by a random row of hero sprites on each side (reshuffled on every page load) — Twitch credit link sits just below

## Twitch Integration (Streamer.bot)

- **`!rank`** — replies in chat with the typer's (or a named player's) rank, Awakening %, and active hero
- **`!top10`** — posts the current top 10 players by Awakening %, with medal emoji for the top 3
- **OBS / Meld browser overlay** — a standalone leaderboard panel (`top10_overlay.html`, hosted on this same site) showing the live top 10, styled to match the site exactly, auto-refreshing every 2 minutes. Revealed/hidden in-stream via a Streamer.bot command
- All of the above read from **`ranks.json`** (see below) rather than scraping the HTML, so they stay fast and simple to query

## Files

| File | Purpose |
|---|---|
| `update_roster.pyw` | Parses `playerdatabase.ini` + `character_list.csv` and generates `index.html` + `ranks.json`. Saved as `.pyw` so it can be double-clicked without a console window flashing up |
| `update_and_push.bat` | Runs the updater, pulls any remote changes first (so it self-heals if something was edited directly on GitHub), then commits and pushes `index.html` and `ranks.json` |
| `update_and_push_silent.vbs` | Launches `update_and_push.bat` completely hidden (no window, no stolen focus) — **point Task Scheduler at this, not the `.bat` directly** |
| `character_list.csv` | Character metadata (Role, Stats, Passive, Awakenings, Speed, Specialty, Description) |
| `portrait/` | Character sprites — must stay in the repo root |
| `index.html` | The generated site (auto-updated, don't hand-edit) |
| `ranks.json` | Clean, auto-generated JSON of every player's rank, Awakening %, active hero, role, and Ascension — built for bots/overlays to query directly |
| `top10_overlay.html` | Static OBS/Meld browser source showing the live top 10 leaderboard. Unlike the files above, this one is static and only needs to be pushed once |
| `.gitignore` | Keeps `roster_update.log` out of version control (a tracked log file previously caused git pull/push conflicts) |

## How to Set Up Your Own Copy

1. **Fork** this repo (or create a new one) and clone it locally
2. Make sure the `portrait/` folder has a PNG for every character in `character_list.csv` (filenames must match the title-cased character name, e.g. `Cloud AC` → `Cloud Ac.png`)
3. Edit the hardcoded `ini_path` near the bottom of `update_roster.pyw` to point at your own `playerdatabase.ini`
4. Update `update_and_push_silent.vbs`'s path to match your local folder location
5. Run `update_and_push.bat` once to test the full pipeline (generate → pull → commit → push)
6. Enable GitHub Pages (Settings → Pages → Deploy from the `main` branch)

### Auto-Update via Task Scheduler

1. Open **Task Scheduler** → **Create Basic Task**
2. Name it something like "FFBOT Roster Update"
3. Set the trigger to repeat on whatever interval you want (e.g. every 30 minutes)
4. Action → **Start a program**, pointing at `update_and_push_silent.vbs` (not the `.bat`)
5. Finish and test — it should run silently with no console window or focus stealing

Your PC needs to be on and the scheduled task enabled for updates to keep flowing.

## Known Upcoming Work

The game's next major update is replacing the single equipped **Passive** with a **Materia system** (multiple learnable/equippable Materia per character). The save file encodes Materia as a compact custom string format to save space, so `update_roster.pyw` will need a small decoder before Materia can show up on character cards. The dev has offered prerelease build access ahead of launch — once that's in hand, the goal is to get the decoder built and tested before the update goes live, rather than reverse-engineering it after the fact.

## Credits
- Built with Grok, llamatodd, and Claude
- Powered by Python + HTML/CSS/JS

---

Enjoy your roster! Feel free to open issues or PRs.