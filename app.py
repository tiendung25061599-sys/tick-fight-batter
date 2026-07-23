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

    .screen { position: absolute; top:0; left:0; width: 100%; height: 100%; background: radial-gradient(circle at center, #1f2833 0%, #050508 100%); display: flex; flex-direction: column; align-items: center; justify-content: center; z-index: 100; gap: 16px; }
    h1 { font-size: 32px; color: #66fcf1; text-align: center; text-shadow: 0 0 20px rgba(102, 252, 241, 0.6); letter-spacing: 3px; font-weight: 900; }
    
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
    <div class="btn" style="border-color:#ff4757; color:#ff4757; margin-top: 15px;" id="btnBackToMenu">⬅ QUAY LẠI MENU</div>
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
      <select id="weaponSelect" onchange="updateSkillIcon()">
        <option value="sword">⚔️ Kiếm Thần (Skill: Hút Gió & Chém Liên Tục 0.2s)</option>
        <option value="axe">🪓 Rìu Chiến (Skill: Bay Nhảy Đập)</option>
        <option value="dagger">🗡️ Dao Độc (Skill: Mưa Dao Găm)</option>
        <option value="spear">🔱 Giáo Dài (Skill: Lướt Đâm Xuyên)</option>
        <option value="staff">🪄 Trượng Ma Thuật (Skill: Bắn Cầu Lửa 0.2s)</option>
        <option value="bow">🏹 Cung Thần (Skill: Bắn Mũi Tên Đôi 0.2s)</option>
        <option value="laser">⚡ Súng Laser (Skill: Tia Xuyên Phá 0.2s)</option>
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
      <div class="btn-ctrl" style="border-color:#ff4757" id="btnSkill">🌀<span class="key-hint" id="skillKeyHint">M2</span></div>
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
    updateSkillIcon();
  });
  addClickEvent('btnMulti', () => { gameMode = 'online'; showScreen('lobbyMenu'); updateSkillIcon(); });
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

    let enemyHp = 500;
    let enemyScale = 1.0;
    let enemyColor = "#ff4757";
    let enemyWeapon = "sword";

    if(gameMode === 'story') {
      if(isBossStage) {
        enemyHp = 1800 + (currentStage * 120);
        enemyScale = 2.0;
        enemyColor = "#ff0055";
        enemyWeapon = "axe";
      } else {
        enemyHp = 450 + (currentStage * 65);
        enemyScale = 1.0 + (currentStage * 0.03);
        let wpList = ["sword", "axe", "dagger", "spear", "staff", "bow", "laser"];
        enemyWeapon = wpList[currentStage % wpList.length];
      }
    }

    pSelf = { x: startX, y: canvas.height - 25, vy: 0, isGrounded: true, hp: 450, maxHp: 450, atk: false, data: myData, facing: 1, walkTimer: 0, scale: 1.0, isSpecialAction: false, lastAtkTime: 0, lastSkillTime: 0, windEffectTimer: 0 };
    
    pEnemy = { 
      x: enemyX, y: canvas.height - 25, vy: 0, isGrounded: true, 
      hp: enemyHp, maxHp: enemyHp, atk: false, 
      data: (gameMode === 'story') ? { color: enemyColor, weapon: enemyWeapon, hat: isBossStage ? "knight" : "none", cape: isBossStage ? "black" : "none" } : enemyData, 
      facing: -1, walkTimer: 0, scale: enemyScale, isSpecialAction: false, lastAtkTime: 0, lastSkillTime: 0, windEffectTimer: 0
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
    } else if(data.type === 'SKILL') {
      executeWeaponSkill(pEnemy);
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

    if(pSelf.data.weapon === 'sword') { reach = 60; dmg = 18; }
    else if(pSelf.data.weapon === 'axe') { reach = 70; dmg = 28; }
    else if(pSelf.data.weapon === 'dagger') { reach = 38; dmg = 11; }
    else if(pSelf.data.weapon === 'spear') { reach = 80; dmg = 22; }

    let other = pEnemy;
    if(Math.abs(pSelf.x - other.x) < reach * pSelf.scale) {
      other.hp = Math.max(0, other.hp - dmg);
      addParticles(other.x, other.y - 20 * other.scale, pSelf.data.color, 12);
    }
    setTimeout(() => pSelf.atk = false, 120);
  }

  function createBullet(caster, target, weapon) {
    let dir = caster.facing;
    let startX = caster.x + dir * 20 * caster.scale;
    let startY = caster.y - 24 * caster.scale;
    let dmgBonus = (caster === pEnemy && gameMode === 'story') ? (10 + currentStage * 2) : 0;

    if (weapon === 'staff') {
      bullets.push({ x: startX, y: startY, vx: dir * 9.5, color: '#fffa65', radius: 9, dmg: 22 + dmgBonus, type: 'orb', shooter: caster });
    } else if (weapon === 'bow') {
      bullets.push({ x: startX, y: startY, vx: dir * 14, color: '#c7ecee', radius: 3.5, dmg: 16 + dmgBonus, type: 'arrow', shooter: caster });
    } else if (weapon === 'laser') {
      bullets.push({ x: startX, y: startY, vx: dir * 20, color: '#66fcf1', radius: 2.5, dmg: 20 + dmgBonus, type: 'laser', shooter: caster });
    }
  }

  function executeWeaponSkill(p) {
    let other = (p === pSelf) ? pEnemy : pSelf;
    let wp = p.data.weapon;
    let isStoryEnemy = (p === pEnemy && gameMode === 'story');

    if (wp === 'sword') {
      p.isSpecialAction = true;
      p.windEffectTimer = 35; // Bật hiệu ứng gió xoáy xung quanh
      addParticles(p.x, p.y - 20, '#66fcf1', 25);

      // Giai đoạn 1: Hút kẻ địch lại gần và gây damage liên tục
      let pullTicks = 0;
      let pullInterval = setInterval(() => {
        pullTicks++;
        // Kéo địch về phía người dùng skill
        if (Math.abs(p.x - other.x) > 15) {
          other.x += (p.x > other.x) ? 6 : -6;
        }
        // Gây damage liên tục mỗi nhịp hút
        let dotDmg = isStoryEnemy ? (8 + currentStage) : 6;
        other.hp = Math.max(0, other.hp - dotDmg);
        addParticles(other.x, other.y - 20, '#66fcf1', 8);

        if (pullTicks >= 5) { // Sau khoảng 5 nhịp (tương đương ~0.4s)
          clearInterval(pullInterval);

          // Giai đoạn 2: Đẩy văng kẻ địch ra xa mạnh mẽ kèm sát thương cuối
          let pushDir = (other.x >= p.x) ? 1 : -1;
          other.x += pushDir * 90;
          other.x = Math.max(20, Math.min(canvas.width - 20, other.x));
          
          let finalDmg = isStoryEnemy ? (35 + currentStage * 4) : 25;
          other.hp = Math.max(0, other.hp - finalDmg);
          addParticles(other.x, other.y - 20, '#ff4757', 20);

          p.isSpecialAction = false;
        }
      }, 75);

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
            let slamDmg = isStoryEnemy ? (75 + currentStage * 8) : 60;
            if(Math.abs(p.x - other.x) < 110) {
              other.hp = Math.max(0, other.hp - slamDmg);
              addParticles(other.x, other.y - 20, '#ff4757', 24);
            }
          }
        }, 20);
      }, 280);

    } else if (wp === 'dagger') {
      p.isSpecialAction = true;
      addParticles(p.x, p.y - 20, '#2ed573', 15);
      let daggerDmg = isStoryEnemy ? (12 + currentStage * 2) : 10;
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
      let thrustDmg = isStoryEnemy ? (60 + currentStage * 6) : 50;
      if(Math.abs(p.x - other.x) < 100) {
        other.hp = Math.max(0, other.hp - thrustDmg);
        addParticles(other.x, other.y - 20, '#f1c40f', 26);
      }
      setTimeout(() => p.isSpecialAction = false, 250);

    } else if (['staff', 'bow', 'laser'].includes(wp)) {
      createBullet(p, other, wp);
      if(wp === 'bow') {
        setTimeout(() => createBullet(p, other, wp), 80);
      }
    }
  }

  function useSkill() {
    if(!pSelf || !isRunning) return;
    
    let now = Date.now();
    let skillCooldown = 2500;
    if (pSelf.data.weapon === 'sword') skillCooldown = 200; // Giảm hồi chiêu Kiếm xuống 0.2s
    else if (pSelf.data.weapon === 'axe') skillCooldown = 4500;
    else if (pSelf.data.weapon === 'spear') skillCooldown = 3000;
    else if (['staff', 'bow', 'laser'].includes(pSelf.data.weapon)) skillCooldown = 200; // Hồi chiêu 0.2s cho Trượng, Cung, Laser

    if (now - (pSelf.lastSkillTime || 0) < skillCooldown) return;
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

    if(gameMode === 'story') {
      pEnemy.y += pEnemy.vy; pEnemy.vy += 0.58;
      if (pEnemy.y >= ground) { pEnemy.y = ground; pEnemy.vy = 0; pEnemy.isGrounded = true; }
      
      pEnemy.facing = pSelf.x < pEnemy.x ? -1 : 1;
      let speed = 2.3 + (currentStage * 0.18);
      if(isBossStage) speed = 3.2;

      if (!pEnemy.isSpecialAction && Math.abs(pSelf.x - pEnemy.x) > 40 * pEnemy.scale) {
        pEnemy.x += (pSelf.x < pEnemy.x) ? -speed : speed;
        pEnemy.walkTimer += 0.3;
      }
      if (pEnemy.windEffectTimer > 0) pEnemy.windEffectTimer--;

      let now = Date.now();
      let enemyCooldown = (pEnemy.data.weapon === 'dagger') ? 100 : 150;
      let canEnemyAtk = (now - (pEnemy.lastAtkTime || 0) > enemyCooldown);

      let atkChance = 0.045 + (currentStage * 0.005);
      if (Math.random() < 0.015 && pEnemy.isGrounded) pEnemy.vy = -13;
      
      if (Math.random() < atkChance && canEnemyAtk) { 
        pEnemy.lastAtkTime = now;
        pEnemy.atk = true; 
        setTimeout(() => pEnemy.atk = false, 100); 
        if(['staff', 'bow', 'laser'].includes(pEnemy.data.weapon)) {
          createBullet(pEnemy, pSelf, pEnemy.data.weapon); 
        } else if(Math.abs(pSelf.x - pEnemy.x) < 70 * pEnemy.scale) {
          let meleeDmg = 16 + (currentStage * 2.5);
          pSelf.hp = Math.max(0, pSelf.hp - meleeDmg);
          addParticles(pSelf.x, pSelf.y - 20, '#ff4757', 10);
        }
      }

      let enemySkillCooldown = ['staff', 'bow', 'laser', 'sword'].includes(pEnemy.data.weapon) ? 200 : 2800;
      if (now - (pEnemy.lastSkillTime || 0) > enemySkillCooldown) {
        pEnemy.lastSkillTime = now;
        executeWeaponSkill(pEnemy);
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
    
    ctx.strokeStyle = "rgba(102, 252, 241, 0.07)";
    ctx.lineWidth = 1;
    for(let i=0; i<canvas.width; i+=40) {
      ctx.beginPath(); ctx.moveTo(i, 0); ctx.lineTo(i, canvas.height); ctx.stroke();
    }

    ctx.fillStyle = "#1f2833"; ctx.fillRect(0, ground + 20, canvas.width, 12);
    ctx.fillStyle = "#66fcf1"; 
    ctx.shadowColor = "#66fcf1"; ctx.shadowBlur = 10;
    ctx.fillRect(0, ground + 18, canvas.width, 3);
    ctx.shadowBlur = 0;

    let w = canvas.width * 0.35;
    ctx.fillStyle = "rgba(31, 40, 51, 0.8)"; ctx.fillRect(12, 12, w, 16); 
    ctx.fillStyle = pSelf.data.color; 
    ctx.shadowColor = pSelf.data.color; ctx.shadowBlur = 8;
    ctx.fillRect(12, 12, w * (Math.max(0, pSelf.hp) / pSelf.maxHp), 16);
    ctx.shadowBlur = 0;
    ctx.strokeStyle = "#fff"; ctx.lineWidth = 1.5; ctx.strokeRect(12, 12, w, 16);

    if(isBossStage) {
      let bossW = canvas.width * 0.6;
      let bossX = (canvas.width - bossW) / 2;
      ctx.fillStyle = "rgba(31, 40, 51, 0.8)"; ctx.fillRect(bossX, 35, bossW, 20);
      ctx.fillStyle = "#ff0055"; 
      ctx.shadowColor = "#ff0055"; ctx.shadowBlur = 12;
      ctx.fillRect(bossX, 35, bossW * (Math.max(0, pEnemy.hp) / pEnemy.maxHp), 20);
      ctx.shadowBlur = 0;
      ctx.strokeStyle = "#ff4757"; ctx.lineWidth = 2; ctx.strokeRect(bossX, 35, bossW, 20);
      ctx.fillStyle = "#fff"; ctx.font = "bold 13px sans-serif"; ctx.fillText("🔥 BOSS KHỔNG LỒ (MÀN " + currentStage + ") 🔥", canvas.width/2 - 95, 28);
    } else {
      ctx.fillStyle = "rgba(31, 40, 51, 0.8)"; ctx.fillRect(canvas.width - 12 - w, 12, w, 16);
      ctx.fillStyle = pEnemy.data.color; 
      ctx.shadowColor = pEnemy.data.color; ctx.shadowBlur = 8;
      ctx.fillRect(canvas.width - 12 - w, 12, w * (Math.max(0, pEnemy.hp) / pEnemy.maxHp), 16);
      ctx.shadowBlur = 0;
      ctx.strokeStyle = "#fff"; ctx.lineWidth = 1.5; ctx.strokeRect(canvas.width - 12 - w, 12, w, 16);
    }

    particles.forEach((p, i) => {
      p.x += p.vx; p.y += p.vy; p.life--;
      ctx.fillStyle = p.color; 
      ctx.fillRect(p.x, p.y, 3.5, 3.5);
      if(p.life <= 0) particles.splice(i, 1);
    });

    bullets.forEach((b, idx) => {
      b.x += b.vx;
      ctx.fillStyle = b.color;
      ctx.shadowColor = b.color;
      ctx.shadowBlur = 15;

      if(b.type === 'laser') {
        ctx.fillRect(b.x, b.y - 3, 28 * Math.sign(b.vx), 6);
      } else {
        ctx.beginPath(); ctx.arc(b.x, b.y, b.radius, 0, Math.PI * 2); ctx.fill();
      }
      ctx.shadowBlur = 0;

      let target = (b.shooter === pEnemy) ? pSelf : pEnemy;
      if (Math.abs(b.x - target.x) < 24 * target.scale && Math.abs(b.y - (target.y - 20 * target.scale)) < 32 * target.scale) {
        target.hp = Math.max(0, target.hp - b.dmg);
        addParticles(b.x, b.y, b.color, 12);
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
    let legSwing = Math.sin(p.walkTimer * 5.5) * 12;

    ctx.save();
    ctx.shadowColor = p.data.color;
    ctx.shadowBlur = p.isSpecialAction ? 25 : 10;

    // Hiệu ứng vòng gió lốc xung quanh khi dùng skill Kiếm Thần
    if(p.windEffectTimer > 0) {
      ctx.strokeStyle = "rgba(102, 252, 241, 0.7)";
      ctx.lineWidth = 2.5;
      ctx.shadowColor = "#66fcf1";
      ctx.shadowBlur = 20;
      ctx.beginPath();
      let ringRadius = 45 + Math.sin(animFrame * 0.4) * 10;
      ctx.arc(x, y - 20, ringRadius, 0, Math.PI * 2);
      ctx.stroke();

      // Vẽ các vòng xoáy phụ
      ctx.beginPath();
      ctx.arc(x, y - 20, ringRadius * 0.6, -animFrame * 0.3, Math.PI - animFrame * 0.3);
      ctx.stroke();
    }

    if(p.isSpecialAction && p.data.weapon === 'axe') {
      ctx.translate(x, y - 20 * s);
      ctx.rotate(animFrame * 0.6); 
      ctx.translate(-x, -(y - 20 * s));
    }

    if(p.data.cape && p.data.cape !== 'none') {
      ctx.fillStyle = p.data.cape === 'red' ? '#ff3838' : '#1e272e';
      ctx.beginPath(); 
      ctx.moveTo(x - f * 4 * s, y - 26 * s); 
      ctx.lineTo(x - f * (20 + Math.sin(animFrame*0.25)*6) * s, y + 6 * s); 
      ctx.lineTo(x - f * 4 * s, y + 3 * s); 
      ctx.fill();
    }

    ctx.strokeStyle = p.data.color; ctx.lineWidth = 3.5 * s;
    ctx.lineCap = 'round'; ctx.lineJoin = 'round';
    
    ctx.beginPath(); ctx.arc(x, y - 36 * s, 9.5 * s, 0, Math.PI * 2); ctx.stroke();
    ctx.beginPath(); ctx.moveTo(x, y - 26 * s); ctx.lineTo(x, y - 8 * s); ctx.stroke();
    
    ctx.beginPath(); ctx.moveTo(x, y - 8 * s); ctx.lineTo(x - (9 + legSwing) * s, y + 21 * s); ctx.stroke();
    ctx.beginPath(); ctx.moveTo(x, y - 8 * s); ctx.lineTo(x + (9 + legSwing) * s, y + 21 * s); ctx.stroke();

    let handX = x + (p.atk ? f * 24 * s : f * 9 * s);
    let handY = y - (p.atk ? 25 * s : 16 * s);
    ctx.beginPath(); ctx.moveTo(x, y - 22 * s); ctx.lineTo(handX, handY); ctx.stroke();

    if(p.data.hat === 'knight') {
      ctx.fillStyle = '#d1d8e0'; ctx.fillRect(x - 11 * s, y - 50 * s, 22 * s, 9 * s);
      ctx.fillStyle = '#ff4757'; ctx.fillRect(x - 2 * s, y - 54 * s, 4 * s, 6 * s);
    } else if(p.data.hat === 'wizard') {
      ctx.fillStyle = '#8854d0'; ctx.beginPath(); ctx.moveTo(x - 13 * s, y - 43 * s); ctx.lineTo(x, y - 65 * s); ctx.lineTo(x + 13 * s, y - 43 * s); ctx.fill();
    }

    ctx.save(); ctx.translate(handX, handY);
    
    if(p.data.weapon === 'sword') {
      ctx.shadowColor = '#66fcf1'; ctx.shadowBlur = 12;
      ctx.strokeStyle = '#fff'; ctx.lineWidth = 3.5 * s; 
      ctx.beginPath(); ctx.moveTo(0, 0); ctx.lineTo(f * 30 * s, -22 * s); ctx.stroke();
      ctx.fillStyle = '#f1c40f'; ctx.fillRect(f * 2 * s, -3 * s, 6 * s, 3 * s);
      ctx.fillStyle = '#66fcf1'; ctx.fillRect(f * 12 * s, -10 * s, 4 * s, 4 * s);
      ctx.shadowBlur = 0;
      
    } else if(p.data.weapon === 'axe') {
      ctx.strokeStyle = '#576574'; ctx.lineWidth = 4.5 * s; 
      ctx.beginPath(); ctx.moveTo(0, 0); ctx.lineTo(f * 22 * s, -26 * s); ctx.stroke();
      ctx.fillStyle = '#ff4757'; ctx.shadowColor = '#ff4757'; ctx.shadowBlur = 12;
      ctx.beginPath(); 
      ctx.moveTo(f * 14 * s, -34 * s); ctx.lineTo(f * 26 * s, -28 * s); 
      ctx.lineTo(f * 22 * s, -18 * s); ctx.lineTo(f * 12 * s, -22 * s); ctx.fill();
      ctx.shadowBlur = 0;
      
    } else if(p.data.weapon === 'dagger') {
      ctx.shadowColor = '#2ed573'; ctx.shadowBlur = 10;
      ctx.strokeStyle = '#2ed573'; ctx.lineWidth = 3 * s; 
      ctx.beginPath(); ctx.moveTo(0, 0); ctx.lineTo(f * 18 * s, -14 * s); ctx.stroke();
      ctx.fillStyle = '#fff'; ctx.fillRect(f * 8 * s, -6 * s, 4 * s, 2 * s);
      ctx.shadowBlur = 0;
      
    } else if(p.data.weapon === 'spear') {
      ctx.strokeStyle = '#744210'; ctx.lineWidth = 4 * s; 
      ctx.beginPath(); ctx.moveTo(0, 0); ctx.lineTo(f * 70 * s, 0); ctx.stroke();
      ctx.fillStyle = '#f1c40f'; ctx.fillRect(f * 16 * s, -4 * s, 6 * s, 8 * s);
      ctx.fillStyle = '#ecf0f1'; ctx.shadowColor = '#3498db'; ctx.shadowBlur = 10;
      ctx.beginPath(); ctx.moveTo(f * 56 * s, -8 * s); ctx.lineTo(f * 80 * s, 0); ctx.lineTo(f * 56 * s, 8 * s); ctx.fill();
      ctx.fillStyle = '#e74c3c'; ctx.fillRect(f * 62 * s, -2 * s, 6 * s, 4 * s);
      ctx.shadowBlur = 0;
      
    } else if(p.data.weapon === 'staff') {
      ctx.strokeStyle = '#10ac84'; ctx.lineWidth = 4 * s; 
      ctx.beginPath(); ctx.moveTo(0, 6 * s); ctx.lineTo(f * 22 * s, -26 * s); ctx.stroke();
      ctx.fillStyle = '#fffa65'; ctx.shadowColor = '#fffa65'; ctx.shadowBlur = 18;
      ctx.beginPath(); ctx.arc(f * 22 * s, -26 * s, 8.5 * s, 0, Math.PI*2); ctx.fill();
      ctx.fillStyle = '#ff6b81'; ctx.beginPath(); ctx.arc(f * 22 * s, -26 * s, 3.5 * s, 0, Math.PI*2); ctx.fill();
      ctx.shadowBlur = 0;
      
    } else if(p.data.weapon === 'bow') {
      ctx.strokeStyle = '#f7b731'; ctx.lineWidth = 3 * s; 
      ctx.shadowColor = '#f7b731'; ctx.shadowBlur = 10;
      ctx.beginPath(); ctx.arc(f * 8 * s, -7 * s, 17 * s, -Math.PI/1.8, Math.PI/1.8); ctx.stroke();
      ctx.strokeStyle = '#66fcf1'; ctx.lineWidth = 1.5 * s;
      ctx.beginPath(); ctx.moveTo(f * 8 * s, -24 * s); ctx.lineTo(f * 8 * s, 10 * s); ctx.stroke();
      ctx.shadowBlur = 0;
      
    } else if(p.data.weapon === 'laser') {
      ctx.fillStyle = '#222f3e'; ctx.fillRect(0, -5 * s, f * 24 * s, 10 * s);
      ctx.fillStyle = '#66fcf1'; ctx.shadowColor = '#66fcf1'; ctx.shadowBlur = 15;
      ctx.fillRect(f * 6 * s, -2.5 * s, f * 18 * s, 5 * s);
      ctx.shadowBlur = 0;
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
