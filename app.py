import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(page_title="Stick Man Batter Fight", layout="wide")

game_code = """
<!DOCTYPE html>
<html>
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no">
  <script src="https://unpkg.com/peerjs@1.5.2/dist/peerjs.min.js"></script>
  <style>
    * { box-sizing: border-box; margin: 0; padding: 0; user-select: none; -webkit-user-select: none; }
    body { width: 100vw; height: 100vh; background: #050508; color: white; font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; display: flex; flex-direction: column; align-items: center; justify-content: center; overflow: hidden; position: relative; }
    
    .top-bar {
      position: absolute; top: 15px; right: 20px; 
      display: flex; gap: 10px; z-index: 999;
    }
    .top-btn { 
      padding: 8px 16px; background: rgba(31, 40, 51, 0.8); border: 2px solid #ff4757; 
      color: #ff4757; border-radius: 10px; cursor: pointer; 
      font-weight: bold; font-size: 13px; backdrop-filter: blur(5px);
      box-shadow: 0 0 15px rgba(255, 71, 87, 0.4);
      transition: all 0.2s; outline: none; display: none;
    }
    .top-btn:active { background: #ff4757; color: #fff; transform: scale(0.95); }

    .screen { position: absolute; top:0; left:0; width: 100%; height: 100%; background: radial-gradient(circle at center, #1f2833 0%, #050508 100%); display: flex; flex-direction: column; align-items: center; justify-content: center; z-index: 100; gap: 14px; }
    
    .title-container {
      display: flex;
      flex-direction: column;
      align-items: center;
      gap: 6px;
      margin-bottom: 5px;
    }
    
    h1 { font-size: 32px; color: #66fcf1; text-align: center; text-shadow: 0 0 20px rgba(102, 252, 241, 0.6); letter-spacing: 3px; font-weight: 900; }
    
    .author-name {
      font-size: 15px;
      color: #70a1ff;
      font-weight: 600;
      letter-spacing: 2px;
      text-shadow: 0 0 10px rgba(112, 161, 255, 0.5);
      text-transform: uppercase;
    }
    
    .btn { padding: 14px 30px; font-size: 16px; font-weight: bold; background: rgba(31, 40, 51, 0.9); border: 2px solid #66fcf1; border-radius: 12px; color: #66fcf1; cursor: pointer; text-align: center; z-index: 110; min-width: 260px; box-shadow: 0 0 15px rgba(102, 252, 241, 0.25); backdrop-filter: blur(5px); transition: all 0.2s; }
    .btn:active { background: #66fcf1; color: #000; transform: scale(0.95); box-shadow: 0 0 25px #66fcf1; }
    
    input, select { padding: 12px 16px; font-size: 15px; border-radius: 10px; border: 2px solid #45a29e; background: rgba(11, 12, 16, 0.9); color: white; text-align: center; width: 260px; outline: none; box-shadow: inset 0 0 10px rgba(0,0,0,0.5); }
    input:focus, select:focus { border-color: #66fcf1; box-shadow: 0 0 10px rgba(102, 252, 241, 0.3); }
    
    .select-box { display: flex; gap: 12px; align-items: center; background: rgba(31, 40, 51, 0.7); padding: 10px 16px; border-radius: 12px; width: 85%; max-width: 380px; justify-content: space-between; border: 1px solid rgba(69, 162, 158, 0.5); backdrop-filter: blur(5px); }
    #statusText { color: #f7b731; font-weight: bold; font-size: 15px; text-align: center; text-shadow: 0 0 10px rgba(247, 183, 49, 0.4); }
    
    #gameCanvas { background: radial-gradient(circle at center, #111318 0%, #030305 100%); border: 2px solid #45a29e; border-radius: 16px; width: 96vw; height: 54vh; display: none; position: relative; z-index: 1; box-shadow: 0 0 30px rgba(69, 162, 158, 0.4); }
    
    #endGameOverlay {
      position: absolute; top: 0; left: 0; width: 100vw; height: 100vh;
      background: rgba(3, 3, 5, 0.9); backdrop-filter: blur(8px); display: none; flex-direction: column;
      align-items: center; justify-content: center; z-index: 200; gap: 18px;
    }
    #winnerText { font-size: 38px; font-weight: 900; color: #f7b731; text-shadow: 0 0 25px rgba(247, 183, 49, 0.8); letter-spacing: 2px; }
    #voteStatusText { color: #66fcf1; font-size: 15px; font-weight: bold; min-height: 22px; text-shadow: 0 0 10px rgba(102, 252, 241, 0.4); }

    .controls { position: absolute; bottom: 15px; width: 100vw; display: none; justify-content: space-between; padding: 0 25px; z-index: 50; }
    .btn-group { display: flex; gap: 12px; }
    .btn-ctrl { 
      position: relative; width: 68px; height: 68px; border-radius: 16px; 
      font-weight: bold; display: flex; align-items: center; justify-content: center; 
      background: rgba(31, 40, 51, 0.85); border: 2px solid #66fcf1; color: #fff; cursor: pointer; 
      font-size: 24px; box-shadow: 0 0 15px rgba(102, 252, 241, 0.3); backdrop-filter: blur(5px);
    }
    .btn-ctrl:active, .btn-ctrl.active { background: #66fcf1; color: #000; box-shadow: 0 0 25px #66fcf1; transform: scale(0.95); }
    .key-hint { 
      position: absolute; top: 3px; right: 5px; font-size: 10px; color: #f7b731; 
      font-weight: bold; background: rgba(0,0,0,0.7); padding: 2px 4px; border-radius: 4px; 
    }
  </style>
</head>
<body>

  <div class="top-bar">
    <button class="top-btn" id="topRightBackBtn" onclick="quitGame()">🏠 THOÁT TRẬN</button>
  </div>

  <!-- MAIN MENU -->
  <div id="mainMenu" class="screen">
    <div class="title-container">
      <h1>STICK MAN BATTER FIGHT</h1>
      <div class="author-name">Make by Tiến Dũng</div>
    </div>
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
    <div class="btn" style="border-color:#ff4757; color:#ff4757; margin-top: 15px;" id="btnBackToMenu">⬅ QUAY LẠI MENU</div>
  </div>

  <!-- LOBBY MENU -->
  <div id="lobbyMenu" class="screen" style="display:none;">
    <h1>CHẾ ĐỘ MULTIPLAYER</h1>
    <div class="btn" style="border-color:#2ed573; color:#2ed573;" id="btnCreateLobby">🎲 TẠO LOBBY MỚI</div>
    <div class="btn" style="border-color:#ffa502; color:#ffa502;" id="btnJoinLobby">🔑 THAM GIA LOBBY</div>
    <div class="btn" style="border-color:#ff4757; color:#ff4757; margin-top: 15px;" id="btnBackFromLobby">⬅ QUAY LẠI</div>
  </div>

  <!-- CHỌN CHẾ ĐỘ CHƠI (MODE SELECTOR CHO CẢ ONLINE & STORY) -->
  <div id="modeSelectScreen" class="screen" style="display:none;">
    <h1>CHỌN CHẾ ĐỘ TRẬN ĐẤU</h1>
    <div class="btn" id="btnClassicMode" style="border-color:#66fcf1; color:#66fcf1;">⚔️ 1. CHẾ ĐỘ CỔ ĐIỂN (PVP / 1v1)</div>
    <div class="btn" id="btnCampaignMode" style="border-color:#2ed573; color:#2ed573;">🧟 2. CHẾ ĐỘ CHIẾN DỊCH (ĐÁNH ZOMBIE)</div>
    <div class="btn" style="border-color:#ff4757; color:#ff4757; margin-top: 15px;" id="btnBackFromMode">⬅ QUAY LẠI</div>
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
      <select id="weaponSelect" onchange="updateSkillIcon()">
        <option value="sword">⚔️ Kiếm Thần (Skill: Hút Gió & Hồi Máu 10s)</option>
        <option value="axe">🪓 Rìu Chiến (Skill: Bay Nhảy Đập 10s)</option>
        <option value="dagger">🗡️ Dao Độc (Skill: Mưa Dao Găm 10s)</option>
        <option value="spear">🔱 Giáo Dài (Skill: Lướt Đâm Xuyên 10s)</option>
        <option value="staff">🪄 Trượng Ma Thuật (Skill: Bắn Cầu Lửa 10s)</option>
        <option value="bow">🏹 Cung Thần (Skill: Bắn Mũi Tên Đôi 0.2s)</option>
        <option value="laser">⚡ Súng Laser (Skill: Tia Xuyên Phá 10s)</option>
        <option value="muscle">💪 Cơ Bắp Thần Thánh (Skill: Bay Lên Quay Lửa & Đập Sóng Xung Kích 10s)</option>
      </select>
    </div>
    <div class="select-box">
      <span>Mũ / Nón:</span>
      <select id="hatSelect">
        <option value="none">Không Đội Mũ</option>
        <option value="knight">🪖 Mũ Chiến Binh Siêu Cấp</option>
        <option value="wizard">🧙 Mũ Phù Thủy Ma Quái</option>
      </select>
    </div>
    <div class="select-box">
      <span>Áo Choàng:</span>
      <select id="capeSelect">
        <option value="none">Không Áo Choàng</option>
        <option value="red">🔴 Áo Choàng Dạ Quang Đỏ</option>
        <option value="black">⚫ Áo Choàng Đen Huyền Bí</option>
      </select>
    </div>
    <div class="btn" id="btnStartGame" style="background: linear-gradient(135deg, #2ed573 0%, #10ac84 100%); border-color:#fff; color:#fff; text-shadow: 0 0 10px rgba(0,0,0,0.5);">BẮT ĐẦU VÀO TRẬN ➔</div>
    <div class="btn" style="border-color:#ff4757; color:#ff4757;" id="btnBackToPrev">⬅ QUAY LẠI</div>
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
      <div class="btn-ctrl" style="border-color:#ff4757" id="btnSkill">🌀<span class="key-hint" id="skillKeyHint">M2</span></div>
    </div>
  </div>

<script>
  const canvas = document.getElementById("gameCanvas");
  const ctx = canvas.getContext("2d");
  
  let peer = null, conn = null;
  let isHost = false, gameMode = 'story', subGameMode = 'classic'; // subGameMode: 'classic' hoặc 'campaign'
  let roomCode = "";
  let currentStage = 1;

  let myData = { color: "#66fcf1", weapon: "sword", hat: "knight", cape: "red" };
  let enemyData = { color: "#ff4757", weapon: "staff", hat: "wizard", cape: "black" };

  let myVoteRematch = false, enemyVoteRematch = false;
  let enemies = []; // Danh sách zombie trong chế độ chiến dịch

  function updateSkillIcon() {
    let wp = document.getElementById("weaponSelect").value;
    let skillBtn = document.getElementById("btnSkill");
    if(wp === 'sword') skillBtn.innerText = "🌪️";
    else if(wp === 'axe') skillBtn.innerText = "🪓";
    else if(wp === 'dagger') skillBtn.innerText = "🗡️";
    else if(wp === 'spear') skillBtn.innerText = "🔱";
    else if(wp === 'staff') skillBtn.innerText = "🔥";
    else if(wp === 'bow') skillBtn.innerText = "🏹";
    else if(wp === 'laser') skillBtn.innerText = "⚡";
    else if(wp === 'muscle') skillBtn.innerText = "💪";
  }

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
    if (id === 'mainMenu' || id === 'settingsScreen' || id === 'lobbyMenu' || id === 'createRoomScreen' || id === 'joinRoomScreen' || id === 'customScreen' || id === 'modeSelectScreen') {
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

  // Story Mode trực tiếp mở menu chọn chế độ phụ
  addClickEvent('btnStory', () => { 
    gameMode = 'story'; 
    showScreen('modeSelectScreen');
  });
  // Multiplayer chọn phòng xong hoặc chọn chế độ trước
  addClickEvent('btnMulti', () => { 
    gameMode = 'online'; 
    showScreen('lobbyMenu'); 
    updateSkillIcon(); 
  });
  
  addClickEvent('btnClassicMode', () => {
    subGameMode = 'classic';
    currentStage = 1;
    document.getElementById('customTitle').innerText = (gameMode === 'story') ? "STORY - CỔ ĐIỂN" : "MULTIPLAYER - PVP";
    showScreen('customScreen');
    updateSkillIcon();
  });

  addClickEvent('btnCampaignMode', () => {
    subGameMode = 'campaign';
    currentStage = 1;
    document.getElementById('customTitle').innerText = (gameMode === 'story') ? "CHIẾN DỊCH ZOMBIE - MÀN 1" : "MULTIPLAYER CO-OP - CHIẾN DỊCH";
    showScreen('customScreen');
    updateSkillIcon();
  });

  addClickEvent('btnSettings', () => showScreen('settingsScreen'));
  addClickEvent('btnBackToMenu', () => showScreen('mainMenu'));
  addClickEvent('btnBackFromLobby', () => showScreen('mainMenu'));
  addClickEvent('btnBackFromMode', () => {
    if(gameMode === 'story') showScreen('mainMenu');
    else showScreen('lobbyMenu');
  });
  addClickEvent('btnBackToPrev', () => {
    if(gameMode === 'story') showScreen('modeSelectScreen');
    else showScreen('lobbyMenu');
  });

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
      showScreen('modeSelectScreen'); // Host chọn chế độ sau khi tạo phòng thành công
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
      showScreen('modeSelectScreen'); // Client vào phòng thành công cũng chọn chế độ (hoặc đồng bộ)
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
      conn.send({ type: 'INIT_PLAYER', data: myData, subGameMode: subGameMode, currentStage: currentStage });
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

    isBossStage = (subGameMode === 'campaign' && currentStage % 10 === 0);

    let enemyHp = 500;
    let enemyScale = 1.0;
    let enemyColor = "#ff4757";
    let enemyWeapon = "sword";

    enemies = [];

    if(subGameMode === 'campaign') {
      // Số lượng zombie: Màn 1 có 1 zombie, mỗi màn tăng thêm 1 (trừ màn boss chỉ có 1 boss cực mạnh)
      let zombieCount = isBossStage ? 1 : currentStage;
      
      if(isBossStage) {
        enemyHp = 1800 + (currentStage * 120);
        enemyScale = 2.0;
        enemyColor = "#ff0055";
        enemyWeapon = "axe";
        enemies.push({
          x: canvas.width - 80, y: canvas.height - 25, vy: 0, isGrounded: true,
          hp: enemyHp, maxHp: enemyHp, atk: false,
          data: { color: enemyColor, weapon: enemyWeapon, hat: "knight", cape: "black" },
          facing: -1, walkTimer: 0, scale: enemyScale, isSpecialAction: false, lastAtkTime: 0, lastSkillTime: 0, windEffectTimer: 0, isBoss: true
        });
      } else {
        for(let i = 0; i < zombieCount; i++) {
          let zHp = 300 + (currentStage * 40);
          let wpList = ["sword", "axe", "dagger", "spear", "staff", "bow", "laser", "muscle"];
          let zWp = wpList[(currentStage + i) % wpList.length];
          enemies.push({
            x: canvas.width - 80 - (i * 40), y: canvas.height - 25, vy: 0, isGrounded: true,
            hp: zHp, maxHp: zHp, atk: false,
            data: { color: "#ff4757", weapon: zWp, hat: "none", cape: "none" },
            facing: -1, walkTimer: 0, scale: 1.0, isSpecialAction: false, lastAtkTime: 0, lastSkillTime: 0, windEffectTimer: 0, isBoss: false
          });
        }
      }
    } else {
      // Chế độ cổ điển (PVP hoặc 1v1 online)
      pEnemy = { 
        x: enemyX, y: canvas.height - 25, vy: 0, isGrounded: true, 
        hp: 450, maxHp: 450, atk: false, 
        data: (gameMode === 'story') ? { color: "#ff4757", weapon: "staff", hat: "wizard", cape: "black" } : enemyData, 
        facing: -1, walkTimer: 0, scale: 1.0, isSpecialAction: false, lastAtkTime: 0, lastSkillTime: 0, windEffectTimer: 0
      };
    }

    pSelf = { x: startX, y: canvas.height - 25, vy: 0, isGrounded: true, hp: 450, maxHp: 450, atk: false, data: myData, facing: 1, walkTimer: 0, scale: 1.0, isSpecialAction: false, lastAtkTime: 0, lastSkillTime: 0, windEffectTimer: 0 };
    
    bullets = []; particles = [];
    myVoteRematch = false; enemyVoteRematch = false;
    document.getElementById("rematchBtn").style.opacity = "1";
    document.getElementById("rematchBtn").innerText = (subGameMode === 'campaign') ? "⏭️ MÀN TIẾP THEO" : "🔄 CHƠI TIẾP";
    document.getElementById("voteStatusText").innerText = "";

    isRunning = true;
    requestAnimationFrame(loop);
  }

  function handleNetworkData(data) {
    if(!data) return;
    
    if(data.type === 'INIT_PLAYER') {
      if(data.data) {
        if(subGameMode === 'classic') pEnemy.data = data.data;
      }
      if(data.subGameMode) subGameMode = data.subGameMode;
      if(data.currentStage) currentStage = data.currentStage;
    } else if(data.type === 'SYNC_POS') {
      if(subGameMode === 'classic') {
        if(typeof data.hp === 'number' && data.hp > 0) {
          pEnemy.hp = data.hp;
        }
        pEnemy.x = data.x; 
        pEnemy.y = data.y; 
        pEnemy.atk = data.atk; 
        pEnemy.facing = data.facing;
        pEnemy.walkTimer = data.walkTimer;
      }
    } else if(data.type === 'SKILL') {
      if(subGameMode === 'classic' && pEnemy) executeWeaponSkill(pEnemy);
    } else if(data.type === 'SHOOT') {
      if(subGameMode === 'classic' && pEnemy) createBullet(pEnemy, pSelf, data.weapon);
    } else if(data.type === 'VOTE_REMATCH') {
      enemyVoteRematch = true;
      checkBothVoted();
    }
  }

  function triggerEndGame(won) {
    isRunning = false;
    let overlay = document.getElementById("endGameOverlay");
    let winTxt = document.getElementById("winnerText");

    if(subGameMode === 'campaign') {
      if(won) {
        winTxt.innerText = isBossStage ? "🏆 DIỆT BOSS HOÀN HẢO!" : "🎉 HOÀN THÀNH MÀN " + currentStage;
        winTxt.style.color = "#2ed573";
        currentStage++;
      } else {
        winTxt.innerText = "💀 BẠN ĐÃ HY SINH!";
        winTxt.style.color = "#ff4757";
      }
    } else {
      winTxt.innerText = won ? "🏆 CHIẾN THẮNG VẺ VANG!" : "💀 THẤT BẠI!";
      winTxt.style.color = won ? "#2ed573" : "#ff4757";
    }

    overlay.style.display = 'flex';
  }

  function requestRematch() {
    if(subGameMode === 'campaign' || gameMode === 'story') {
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
    if(gameMode === 'online' && subGameMode === 'classic') {
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

  function jump() { if (pSelf && pSelf.isGrounded && isRunning) { pSelf.vy = -12; pSelf.isGrounded = false; } }

  function attack() {
    if(!pSelf || !isRunning) return;
    
    let now = Date.now();
    let cooldown = (pSelf.data.weapon === 'dagger') ? 140 : 190; 
    if (now - (pSelf.lastAtkTime || 0) < cooldown) return;
    pSelf.lastAtkTime = now;

    pSelf.atk = true; 
    let reach = 45;
    let dmg = 15;

    if(pSelf.data.weapon === 'sword') { reach = 65; dmg = 18; }
    else if(pSelf.data.weapon === 'axe') { reach = 75; dmg = 28; }
    else if(pSelf.data.weapon === 'dagger') { reach = 42; dmg = 11; }
    else if(pSelf.data.weapon === 'spear') { reach = 85; dmg = 22; }
    else if(pSelf.data.weapon === 'muscle') { reach = 85; dmg = 32; }

    if(subGameMode === 'campaign') {
      for(let z of enemies) {
        if(z.hp > 0 && Math.abs(pSelf.x - z.x) < reach * pSelf.scale) {
          z.hp = Math.max(0, z.hp - dmg);
          addParticles(z.x, z.y - 20 * z.scale, pSelf.data.color, 12);
        }
      }
    } else {
      let other = pEnemy;
      if(Math.abs(pSelf.x - other.x) < reach * pSelf.scale) {
        other.hp = Math.max(0, other.hp - dmg);
        addParticles(other.x, other.y - 20 * other.scale, pSelf.data.color, 12);
      }
    }
    setTimeout(() => pSelf.atk = false, 120);
  }

  function createBullet(caster, target, weapon) {
    let dir = caster.facing;
    let startX = caster.x + dir * 20 * caster.scale;
    let startY = caster.y - 24 * caster.scale;
    let dmgBonus = (subGameMode === 'campaign') ? (10 + currentStage * 2) : 0;

    if (weapon === 'staff') {
      bullets.push({ x: startX, y: startY, vx: dir * 9.5, color: '#fffa65', radius: 9, dmg: 22 + dmgBonus, type: 'orb', shooter: caster });
    } else if (weapon === 'bow') {
      let bowDmg = (subGameMode === 'campaign') ? Math.max(2, 2 + Math.floor(currentStage / 2)) : 2;
      bullets.push({ x: startX, y: startY, vx: dir * 14, color: '#c7ecee', radius: 3.5, dmg: bowDmg, type: 'arrow', shooter: caster });
    } else if (weapon === 'laser') {
      bullets.push({ x: startX, y: startY, vx: dir * 20, color: '#66fcf1', radius: 2.5, dmg: 20 + dmgBonus, type: 'laser', shooter: caster });
    }
  }

  function executeWeaponSkill(p) {
    let wp = p.data.weapon;
    let isCampaignZombie = (subGameMode === 'campaign' && enemies.includes(p));

    if (wp === 'sword') {
      p.isSpecialAction = true;
      p.windEffectTimer = 35;
      addParticles(p.x, p.y - 20, '#2ed573', 25);

      let healTicks = 0;
      let healInterval = setInterval(() => {
        healTicks++;
        let healAmount = 30;
        p.hp = Math.min(p.maxHp, p.hp + healAmount);
        addParticles(p.x, p.y - 20, '#2ed573', 10);

        if (healTicks >= 5) {
          clearInterval(healInterval);
          p.isSpecialAction = false;
        }
      }, 200);

    } else if (wp === 'axe') {
      p.isSpecialAction = true;
      p.vy = -14; p.isGrounded = false;
      addParticles(p.x, p.y - 20, '#ffa502', 22);

      setTimeout(() => {
        p.vy = 18;
        let checkSlam = setInterval(() => {
          let ground = canvas.height - 25;
          if(p.y >= ground) {
            p.y = ground; p.vy = 0; p.isSpecialAction = false;
            clearInterval(checkSlam);
            addParticles(p.x, p.y, '#ff4757', 30);
            let slamDmg = isCampaignZombie ? (75 + currentStage * 8) : 60;
            
            if(subGameMode === 'campaign') {
              let targets = (p === pSelf) ? enemies : [pSelf];
              for(let t of targets) {
                if(t && t.hp > 0 && Math.abs(p.x - t.x) < 110) {
                  t.hp = Math.max(0, t.hp - slamDmg);
                  addParticles(t.x, t.y - 20, '#ff4757', 24);
                }
              }
            } else {
              let other = (p === pSelf) ? pEnemy : pSelf;
              if(Math.abs(p.x - other.x) < 110) {
                other.hp = Math.max(0, other.hp - slamDmg);
                addParticles(other.x, other.y - 20, '#ff4757', 24);
              }
            }
          }
        }, 20);
      }, 280);

    } else if (wp === 'dagger') {
      p.isSpecialAction = true;
      addParticles(p.x, p.y - 20, '#2ed573', 15);
      let daggerDmg = isCampaignZombie ? (12 + currentStage * 2) : 10;
      for(let i=0; i<3; i++) {
        setTimeout(() => {
          bullets.push({ x: p.x + p.facing*20, y: p.y - 25, vx: p.facing * (16 + i*2), color: '#2ed573', radius: 4, dmg: daggerDmg, type: 'arrow', shooter: p });
        }, i * 70);
      }
      setTimeout(() => p.isSpecialAction = false, 250);

    } else if (wp === 'spear') {
      p.isSpecialAction = true;
      addParticles(p.x, p.y - 20, '#f1c40f', 20);
      let dashDist = p.facing * 150;
      p.x = Math.max(20, Math.min(canvas.width - 20, p.x + dashDist));
      let thrustDmg = isCampaignZombie ? (60 + currentStage * 6) : 50;

      if(subGameMode === 'campaign') {
        let targets = (p === pSelf) ? enemies : [pSelf];
        for(let t of targets) {
          if(t && t.hp > 0 && Math.abs(p.x - t.x) < 100) {
            t.hp = Math.max(0, t.hp - thrustDmg);
            addParticles(t.x, t.y - 20, '#f1c40f', 26);
          }
        }
      } else {
        let other = (p === pSelf) ? pEnemy : pSelf;
        if(Math.abs(p.x - other.x) < 100) {
          other.hp = Math.max(0, other.hp - thrustDmg);
          addParticles(other.x, other.y - 20, '#f1c40f', 26);
        }
      }
      setTimeout(() => p.isSpecialAction = false, 250);

    } else if (wp === 'muscle') {
      p.isSpecialAction = true;
      p.vy = -16; p.isGrounded = false;
      addParticles(p.x, p.y - 20, '#ff4757', 30);

      let flameSpinTimer = 0;
      let spinInterval = setInterval(() => {
        flameSpinTimer++;
        addParticles(p.x + (Math.random()-0.5)*40, p.y - 30 + (Math.random()-0.5)*40, '#ff4757', 5);
        addParticles(p.x + (Math.random()-0.5)*40, p.y - 30 + (Math.random()-0.5)*40, '#ffa502', 5);
        
        if(subGameMode === 'campaign') {
          let targets = (p === pSelf) ? enemies : [pSelf];
          for(let t of targets) {
            if(t && t.hp > 0 && Math.abs(p.x - t.x) < 70) t.hp = Math.max(0, t.hp - 4);
          }
        } else {
          let other = (p === pSelf) ? pEnemy : pSelf;
          if(Math.abs(p.x - other.x) < 70) other.hp = Math.max(0, other.hp - 4);
        }

        if(flameSpinTimer >= 15) {
          clearInterval(spinInterval);
          p.vy = 22;
          let checkMuscleSlam = setInterval(() => {
            let ground = canvas.height - 25;
            if(p.y >= ground) {
              p.y = ground; p.vy = 0; p.isSpecialAction = false;
              clearInterval(checkMuscleSlam);
              addParticles(p.x, p.y, '#ff4757', 45);
              let muscleSlamDmg = isCampaignZombie ? (90 + currentStage * 10) : 75;

              if(subGameMode === 'campaign') {
                let targets = (p === pSelf) ? enemies : [pSelf];
                for(let t of targets) {
                  if(t && t.hp > 0 && Math.abs(p.x - t.x) < 140) {
                    t.hp = Math.max(0, t.hp - muscleSlamDmg);
                    t.x += (t.x > p.x) ? 90 : -90;
                    t.x = Math.max(20, Math.min(canvas.width - 20, t.x));
                    addParticles(t.x, t.y - 20, '#ff4757', 30);
                  }
                }
              } else {
                let other = (p === pSelf) ? pEnemy : pSelf;
                if(Math.abs(p.x - other.x) < 140) {
                  other.hp = Math.max(0, other.hp - muscleSlamDmg);
                  other.x += (other.x > p.x) ? 90 : -90;
                  other.x = Math.max(20, Math.min(canvas.width - 20, other.x));
                  addParticles(other.x, other.y - 20, '#ff4757', 30);
                }
              }
            }
          }, 20);
        }
      }, 50);

    } else if (['staff', 'bow', 'laser'].includes(wp)) {
      let otherTarget = (subGameMode === 'classic') ? ((p === pSelf) ? pEnemy : pSelf) : pSelf;
      createBullet(p, otherTarget, wp);
      if(wp === 'bow') {
        setTimeout(() => createBullet(p, otherTarget, wp), 80);
      }
    }
  }

  function useSkill() {
    if(!pSelf || !isRunning) return;
    
    let now = Date.now();
    let skillCooldown = 10000;
    if (pSelf.data.weapon === 'bow') {
      skillCooldown = 200;
    }

    if (now - (pSelf.lastSkillTime || 0) < skillCooldown) return;
    pSelf.lastSkillTime = now;

    executeWeaponSkill(pSelf);

    if(gameMode === 'online' && conn && conn.open && subGameMode === 'classic') {
      if(['staff', 'bow', 'laser'].includes(pSelf.data.weapon)) {
        conn.send({ type: 'SHOOT', weapon: pSelf.data.weapon });
      } else {
        conn.send({ type: 'SKILL' });
      }
    }
  }

  function addParticles(x, y, color, count) {
    for(let i=0; i<count; i++) {
      particles.push({ x: x, y: y, vx: (Math.random()-0.5)*9, vy: (Math.random()-0.5)*9, life: 22, color: color });
    }
  }

  function drawStickMan(ctx, p) {
    ctx.save();
    ctx.translate(p.x, p.y);
    ctx.scale(p.facing * p.scale, p.scale);

    let color = p.data.color || '#66fcf1';
    ctx.strokeStyle = color;
    ctx.fillStyle = color;
    ctx.lineWidth = 3;
    ctx.lineCap = 'round';

    // Head
    ctx.beginPath();
    ctx.arc(0, -42, 10, 0, Math.PI * 2);
    ctx.stroke();

    // Hat
    if (p.data.hat === 'knight') {
      ctx.fillStyle = '#a4b0be';
      ctx.fillRect(-12, -56, 24, 6);
      ctx.fillRect(-8, -64, 16, 8);
    } else if (p.data.hat === 'wizard') {
      ctx.fillStyle = '#7158e2';
      ctx.beginPath();
      ctx.moveTo(0, -72); ctx.lineTo(-14, -52); ctx.lineTo(14, -52); ctx.closePath();
      ctx.fill();
    }

    // Cape
    if (p.data.cape && p.data.cape !== 'none') {
      ctx.fillStyle = (p.data.cape === 'red') ? '#ff4757' : '#2f3640';
      ctx.beginPath();
      ctx.moveTo(-4, -34);
      ctx.lineTo(-18, -5);
      ctx.lineTo(-8, -2);
      ctx.closePath();
      ctx.fill();
    }

    // Body
    ctx.beginPath();
    ctx.moveTo(0, -32);
    ctx.lineTo(0, -12);
    ctx.stroke();

    let legOffset = Math.sin(p.walkTimer) * 10;
    
    // Legs
    ctx.beginPath();
    ctx.moveTo(0, -12);
    ctx.lineTo(-8 + legOffset, 0);
    ctx.moveTo(0, -12);
    ctx.lineTo(8 - legOffset, 0);
    ctx.stroke();

    // Arms
    let armAngle = p.atk ? -Math.PI / 3 : Math.sin(p.walkTimer) * 0.5;
    ctx.beginPath();
    ctx.moveTo(0, -26);
    ctx.lineTo(14 + Math.cos(armAngle)*10, -20 + Math.sin(armAngle)*10);
    ctx.stroke();

    ctx.restore();
  }

  function loop() {
    if (!isRunning) return;
    animFrame++;
    let ground = canvas.height - 25;

    // Player self movement
    pSelf.y += pSelf.vy; pSelf.vy += 0.58;
    if (pSelf.y >= ground) { pSelf.y = ground; pSelf.vy = 0; pSelf.isGrounded = true; }

    if (moveL) { pSelf.x -= 4.5; pSelf.facing = -1; pSelf.walkTimer += 0.25; }
    else if (moveR) { pSelf.x += 4.5; pSelf.facing = 1; pSelf.walkTimer += 0.25; }
    else { pSelf.walkTimer = 0; }
    
    pSelf.x = Math.max(20, Math.min(canvas.width - 20, pSelf.x));
    if (pSelf.windEffectTimer > 0) pSelf.windEffectTimer--;

    // LOGIC CHO CHẾ ĐỘ CHIẾN DỊCH (CAMPAIGN / ZOMBIE)
    if(subGameMode === 'campaign') {
      let allZombiesDead = true;

      for(let z of enemies) {
        if(z.hp <= 0) continue;
        allZombiesDead = false;

        z.y += z.vy; z.vy += 0.58;
        if (z.y >= ground) { z.y = ground; z.vy = 0; z.isGrounded = true; }
        
        // Zombie ưu tiên đuổi người chơi gần nhất (hoặc pSelf nếu chơi đơn / host-client)
        z.facing = pSelf.x < z.x ? -1 : 1;
        let speed = 2.3 + (currentStage * 0.18);
        if(z.isBoss) speed = 3.2;

        if (!z.isSpecialAction && Math.abs(pSelf.x - z.x) > 40 * z.scale) {
          z.x += (pSelf.x < z.x) ? -speed : speed;
          z.walkTimer += 0.3;
        }
        if (z.windEffectTimer > 0) z.windEffectTimer--;

        let now = Date.now();
        let zombieCooldown = (z.data.weapon === 'dagger') ? 100 : 150;
        let canZAtk = (now - (z.lastAtkTime || 0) > zombieCooldown);

        if (Math.random() < 0.015 && z.isGrounded) z.vy = -13;
        
        if (Math.random() < (0.045 + currentStage * 0.005) && canZAtk) { 
          z.lastAtkTime = now;
          z.atk = true; 
          setTimeout(() => z.atk = false, 100); 
          if(['staff', 'bow', 'laser'].includes(z.data.weapon)) {
            createBullet(z, pSelf, z.data.weapon); 
          } else if(Math.abs(pSelf.x - z.x) < 70 * z.scale) {
            let meleeDmg = 16 + (currentStage * 2.5);
            pSelf.hp = Math.max(0, pSelf.hp - meleeDmg);
            addParticles(pSelf.x, pSelf.y - 20, '#ff4757', 10);
          }
        }

        let zSkillCooldown = (z.data.weapon === 'bow') ? 200 : 10000;
        if (now - (z.lastSkillTime || 0) > zSkillCooldown) {
          z.lastSkillTime = now;
          executeWeaponSkill(z);
        }
      }

      if(allZombiesDead) {
        triggerEndGame(true);
        return;
      }

    } else {
      // Logic Chế độ cổ điển (PVP / 1v1)
      if(gameMode === 'story' || (gameMode === 'online' && isHost)) {
        pEnemy.y += pEnemy.vy; pEnemy.vy += 0.58;
        if (pEnemy.y >= ground) { pEnemy.y = ground; pEnemy.vy = 0; pEnemy.isGrounded = true; }
        
        if(gameMode === 'story') {
          pEnemy.facing = pSelf.x < pEnemy.x ? -1 : 1;
          if (Math.abs(pSelf.x - pEnemy.x) > 40) {
            pEnemy.x += (pSelf.x < pEnemy.x) ? -2.5 : 2.5;
            pEnemy.walkTimer += 0.3;
          }
          if(Math.abs(pSelf.x - pEnemy.x) < 60 && Math.random() < 0.05) {
            pEnemy.atk = true;
            pSelf.hp = Math.max(0, pSelf.hp - 12);
            setTimeout(() => pEnemy.atk = false, 100);
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
    }

    // Bullets update
    for(let i = bullets.length - 1; i >= 0; i--) {
      let b = bullets[i];
      b.x += b.vx;

      if(subGameMode === 'campaign') {
        let hitTarget = null;
        if(b.shooter === pSelf) {
          for(let z of enemies) {
            if(z.hp > 0 && Math.abs(b.x - z.x) < 25 * z.scale && Math.abs(b.y - (z.y - 25)) < 30 * z.scale) {
              hitTarget = z; break;
            }
          }
        } else {
          if(Math.abs(b.x - pSelf.x) < 25 && Math.abs(b.y - (pSelf.y - 25)) < 30) {
            hitTarget = pSelf;
          }
        }
        if(hitTarget) {
          hitTarget.hp = Math.max(0, hitTarget.hp - b.dmg);
          addParticles(b.x, b.y, b.color, 8);
          bullets.splice(i, 1);
          continue;
        }
      } else {
        let target = (b.shooter === pSelf) ? pEnemy : pSelf;
        if(Math.abs(b.x - target.x) < 25 * target.scale && Math.abs(b.y - (target.y - 25)) < 30 * target.scale) {
          target.hp = Math.max(0, target.hp - b.dmg);
          addParticles(b.x, b.y, b.color, 8);
          bullets.splice(i, 1);
          continue;
        }
      }

      if(b.x < 0 || b.x > canvas.width) {
        bullets.splice(i, 1);
      }
    }

    // Check Win/Loss
    if(pSelf.hp <= 0) {
      triggerEndGame(false);
      return;
    } else if(subGameMode === 'classic') {
      if(pEnemy.hp <= 0) {
        triggerEndGame(true);
        return;
      }
    }

    ctx.clearRect(0, 0, canvas.width, canvas.height);
    
    // Background Grid
    ctx.strokeStyle = "rgba(102, 252, 241, 0.07)";
    ctx.lineWidth = 1;
    for(let i=0; i<canvas.width; i+=40) {
      ctx.beginPath(); ctx.moveTo(i, 0); ctx.lineTo(i, canvas.height); ctx.stroke();
    }

    // Ground platform
    ctx.fillStyle = "#1f2833"; ctx.fillRect(0, ground + 20, canvas.width, 12);
    ctx.fillStyle = "#66fcf1"; 
    ctx.shadowColor = "#66fcf1"; ctx.shadowBlur = 10;
    ctx.fillRect(0, ground + 18, canvas.width, 3);
    ctx.shadowBlur = 0;

    // UI Health Bars
    let w = canvas.width * 0.35;
    ctx.fillStyle = "rgba(31, 40, 51, 0.8)"; ctx.fillRect(12, 12, w, 16); 
    ctx.fillStyle = pSelf.data.color; 
    ctx.shadowColor = pSelf.data.color; ctx.shadowBlur = 8;
    ctx.fillRect(12, 12, w * (Math.max(0, pSelf.hp) / pSelf.maxHp), 16);
    ctx.shadowBlur = 0;
    ctx.strokeStyle = "#fff"; ctx.lineWidth = 1.5; ctx.strokeRect(12, 12, w, 16);

    // Enemy / Boss Health Bar hoặc danh sách zombie
    if(subGameMode === 'classic') {
      ctx.fillStyle = "rgba(31, 40, 51, 0.8)"; ctx.fillRect(canvas.width - w - 12, 12, w, 16);
      ctx.fillStyle = pEnemy.data.color;
      ctx.shadowColor = pEnemy.data.color; ctx.shadowBlur = 8;
      ctx.fillRect(canvas.width - w - 12, 12, w * (Math.max(0, pEnemy.hp) / pEnemy.maxHp), 16);
      ctx.shadowBlur = 0;
      ctx.strokeStyle = "#fff"; ctx.lineWidth = 1.5; ctx.strokeRect(canvas.width - w - 12, 12, w, 16);
    } else {
      // Hiển thị thông tin màn chơi chiến dịch zombie
      ctx.fillStyle = "#f7b731";
      ctx.font = "bold 14px Segoe UI";
      ctx.fillText("MÀN: " + currentStage + (isBossStage ? " (BOSS)" : ""), canvas.width - 150, 24);
    }

    // Draw characters
    drawStickMan(ctx, pSelf);
    
    if(subGameMode === 'classic') {
      drawStickMan(ctx, pEnemy);
    } else {
      for(let z of enemies) {
        if(z.hp > 0) drawStickMan(ctx, z);
      }
    }

    // Draw Bullets
    for(let b of bullets) {
      ctx.save();
      ctx.fillStyle = b.color;
      ctx.shadowColor = b.color; ctx.shadowBlur = 8;
      ctx.beginPath();
      ctx.arc(b.x, b.y, b.radius, 0, Math.PI * 2);
      ctx.fill();
      ctx.restore();
    }

    // Draw Particles
    for(let i = particles.length - 1; i >= 0; i--) {
      let pt = particles[i];
      pt.x += pt.vx; pt.y += pt.vy; pt.life--;
      ctx.fillStyle = pt.color;
      ctx.fillRect(pt.x, pt.y, 3, 3);
      if(pt.life <= 0) particles.splice(i, 1);
    }

    requestAnimationFrame(loop);
  }

  // Keyboard and Touch Control Event Listeners
  window.addEventListener('keydown', (e) => {
    if(e.key === 'a' || e.key === 'ArrowLeft') moveL = true;
    if(e.key === 'd' || e.key === 'ArrowRight') moveR = true;
    if(e.key === 'w' || e.key === 'ArrowUp') jump();
    if(e.key === ' ' || e.key === 'j') attack();
    if(e.key === 'k' || e.key === 'Shift') useSkill();
  });

  window.addEventListener('keyup', (e) => {
    if(e.key === 'a' || e.key === 'ArrowLeft') moveL = false;
    if(e.key === 'd' || e.key === 'ArrowRight') moveR = false;
  });

  function bindTouch(id, startFn, endFn) {
    let el = document.getElementById(id);
    if(!el) return;
    el.addEventListener('touchstart', (e) => { e.preventDefault(); if(startFn) startFn(); });
    el.addEventListener('touchend', (e) => { e.preventDefault(); if(endFn) endFn(); });
    el.addEventListener('mousedown', (e) => { e.preventDefault(); if(startFn) startFn(); });
    el.addEventListener('mouseup', (e) => { e.preventDefault(); if(endFn) endFn(); });
  }

  bindTouch('btnLeft', () => moveL = true, () => moveL = false);
  bindTouch('btnRight', () => moveR = true, () => moveR = false);
  bindTouch('btnJump', jump, null);
  bindTouch('btnAtk', attack, null);
  bindTouch('btnSkill', useSkill, null);
</script>
</body>
</html>
"""

components.html(game_code, height=650, scrolling=False)
