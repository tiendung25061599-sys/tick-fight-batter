import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(page_title="Stickman Battle PC & Mobile", layout="wide")

game_code = """
<!DOCTYPE html>
<html>
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no">
  <script src="https://unpkg.com/peerjs@1.5.2/dist/peerjs.min.js"></script>
  <style>
    * { box-sizing: border-box; margin: 0; padding: 0; user-select: none; -webkit-user-select: none; }
    body { width: 100vw; height: 100vh; background: #0f0f13; color: white; font-family: sans-serif; display: flex; flex-direction: column; align-items: center; justify-content: center; overflow: hidden; }
    
    .screen { position: absolute; top:0; left:0; width: 100%; height: 100%; background: #0f0f13; display: flex; flex-direction: column; align-items: center; justify-content: center; z-index: 10; gap: 12px; }
    h1 { font-size: 24px; color: #00d2d3; text-align: center; }
    
    .btn { padding: 12px 24px; font-size: 15px; font-weight: bold; background: #222233; border: 2px solid #00d2d3; border-radius: 8px; color: white; cursor: pointer; text-align: center; z-index: 20; min-width: 220px; }
    .btn:active { background: #00d2d3; color: #000; transform: scale(0.95); }
    
    input, select { padding: 8px 12px; font-size: 15px; border-radius: 8px; border: 1px solid #00d2d3; background: #1a1a24; color: white; text-align: center; width: 220px; }
    .select-box { display: flex; gap: 10px; align-items: center; background: #1a1a24; padding: 8px 12px; border-radius: 8px; width: 85%; max-width: 350px; justify-content: space-between; }
    #statusText { color: #ffa502; font-weight: bold; font-size: 14px; text-align: center; }
    
    #gameCanvas { background: #111118; border: 2px solid #333; border-radius: 10px; width: 95vw; height: 52vh; }
    #backBtn { position: absolute; top: 10px; left: 50%; transform: translateX(-50%); padding: 6px 14px; background: #333; border: 1px solid #fff; color: #fff; border-radius: 6px; z-index: 50; cursor: pointer; }
    
    /* GIAO DIỆN KẾT THÚC TRẬN ĐẤU (OVERLAY) */
    #endGameOverlay {
      position: absolute; top: 0; left: 0; width: 100vw; height: 100vh;
      background: rgba(0, 0, 0, 0.85); display: none; flex-direction: column;
      align-items: center; justify-content: center; z-index: 100; gap: 15px;
    }
    #winnerText { font-size: 32px; font-weight: bold; color: #ffa502; text-shadow: 0 0 10px #ffa502; }
    #voteStatusText { color: #00d2d3; font-size: 14px; font-weight: bold; min-height: 20px; }

    /* CONTROLS */
    .controls { position: absolute; bottom: 10px; width: 100vw; display: flex; justify-content: space-between; padding: 0 15px; z-index: 30; }
    .btn-group { display: flex; gap: 8px; }
    .btn-ctrl { 
      position: relative; width: 60px; height: 60px; border-radius: 12px; 
      font-weight: bold; display: flex; align-items: center; justify-content: center; 
      background: #222233; border: 2px solid #00d2d3; color: #fff; cursor: pointer; 
      font-size: 20px;
    }
    .btn-ctrl:active, .btn-ctrl.active { background: #00d2d3; color: #000; }
    .key-hint { 
      position: absolute; top: 2px; right: 3px; font-size: 9px; color: #ffa502; 
      font-weight: bold; background: rgba(0,0,0,0.6); padding: 1px 3px; border-radius: 3px; 
    }
  </style>
</head>
<body>

  <!-- MAIN MENU -->
  <div id="mainMenu" class="screen">
    <h1>STICKMAN BATTLE ONLINE</h1>
    <div class="btn" onclick="startSingle()">🤖 CHƠI VỚI BOT</div>
    <div class="btn" style="border-color:#ff6b81" onclick="showLobbyMenu()">🌐 MULTIPLAYER (ONLINE)</div>
  </div>

  <!-- LOBBY SELECTION MENU -->
  <div id="lobbyMenu" class="screen" style="display:none;">
    <h1>CHẾ ĐỘ MULTIPLAYER</h1>
    <div class="btn" style="border-color:#2ed573" onclick="showCreateRoomScreen()">🎲 TẠO LOBBY MỚI</div>
    <div class="btn" style="border-color:#eccc68" onclick="showJoinRoomScreen()">🔑 THAM GIA LOBBY</div>
    <div class="btn" style="border-color:#ff6b81" onclick="showScreen('mainMenu')">⬅ TRỜ VỀ</div>
  </div>

  <!-- TẠO PHÒNG (CREATE ROOM) -->
  <div id="createRoomScreen" class="screen" style="display:none;">
    <h1>TẠO PHÒNG MỚI</h1>
    <input type="text" id="customRoomCode" placeholder="Nhập Mã Phòng (VD: ROOM123)">
    <div class="select-box">
      <span>Số người chơi tối đa:</span>
      <select id="maxPlayersSelect">
        <option value="2">2 Người (1v1)</option>
        <option value="3">3 Người</option>
        <option value="4">4 Người</option>
      </select>
    </div>
    <div id="createStatusText" style="color:#ffa502; font-size:13px;"></div>
    <div class="btn" style="border-color:#2ed573" onclick="initHostRoom()">🚀 KHOẢI TẠO LOBBY</div>
    <div class="btn" style="border-color:#ff6b81" onclick="showScreen('lobbyMenu')">⬅ TRỞ VỀ</div>
  </div>

  <!-- THAM GIA PHÒNG (JOIN ROOM) -->
  <div id="joinRoomScreen" class="screen" style="display:none;">
    <h1>THAM GIA PHÒNG</h1>
    <input type="text" id="joinRoomCodeInput" placeholder="Nhập Mã Phòng Người Khác...">
    <div id="joinStatusText" style="color:#ffa502; font-size:13px;"></div>
    <div class="btn" style="border-color:#2ed573" onclick="joinTargetRoom()">🔑 VÀO PHÒNG</div>
    <div class="btn" style="border-color:#ff6b81" onclick="showScreen('lobbyMenu')">⬅ TRỜ VỀ</div>
  </div>

  <!-- CẤU HÌNH TRANG BỊ -->
  <div id="customScreen" class="screen" style="display:none;">
    <h1>TRANG BỊ CHIẾN BẤT</h1>
    <div id="statusText">Đang chuẩn bị...</div>
    <div class="select-box">
      <span>Màu Skin:</span>
      <input type="color" id="skinColor" value="#00d2d3">
    </div>
    <div class="select-box">
      <span>Vũ Khí:</span>
      <select id="weaponSelect">
        <option value="sword">⚔️ Kiếm Thần (Cận chiến)</option>
        <option value="staff">🪄 Trượng Ma Thuật (Cầu Lửa)</option>
        <option value="bow">🏹 Cung Thần (Bắn Tốc Độ)</option>
      </select>
    </div>
    <div class="select-box">
      <span>Mũ / Nón:</span>
      <select id="hatSelect">
        <option value="none">Không Đội Mũ</option>
        <option value="knight">🪖 Mũ Chiến Binh</option>
        <option value="wizard">🧙 Mũ Phù Thủy</option>
      </select>
    </div>
    <div class="select-box">
      <span>Áo Choàng:</span>
      <select id="capeSelect">
        <option value="none">Không Áo Choàng</option>
        <option value="red">🔴 Áo Choàng Đỏ</option>
        <option value="black">⚫ Áo Choàng Đen</option>
      </select>
    </div>
    <div class="btn" onclick="confirmCustom()">VÀO TRẬN ĐẤU ➔</div>
  </div>

  <!-- GAME CANVAS -->
  <button id="backBtn" onclick="quitGame()" style="display:none;">≡ MENU</button>
  <canvas id="gameCanvas" style="display:none;"></canvas>

  <!-- MÀN HÌNH KẾT THÚC VÀ BÌNH CHỌN -->
  <div id="endGameOverlay">
    <div id="winnerText">BẠN THẮNG!</div>
    <div id="voteStatusText"></div>
    <div class="btn" id="rematchBtn" style="border-color:#2ed573" onclick="requestRematch()">🔄 CHƠI TIẾP</div>
    <div class="btn" style="border-color:#ff6b81" onclick="quitGame()">🏠 MÀN HÌNH CHÍNH</div>
  </div>
  
  <!-- BẢNG ĐIỀU KHIỂN -->
  <div class="controls" id="gameControls" style="display:none;">
    <div class="btn-group">
      <div class="btn-ctrl" id="btnLeft">◀<span class="key-hint">A</span></div>
      <div class="btn-ctrl" id="btnRight">▶<span class="key-hint">D</span></div>
      <div class="btn-ctrl" id="btnJump">🦘<span class="key-hint">W</span></div>
    </div>
    <div class="btn-group">
      <div class="btn-ctrl" id="btnAtk">⚔️<span class="key-hint">M1</span></div>
      <div class="btn-ctrl" style="border-color:#ff4757" id="btnSkill">🔥<span class="key-hint">M2</span></div>
    </div>
  </div>

<script>
  const canvas = document.getElementById("gameCanvas");
  const ctx = canvas.getContext("2d");
  
  let peer = null, conn = null;
  let isHost = false, gameMode = 'single';
  let roomCode = "", maxPlayers = 2;

  let myData = { color: "#00d2d3", weapon: "sword", hat: "knight", cape: "red" };
  let enemyData = { color: "#ff6b81", weapon: "staff", hat: "wizard", cape: "black" };

  let myVoteRematch = false, enemyVoteRematch = false;

  function showScreen(id) {
    document.querySelectorAll('.screen').forEach(s => s.style.display = 'none');
    document.getElementById(id).style.display = 'flex';
  }

  function startSingle() { gameMode = 'single'; showScreen('customScreen'); }
  function showLobbyMenu() { gameMode = 'online'; showScreen('lobbyMenu'); }
  function showCreateRoomScreen() { showScreen('createRoomScreen'); }
  function showJoinRoomScreen() { showScreen('joinRoomScreen'); }

  // KHỞI TẠO HOST
  function initHostRoom() {
    let codeInput = document.getElementById("customRoomCode").value.trim();
    if(!codeInput) { alert("Vui lòng nhập Mã Phòng!"); return; }
    roomCode = codeInput;
    maxPlayers = parseInt(document.getElementById("maxPlayersSelect").value);
    
    document.getElementById("createStatusText").innerText = "Đang tạo Lobby...";
    
    if(peer) peer.destroy();
    peer = new Peer(roomCode);

    peer.on('open', (id) => {
      isHost = true;
      document.getElementById("createStatusText").innerText = "Lobby thành công! Đang chờ người vào...";
      document.getElementById("statusText").innerText = "Lobby: " + roomCode + " (Tối đa " + maxPlayers + " người)";
      showScreen('customScreen');
    });

    peer.on('connection', (c) => {
      conn = c;
      setupConnection();
    });

    peer.on('error', (err) => {
      alert("Mã phòng này đã tồn tại hoặc không hợp lệ. Vui lòng chọn mã khác!");
      document.getElementById("createStatusText").innerText = "";
    });
  }

  // KHỞI TẠO CLIENT
  function joinTargetRoom() {
    let codeInput = document.getElementById("joinRoomCodeInput").value.trim();
    if(!codeInput) { alert("Vui lòng nhập Mã Phòng!"); return; }
    roomCode = codeInput;

    document.getElementById("joinStatusText").innerText = "Đang kết nối tới " + roomCode + "...";

    if(peer) peer.destroy();
    peer = new Peer();

    peer.on('open', () => {
      conn = peer.connect(roomCode);
      isHost = false;
      setupConnection();
    });

    peer.on('error', (err) => {
      alert("Không tìm thấy phòng hoặc mã phòng sai!");
      document.getElementById("joinStatusText").innerText = "";
    });
  }

  function setupConnection() {
    conn.on('open', () => {
      document.getElementById("statusText").innerText = "Đã kết nối vào phòng " + roomCode + "!";
      setTimeout(() => showScreen('customScreen'), 300);
    });
    conn.on('data', (data) => handleNetworkData(data));
  }

  function confirmCustom() {
    myData.color = document.getElementById("skinColor").value;
    myData.weapon = document.getElementById("weaponSelect").value;
    myData.hat = document.getElementById("hatSelect").value;
    myData.cape = document.getElementById("capeSelect").value;
    
    if(gameMode === 'online' && conn) {
      conn.send({ type: 'INIT_PLAYER', data: myData });
    } else {
      startGame();
    }
  }

  // GAME ENGINE
  let isRunning = false;
  let pSelf, pEnemy, bullets = [], particles = [];
  let moveL = false, moveR = false;

  function startGame() {
    document.querySelectorAll('.screen').forEach(s => s.style.display = 'none');
    document.getElementById("endGameOverlay").style.display = 'none';
    canvas.style.display = 'block';
    document.getElementById("backBtn").style.display = 'block';
    document.getElementById("gameControls").style.display = 'flex';

    canvas.width = canvas.clientWidth || 300;
    canvas.height = canvas.clientHeight || 150;

    let startX = isHost || gameMode === 'single' ? 80 : canvas.width - 80;
    let enemyX = isHost || gameMode === 'single' ? canvas.width - 80 : 80;

    pSelf = { x: startX, y: canvas.height - 25, vy: 0, isGrounded: true, hp: 100, atk: false, data: myData, facing: 1 };
    pEnemy = { x: enemyX, y: canvas.height - 25, vy: 0, isGrounded: true, hp: 100, atk: false, data: enemyData, facing: -1 };
    
    bullets = []; particles = [];
    myVoteRematch = false; enemyVoteRematch = false;
    document.getElementById("rematchBtn").style.opacity = "1";
    document.getElementById("rematchBtn").innerText = "🔄 CHƠI TIẾP";
    document.getElementById("voteStatusText").innerText = "";

    isRunning = true;
    requestAnimationFrame(loop);
  }

  function handleNetworkData(data) {
    if(data.type === 'INIT_PLAYER') {
      pEnemy.data = data.data; startGame();
    } else if(data.type === 'SYNC_POS') {
      pEnemy.x = data.x; pEnemy.y = data.y; pEnemy.hp = data.hp; pEnemy.atk = data.atk; pEnemy.facing = data.facing;
    } else if(data.type === 'SKILL') {
      createBullet(pEnemy, pSelf, data.weapon);
    } else if(data.type === 'VOTE_REMATCH') {
      enemyVoteRematch = true;
      checkBothVoted();
    }
  }

  function triggerEndGame(won) {
    isRunning = false;
    let overlay = document.getElementById("endGameOverlay");
    let winTxt = document.getElementById("winnerText");
    winTxt.innerText = won ? "🏆 BẠN THẮNG!" : "💀 BẠN THUA!";
    winTxt.style.color = won ? "#2ed573" : "#ff4757";
    overlay.style.display = 'flex';
  }

  function requestRematch() {
    if(gameMode === 'single') {
      startGame();
    } else {
      myVoteRematch = true;
      document.getElementById("rematchBtn").style.opacity = "0.5";
      document.getElementById("rematchBtn").innerText = "⏳ ĐÃ BÌNH CHỌN (ĐỢI ĐỐI THỦ)";
      if(conn) conn.send({ type: 'VOTE_REMATCH' });
      checkBothVoted();
    }
  }

  function checkBothVoted() {
    if(gameMode === 'online') {
      if(myVoteRematch && enemyVoteRematch) {
        startGame();
      } else if(enemyVoteRematch && !myVoteRematch) {
        document.getElementById("voteStatusText").innerText = "Đối thủ đã bình chọn chơi tiếp! Bấm 'Chơi tiếp' để vào trận.";
      }
    }
  }

  function quitGame() {
    isRunning = false;
    if(conn) { conn.close(); conn = null; }
    if(peer) { peer.destroy(); peer = null; }
    canvas.style.display = 'none';
    document.getElementById("backBtn").style.display = 'none';
    document.getElementById("gameControls").style.display = 'none';
    document.getElementById("endGameOverlay").style.display = 'none';
    showScreen('mainMenu');
  }

  function jump() { if (pSelf && pSelf.isGrounded && isRunning) { pSelf.vy = -10; pSelf.isGrounded = false; } }

  function attack() {
    if(!pSelf || !isRunning) return;
    pSelf.atk = true; 
    let reach = pSelf.data.weapon === 'sword' ? 50 : 35;
    if(Math.abs(pSelf.x - pEnemy.x) < reach) {
      pEnemy.hp = Math.max(0, pEnemy.hp - 10);
      addParticles(pEnemy.x, pEnemy.y - 20, '#ff4757', 6);
    }
    setTimeout(() => pSelf.atk = false, 120);
  }

  function createBullet(caster, target, weapon) {
    let dir = caster.facing;
    if (weapon === 'staff') {
      bullets.push({ x: caster.x + dir * 15, y: caster.y - 20, vx: dir * 7, color: '#fffa65', radius: 8, dmg: 18 });
    } else if (weapon === 'bow') {
      bullets.push({ x: caster.x + dir * 15, y: caster.y - 20, vx: dir * 11, color: '#c7ecee', radius: 3, dmg: 12 });
    }
  }

  function useSkill() {
    if(!pSelf || !isRunning) return;
    pSelf.atk = true; setTimeout(() => pSelf.atk = false, 150);
    if(pSelf.data.weapon === 'sword') {
      if(Math.abs(pSelf.x - pEnemy.x) < 70) {
        pEnemy.hp = Math.max(0, pEnemy.hp - 20);
        addParticles(pEnemy.x, pEnemy.y - 20, '#00d2d3', 12);
      }
    } else {
      createBullet(pSelf, pEnemy, pSelf.data.weapon);
    }
    if(gameMode === 'online' && conn) conn.send({ type: 'SKILL', weapon: pSelf.data.weapon });
  }

  function addParticles(x, y, color, count) {
    for(let i=0; i<count; i++) {
      particles.push({ x: x, y: y, vx: (Math.random()-0.5)*6, vy: (Math.random()-0.5)*6, life: 15, color: color });
    }
  }

  function loop() {
    if (!isRunning) return;
    let ground = canvas.height - 25;

    pSelf.y += pSelf.vy; pSelf.vy += 0.5;
    if (pSelf.y >= ground) { pSelf.y = ground; pSelf.vy = 0; pSelf.isGrounded = true; }

    if (moveL) { pSelf.x -= 4; pSelf.facing = -1; }
    if (moveR) { pSelf.x += 4; pSelf.facing = 1; }
    pSelf.x = Math.max(15, Math.min(canvas.width - 15, pSelf.x));

    if(gameMode === 'single') {
      pEnemy.y += pEnemy.vy; pEnemy.vy += 0.5;
      if (pEnemy.y >= ground) { pEnemy.y = ground; pEnemy.vy = 0; pEnemy.isGrounded = true; }
      pEnemy.facing = pSelf.x < pEnemy.x ? -1 : 1;
      if (Math.abs(pSelf.x - pEnemy.x) > 40) pEnemy.x += (pSelf.x < pEnemy.x) ? -1.5 : 1.5;
      if (Math.random() < 0.01) pEnemy.vy = -10;
      if (Math.random() < 0.015) { pEnemy.atk = true; setTimeout(() => pEnemy.atk = false, 120); createBullet(pEnemy, pSelf, pEnemy.data.weapon); }
    }

    if(gameMode === 'online' && conn && conn.open) {
      conn.send({ type: 'SYNC_POS', x: pSelf.x, y: pSelf.y, hp: pSelf.hp, atk: pSelf.atk, facing: pSelf.facing });
    }

    ctx.clearRect(0, 0, canvas.width, canvas.height);
    
    // Mặt đất
    ctx.fillStyle = "#222"; ctx.fillRect(0, ground + 20, canvas.width, 10);

    // Thanh Máu
    let w = canvas.width * 0.35;
    ctx.fillStyle = "#444"; ctx.fillRect(10, 10, w, 12); ctx.fillRect(canvas.width - 10 - w, 10, w, 12);
    ctx.fillStyle = pSelf.data.color; ctx.fillRect(10, 10, w * (pSelf.hp / 100), 12);
    ctx.fillStyle = pEnemy.data.color; ctx.fillRect(canvas.width - 10 - w, 10, w * (pEnemy.hp / 100), 12);

    // Particle
    particles.forEach((p, i) => {
      p.x += p.vx; p.y += p.vy; p.life--;
      ctx.fillStyle = p.color; ctx.fillRect(p.x, p.y, 3, 3);
      if(p.life <= 0) particles.splice(i, 1);
    });

    // Đạn
    bullets.forEach((b, idx) => {
      b.x += b.vx;
      ctx.fillStyle = b.color;
      ctx.beginPath(); ctx.arc(b.x, b.y, b.radius, 0, Math.PI * 2); ctx.fill();
      let target = (b.vx > 0 && isHost) || (b.vx < 0 && !isHost) ? pEnemy : pSelf;
      if (Math.abs(b.x - target.x) < 20 && Math.abs(b.y - (target.y - 20)) < 25) {
        target.hp = Math.max(0, target.hp - b.dmg);
        addParticles(b.x, b.y, b.color, 8);
        bullets.splice(idx, 1);
      }
    });

    drawPlayer(pSelf); drawPlayer(pEnemy);

    // KIỂM TRA THẮNG / THUA
    if (pSelf.hp <= 0 || pEnemy.hp <= 0) {
      triggerEndGame(pSelf.hp > 0);
      return;
    }

    requestAnimationFrame(loop);
  }

  // VẼ NHÂN VẬT (STICKMAN + VŨ KHÍ + TRANG PHỤC)
  function drawPlayer(p) {
    let f = p.facing, x = p.x, y = p.y;
    
    // Áo Choàng
    if(p.data.cape && p.data.cape !== 'none') {
      ctx.fillStyle = p.data.cape === 'red' ? '#ff3838' : '#2f3542';
      ctx.beginPath(); ctx.moveTo(x - f * 4, y - 25); ctx.lineTo(x - f * 18, y + 5); ctx.lineTo(x - f * 4, y + 2); ctx.fill();
    }

    // Stickman
    ctx.strokeStyle = p.data.color; ctx.lineWidth = 3;
    ctx.beginPath(); ctx.arc(x, y - 35, 9, 0, Math.PI * 2); ctx.stroke();
    ctx.beginPath(); ctx.moveTo(x, y - 26); ctx.lineTo(x, y - 8); ctx.stroke();
    ctx.beginPath(); ctx.moveTo(x, y - 8); ctx.lineTo(x - 8, y + 20); ctx.stroke();
    ctx.beginPath(); ctx.moveTo(x, y - 8); ctx.lineTo(x + 8, y + 20); ctx.stroke();

    let handX = x + (p.atk ? f * 18 : f * 8);
    let handY = y - (p.atk ? 22 : 16);
    ctx.beginPath(); ctx.moveTo(x, y - 22); ctx.lineTo(handX, handY); ctx.stroke();

    // Mũ
    if(p.data.hat === 'knight') {
      ctx.fillStyle = '#a4b0be'; ctx.fillRect(x - 10, y - 48, 20, 8);
    } else if(p.data.hat === 'wizard') {
      ctx.fillStyle = '#5f27cd'; ctx.beginPath(); ctx.moveTo(x - 12, y - 42); ctx.lineTo(x, y - 60); ctx.lineTo(x + 12, y - 42); ctx.fill();
    }

    // Vũ Khí
    ctx.save(); ctx.translate(handX, handY);
    if(p.data.weapon === 'sword') {
      ctx.strokeStyle = '#dcdde1'; ctx.lineWidth = 3; ctx.beginPath(); ctx.moveTo(0, 0); ctx.lineTo(f * 22, -15); ctx.stroke();
    } else if(p.data.weapon === 'staff') {
      ctx.strokeStyle = '#78e08f'; ctx.lineWidth = 3; ctx.beginPath(); ctx.moveTo(0, 5); ctx.lineTo(f * 15, -20); ctx.stroke();
      ctx.fillStyle = '#fffa65'; ctx.beginPath(); ctx.arc(f * 15, -20, 5, 0, Math.PI*2); ctx.fill();
    } else if(p.data.weapon === 'bow') {
      ctx.strokeStyle = '#e1b12c'; ctx.lineWidth = 2; ctx.beginPath(); ctx.arc(f * 5, -5, 12, -Math.PI/2, Math.PI/2); ctx.stroke();
    }
    ctx.restore();
  }

  // PHÍM BẤM PC
  window.addEventListener('keydown', (e) => {
    let k = e.key.toLowerCase();
    if (k === 'a' || k === 'arrowleft') { moveL = true; document.getElementById('btnLeft').classList.add('active'); }
    if (k === 'd' || k === 'arrowright') { moveR = true; document.getElementById('btnRight').classList.add('active'); }
    if (k === 'w' || k === ' ' || k === 'arrowup') { jump(); document.getElementById('btnJump').classList.add('active'); }
  });

  window.addEventListener('keyup', (e) => {
    let k = e.key.toLowerCase();
    if (k === 'a' || k === 'arrowleft') { moveL = false; document.getElementById('btnLeft').classList.remove('active'); }
    if (k === 'd' || k === 'arrowright') { moveR = false; document.getElementById('btnRight').classList.remove('active'); }
    if (k === 'w' || k === ' ' || k === 'arrowup') { document.getElementById('btnJump').classList.remove('active'); }
  });

  window.addEventListener('mousedown', (e) => {
    if(e.button === 0) { attack(); document.getElementById('btnAtk').classList.add('active'); }
    if(e.button === 2) { useSkill(); document.getElementById('btnSkill').classList.add('active'); }
  });
  window.addEventListener('mouseup', (e) => {
    if(e.button === 0) document.getElementById('btnAtk').classList.remove('active');
    if(e.button === 2) document.getElementById('btnSkill').classList.remove('active');
  });
  window.addEventListener('contextmenu', e => e.preventDefault());

  // TOUCH EVENTS
  function bindBtn(id, start, end) {
    let el = document.getElementById(id);
    el.addEventListener("mousedown", (e)=>{ e.stopPropagation(); start(); });
    el.addEventListener("mouseup", (e)=>{ e.stopPropagation(); if(end) end(); });
    el.addEventListener("touchstart", (e)=>{e.preventDefault(); start();});
    el.addEventListener("touchend", (e)=>{e.preventDefault(); if(end) end();});
  }

  bindBtn("btnLeft", () => moveL = true, () => moveL = false);
  bindBtn("btnRight", () => moveR = true, () => moveR = false);
  bindBtn("btnJump", () => jump());
  bindBtn("btnAtk", () => attack());
  bindBtn("btnSkill", () => useSkill());
</script>
</body>
</html>
"""

components.html(game_code, height=720)
