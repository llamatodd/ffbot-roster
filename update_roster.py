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
                        <p>Wins: ${parseInt(p.wins || 0).toLocaleString()}</p>
                    `;
                    card.onclick = () => showDetails(p);
                    grid.appendChild(card);
                }
            });
        }

        function showDetails(p) {
            let charHTML = '<h2>Recruited Characters</h2><div style="display:grid;grid-template-columns:repeat(auto-fill,minmax(220px,1fr));gap:12px;">';
            
            Object.keys(p).forEach(key => {
                if (key.startsWith('awakeninglv')) {
                    const charName = key.replace('awakeninglv', '').replace(/["']/g, '').trim();
                    const level = p[key];
                    const passiveKey = key.replace('awakeninglv', 'ps');
                    let passive = p[passiveKey] || p['ps5' + charName] || 'None';
                    
                    charHTML += `
                        <div style="background:#1e2a5e;padding:12px;border-radius:8px;">
                            <strong>${charName}</strong><br>
                            Level: ${level}<br>
                            Passive: ${passive}
                        </div>`;
                }
            });
            charHTML += '</div>';

            document.getElementById('modalContent').innerHTML = `
                <h2>${p.username}</h2>
                <p><strong>Level:</strong> ${p.lv} | <strong>Unit:</strong> ${p.unit}</p>
                <p><strong>Wins:</strong> ${parseInt(p.wins||0).toLocaleString()} | <strong>Wins:</strong> ${p.wins||0}</p>
                ${charHTML}
                <button onclick="document.getElementById('modal').style.display='none'" style="margin-top:20px;padding:10px 20px;">Close</button>
            `;
            document.getElementById('modal').style.display = 'block';
        }

        // Initial load
        window.onload = filterPlayers;
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
    print(f"✅ Success! Generated roster with {len(players)} players")
    print(f"✅ index.html has been created in this folder")
    print("You can now upload index.html to GitHub Pages")
# ================================================
