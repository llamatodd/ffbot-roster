import configparser
import json
from pathlib import Path
import csv
import datetime
import re

# Load character metadata
character_data = {}
try:
    with open('character_list.csv', 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            name = row['Name'].strip()
            if name:
                norm1 = name.lower()
                norm2 = name.lower().replace(' ', '')
                norm3 = name.lower().replace(' ', '').replace('x2', 'x 2')
                character_data[norm1] = row
                character_data[norm2] = row
                character_data[norm3] = row
    print(f"Loaded {len(character_data)} character entries")
except Exception as e:
    print("Could not load character_list.csv:", e)

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
        
        if 'unit' in player:
            unit_name = player['unit'].strip().strip('"')
            norm1 = unit_name.lower()
            norm2 = unit_name.lower().replace(' ', '')
            norm3 = unit_name.lower().replace(' ', '').replace('x2', 'x 2')
            if norm1 in character_data:
                char = character_data[norm1]
            elif norm2 in character_data:
                char = character_data[norm2]
            elif norm3 in character_data:
                char = character_data[norm3]
            else:
                char = {}
            player['role'] = char.get('Role', '')
            player['spe'] = char.get('Speed', '')
            player['specialty'] = char.get('Specialty', '')
            player['description'] = char.get('Description', '')
            player['stats'] = char.get('Stats', '')
        
        players.append(player)
    return players

def generate_html(players):
    last_updated = datetime.datetime.now().strftime("%B %d, %Y at %I:%M %p")
    
    html = '''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>FFBOT Roster</title>
    <style>
        body { font-family: Arial, sans-serif; background: #1a1a2e; color: #eee; margin: 0; padding: 20px; }
        h1 { text-align: center; color: #00ffcc; }
        #lastUpdated { text-align:center; color:#888; margin: -10px 0 15px 0; font-size: 14px; }
        #search { width: 100%; max-width: 600px; margin: 20px auto; display: block; padding: 12px; font-size: 18px; border-radius: 8px; border: none; }
        .player-grid { display: grid; grid-template-columns: repeat(auto-fill, minmax(320px, 1fr)); gap: 16px; max-width: 1400px; margin: 0 auto; }
        .player-card { background: #16213e; border-radius: 12px; overflow: hidden; cursor: pointer; transition: all 0.2s; }
        .player-card:hover { transform: scale(1.03); }
        .portrait { height: 160px; background-size: contain; background-position: center; background-repeat: no-repeat; background-color: #0f1621; }
        .modal { display: none; position: fixed; top: 0; left: 0; width: 100%; height: 100%; background: rgba(0,0,0,0.9); z-index: 1000; }
        .modal-content { background: #16213e; max-width: 900px; margin: 50px auto; padding: 25px; border-radius: 12px; max-height: 90vh; overflow-y: auto; position: relative; }
        .char-card { display: flex; gap: 12px; background: #1e2a5e; padding: 12px; border-radius: 8px; margin-bottom: 12px; }
        .char-portrait { width: 60px; height: 60px; background-size: contain; background-position: center; background-repeat: no-repeat; background-color: #0f1621; border-radius: 6px; flex-shrink: 0; }
        .awakening.unlearned { color: #888; opacity: 0.7; }
        .role-dps { color: #ff6666; }
        .role-tank { color: #66aaff; }
        .role-healer { color: #66ff99; }
        .role-support { color: #cc99ff; }
    </style>
</head>
<body>
    <h1>FFBOT Player Roster</h1>
    <p id="lastUpdated">Last Updated: ''' + last_updated + '''</p>
    <input type="text" id="search" placeholder="Search by username..." onkeyup="filterPlayers()">
    
    <div class="player-grid" id="playerGrid"></div>

    <div id="modal" class="modal">
        <div class="modal-content" id="modalContent"></div>
    </div>

    <script>
        const players = ''' + json.dumps(players, ensure_ascii=False) + ''';
        const characterData = ''' + json.dumps(character_data, ensure_ascii=False) + ''';

        function filterPlayers() {
            const term = document.getElementById('search').value.toLowerCase();
            const grid = document.getElementById('playerGrid');
            grid.innerHTML = '';
            
            players.forEach(p => {
                if (p.username.toLowerCase().includes(term)) {
                    const card = document.createElement('div');
                    card.className = 'player-card';
                    card.innerHTML = `
                        <div class="portrait" style="background-image:url('portrait/${encodeURIComponent((p.unit || 'Unknown').replace(/["']/g, '').trim())}.png')"></div>
                        <div style="padding:16px;">
                            <h3 style="margin:0 0 8px 0;">${p.username}</h3>
                            <p><strong>Unit:</strong> ${p.unit || 'N/A'} | <strong>LV:</strong> ${p.lv || 'N/A'}</p>
                            <p><strong>Collection:</strong> ${p.collection || 0}/160</p>
                            
                            <div style="display:grid;grid-template-columns:1fr 1fr;gap:6px;font-size:14px;margin:10px 0;">
                                <div><strong style="${(p.preferedstat || '').toString().toLowerCase().includes('atk') ? 'color:#ffcc00;font-weight:bold' : ''}">ATK: ${p.atk || 0}</strong></div>
                                <div><strong style="${(p.preferedstat || '').toString().toLowerCase().includes('mag') ? 'color:#ffcc00;font-weight:bold' : ''}">MAG: ${p.mag || 0}</strong></div>
                                <div><strong style="${(p.preferedstat || '').toString().toLowerCase().includes('spi') ? 'color:#ffcc00;font-weight:bold' : ''}">SPI: ${p.spi || 0}</strong></div>
                                <div><strong style="${(p.preferedstat || '').toString().toLowerCase().includes('hp') ? 'color:#ffcc00;font-weight:bold' : ''}">HP: ${p.hp || 0}</strong></div>
                            </div>
                            
                            <div style="font-size:13px;color:#aaa;">
                                Asc: ${p.ascension || 0}<br>
                                Awakening: ${p.awakeningexp || 0}%
                            </div>
                            
                            <p style="margin-top:8px;">Wins: ${parseInt(p.wins || 0).toLocaleString()}</p>
                        </div>
                    `;
                    card.onclick = () => showDetails(p);
                    grid.appendChild(card);
                }
            });
        }

        function showDetails(p) {
            let characters = [];
            
            Object.keys(p).forEach(rawKey => {
                let key = rawKey.toString().toLowerCase();
                if (key.includes('awakeninglv')) {
                    let rawName = rawKey.replace(/awakeninglv/i, '').trim();
                    rawName = rawName.replace(/^["']|["']$/g, '').trim();
                    let normName = rawName.toLowerCase();
                    let normNoSpace = normName.replace(/ /g, '');
                    
                    let displayName = rawName.split(' ').map(word => word.charAt(0).toUpperCase() + word.slice(1).toLowerCase()).join(' ');
                    
                    const level = parseInt(p[rawKey]) || 0;
                    
                    let passive = 'None';
                    const possiblePassiveKeys = [
                        `ps5${rawName}`, `ps${rawName}`,
                        `ps5${normNoSpace}`, `ps${normNoSpace}`
                    ];
                    
                    for (let pk of possiblePassiveKeys) {
                        if (p[pk]) {
                            passive = p[pk].toString().replace(/["']/g, '');
                            break;
                        }
                    }
                    
                    const charInfo = characterData[normName] || characterData[normNoSpace] || {};
                    
                    characters.push({
                        name: rawName,
                        displayName: displayName,
                        level: level,
                        passive: passive,
                        awakening1: charInfo.Awakening1 || charInfo.awakening1 || '',
                        awakening2: charInfo.Awakening2 || charInfo.awakening2 || '',
                        awakening3: charInfo.Awakening3 || charInfo.awakening3 || '',
                        spe: charInfo.Speed || charInfo.speed || '',
                        specialty: charInfo.Specialty || charInfo.specialty || '',
                        description: charInfo.Description || charInfo.description || '',
                        role: charInfo.Role || '',
                        stats: charInfo.Stats || ''
                    });
                }
            });

            characters.sort((a, b) => a.name.localeCompare(b.name));

            let charHTML = '<h2>Recruited Characters</h2>';
            charHTML += `<div style="margin:10px 0 15px 0;">
                <button onclick="toggleSort('alpha')" id="alphaBtn">A-Z</button> 
                <button onclick="toggleSort('level')" id="levelBtn">Hi-Low</button>
                <button onclick="toggleSort('role')" id="roleBtn">Sort by Role</button>
            </div>`;
            charHTML += '<div id="charGrid" style="display:grid;grid-template-columns:repeat(auto-fill,minmax(320px,1fr));gap:12px;">';

            characters.forEach(char => {
                charHTML += `
                    <div class="char-card">
                        <div class="char-portrait" style="background-image:url('portrait/${encodeURIComponent(char.displayName)}.png')"></div>
                        <div>
                            <strong>${char.displayName}</strong> <span class="${char.role.toLowerCase().includes('dps') ? 'role-dps' : char.role.toLowerCase().includes('tank') ? 'role-tank' : char.role.toLowerCase().includes('healer') ? 'role-healer' : char.role.toLowerCase().includes('support') ? 'role-support' : ''}">[${char.role}]</span> | Stats: ${char.stats || 'N/A'}<br>
                            <span style="color:#00ffcc;">Level: ${char.level}</span><br>
                            <span style="color:#aaa;">Passive: ${char.passive}</span><br>
                            <div style="margin-top:8px;font-size:13px;">
                                Awakenings:<br>
                                <span class="${char.level >= 100 ? '' : 'awakening unlearned'}">1. ${char.awakening1 || '???'} </span><br>
                                <span class="${char.level >= 200 ? '' : 'awakening unlearned'}">2. ${char.awakening2 || '???'} </span><br>
                                <span class="${char.level >= 500 ? '' : 'awakening unlearned'}">3. ${char.awakening3 || '???'} </span><br>
                            </div><br>
                            ${char.spe ? `<div style="font-size:13px;">Speed: ${char.spe}</div>` : ''}
                            ${char.specialty ? `<div style="font-size:13px;">Specialty: ${char.specialty}</div>` : ''}
                            ${char.description ? `<div style="font-size:12px;margin-top:8px;color:#ccc;">${char.description}</div>` : ''}
                        </div>
                    </div>`;
            });
            charHTML += '</div>';

            document.getElementById('modalContent').innerHTML = `
                <span onclick="closeModal()" style="position:absolute;top:15px;right:25px;font-size:36px;cursor:pointer;color:#ff6666;">×</span>
                <h2>${p.username}</h2>
                <p><strong>Level:</strong> ${p.lv || 'N/A'} | <strong>Unit:</strong> ${p.unit || 'N/A'}</p>
                <p><strong>Collection:</strong> ${p.collection || 0}/160</p>
                <p><strong>Gil:</strong> ${parseInt(p.gil||0).toLocaleString()} | <strong>Wins:</strong> ${p.wins||0}</p>
                ${charHTML}
            `;
            
            document.getElementById('modal').style.display = 'block';
            window.currentCharacters = characters;
        }

        function toggleSort(type) {
            if (!window.currentCharacters) return;
            let sorted = [...window.currentCharacters];
            if (type === 'level') {
                window.currentSortLevel = window.currentSortLevel === 'desc' ? 'asc' : 'desc';
                if (window.currentSortLevel === 'desc') {
                    sorted.sort((a, b) => b.level - a.level);
                    document.getElementById('levelBtn').textContent = 'Hi-Low';
                } else {
                    sorted.sort((a, b) => a.level - b.level);
                    document.getElementById('levelBtn').textContent = 'Low-Hi';
                }
            } else if (type === 'role') {
                const roleOrder = ['dps', 'tank', 'healer', 'support'];
                sorted.sort((a, b) => {
                    const ra = (a.role || 'dps').toLowerCase();
                    const rb = (b.role || 'dps').toLowerCase();
                    return roleOrder.indexOf(ra) - roleOrder.indexOf(rb) || a.name.localeCompare(b.name);
                });
                document.getElementById('roleBtn').textContent = 'Role';
            } else {
                window.currentSortAlpha = window.currentSortAlpha === 'asc' ? 'desc' : 'asc';
                if (window.currentSortAlpha === 'asc') {
                    sorted.sort((a, b) => a.name.localeCompare(b.name));
                    document.getElementById('alphaBtn').textContent = 'A-Z';
                } else {
                    sorted.sort((a, b) => b.name.localeCompare(a.name));
                    document.getElementById('alphaBtn').textContent = 'Z-A';
                }
            }
            let html = '';
            sorted.forEach(char => {
                html += `
                    <div class="char-card">
                        <div class="char-portrait" style="background-image:url('portrait/${encodeURIComponent(char.displayName)}.png')"></div>
                        <div>
                            <strong>${char.displayName}</strong> <span class="${char.role.toLowerCase().includes('dps') ? 'role-dps' : char.role.toLowerCase().includes('tank') ? 'role-tank' : char.role.toLowerCase().includes('healer') ? 'role-healer' : char.role.toLowerCase().includes('support') ? 'role-support' : ''}">[${char.role}]</span> | Stats: ${char.stats || 'N/A'}<br>
                            <span style="color:#00ffcc;">Level: ${char.level}</span><br>
                            <span style="color:#aaa;">Passive: ${char.passive}</span><br>
                            <div style="margin-top:8px;font-size:13px;">
                                Awakenings:<br>
                                <span class="${char.level >= 100 ? '' : 'awakening unlearned'}">1. ${char.awakening1 || '???'} </span><br>
                                <span class="${char.level >= 200 ? '' : 'awakening unlearned'}">2. ${char.awakening2 || '???'} </span><br>
                                <span class="${char.level >= 500 ? '' : 'awakening unlearned'}">3. ${char.awakening3 || '???'} </span><br>
                            </div><br>
                            ${char.spe ? `<div style="font-size:13px;">Speed: ${char.spe}</div>` : ''}
                            ${char.specialty ? `<div style="font-size:13px;">Specialty: ${char.specialty}</div>` : ''}
                            ${char.description ? `<div style="font-size:12px;margin-top:8px;color:#ccc;">${char.description}</div>` : ''}
                        </div>
                    </div>`;
            });
            document.getElementById('charGrid').innerHTML = html;
        }

        function closeModal() {
            document.getElementById('modal').style.display = 'none';
        }

        filterPlayers();
    </script>
</body>
</html>'''

    return html

# ====================== CONFIG ======================
ini_path = Path(r"C:\Users\User\Desktop\FFBOT\playerdatabase.ini")   # ←←← EDIT THIS LINE

output_path = Path("index.html")

if not ini_path.exists():
    print(f"❌ Could not find the .ini file at: {ini_path}")
else:
    players = parse_ffbot_ini(ini_path)
    html_content = generate_html(players)
    output_path.write_text(html_content, encoding='utf-8')
    print(f"SUCCESS! Generated roster with {len(players)} players")
    print(f"SUCCESS! index.html has been created in this folder")
    print("You can now upload index.html to GitHub Pages")
# ================================================