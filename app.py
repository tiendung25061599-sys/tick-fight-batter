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
    
    .btn { padding: 14px 30px; font-size: 16px; font-weight: bold; background: rgba(31, 40, 51, 0.9); border: 2px solid #66fcf1; border-radius: 12px; color: #66fcf1; cursor: pointer; text-align: center; z-index: 110; min-width: 280px; box-shadow: 0 0 15px rgba(102, 252, 241, 0.25); backdrop-filter: blur(5px); transition: all 0.2s; }
    .btn:active { background: #66fcf1; color: #000; transform: scale(0.95); box-shadow: 0 0 25px #66fcf1; }
    
    input, select { padding: 12px 16px; font-size: 15px; border-radius: 10px; border: 2px solid #45a29e; background: rgba(11, 12, 16, 0.9); color: white; text-align: center; width: 280px; outline: none; box-shadow: inset 0 0 10px rgba(0,0,0,0.5); }
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
    <div class="btn" id="btnSinglePlayer">👤 CHƠI ĐƠN (SINGLEPLAYER)</div>
    <div class="btn" style="border-color:#ff4757; color:#ff4757;" id="btnMulti">🌐 MULTIPLAYER (ONLINE)</div>
    <div class="btn" style="border-color:#f7b731; color:#f7b731;" id="btnSettings">⚙️ CÀI ĐẶT</div>
  </div>

  <!-- GAME MODE SELECTOR MENU (Dùng chung cho cả Single & Multiplayer) -->
  <div id="modeSelectScreen" class="screen" style="display:none;">
    <h1 id="modeSelectTitle">CHỌN CHẾ ĐỘ CHƠI</h1>
    <div class="btn" id="btnModeClassic" style="border-color:#2ed573; color:#2ed573;">🛡️ 1. CHẾ ĐỘ CỔ ĐIỂN (CLASSIC)</div>
    <div class="btn" id="btnModeCampaign" style="border-color:#ffa502; color:#ffa502;">🧟 2. CHẾ ĐỘ CHIẾN DỊCH (CAMPAIGN)</div>
    <div class="btn" style="border-color:#ff4757; color:#ff4757; margin-top: 15px;" id="btnBackFromMode">⬅ QUAY LẠI</div>
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
    <h1>MULTIPLAYER ONLINE</h1>
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
      <select id="weaponSelect" onchange="updateSkillIcon()">
        <option value="sword">⚔️ Kiếm Thần (Skill: Hút Gió & Hồi Máu 10s)</option>
        <option value="axe">🪓 Rìu Chiến (Skill: Bay Nhảy Đập 10s)</option>
        <option value="dagger">🗡️ Dao Độc (Skill: Mưa Dao Găm 10s)</option>
        <option value="spear">🔱 Giáo Dài (Skill: Lướt Đâm Xuyên 10s)</option>
        <option value="staff">🪄 Trượng Ma Thuật (Skill: Bắn Cầu Lửa 10s)</option>
        <option value="bow">🏹 Cung Thần (Skill: Bắn Mũi Tên Đôi 0.2s)</option>
        <option value="laser">⚡ Súng Laser (Skill: Tia Xuyên Phá 10s)</option>
        <option value="muscle">💪 Cơ Bắp Thần Thánh (Skill: Bay Lên Quay Lửa 10s)</option>
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
    <div class="btn" id="btnStartGame" style="background: linear-gradient(135deg, #2ed573 0%, #10ac84 100%); border-color:#fff; color:#fff;">BẮT ĐẦU VÀO TRẬN ➔</div>
    <div class="btn" style="border-color:#ff4757; color:#ff4757;" id="btnBackFromCustom">⬅ QUAY LẠI</div>
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
  let isHost = false, gameMode = 'single', playSubType = 'classic';
  let roomCode = "";
  let currentStage = 1;

  let myData = { color: "#66fcf1", weapon: "sword", hat: "knight", cape: "red" };
  let enemyData = { color: "#ff4757", weapon: "staff", hat: "wizard", cape: "black" };

  let myVoteRematch = false, enemyVoteRematch = false;
  let enemies = []; // Danh sách các zombie/kẻ địch trong màn chơi

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
      else if(btnFS) btnFS.innerText = "📉 THOÁT FULLSCREEN";
    } else {
      if (document.exitFullscreen) { document.exitFullscreen(); }
      else if(btnFS) btnFS.innerText = "📺 BẬT FULLSCREEN";
    }
  }

  function showScreen(id) {
    document.querySelectorAll('.screen').forEach(s => s.style.display = 'none');
    document.getElementById(id).style.display = 'flex';
    
    const topBtn = document.getElementById('topRightBackBtn');
    if (['mainMenu', 'modeSelectScreen', 'settingsScreen', 'lobbyMenu', 'createRoomScreen', 'joinRoomScreen', 'customScreen'].includes(id)) {
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

  // Điều hướng từ menu chính
  addClickEvent('btnSinglePlayer', () => { 
    gameMode = 'single'; 
    document.getElementById('modeSelectTitle').innerText = "CHỌN CHẾ ĐỘ (SINGLEPLAYER)";
    showScreen('modeSelectScreen'); 
  });
  
  addClickEvent('btnMulti', () => { 
    gameMode = 'online'; 
    document.getElementById('modeSelectTitle').innerText = "CHỌN CHẾ ĐỘ (MULTIPLIER)";
    showScreen('modeSelectScreen'); 
  });

  // Chọn loại chế độ (Cổ điển hay Chiến dịch) cho cả Single và Multi
  addClickEvent('btnModeClassic', () => {
    playSubType = 'classic';
    currentStage = 1;
    if(gameMode === 'single') {
      document.getElementById('customTitle').innerText = "TRANG BỊ - CỔ ĐIỂN";
      showScreen('customScreen');
      updateSkillIcon();
    } else {
      showScreen('lobbyMenu');
    }
  });

  addClickEvent('btnModeCampaign', () => {
    playSubType = 'campaign';
    currentStage = 1;
    if(gameMode === 'single') {
      document.getElementById('customTitle').innerText = "CHIẾN DỊCH - MÀN " + currentStage;
      showScreen('customScreen');
      updateSkillIcon();
    } else {
      showScreen('lobbyMenu');
    }
  });

  addClickEvent('btnBackFromMode', () => showScreen('mainMenu'));
  addClickEvent('btnSettings', () => showScreen('settingsScreen'));
  addClickEvent('btnBackToMenu', () => showScreen('mainMenu'));
  addClickEvent('btnBackFromLobby', () => showScreen('modeSelectScreen'));
  addClickEvent('btnCreateLobby', () => showScreen('createRoomScreen'));
  addClickEvent('btnJoinLobby', () => showScreen('joinRoomScreen'));
  addClickEvent('btnInitHost', initHostRoom);
  addClickEvent('btnJoinTarget', joinTargetRoom);
  addClickEvent('btnStartGame', confirmCustom);
  addClickEvent('rematchBtn', requestRematch);
  addClickEvent('btnBackFromCustom', () => {
    if(gameMode === 'single') showScreen('modeSelectScreen');
    else showScreen('lobbyMenu');
  });

  function initHostRoom() {
    let codeInput = document.getElementById("customRoomCode").value.trim();
    if(!codeInput) { alert("Vui lòng nhập Mã Phòng!"); return; }
    roomCode = codeInput;
    
    document.getElementById("createStatusText").innerText = "Đang khởi tạo...";
    if(peer) { try { peer.destroy(); } catch(e){} }
    
    peer = new Peer(roomCode);
    peer.on('open', (id) => {
      document.getElementById("statusText").innerText = "Mã phòng: " + roomCode + " (Chờ đối thủ...)";
      document.getElementById('customTitle').innerText = playSubType === 'campaign' ? "MULTIPLIER CAMPAIGN - PHÒNG" : "MULTIPLIER CLASSIC - PHÒNG";
      showScreen('customScreen');
      updateSkillIcon();
    });
    peer.on('connection', (c) => { conn = c; setupConnection(); });
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
      document.getElementById('customTitle').innerText = playSubType === 'campaign' ? "MULTIPLIER CAMPAIGN" : "MULTIPLIER CLASSIC";
      showScreen('customScreen');
      updateSkillIcon();
      conn.send({ type: 'INIT_PLAYER', data: myData, subType: playSubType });
    });
    conn.on('data', (data) => handleNetworkData(data));
    conn.on('close', () => {
      if (isRunning) { alert("Đối thủ đã thoát trận đấu!"); quitGame(); }
    });
  }

  function confirmCustom() {
    myData.color = document.getElementById("skinColor").value;
    myData.weapon = document.getElementById("weaponSelect").value;
    myData.hat = document.getElementById("hatSelect").value;
    myData.cape = document.getElementById("capeSelect").value;
    
    if(gameMode === 'online' && conn && conn.open) {
      conn.send({ type: 'INIT_PLAYER', data: myData, subType: playSubType });
    }
    startGame();
  }

  let isRunning = false;
  let pSelf;
  let bullets = [], particles = [];
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

    let startX = 80;
    pSelf = { x: startX, y: canvas.height - 25, vy: 0, isGrounded: true, hp: 450, maxHp: 450, atk: false, data: myData, facing: 1, walkTimer: 0, scale: 1.0, isSpecialAction: false, lastAtkTime: 0, lastSkillTime: 0, windEffectTimer: 0 };
    
    enemies = [];
    isBossStage = (playSubType === 'campaign' && currentStage % 10 === 0);

    if(gameMode === 'single') {
      if(playSubType === 'classic') {
        // Chế độ cổ điển chỉ có 1 đối thủ thông thường
        enemies.push(createEnemyObject(canvas.width - 80, 450, 1.0, "#ff4757", "sword", false));
      } else {
        // Chế độ chiến dịch: Mỗi màn tăng thêm 1 zombie (trừ màn boss có 1 Boss khổng lồ)
        if(isBossStage) {
          enemies.push(createEnemyObject(canvas.width - 80, 1800 + currentStage*120, 2.0, "#ff0055", "axe", true));
        } else {
          let zombieCount = currentStage; // Mỗi màn tăng thêm 1 zombie
          let wpList = ["sword", "axe", "dagger", "spear", "staff", "bow", "laser", "muscle"];
          for(let i=0; i<zombieCount; i++) {
            let ex = canvas.width - 80 - (i * 45);
            let eHp = 400 + (currentStage * 40);
            let eWp = wpList[(currentStage + i) % wpList.length];
            enemies.push(createEnemyObject(ex, eHp, 1.0, "#ff4757", eWp, false));
          }
        }
      }
    } else {
      // Multiplayer online: 1 đối thủ là người chơi còn lại
      let enemyX = isHost ? canvas.width - 80 : 80;
      let eObj = createEnemyObject(enemyX, 450, 1.0, enemyData.color, enemyData.weapon, false);
      eObj.data = enemyData;
      enemies.push(eObj);
    }
    
    bullets = []; particles = [];
    myVoteRematch = false; enemyVoteRematch = false;
    document.getElementById("rematchBtn").style.opacity = "1";
    document.getElementById("rematchBtn").innerText = (playSubType === 'campaign') ? "⏭️ MÀN TIẾP THEO" : "🔄 CHƠI TIẾP";
    document.getElementById("voteStatusText").innerText = "";

    isRunning = true;
    requestAnimationFrame(loop);
  }

  function createEnemyObject(x, hp, scale, color, weapon, isBoss) {
    return {
      x: x, y: canvas.height - 25, vy: 0, isGrounded: true, 
      hp: hp, maxHp: hp, atk: false, 
      data: { color: color, weapon: weapon, hat: isBoss ? "knight" : "none", cape: isBoss ? "black" : "none" }, 
      facing: -1, walkTimer: 0, scale: scale, isSpecialAction: false, lastAtkTime: 0, lastSkillTime: 0, windEffectTimer: 0, isBoss: isBoss
    };
  }

  function handleNetworkData(data) {
    if(!data) return;
    if(data.type === 'INIT_PLAYER') {
      if(data.data) { enemyData = data.data; if(enemies[0]) enemies[0].data = enemyData; }
      if(data.subType) playSubType = data.subType;
    } else if(data.type === 'SYNC_POS') {
      if(enemies[0]) {
        if(typeof data.hp === 'number' && data.hp > 0) enemies[0].hp = data.hp;
        enemies[0].x = data.x; enemies[0].y = data.y; enemies[0].atk = data.atk; 
        enemies[0].facing = data.facing; enemies[0].walkTimer = data.walkTimer;
      }
    } else if(data.type === 'SKILL') {
      if(enemies[0]) executeWeaponSkill(enemies[0]);
    } else if(data.type === 'SHOOT') {
      if(enemies[0]) createBullet(enemies[0], pSelf, data.weapon);
    } else if(data.type === 'VOTE_REMATCH') {
      enemyVoteRematch = true;
      checkBothVoted();
    }
  }

  function triggerEndGame(won) {
    isRunning = false;
    let overlay = document.getElementById("endGameOverlay");
    let winTxt = document.getElementById("winnerText");

    if(playSubType === 'campaign') {
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
    if(gameMode === 'single') {
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
    if(gameMode === 'online' && myVoteRematch && enemyVoteRematch) startGame();
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
    let reach = 45, dmg = 15;
    if(pSelf.data.weapon === 'sword') { reach = 65; dmg = 18; }
    else if(pSelf.data.weapon === 'axe') { reach = 75; dmg = 28; }
    else if(pSelf.data.weapon === 'dagger') { reach = 42; dmg = 11; }
    else if(pSelf.data.weapon === 'spear') { reach = 85; dmg = 22; }
    else if(pSelf.data.weapon === 'muscle') { reach = 85; dmg = 32; }

    enemies.forEach(en => {
      if(en.hp > 0 && Math.abs(pSelf.x - en.x) < reach * pSelf.scale) {
        en.hp = Math.max(0, en.hp - dmg);
        addParticles(en.x, en.y - 20 * en.scale, pSelf.data.color, 12);
      }
    });
    setTimeout(() => pSelf.atk = false, 120);
  }

  function createBullet(caster, target, weapon) {
    let dir = caster.facing;
    let startX = caster.x + dir * 20 * caster.scale;
    let startY = caster.y - 24 * caster.scale;
    let dmgBonus = (gameMode === 'single' && playSubType === 'campaign') ? (10 + currentStage * 2) : 0;

    if (weapon === 'staff') {
      bullets.push({ x: startX, y: startY, vx: dir * 9.5, color: '#fffa65', radius: 9, dmg: 22 + dmgBonus, type: 'orb', shooter: caster });
    } else if (weapon === 'bow') {
      bullets.push({ x: startX, y: startY, vx: dir * 14, color: '#c7ecee', radius: 3.5, dmg: 10 + dmgBonus, type: 'arrow', shooter: caster });
    } else if (weapon === 'laser') {
      bullets.push({ x: startX, y: startY, vx: dir * 20, color: '#66fcf1', radius: 2.5, dmg: 20 + dmgBonus, type: 'laser', shooter: caster });
    }
  }

  function executeWeaponSkill(p) {
    let wp = p.data.weapon;
    let target = (p === pSelf) ? enemies[0] : pSelf;

    if (wp === 'sword') {
      p.isSpecialAction = true;
      p.windEffectTimer = 35;
      addParticles(p.x, p.y - 20, '#2ed573', 25);
      let healTicks = 0;
      let healInterval = setInterval(() => {
        healTicks++;
        p.hp = Math.min(p.maxHp, p.hp + 30);
        if (healTicks >= 5) { clearInterval(healInterval); p.isSpecialAction = false; }
      }, 200);
    } else if (wp === 'axe') {
      p.isSpecialAction = true;
      p.vy = -14; p.isGrounded = false;
      setTimeout(() => {
        p.vy = 18;
        let checkSlam = setInterval(() => {
          if(p.y >= canvas.height - 25) {
            p.y = canvas.height - 25; p.vy = 0; p.isSpecialAction = false;
            clearInterval(checkSlam);
            addParticles(p.x, p.y, '#ff4757', 30);
            if(target && Math.abs(p.x - target.x) < 110) target.hp = Math.max(0, target.hp - 60);
          }
        }, 20);
      }, 280);
    } else if (['staff', 'bow', 'laser'].includes(wp)) {
      createBullet(p, target, wp);
    }
  }

  function useSkill() {
    if(!pSelf || !isRunning) return;
    let now = Date.now();
    if (now - (pSelf.lastSkillTime || 0) < 10000) return;
    pSelf.lastSkillTime = now;
    executeWeaponSkill(pSelf);

    if(gameMode === 'online' && conn && conn.open) {
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

  function loop() {
    if (!isRunning) return;
    animFrame++;
    let ground = canvas.height - 25;

    pSelf.y += pSelf.vy; pSelf.vy += 0.58;
    if (pSelf.y >= ground) { pSelf.y = ground; pSelf.vy = 0; pSelf.isGrounded = true; }

    if (moveL) { pSelf.x -= 4.5; pSelf.facing = -1; pSelf.walkTimer += 0.25; }
    else if (moveR) { pSelf.x += 4.5; pSelf.facing = 1; pSelf.walkTimer += 0.25; }
    else { pSelf.walkTimer = 0; }
    pSelf.x = Math.max(20, Math.min(canvas.width - 20, pSelf.x));
    if (pSelf.windEffectTimer > 0) pSelf.windEffectTimer--;

    // Xử lý AI của các zombie / kẻ địch trong chế độ chiến dịch đơn
    if(gameMode === 'single') {
      enemies.forEach(en => {
        if(en.hp <= 0) return;
        en.y += en.vy; en.vy += 0.58;
        if (en.y >= ground) { en.y = ground; en.vy = 0; en.isGrounded = true; }
        
        en.facing = pSelf.x < en.x ? -1 : 1;
        let speed = 2.0 + (currentStage * 0.1);
        if (Math.abs(pSelf.x - en.x) > 40 * en.scale) {
          en.x += (pSelf.x < en.x) ? -speed : speed;
          en.walkTimer += 0.3;
        }

        let now = Date.now();
        if (Math.random() < 0.03 && (now - (en.lastAtkTime || 0) > 150)) {
          en.lastAtkTime = now;
          en.atk = true;
          setTimeout(() => en.atk = false, 100);
          if(Math.abs(pSelf.x - en.x) < 70 * en.scale) {
            pSelf.hp = Math.max(0, pSelf.hp - (12 + currentStage));
            addParticles(pSelf.x, pSelf.y - 20, '#ff4757', 8);
          }
        }
      });
    }

    if(gameMode === 'online' && conn && conn.open) {
      conn.send({ type: 'SYNC_POS', x: pSelf.x, y: pSelf.y, hp: pSelf.hp, atk: pSelf.atk, facing: pSelf.facing, walkTimer: pSelf.walkTimer });
    }

    ctx.clearRect(0, 0, canvas.width, canvas.height);
    
    // Vẽ sàn & background
    ctx.fillStyle = "#1f2833"; ctx.fillRect(0, ground + 20, canvas.width, 12);
    ctx.fillStyle = "#66fcf1"; ctx.fillRect(0, ground + 18, canvas.width, 3);

    // Thanh HP người chơi
    let w = canvas.width * 0.35;
    ctx.fillStyle = "rgba(31, 40, 51, 0.8)"; ctx.fillRect(12, 12, w, 16); 
    ctx.fillStyle = pSelf.data.color; 
    ctx.fillRect(12, 12, w * (Math.max(0, pSelf.hp) / pSelf.maxHp), 16);
    ctx.strokeStyle = "#fff"; ctx.strokeRect(12, 12, w, 16);

    // Thanh HP Địch / Boss
    if(enemies.length > 0) {
      let activeEn = enemies[0];
      ctx.fillStyle = "rgba(31, 40, 51, 0.8)"; ctx.fillRect(canvas.width - 12 - w, 12, w, 16);
      ctx.fillStyle = activeEn.data.color; 
      ctx.fillRect(canvas.width - 12 - w, 12, w * (Math.max(0, activeEn.hp) / activeEn.maxHp), 16);
      ctx.strokeStyle = "#fff"; ctx.strokeRect(canvas.width - 12 - w, 12, w, 16);
    }

    particles.forEach((p, i) => {
      p.x += p.vx; p.y += p.vy; p.life--;
      ctx.fillStyle = p.color; ctx.fillRect(p.x, p.y, 3.5, 3.5);
      if(p.life <= 0) particles.splice(i, 1);
    });

    bullets.forEach((b, idx) => {
      b.x += b.vx;
      ctx.fillStyle = b.color;
      ctx.beginPath(); ctx.arc(b.x, b.y, b.radius, 0, Math.PI * 2); ctx.fill();
      
      enemies.forEach(en => {
        if(en.hp > 0 && Math.abs(b.x - en.x) < 24 && Math.abs(b.y - en.y) < 32) {
          en.hp = Math.max(0, en.hp - b.dmg);
          bullets.splice(idx, 1);
        }
      });
    });

    drawPlayer(pSelf);
    enemies.forEach(en => { if(en.hp > 0) drawPlayer(en); });

    // Kiểm tra điều kiện thắng thua
    let allEnemiesDead = enemies.every(en => en.hp <= 0);
    if (pSelf.hp <= 0 || allEnemiesDead) {
      triggerEndGame(pSelf.hp > 0);
      return;
    }

    requestAnimationFrame(loop);
  }

  function drawPlayer(p) {
    let f = p.facing, x = p.x, y = p.y, s = p.scale;
    let legSwing = Math.sin(p.walkTimer * 5.5) * 12;

    ctx.save();
    ctx.strokeStyle = p.data.color; ctx.lineWidth = 3.5 * s;
    ctx.lineCap = 'round'; ctx.lineJoin = 'round';
    
    ctx.beginPath(); ctx.arc(x, y - 36 * s, 9.5 * s, 0, Math.PI * 2); ctx.stroke();
    ctx.beginPath(); ctx.moveTo(x, y - 26 * s); ctx.lineTo(x, y - 8 * s); ctx.stroke();
    ctx.beginPath(); ctx.moveTo(x, y - 8 * s); ctx.lineTo(x - (9 + legSwing) * s, y + 21 * s); ctx.stroke();
    ctx.beginPath(); ctx.moveTo(x, y - 8 * s); ctx.lineTo(x + (9 + legSwing) * s, y + 21 * s); ctx.stroke();

    // Duỗi thẳng tay khi đánh
    let handDistance = p.atk ? 38 * s : 12 * s;
    let handX = x + f * handDistance;
    let handY = y - 18 * s;
    
    ctx.beginPath(); ctx.moveTo(x, y - 22 * s); ctx.lineTo(handX, handY); ctx.stroke();
    
    ctx.save(); ctx.translate(handX, handY);
    ctx.strokeStyle = '#fff'; ctx.lineWidth = 3.5 * s;
    ctx.beginPath(); ctx.moveTo(0, 0); ctx.lineTo(f * 25 * s, -18 * s); ctx.stroke();
    ctx.restore();
    ctx.restore();
  }

  window.addEventListener('keydown', (e) => {
    let k = e.key.toLowerCase();
    if (k === 'a' || k === 'arrowleft') moveL = true;
    if (k === 'd' || k === 'arrowright') moveR = true;
    if (k === 'w' || k === ' ' || k === 'arrowup') jump();
  });

  window.addEventListener('keyup', (e) => {
    let k = e.key.toLowerCase();
    if (k === 'a' || k === 'arrowleft') moveL = false;
    if (k === 'd' || k === 'arrowright') moveR = false;
  });

  window.addEventListener('mousedown', (e) => {
    if(e.button === 0) attack();
    if(e.button === 2) useSkill();
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
