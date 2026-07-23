import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(page_title="Stickman Battle Online & Story", layout="wide")

game_code = """
<!DOCTYPE html>
<html>
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no">
  <script src="https://unpkg.com/peerjs@1.5.2/dist/peerjs.min.js"></script>
  <style>
    * { box-sizing: border-box; margin: 0; padding: 0; user-select: none; -webkit-user-select: none; }
    body { width: 100vw; height: 100vh; background: #0b0c10; color: white; font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; display: flex; flex-direction: column; align-items: center; justify-content: center; overflow: hidden; position: relative; }
    
    /* NÚT QUAY LẠI CỐ ĐỊNH Ở GÓC TRÊN BÊN PHẢI (TRONG TRẬN) */
    .top-bar {
      position: absolute; top: 15px; right: 20px; 
      display: flex; gap: 10px; z-index: 999;
    }

    .top-btn { 
      padding: 8px 16px; background: #1f2833; border: 2px solid #ff4757; 
      color: #ff4757; border-radius: 8px; cursor: pointer; 
      font-weight: bold; font-size: 13px; box-shadow: 0 0 10px rgba(255, 71, 87, 0.3);
      transition: all 0.2s; outline: none; display: none;
    }
    .top-btn:active { background: #ff4757; color: #fff; transform: scale(0.95); }

    .screen { position: absolute; top:0; left:0; width: 100%; height: 100%; background: radial-gradient(circle, #1f2833 0%, #0b0c10 100%); display: flex; flex-direction: column; align-items: center; justify-content: center; z-index: 100; gap: 14px; }
    h1 { font-size: 28px; color: #66fcf1; text-align: center; text-shadow: 0 0 15px #66fcf1; letter-spacing: 2px; }
    
    .btn { padding: 12px 28px; font-size: 16px; font-weight: bold; background: #1f2833; border: 2px solid #66fcf1; border-radius: 8px; color: #66fcf1; cursor: pointer; text-align: center; z-index: 110; min-width: 240px; box-shadow: 0 0 10px rgba(102, 252, 241, 0.2); transition: all 0.2s; }
    .btn:active { background: #66fcf1; color: #000; transform: scale(0.95); }
    
    input, select { padding: 10px 14px; font-size: 15px; border-radius: 8px; border: 1px solid #66fcf1; background: #0b0c10; color: white; text-align: center; width: 240px; outline: none; }
    .select-box { display: flex; gap: 10px; align-items: center; background: #1f2833; padding: 8px 14px; border-radius: 8px; width: 85%; max-width: 360px; justify-content: space-between; border: 1px solid #45a29e; }
    #statusText { color: #f7b731; font-weight: bold; font-size: 14px; text-align: center; }
    
    #gameCanvas { background: #050508; border: 2px solid #45a29e; border-radius: 12px; width: 96vw; height: 54vh; display: none; position: relative; z-index: 1; box-shadow: 0 0 20px rgba(69, 162, 158, 0.3); }
    
    #endGameOverlay {
      position: absolute; top: 0; left: 0; width: 100vw; height: 100vh;
      background: rgba(0, 0, 0, 0.88); display: none; flex-direction: column;
      align-items: center; justify-content: center; z-index: 200; gap: 15px;
    }
    #winnerText { font-size: 34px; font-weight: bold; color: #f7b731; text-shadow: 0 0 15px #f7b731; }
    #voteStatusText { color: #66fcf1; font-size: 14px; font-weight: bold; min-height: 20px; }

    .controls { position: absolute; bottom: 10px; width: 100vw; display: none; justify-content: space-between; padding: 0 20px; z-index: 50; }
    .btn-group { display: flex; gap: 10px; }
    .btn-ctrl { 
      position: relative; width: 62px; height: 62px; border-radius: 14px; 
      font-weight: bold; display: flex; align-items: center; justify-content: center; 
      background: #1f2833; border: 2px solid #66fcf1; color: #fff; cursor: pointer; 
      font-size: 22px; box-shadow: 0 0 10px rgba(102, 252, 241, 0.3);
    }
    .btn-ctrl:active, .btn-ctrl.active { background: #66fcf1; color: #000; }
    .key-hint { 
      position: absolute; top: 2px; right: 4px; font-size: 9px; color: #f7b731; 
      font-weight: bold; background: rgba(0,0,0,0.6); padding: 1px 3px; border-radius: 3px; 
    }
  </style>
</head>
<body>

  <!-- NÚT QUAY LẠI KHI TRONG TRẬN -->
  <div class="top-bar">
    <button class="top-btn" id="topRightBackBtn" onclick="quitGame()">🏠 MENU VỀ TRANG CHÍNH</button>
  </div>

  <!-- MAIN MENU -->
  <div id="mainMenu" class="screen">
    <h1>STICKMAN BATTLE</h1>
    <div class="btn" id="btnStory">📖 STORY MODE (VƯỢT ẢI)</div>
    <div class="btn" style="border-color:#ff4757; color:#ff4757;" id="btnMulti">🌐 MULTIPLAYER (ONLINE)</div>
    <div class="btn" style="border-color:#f7b731; color:#f7b731;" id="btnSettings">⚙️ SETTINGS (CÀI ĐẶT)</div>
  </div>

  <!-- SETTINGS SCREEN -->
  <div id="settingsScreen" class="screen" style="display:none;">
    <h1>CÀI ĐẶT TRÒ CHƠI</h1>
    <div class="select-box" style="justify-content: center;">
      <button class="btn" id="btnFullscreenToggle" onclick="toggleFullscreen()" style="min-width: 280px; border-color:#66fcf1; color:#66fcf1;">📺 BẬT FULLSCREEN</button>
    </div>
    <div class="btn" style="border-color:#ff4757; color:#ff4757; margin-top: 20px;" id="btnBackToMenu">⬅ QUAY LẠI MENU</div>
  </div>

  <!-- LOBBY MENU -->
  <div id="lobbyMenu" class="screen" style="display:none;">
    <h1>CHẾ ĐỘ MULTIPLAYER</h1>
    <div class="btn" style="border-color:#2ed573; color:#2ed573;" id="btnCreateLobby">🎲 TẠO LOBBY MỚI</div>
    <div class="btn" style="border-color:#ffa502; color:#ffa502;" id="btnJoinLobby">🔑 THAM GIA LOBBY</div>
    <div class="btn" style="border-color:#ff4757; color:#ff4757; margin-top: 15px;" id="btnBackFromLobby">⬅ QUAY LẠI</div>
  </div>

  <!-- TẠO PHÒNG -->
  <div id="createRoomScreen" class="screen" style="display:none;">
    <h1>TẠO PHÒNG MỚI</h1>
    <input type="text" id="customRoomCode" placeholder="Nhập Mã Phòng (VD: ROOM123)">
    <div id="createStatusText" style="color:#f7b731; font-size:13px;"></div>
    <div class="btn" style="border-color:#2ed573; color:#2ed573;" id="btnInitHost">🚀 KHỞI TẠO LOBBY</div>
    <div class="btn" style="border-color:#ff4757; color:#ff4757;" onclick="showScreen('lobbyMenu')">⬅ QUAY LẠI</div>
  </div>

  <!-- THAM GIA PHÒNG -->
  <div id="joinRoomScreen" class="screen" style="display:none;">
    <h1>THAM GIA PHÒNG</h1>
    <input type="text" id="joinRoomCodeInput" placeholder="Nhập Mã Phòng Người Khác...">
    <div id="joinStatusText" style="color:#f7b731; font-size:13px;"></div>
    <div class="btn" style="border-color:#2ed573; color:#2ed573;" id="btnJoinTarget">🔑 VÀO PHÒNG</div>
    <div class="btn" style="border-color:#ff4757; color:#ff4757;" onclick="showScreen('lobbyMenu')">⬅ QUAY LẠI</div>
  </div>

  <!-- CẤU HÌNH TRANG BỊ -->
  <div id="customScreen" class="screen" style="display:none;">
    <h1 id="customTitle">TRANG BỊ CHIẾN ĐẤU</h1>
    <div id="statusText">Sẵn sàng xuất chiến!</div>
    <div class="select-box">
      <span>Màu Skin:</span>
      <input type="color" id="skinColor" value="#66fcf1">
    </div>
    <div class="select-box">
      <span>Vũ Khí:</span>
      <select id="weaponSelect">
        <option value="sword">⚔️ Kiếm Thần (Cân Bằng)</option>
        <option value="axe">🪓 Rìu Chiến (Sát Thương Lớn)</option>
        <option value="dagger">🗡️ Dao Độc (Tốc Đánh Nhanh)</option>
        <option value="spear">🔱 Giáo Dài (Tầm Đánh Xa)</option>
        <option value="staff">🪄 Trượng Ma Thuật (Cầu Lửa)</option>
        <option value="bow">🏹 Cung Thần (Bắn Nhanh)</option>
        <option value="laser">⚡ Súng Laser (Tia Xuyên)</option>
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
    <div class="btn" id="btnStartGame" style="background:#2ed573; border-color:#fff; color:#000;">BẮT ĐẦU VÀO TRẬN ➔</div>
    <div class="btn" style="border-color:#ff4757; color:#ff4757;" onclick="showScreen('mainMenu')">⬅ QUAY LẠI</div>
  </div>

  <!-- GAME CANVAS -->
  <canvas id="gameCanvas"></canvas>

  <!-- OVERLAY KẾT THÚC -->
  <div id="endGameOverlay">
    <div id="winnerText">BẠN THẮNG!</div>
    <div id="voteStatusText"></div>
    <div class="btn" id="rematchBtn" style="border-color:#2ed573; color:#2ed573;">🔄 CHƠI TIẾP</div>
    <div class="btn" style="border-color:#ff4757; color:#ff4757;" onclick="quitGame()">🏠 MÀN HÌNH CHÍNH</div>
  </div>
  
  <!-- CONTROLS -->
  <div class="controls" id="gameControls">
    <div class="btn-group">
      <div class="btn-ctrl" id="btnLeft">◀<span class="key-hint">A</span></div>
      <div class="btn-ctrl" id="btnRight">▶<span class="key-hint">D</span></div>
      <div class="btn-ctrl" id="btnJump">🦘<span class="key-hint">W</span></div>
    </div>
    <div class="btn-group">
      <div class="btn-ctrl" id="btnAtk">⚔️<span class="key-hint">M1</span></div>
      <div class="btn-ctrl" style="border-color:#ff4757" id="btnSkill">💨<span class="key-hint">M2</span></div>
    </div>
  </div>

<script>
  const canvas = document.getElementById("gameCanvas");
  const ctx = canvas.getContext("2d");
  
  let peer = null, conn = null;
  let isHost = false, gameMode = 'story';
  let roomCode = "";
  let currentStage = 1;

  let myData = { color: "#66fcf1", weapon: "sword", hat: "knight", cape: "red" };
  let enemyData = { color: "#ff4757", weapon: "staff", hat: "wizard", cape: "black" };

  let myVoteRematch = false, enemyVoteRematch = false;

  function toggleFullscreen() {
    let elem = document.documentElement;
    let btnFS = document.getElementById('btnFullscreenToggle');
    if (!document.fullscreenElement && !document.mozFullScreenElement && !document.webkitFullscreenElement && !document.msFullscreenElement) {
      if (elem.requestFullscreen) { elem.requestFullscreen(); }
      else if (elem.msRequestFullscreen) { elem.msRequestFullscreen(); }
      else if (elem.mozRequestFullScreen) { elem.mozRequestFullScreen(); }
      else if (elem.webkitRequestFullscreen) { elem.webkitRequestFullscreen(Element.ALLOW_KEYBOARD_INPUT); }
      if(btnFS) btnFS.innerText = "📉 THOÁT FULLSCREEN";
    } else {
      if (document.exitFullscreen) { document.exitFullscreen(); }
      else if (document.msExitFullscreen) { document.msExitFullscreen(); }
      else if (document.mozCancelFullScreen) { document.mozCancelFullScreen(); }
      else if (document.webkitExitFullscreen) { document.webkitExitFullscreen(); }
      if(btnFS) btnFS.innerText = "📺 BẬT FULLSCREEN";
    }
  }

  function showScreen(id) {
    document.querySelectorAll('.screen').forEach(s => s.style.display = 'none');
    document.getElementById(id).style.display = 'flex';
    
    const topBtn = document.getElementById('topRightBackBtn');
    if (id === 'mainMenu' || id === 'settingsScreen' || id === 'lobbyMenu' || id === 'createRoomScreen' || id === 'joinRoomScreen' || id === 'customScreen') {
      topBtn.style.display = 'none';
    } else {
      topBtn.style.display = 'block';
    }
  }

  function addClickEvent(id, fn) {
    let el = document.getElementById(id);
    if(!el) return;
    el.addEventListener('click', (e) => { e.preventDefault(); fn(); });
    el.addEventListener('touchend', (e) => { e.preventDefault(); fn(); });
  }

  addClickEvent('btnStory', () => { 
    gameMode = 'story'; 
    currentStage = 1;
    document.getElementById('customTitle').innerText = "STORY MODE - MÀN " + currentStage;
    showScreen('customScreen'); 
  });
  addClickEvent('btnMulti', () => { gameMode = 'online'; showScreen('lobbyMenu'); });
  addClickEvent('btnSettings', () => showScreen('settingsScreen'));
  addClickEvent('btnBackToMenu', () => showScreen('mainMenu'));
  addClickEvent('btnBackFromLobby', () => showScreen('mainMenu'));
  addClickEvent('btnCreateLobby', () => showScreen('createRoomScreen'));
  addClickEvent('btnJoinLobby', () => showScreen('joinRoomScreen'));
  addClickEvent('btnInitHost', initHostRoom);
  addClickEvent('btnJoinTarget', joinTargetRoom);
  addClickEvent('btnStartGame', confirmCustom);
  addClickEvent('rematchBtn', requestRematch);

  function initHostRoom() {
    let codeInput = document.getElementById("customRoomCode").value.trim();
    if(!codeInput) { alert("Vui lòng nhập Mã Phòng!"); return; }
    roomCode = codeInput;
    
    document.getElementById("createStatusText").innerText = "Đang khởi tạo...";
    if(peer) { try { peer.destroy(); } catch(e){} }
    
    peer = new Peer(roomCode);

    peer.on('open', (id) => {
      isHost = true;
      document.getElementById("statusText").innerText = "Mã phòng: " + roomCode + " (Chờ đối thủ...)";
      showScreen('customScreen');
    });

    peer.on('connection', (c) => {
      conn = c;
      setupConnection();
    });

    peer.on('error', (err) => {
      alert("Mã phòng trùng hoặc bị lỗi, thử mã khác nhé!");
      document.getElementById("createStatusText").innerText = "";
    });
  }

  function joinTargetRoom() {
    let codeInput = document.getElementById("joinRoomCodeInput").value.trim();
    if(!codeInput) { alert("Vui lòng nhập Mã Phòng!"); return; }
    roomCode = codeInput;

    document.getElementById("joinStatusText").innerText = "Đang kết nối...";
    if(peer) { try { peer.destroy(); } catch(e){} }
    
    peer = new Peer();

    peer.on('open', () => {
      conn = peer.connect(roomCode);
      isHost = false;
      setupConnection();
    });

    peer.on('error', (err) => {
      alert("Không tìm thấy phòng!");
      document.getElementById("joinStatusText").innerText = "";
    });
  }

  function setupConnection() {
    conn.on('open', () => {
      document.getElementById("statusText").innerText = "Đã kết nối thành công!";
      showScreen('customScreen');
      conn.send({ type: 'INIT_PLAYER', data: myData });
    });
    
    conn.on('data', (data) => handleNetworkData(data));
    
    conn.on('close', () => {
      if (isRunning) {
        alert("Đối thủ đã thoát trận đấu!");
        quitGame();
      }
    });
  }

  function confirmCustom() {
    myData.color = document.getElementById("skinColor").value;
    myData.weapon = document.getElementById("weaponSelect").value;
    myData.hat = document.getElementById("hatSelect").value;
    myData.cape = document.getElementById("capeSelect").value;
    
    if(gameMode === 'online' && conn && conn.open) {
      conn.send({ type: 'INIT_PLAYER', data: myData });
    }
    startGame();
  }

  let isRunning = false;
  let pSelf, pEnemy, bullets = [], particles = [];
  let moveL = false, moveR = false;
  let animFrame = 0;
  let isBossStage = false;

  function startGame() {
    document.querySelectorAll('.screen').forEach(s => s.style.display = 'none');
    document.getElementById("endGameOverlay").style.display = 'none';
    
    canvas.style.display = 'block';
    document.getElementById("topRightBackBtn").style.display = 'block';
    document.getElementById("gameControls").style.display = 'flex';

    canvas.width = window.innerWidth * 0.95;
    canvas.height = window.innerHeight * 0.52;

    let startX = isHost || gameMode === 'story' ? 80 : canvas.width - 80;
    let enemyX = isHost || gameMode === 'story' ? canvas.width - 80 : 80;

    isBossStage = (gameMode === 'story' && currentStage % 10 === 0);

    let enemyHp = 200;
    let enemyScale = 1.0;
    let enemyColor = "#ff4757";
    let enemyWeapon = "staff";

    if(gameMode === 'story') {
      if(isBossStage) {
        enemyHp = 450 + (currentStage * 20);
        enemyScale = 1.8;
        enemyColor = "#ff0055";
        enemyWeapon = "spear";
      } else {
        enemyHp = 150 + (currentStage * 15);
        enemyScale = 1.0 + (currentStage * 0.02);
        let wpList = ["sword", "axe", "dagger", "spear", "staff", "bow", "laser"];
        enemyWeapon = wpList[currentStage % wpList.length];
      }
    }

    pSelf = { x: startX, y: canvas.height - 25, vy: 0, isGrounded: true, hp: 200, maxHp: 200, atk: false, data: myData, facing: 1, walkTimer: 0, scale: 1.0, isDashing: false };
    
    pEnemy = { 
      x: enemyX, y: canvas.height - 25, vy: 0, isGrounded: true, 
      hp: enemyHp, maxHp: enemyHp, atk: false, 
      data: (gameMode === 'story') ? { color: enemyColor, weapon: enemyWeapon, hat: isBossStage ? "knight" : "none", cape: isBossStage ? "black" : "none" } : enemyData, 
      facing: -1, walkTimer: 0, scale: enemyScale, isDashing: false 
    };
    
    bullets = []; particles = [];
    myVoteRematch = false; enemyVoteRematch = false;
    document.getElementById("rematchBtn").style.opacity = "1";
    document.getElementById("rematchBtn").innerText = gameMode === 'story' ? "⏭️ MÀN TIẾP THEO" : "🔄 CHƠI TIẾP";
    document.getElementById("voteStatusText").innerText = "";

    isRunning = true;
    requestAnimationFrame(loop);
  }

  function handleNetworkData(data) {
    if(!data) return;
    
    if(data.type === 'INIT_PLAYER') {
      if(data.data) pEnemy.data = data.data;
    } else if(data.type === 'SYNC_POS') {
      if(typeof data.hp === 'number' && data.hp > 0) {
        pEnemy.hp = data.hp;
      }
      pEnemy.x = data.x; 
      pEnemy.y = data.y; 
      pEnemy.atk = data.atk; 
      pEnemy.facing = data.facing;
      pEnemy.walkTimer = data.walkTimer;
    } else if(data.type === 'SKILL' || data.type === 'DASH') {
      triggerDash(pEnemy);
    } else if(data.type === 'SHOOT') {
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

    if(gameMode === 'story') {
      if(won) {
        winTxt.innerText = isBossStage ? "🏆 DIỆT BOSS THÀNH CÔNG!" : "🎉 HOÀN THÀNH MÀN " + currentStage;
        winTxt.style.color = "#2ed573";
        currentStage++;
      } else {
        winTxt.innerText = "💀 BẠN ĐÃ HY SINH!";
        winTxt.style.color = "#ff4757";
      }
    } else {
      winTxt.innerText = won ? "🏆 BẠN THẮNG!" : "💀 BẠN THUA!";
      winTxt.style.color = won ? "#2ed573" : "#ff4757";
    }

    overlay.style.display = 'flex';
  }

  function requestRematch() {
    if(gameMode === 'story') {
      startGame();
    } else {
      myVoteRematch = true;
      document.getElementById("rematchBtn").style.opacity = "0.5";
      document.getElementById("rematchBtn").innerText = "⏳ ĐÃ BÌNH CHỌN (ĐỢI ĐỐI THỦ)";
      if(conn && conn.open) conn.send({ type: 'VOTE_REMATCH' });
      checkBothVoted();
    }
  }

  function checkBothVoted() {
    if(gameMode === 'online') {
      if(myVoteRematch && enemyVoteRematch) {
        startGame();
      } else if(enemyVoteRematch && !myVoteRematch) {
        document.getElementById("voteStatusText").innerText = "Đối thủ đã bấm Chơi tiếp!";
      }
    }
  }

  function quitGame() {
    isRunning = false;
    if(conn) { try{ conn.close(); } catch(e){} conn = null; }
    if(peer) { try{ peer.destroy(); } catch(e){} peer = null; }
    
    canvas.style.display = 'none';
    document.getElementById("gameControls").style.display = 'none';
    document.getElementById("endGameOverlay").style.display = 'none';
    showScreen('mainMenu');
  }

  function jump() { if (pSelf && pSelf.isGrounded && isRunning) { pSelf.vy = -11; pSelf.isGrounded = false; } }

  function attack() {
    if(!pSelf || !isRunning) return;
    pSelf.atk = true; 
    let reach = 40;
    let dmg = 12;

    if(pSelf.data.weapon === 'sword') { reach = 55; dmg = 14; }
    else if(pSelf.data.weapon === 'axe') { reach = 65; dmg = 25; }
    else if(pSelf.data.weapon === 'dagger') { reach = 35; dmg = 9; }
    else if(pSelf.data.weapon === 'spear') { reach = 75; dmg = 18; }

    if(Math.abs(pSelf.x - pEnemy.x) < reach * pSelf.scale) {
      pEnemy.hp = Math.max(0, pEnemy.hp - dmg);
      addParticles(pEnemy.x, pEnemy.y - 20 * pEnemy.scale, '#ff4757', 8);
    }
    setTimeout(() => pSelf.atk = false, 120);
  }

  function createBullet(caster, target, weapon) {
    let dir = caster.facing;
    let startX = caster.x + dir * 18 * caster.scale;
    let startY = caster.y - 22 * caster.scale;

    if (weapon === 'staff') {
      bullets.push({ x: startX, y: startY, vx: dir * 7.5, color: '#fffa65', radius: 8, dmg: 18, type: 'orb' });
    } else if (weapon === 'bow') {
      bullets.push({ x: startX, y: startY, vx: dir * 12, color: '#c7ecee', radius: 3, dmg: 12, type: 'arrow' });
    } else if (weapon === 'laser') {
      bullets.push({ x: startX, y: startY, vx: dir * 18, color: '#66fcf1', radius: 2, dmg: 16, type: 'laser' });
    }
  }

  function triggerDash(p) {
    p.isDashing = true;
    addParticles(p.x, p.y - 20, p.data.color, 10);
    let dashDist = p.facing * 75;
    p.x = Math.max(20, Math.min(canvas.width - 20, p.x + dashDist));
    
    // Gây sát thương lướt qua nếu trúng đối thủ
    let other = (p === pSelf) ? pEnemy : pSelf;
    if(Math.abs(p.x - other.x) < 40) {
      other.hp = Math.max(0, other.hp - 15);
      addParticles(other.x, other.y - 20, '#ff4757', 12);
    }
    setTimeout(() => p.isDashing = false, 200);
  }

  function useSkill() {
    if(!pSelf || !isRunning) return;
    
    // Skill mặc định cho mọi vũ khí: Lướt nhanh (Dash)
    triggerDash(pSelf);

    // Nếu dùng vũ khí tầm xa thì bắn thêm đạn
    if(['staff', 'bow', 'laser'].includes(pSelf.data.weapon)) {
      createBullet(pSelf, pEnemy, pSelf.data.weapon);
      if(gameMode === 'online' && conn && conn.open) conn.send({ type: 'SHOOT', weapon: pSelf.data.weapon });
    }

    if(gameMode === 'online' && conn && conn.open) conn.send({ type: 'DASH' });
  }

  function addParticles(x, y, color, count) {
    for(let i=0; i<count; i++) {
      particles.push({ x: x, y: y, vx: (Math.random()-0.5)*8, vy: (Math.random()-0.5)*8, life: 18, color: color });
    }
  }

  function loop() {
    if (!isRunning) return;
    animFrame++;
    let ground = canvas.height - 25;

    pSelf.y += pSelf.vy; pSelf.vy += 0.55;
    if (pSelf.y >= ground) { pSelf.y = ground; pSelf.vy = 0; pSelf.isGrounded = true; }

    if (moveL) { pSelf.x -= 4.2; pSelf.facing = -1; pSelf.walkTimer += 0.2; }
    else if (moveR) { pSelf.x += 4.2; pSelf.facing = 1; pSelf.walkTimer += 0.2; }
    else { pSelf.walkTimer = 0; }
    
    pSelf.x = Math.max(20, Math.min(canvas.width - 20, pSelf.x));

    if(gameMode === 'story') {
      pEnemy.y += pEnemy.vy; pEnemy.vy += 0.55;
      if (pEnemy.y >= ground) { pEnemy.y = ground; pEnemy.vy = 0; pEnemy.isGrounded = true; }
      
      pEnemy.facing = pSelf.x < pEnemy.x ? -1 : 1;
      let speed = 1.5 + (currentStage * 0.15);
      if(isBossStage) speed = 2.2;

      if (Math.abs(pSelf.x - pEnemy.x) > 35 * pEnemy.scale) {
        pEnemy.x += (pSelf.x < pEnemy.x) ? -speed : speed;
        pEnemy.walkTimer += 0.2;
      }

      let atkChance = 0.015 + (currentStage * 0.003);
      if (Math.random() < 0.008 && pEnemy.isGrounded) pEnemy.vy = -11;
      
      if (Math.random() < atkChance) { 
        pEnemy.atk = true; 
        setTimeout(() => pEnemy.atk = false, 120); 
        if(['staff', 'bow', 'laser'].includes(pEnemy.data.weapon)) {
          createBullet(pEnemy, pSelf, pEnemy.data.weapon); 
        } else if(Math.abs(pSelf.x - pEnemy.x) < 55 * pEnemy.scale) {
          pSelf.hp = Math.max(0, pSelf.hp - (8 + currentStage * 1.5));
          addParticles(pSelf.x, pSelf.y - 20, '#ff4757', 6);
        }
      }
    }

    if(gameMode === 'online' && conn && conn.open) {
      conn.send({ 
        type: 'SYNC_POS', 
        x: pSelf.x, 
        y: pSelf.y, 
        hp: pSelf.hp, 
        atk: pSelf.atk, 
        facing: pSelf.facing,
        walkTimer: pSelf.walkTimer
      });
    }

    ctx.clearRect(0, 0, canvas.width, canvas.height);
    
    ctx.fillStyle = "#1f2833"; ctx.fillRect(0, ground + 20, canvas.width, 10);
    ctx.fillStyle = "#66fcf1"; ctx.fillRect(0, ground + 18, canvas.width, 2);

    let w = canvas.width * 0.35;
    ctx.fillStyle = "#1f2833"; ctx.fillRect(10, 10, w, 14); 
    ctx.fillStyle = pSelf.data.color; ctx.fillRect(10, 10, w * (Math.max(0, pSelf.hp) / pSelf.maxHp), 14);
    ctx.strokeStyle = "#fff"; ctx.lineWidth = 1; ctx.strokeRect(10, 10, w, 14);

    if(isBossStage) {
      let bossW = canvas.width * 0.6;
      let bossX = (canvas.width - bossW) / 2;
      ctx.fillStyle = "#1f2833"; ctx.fillRect(bossX, 32, bossW, 18);
      ctx.fillStyle = "#ff0055"; ctx.fillRect(bossX, 32, bossW * (Math.max(0, pEnemy.hp) / pEnemy.maxHp), 18);
      ctx.strokeStyle = "#ff4757"; ctx.lineWidth = 2; ctx.strokeRect(bossX, 32, bossW, 18);
      ctx.fillStyle = "#fff"; ctx.font = "bold 12px sans-serif"; ctx.fillText("🔥 BOSS KHỔNG LỒ (MÀN " + currentStage + ") 🔥", canvas.width/2 - 80, 26);
    } else {
      ctx.fillStyle = "#1f2833"; ctx.fillRect(canvas.width - 10 - w, 10, w, 14);
      ctx.fillStyle = pEnemy.data.color; ctx.fillRect(canvas.width - 10 - w, 10, w * (Math.max(0, pEnemy.hp) / pEnemy.maxHp), 14);
      ctx.strokeStyle = "#fff"; ctx.lineWidth = 1; ctx.strokeRect(canvas.width - 10 - w, 10, w, 14);
    }

    particles.forEach((p, i) => {
      p.x += p.vx; p.y += p.vy; p.life--;
      ctx.fillStyle = p.color; ctx.fillRect(p.x, p.y, 3, 3);
      if(p.life <= 0) particles.splice(i, 1);
    });

    bullets.forEach((b, idx) => {
      b.x += b.vx;
      ctx.fillStyle = b.color;
      ctx.shadowColor = b.color;
      ctx.shadowBlur = 10;

      if(b.type === 'laser') {
        ctx.fillRect(b.x, b.y - 2, 25 * Math.sign(b.vx), 4);
      } else {
        ctx.beginPath(); ctx.arc(b.x, b.y, b.radius, 0, Math.PI * 2); ctx.fill();
      }
      ctx.shadowBlur = 0;

      let target = (b.vx > 0 && (isHost || gameMode === 'story')) ? pEnemy : pSelf;
      if (Math.abs(b.x - target.x) < 22 * target.scale && Math.abs(b.y - (target.y - 20 * target.scale)) < 30 * target.scale) {
        target.hp = Math.max(0, target.hp - b.dmg);
        addParticles(b.x, b.y, b.color, 10);
        bullets.splice(idx, 1);
      }
    });

    drawPlayer(pSelf); drawPlayer(pEnemy);

    if (pSelf.hp <= 0 || pEnemy.hp <= 0) {
      triggerEndGame(pSelf.hp > 0);
      return;
    }

    requestAnimationFrame(loop);
  }

  function drawPlayer(p) {
    let f = p.facing, x = p.x, y = p.y, s = p.scale;
    let legSwing = Math.sin(p.walkTimer * 5) * 10;

    ctx.save();
    ctx.shadowColor = p.data.color;
    ctx.shadowBlur = p.isDashing ? 20 : 8;

    if(p.data.cape && p.data.cape !== 'none') {
      ctx.fillStyle = p.data.cape === 'red' ? '#ff3838' : '#2f3542';
      ctx.beginPath(); 
      ctx.moveTo(x - f * 4 * s, y - 25 * s); 
      ctx.lineTo(x - f * (18 + Math.sin(animFrame*0.2)*4) * s, y + 5 * s); 
      ctx.lineTo(x - f * 4 * s, y + 2 * s); 
      ctx.fill();
    }

    ctx.strokeStyle = p.data.color; ctx.lineWidth = 3 * s;
    
    ctx.beginPath(); ctx.arc(x, y - 35 * s, 9 * s, 0, Math.PI * 2); ctx.stroke();
    ctx.beginPath(); ctx.moveTo(x, y - 26 * s); ctx.lineTo(x, y - 8 * s); ctx.stroke();
    
    ctx.beginPath(); ctx.moveTo(x, y - 8 * s); ctx.lineTo(x - (8 + legSwing) * s, y + 20 * s); ctx.stroke();
    ctx.beginPath(); ctx.moveTo(x, y - 8 * s); ctx.lineTo(x + (8 + legSwing) * s, y + 20 * s); ctx.stroke();

    let handX = x + (p.atk ? f * 22 * s : f * 8 * s);
    let handY = y - (p.atk ? 24 * s : 16 * s);
    ctx.beginPath(); ctx.moveTo(x, y - 22 * s); ctx.lineTo(handX, handY); ctx.stroke();

    if(p.data.hat === 'knight') {
      ctx.fillStyle = '#a4b0be'; ctx.fillRect(x - 10 * s, y - 48 * s, 20 * s, 8 * s);
    } else if(p.data.hat === 'wizard') {
      ctx.fillStyle = '#5f27cd'; ctx.beginPath(); ctx.moveTo(x - 12 * s, y - 42 * s); ctx.lineTo(x, y - 62 * s); ctx.lineTo(x + 12 * s, y - 42 * s); ctx.fill();
    }

    ctx.save(); ctx.translate(handX, handY);
    if(p.data.weapon === 'sword') {
      ctx.strokeStyle = '#fff'; ctx.lineWidth = 3 * s; ctx.beginPath(); ctx.moveTo(0, 0); ctx.lineTo(f * 25 * s, -18 * s); ctx.stroke();
    } else if(p.data.weapon === 'axe') {
      ctx.strokeStyle = '#dcdde1'; ctx.lineWidth = 4 * s; ctx.beginPath(); ctx.moveTo(0, 0); ctx.lineTo(f * 20 * s, -22 * s); ctx.stroke();
      ctx.fillStyle = '#ff4757'; ctx.fillRect(f * 15 * s, -28 * s, 10 * s, 12 * s);
    } else if(p.data.weapon === 'dagger') {
      ctx.strokeStyle = '#2ed573'; ctx.lineWidth = 2 * s; ctx.beginPath(); ctx.moveTo(0, 0); ctx.lineTo(f * 14 * s, -10 * s); ctx.stroke();
    } else if(p.data.weapon === 'spear') {
      ctx.strokeStyle = '#ffa502'; ctx.lineWidth = 3 * s; ctx.beginPath(); ctx.moveTo(0, 0); ctx.lineTo(f * 38 * s, -28 * s); ctx.stroke();
      ctx.fillStyle = '#ff4757'; ctx.beginPath(); ctx.moveTo(f * 38 * s, -28 * s); ctx.lineTo(f * 32 * s, -22 * s); ctx.lineTo(f * 30 * s, -32 * s); ctx.fill();
    } else if(p.data.weapon === 'staff') {
      ctx.strokeStyle = '#78e08f'; ctx.lineWidth = 3 * s; ctx.beginPath(); ctx.moveTo(0, 5 * s); ctx.lineTo(f * 18 * s, -22 * s); ctx.stroke();
      ctx.fillStyle = '#fffa65'; ctx.beginPath(); ctx.arc(f * 18 * s, -22 * s, 6 * s, 0, Math.PI*2); ctx.fill();
    } else if(p.data.weapon === 'bow') {
      ctx.strokeStyle = '#e1b12c'; ctx.lineWidth = 2 * s; ctx.beginPath(); ctx.arc(f * 6 * s, -5 * s, 14 * s, -Math.PI/2, Math.PI/2); ctx.stroke();
    } else if(p.data.weapon === 'laser') {
      ctx.fillStyle = '#66fcf1'; ctx.fillRect(0, -4 * s, f * 20 * s, 8 * s);
    }
    ctx.restore();
    ctx.restore();
  }

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

  function bindBtn(id, start, end) {
    let el = document.getElementById(id);
    if(!el) return;
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
