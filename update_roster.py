import configparser
import json
from pathlib import Path

def parse_ffbot_ini(ini_path):
    config = configparser.ConfigParser()
    config.read(ini_path, encoding='utf-8')
    
    players = []
    for section in config.sections():
        if section.lower() in ['metadata']:
            continue
        player = {'username': section}
        for key, value in config.items(section):
            player[key] = value
        players.append(player)
    return players

def generate_html(players):
    html = '''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>FFBOT Roster</title>
    <style>
        body { font-family: Arial, sans-serif; background: #1a1a2e; color: #eee; margin: 0; padding: 20px; }
        h1 { text-align: center; color: #00ffcc; }
        #search { width: 100%; max-width: 600px; margin: 20px auto; display: block; padding: 12px; font-size: 18px; border-radius: 8px; border: none; }
        .player-grid { display: grid; grid-template-columns: repeat(auto-fill, minmax(280px, 1fr)); gap: 16px; max-width: 1400px; margin: 0 auto; }
        .player-card { background: #16213e; border-radius: 12px; padding: 16px; cursor: pointer; transition: all 0.2s; }
        .player-card:hover { transform: scale(1.03); background: #1e2a5e; }
        .modal { display: none; position: fixed; top: 0; left: 0; width: 100%; height: 100%; background: rgba(0,0,0,0.9); z-index: 1000; }
        .modal-content { background: #16213e; max-width: 900px; margin: 50px auto; padding: 25px; border-radius: 12px; max-height: 90vh; overflow-y: auto; }
    </style>
</head>
<body>
    <h1>FFBOT Player Roster</h1>
    <input type="text" id="search" placeholder="Search by username..." onkeyup="filterPlayers()">
    
    <div class="player-grid" id="playerGrid"></div>

    <div id="modal" class="modal">
        <div class="modal-content" id="modalContent"></div>
    </div>

    <script>
        const players = ''' + json.dumps(players, ensure_ascii=False) + ''';

        function filterPlayers() {
            const term = document.getElementById('search').value.toLowerCase();
            const grid = document.getElementById('playerGrid');
            grid.innerHTML = '';
            
            players.forEach(p => {
                if (p.username.toLowerCase().includes(term)) {
                    const card = document.createElement('div');
                    card.className = 'player-card';
                    card.innerHTML = `
                        <h3>${p.username}</h3>
                        <p>Level: ${p.lv || 'N/A'} | Unit: ${p.unit || 'N/A'}</p>
                        <p>Collection: <strong>${p.collection || 0}/160</strong></p>
                        <p>Wins: ${parseInt(p.wins || 0).toLocaleString()}</p>
                    `;
                    card.onclick = () => showDetails(p);
                    grid.appendChild(card);
                }
            });
        }

        function showDetails(p) {
            let characters = [];
            
            Object.keys(p).forEach(key => {
                if (key.startsWith('awakeninglv')) {
                    let rawName = key.replace('awakeninglv', '').replace(/["']/g, '').trim();
                    
                    // Stronger title case
                    let displayName = rawName.split(' ').map(word => {
                        return word.charAt(0).toUpperCase() + word.slice(1).toLowerCase();
                    }).join(' ');
                    
                    const level = parseInt(p[key]) || 0;
                    
                    let passive = 'None';
                    const possibleKeys = [`ps5${rawName}`, `ps${rawName}`, `ps5${rawName.replace(/ /g,'')}`, `ps${rawName.replace(/ /g,'')}`];
                    for (let pk of possibleKeys) {
                        if (p[pk]) {
                            passive = p[pk];
                            break;
                        }
                    }
                    
                    characters.push({name: rawName, displayName: displayName, level: level, passive: passive});
                }
            });

            characters.sort((a, b) => a.name.localeCompare(b.name));

            let charHTML = '<h2>Recruited Characters</h2>';
            charHTML += `
                <div style="margin:10px 0 15px 0;">
                    <button onclick="sortCharacters('alpha')" style="margin-right:8px;padding:6px 12px;">A-Z</button>
                    <button onclick="sortCharacters('level')" style="padding:6px 12px;">Sort by Level ↓</button>
                </div>
            `;
            charHTML += '<div id="charGrid" style="display:grid;grid-template-columns:repeat(auto-fill,minmax(220px,1fr));gap:12px;">';

            characters.forEach(char => {
                charHTML += `
                    <div style="background:#1e2a5e;padding:12px;border-radius:8px;">
                        <strong>${char.displayName}</strong><br>
                        <span style="color:#00ffcc;">Level: ${char.level}</span><br>
                        <span style="color:#aaa;">Passive: ${char.passive}</span>
                    </div>`;
            });
            charHTML += '</div>';

            document.getElementById('modalContent').innerHTML = `
                <h2>${p.username}</h2>
                <p><strong>Level:</strong> ${p.lv || 'N/A'} | <strong>Unit:</strong> ${p.unit || 'N/A'}</p>
                <p><strong>Collection:</strong> <strong>${p.collection || 0}/160</strong></p>
                <p><strong>Gil:</strong> ${parseInt(p.gil||0).toLocaleString()} | <strong>Wins:</strong> ${p.wins||0}</p>
                ${charHTML}
                <button onclick="document.getElementById('modal').style.display='none'" style="margin-top:20px;padding:10px 20px;">Close</button>
            `;
            document.getElementById('modal').style.display = 'block';
            window.currentCharacters = characters;
        }

        function sortCharacters(type) {
            if (!window.currentCharacters) return;
            let sorted = [...window.currentCharacters];
            if (type === 'level') {
                sorted.sort((a, b) => b.level - a.level);
            } else {
                sorted.sort((a, b) => a.name.localeCompare(b.name));
            }
            let html = '';
            sorted.forEach(char => {
                html += `
                    <div style="background:#1e2a5e;padding:12px;border-radius:8px;">
                        <strong>${char.displayName}</strong><br>
                        <span style="color:#00ffcc;">Level: ${char.level}</span><br>
                        <span style="color:#aaa;">Passive: ${char.passive}</span>
                    </div>`;
            });
            document.getElementById('charGrid').innerHTML = html;
        }

        filterPlayers();
    </script>
</body>
</html>'''

    return html

# ====================== CONFIG ======================
# CHANGE THIS PATH to your actual playerdatabase.ini location
ini_path = Path(r"C:\Users\User\Desktop\FFBOT\playerdatabase.ini")   # ←←← EDIT THIS LINE

output_path = Path("index.html")

if not ini_path.exists():
    print(f"❌ Could not find the .ini file at: {ini_path}")
    print("Please edit the 'ini_path' line in this script with the correct full path.")
else:
    players = parse_ffbot_ini(ini_path)
    html_content = generate_html(players)
    output_path.write_text(html_content, encoding='utf-8')
    print(f"SUCCESS! Generated roster with {len(players)} players")
    print(f"SUCCESS! index.html has been created in this folder")
    print("You can now upload index.html to GitHub Pages")
# ================================================
