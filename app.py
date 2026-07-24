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

    .screen { position: absolute; top:0; left:0; width: 100%; height: 100%; background: radial-gradient(circle at center, #1f2833 0%, #050508 100%); display: flex; flex-direction: column; align-items: center; justify-content: center; z-index: 100; gap: 12px; }
    
    .title-container {
      display: flex; flex-direction: column; align-items: center; gap: 6px; margin-bottom: 5px;
    }
    
    h1 { font-size: 32px; color: #66fcf1; text-align: center; text-shadow: 0 0 20px rgba(102, 252, 241, 0.6); letter-spacing: 3px; font-weight: 900; }
    
    .author-name {
      font-size: 15px; color: #70a1ff; font-weight: 600; letter-spacing: 2px;
      text-shadow: 0 0 10px rgba(112, 161, 255, 0.5); text-transform: uppercase;
    }
    
    .btn { padding: 12px 26px; font-size: 15px; font-weight: bold; background: rgba(31, 40, 51, 0.9); border: 2px solid #66fcf1; border-radius: 12px; color: #66fcf1; cursor: pointer; text-align: center; z-index: 110; min-width: 260px; box-shadow: 0 0 15px rgba(102, 252, 241, 0.25); backdrop-filter: blur(5px); transition: all 0.2s; }
    .btn:active { background: #66fcf1; color: #000; transform: scale(0.95); box-shadow: 0 0 25px #66fcf1; }
    
    input, select { padding: 10px 14px; font-size: 14px; border-radius: 10px; border: 2px solid #45a29e; background: rgba(11, 12, 16, 0.9); color: white; text-align: center; width: 260px; outline: none; box-shadow: inset 0 0 10px rgba(0,0,0,0.5); }
    input:focus, select:focus { border-color: #66fcf1; box-shadow: 0 0 10px rgba(102, 252, 241, 0.3); }
    
    .select-box { display: flex; gap: 12px; align-items: center; background: rgba(31, 40, 51, 0.7); padding: 8px 16px; border-radius: 12px; width: 85%; max-width: 380px; justify-content: space-between; border: 1px solid rgba(69, 162, 158, 0.5); backdrop-filter: blur(5px); }
    #statusText { color: #f7b731; font-weight: bold; font-size: 14px; text-align: center; text-shadow: 0 0 10px rgba(247, 183, 49, 0.4); }
    
    #gameCanvas { background: radial-gradient(circle at center, #111318 0%, #030305 100%); border: 2px solid #45a29e; border-radius: 16px; width: 96vw; height: 75vh; display: none; position: relative; z-index: 1; box-shadow: 0 0 30px rgba(69, 162, 158, 0.4); }
    
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

    /* Roll Modal Styles */
    #rollModal {
      position: absolute; top: 0; left: 0; width: 100vw; height: 100vh;
      background: rgba(3, 3, 5, 0.92); backdrop-filter: blur(10px); display: none; flex-direction: column;
      align-items: center; justify-content: center; z-index: 300; gap: 20px;
    }
    .roll-box {
      width: 320px; height: 180px; background: rgba(31, 40, 51, 0.9); border: 3px solid #f7b731;
      border-radius: 20px; display: flex; flex-direction: column; align-items: center; justify-content: center;
      box-shadow: 0 0 30px rgba(247, 183, 49, 0.5); gap: 10px; position: relative; overflow: hidden;
    }
    .roll-result-title { font-size: 22px; font-weight: 900; color: #f7b731; text-shadow: 0 0 10px rgba(247,183,49,0.8); }
    .roll-result-desc { font-size: 16px; font-weight: bold; color: #fff; text-align: center; padding: 0 15px; }
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
    <div class="btn" id="btnStory">📖 STORY MODE (VƯỢT ẢI 10 MÀN)</div>
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

  <!-- CẤU HÌNH TRANG BỊ & ROLL NGUYÊN TỐ -->
  <div id="customScreen" class="screen" style="display:none;">
    <h1 id="customTitle">TRANG BỊ CHIẾN ĐẤU</h1>
    <div id="statusText">Sẵn sàng xuất chiến!</div>
    
    <div class="select-box" style="border-color: #f7b731; background: rgba(247, 183, 49, 0.1);">
      <span style="color: #f7b731; font-weight: bold;">Hiệu Ứng Nguyên Tố:</span>
      <span id="currentElementDisplay" style="color: #66fcf1; font-weight: bold;">Chưa có</span>
    </div>

    <div class="select-box" style="border-color: #f7b731; background: rgba(247, 183, 49, 0.1); cursor: pointer;" id="btnOpenRoll">
      <span style="color: #f7b731; font-weight: bold;">🎲 Roll Nguyên Tố:</span>
      <span id="rollTicketsDisplay" style="color: #f7b731; font-weight: bold;">(Lượt: 0)</span>
    </div>

    <div class="select-box">
      <span>Màu Skin:</span>
      <input type="color" id="skinColor" value="#66fcf1">
    </div>
    <div class="select-box">
      <span>Vũ Khí:</span>
      <select id="weaponSelect" onchange="updateSkillIcon()">
        <option value="sword">⚔️ Kiếm Thần (Skill: Lốc Xoáy Phi Thân)</option>
        <option value="axe">🪓 Rìu Chiến (Skill: Bay Xoay Tròn Đập Rìu)</option>
        <option value="dagger">🗡️ Dao Độc (Skill: Mưa Dao Găm)</option>
        <option value="spear">🔱 Giáo Dài (Skill: Lướt Đâm Xuyên Gây Sát Thương)</option>
        <option value="staff">🪄 Trượng Ma Thuật (Skill: Bắn Cầu Lửa)</option>
        <option value="bow">🏹 Cung Thần (Skill: Bắn Mũi Tên Đôi)</option>
        <option value="laser">⚡ Súng Laser (Skill: Tia Xuyên Phá)</option>
        <option value="muscle">💪 Cánh Tay Cơ Bắp (Skill: Bay Xoay Tròn Đập Sóng)</option>
        <option value="glove">🥊 Găng Tay Đấm Bốc (Skill: Nắm Đấm Sấm Sét Bay Tới)</option>
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

  <!-- ROLL MODAL OVERLAY -->
  <div id="rollModal">
    <h1 style="color: #f7b731; text-shadow: 0 0 20px rgba(247,183,49,0.8);">VÒNG QUAY NGUYÊN TỐ</h1>
    <div class="roll-box" id="rollBoxContainer">
      <div class="roll-result-title" id="rollTitle">SẴN SÀNG</div>
      <div class="roll-result-desc" id="rollDesc">Nhấn nút bên dưới để Roll ngẫu nhiên Độc, Lửa hoặc Băng!</div>
    </div>
    <div class="btn" id="btnDoRoll" style="border-color:#f7b731; color:#f7b731; background: rgba(31,40,51,0.9);">🎲 QUAY NGAY (1 Lượt)</div>
    <div class="btn" style="border-color:#ff4757; color:#ff4757;" id="btnCloseRoll">✔ XÁC NHẬN & QUAY LẠI</div>
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
      <div class="btn-ctrl" id="btnAtk">⚔️<span class="key-hint">J / M1</span></div>
      <div class="btn-ctrl" style="border-color:#ff4757" id="btnSkill">🌀<span class="key-hint" id="skillKeyHint">K / M2</span></div>
    </div>
  </div>

<script>
  const canvas = document.getElementById("gameCanvas");
  const ctx = canvas.getContext("2d");
  
  let peer = null, conn = null;
  let isHost = false, gameMode = 'story';
  let roomCode = "";
  let currentStage = 1;
  let rollTickets = 0;
  let currentElement = 'none'; // 'none', 'poison', 'fire', 'ice'

  let myData = { color: "#66fcf1", weapon: "sword", hat: "knight", cape: "red", element: "none" };
  let enemyData = { color: "#ff4757", weapon: "staff", hat: "wizard", cape: "black", element: "none" };

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
    else if(wp === 'muscle') skillBtn.innerText = "💪";
    else if(wp === 'glove') skillBtn.innerText = "🥊";
  }

  function updateRollUI() {
    document.getElementById("rollTicketsDisplay").innerText = "(Lượt: " + rollTickets + ")";
    let elText = "Chưa có";
    let elColor = "#66fcf1";
    if(currentElement === 'poison') { elText = "🟢 ĐỘC (+25% Sát Thương)"; elColor = "#2ed573"; }
    else if(currentElement === 'fire') { elText = "🔥 LỬA (+50% Sát Thương)"; elColor = "#ff4757"; }
    else if(currentElement === 'ice') { elText = "❄️ BĂNG (Làm Chậm Kẻ Địch)"; elColor = "#70a1ff"; }
    
    let disp = document.getElementById("currentElementDisplay");
    disp.innerText = elText;
    disp.style.color = elColor;
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
    updateRollUI();
  });
  addClickEvent('btnMulti', () => { gameMode = 'online'; showScreen('lobbyMenu'); updateSkillIcon(); updateRollUI(); });
  addClickEvent('btnSettings', () => showScreen('settingsScreen'));
  addClickEvent('btnBackToMenu', () => showScreen('mainMenu'));
  addClickEvent('btnBackFromLobby', () => showScreen('mainMenu'));
  addClickEvent('btnCreateLobby', () => showScreen('createRoomScreen'));
  addClickEvent('btnJoinLobby', () => showScreen('joinRoomScreen'));
  addClickEvent('btnInitHost', initHostRoom);
  addClickEvent('btnJoinTarget', joinTargetRoom);
  addClickEvent('btnStartGame', confirmCustom);
  addClickEvent('rematchBtn', requestRematch);

  addClickEvent('btnOpenRoll', () => {
    document.getElementById('rollModal').style.display = 'flex';
  });
  addClickEvent('btnCloseRoll', () => {
    document.getElementById('rollModal').style.display = 'none';
  });
  addClickEvent('btnDoRoll', () => {
    if(rollTickets <= 0) {
      alert("Bạn đã hết lượt Roll! Hãy hoàn thành các màn trong Story Mode để tích lũy thêm (Cứ mỗi 10 màn được thưởng lớn hoặc qua màn nhận lượt roll)!");
      return;
    }
    rollTickets--;
    updateRollUI();

    let elements = ['poison', 'fire', 'ice'];
    let chosen = elements[Math.floor(Math.random() * elements.length)];
    currentElement = chosen;

    let tElem = document.getElementById('rollTitle');
    let dElem = document.getElementById('rollDesc');
    if(chosen === 'poison') {
      tElem.innerText = "🟢 NHẬN ĐƯỢC: ĐỘC";
      tElem.style.color = "#2ed573";
      dElem.innerText = "Tăng 25% Sát Thương! Vũ khí phủ độc xanh lá cực mạnh!";
    } else if(chosen === 'fire') {
      tElem.innerText = "🔥 NHẬN ĐƯỢC: LỬA";
      tElem.style.color = "#ff4757";
      dElem.innerText = "Tăng 50% Sát Thương! Vũ khí bùng cháy sức mạnh hủy diệt!";
    } else if(chosen === 'ice') {
      tElem.innerText = "❄️ NHẬN ĐƯỢC: BĂNG";
      tElem.style.color = "#70a1ff";
      dElem.innerText = "Làm chậm tốc độ đối thủ khi tấn công!";
    }
    updateRollUI();
  });

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
    myData.element = currentElement;
    
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
    canvas.height = window.innerHeight * 0.75;

    let startX = isHost || gameMode === 'story' ? 80 : canvas.width - 80;
    let enemyX = isHost || gameMode === 'story' ? canvas.width - 80 : 80;

    isBossStage = (gameMode === 'story' && currentStage % 10 === 0);

    let enemyHp = 500;
    let enemyScale = 1.35; // Nhân vật to hơn
    let enemyColor = "#ff4757";
    let enemyWeapon = "sword";

    if(gameMode === 'story') {
      if(isBossStage) {
        enemyHp = 1800 + (currentStage * 120);
        enemyScale = 1.8;
        enemyColor = "#ff0055";
        enemyWeapon = "axe";
      } else {
        enemyHp = 450 + (currentStage * 65);
        enemyScale = 1.35;
        let wpList = ["sword", "axe", "dagger", "spear", "staff", "bow", "laser", "muscle", "glove"];
        enemyWeapon = wpList[currentStage % wpList.length];
      }
    }

    pSelf = { 
      x: startX, y: canvas.height - 25, vy: 0, isGrounded: true, 
      hp: 500, maxHp: 500, atk: false, data: myData, facing: 1, 
      walkTimer: 0, scale: 1.35, isSpecialAction: false, isSpinning: false, 
      spinAngle: 0, lastAtkTime: 0, lastSkillTime: 0, slowTimer: 0 
    };
    
    pEnemy = { 
      x: enemyX, y: canvas.height - 25, vy: 0, isGrounded: true, 
      hp: enemyHp, maxHp: enemyHp, atk: false, 
      data: (gameMode === 'story') ? { color: enemyColor, weapon: enemyWeapon, hat: isBossStage ? "knight" : "none", cape: isBossStage ? "black" : "none", element: "none" } : enemyData, 
      facing: -1, walkTimer: 0, scale: enemyScale, isSpecialAction: false, isSpinning: false, 
      spinAngle: 0, lastAtkTime: 0, lastSkillTime: 0, slowTimer: 0
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
        // Thưởng lượt roll nguyên tố (Cứ qua màn tăng lượt roll, 10 màn tặng nhiều hơn)
        let earned = (currentStage % 10 === 0) ? 3 : 1;
        rollTickets += earned;
        updateRollUI();
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

  function jump() { if (pSelf && pSelf.isGrounded && isRunning) { pSelf.vy = -13; pSelf.isGrounded = false; } }

  function attack() {
    if(!pSelf || !isRunning) return;
    
    let now = Date.now();
    let cooldown = (pSelf.data.weapon === 'dagger') ? 140 : 190; 
    if (now - (pSelf.lastAtkTime || 0) < cooldown) return;
    pSelf.lastAtkTime = now;

    pSelf.atk = true; 
    let reach = 50;
    let baseDmg = 16;

    if(pSelf.data.weapon === 'sword') { reach = 65; baseDmg = 20; }
    else if(pSelf.data.weapon === 'axe') { reach = 80; baseDmg = 35; }
    else if(pSelf.data.weapon === 'dagger') { reach = 42; baseDmg = 12; }
    else if(pSelf.data.weapon === 'spear') { reach = 85; baseDmg = 24; }
    else if(pSelf.data.weapon === 'muscle') { reach = 80; baseDmg = 35; }
    else if(pSelf.data.weapon === 'glove') { reach = 45; baseDmg = 18; }

    // Tính toán sát thương theo nguyên tố
    let finalDmg = baseDmg;
    let particleColor = pSelf.data.color;
    if(pSelf.data.element === 'poison') {
      finalDmg *= 1.25; // Tăng 25% damge độc
      particleColor = '#2ed573';
    } else if(pSelf.data.element === 'fire') {
      finalDmg *= 1.50; // Tăng 50% damge lửa
      particleColor = '#ff4757';
    } else if(pSelf.data.element === 'ice') {
      particleColor = '#70a1ff';
    }

    for(let i=0; i<4; i++) {
      particles.push({ 
        x: pSelf.x + pSelf.facing * (25 + i * 12), 
        y: pSelf.y - 25 + (Math.random() - 0.5) * 15, 
        vx: pSelf.facing * (3 + Math.random() * 3), 
        vy: (Math.random() - 0.5) * 3, 
        life: 14, 
        color: particleColor 
      });
    }

    let other = pEnemy;
    if(Math.abs(pSelf.x - other.x) < reach * pSelf.scale) {
      other.hp = Math.max(0, other.hp - finalDmg);
      if(pSelf.data.element === 'ice') {
        other.slowTimer = 90; // Băng làm chậm đối thủ
      }
      addParticles(other.x, other.y - 20 * other.scale, particleColor, 12);
    }
    setTimeout(() => pSelf.atk = false, 140);
  }

  function createBullet(caster, target, weapon) {
    let dir = caster.facing;
    let startX = caster.x + dir * 20 * caster.scale;
    let startY = caster.y - 24 * caster.scale;
    let dmgBonus = (caster === pEnemy && gameMode === 'story') ? (10 + currentStage * 2) : 0;
    let isStoryEnemy = (caster === pEnemy && gameMode === 'story');

    let multiplier = 1.0;
    let bulletColor = '#fffa65';
    if(caster.data.element === 'poison') { multiplier = 1.25; bulletColor = '#2ed573'; }
    else if(caster.data.element === 'fire') { multiplier = 1.50; bulletColor = '#ff4757'; }
    else if(caster.data.element === 'ice') { bulletColor = '#70a1ff'; }

    if (weapon === 'staff') {
      bullets.push({ x: startX, y: startY, vx: dir * 9.5, color: bulletColor, radius: 9, dmg: (22 + dmgBonus) * multiplier, type: 'orb', shooter: caster });
    } else if (weapon === 'bow') {
      let bowDmg = (caster === pEnemy && gameMode === 'story') ? Math.max(2, 2 + Math.floor(currentStage / 2)) : 3;
      bullets.push({ x: startX, y: startY, vx: dir * 14, color: bulletColor, radius: 3.5, dmg: bowDmg * multiplier, type: 'arrow', shooter: caster });
    } else if (weapon === 'laser') {
      bullets.push({ x: startX, y: startY, vx: dir * 20, color: bulletColor, radius: 2.5, dmg: (20 + dmgBonus) * multiplier, type: 'laser', shooter: caster });
    } else if (weapon === 'sword') {
      let tornadoDmg = (isStoryEnemy ? (65 + currentStage * 7) : 50) * multiplier;
      bullets.push({ x: startX, y: startY, vx: dir * 8, color: bulletColor, radius: 22, dmg: tornadoDmg, type: 'tornado', shooter: caster });
    } else if (weapon === 'glove') {
      let gloveDmg = (isStoryEnemy ? (65 + currentStage * 7) : 50) * multiplier;
      bullets.push({ x: startX, y: startY, vx: dir * 12, color: bulletColor, radius: 15, dmg: gloveDmg, type: 'fist', shooter: caster });
    }
  }

  function executeWeaponSkill(p) {
    let other = (p === pSelf) ? pEnemy : pSelf;
    let wp = p.data.weapon;
    let isStoryEnemy = (p === pEnemy && gameMode === 'story');

    if (wp === 'sword') {
      p.isSpecialAction = true;
      p.isSpinning = true;
      p.spinAngle = 0;
      addParticles(p.x, p.y - 20, '#66fcf1', 35);
      createBullet(p, other, 'sword');
      setTimeout(() => {
        p.isSpecialAction = false;
        p.isSpinning = false;
      }, 350);

    } else if (wp === 'axe' || wp === 'muscle') {
      p.isSpecialAction = true;
      p.isSpinning = true;
      p.spinAngle = 0;
      p.vy = -18; p.isGrounded = false;
      let effectColor = (wp === 'axe') ? '#ff4757' : '#ffa502';
      addParticles(p.x, p.y - 20, effectColor, 30);

      let spinInterval = setInterval(() => {
        if (!p.isSpecialAction) {
          clearInterval(spinInterval);
          p.isSpinning = false;
          return;
        }
        p.spinAngle += 0.35;
      }, 20);

      setTimeout(() => {
        p.vy = 24;
        let checkSlam = setInterval(() => {
          let ground = canvas.height - 25;
          if(p.y >= ground) {
            p.y = ground; p.vy = 0; 
            p.isSpecialAction = false; 
            p.isSpinning = false;
            clearInterval(checkSlam);
            clearInterval(spinInterval);
            addParticles(p.x, p.y, effectColor, 40);
            let slamDmg = isStoryEnemy ? (90 + currentStage * 9) : 75;
            if(Math.abs(p.x - other.x) < 140) {
              other.hp = Math.max(0, other.hp - slamDmg);
              other.x += (other.x > p.x) ? 70 : -70;
              other.x = Math.max(20, Math.min(canvas.width - 20, other.x));
              addParticles(other.x, other.y - 20, effectColor, 30);
            }
          }
        }, 20);
      }, 300);

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
      addParticles(p.x, p.y - 20, '#f1c40f', 22);
      let dashDist = p.facing * 160;
      p.x = Math.max(20, Math.min(canvas.width - 20, p.x + dashDist));
      let thrustDmg = isStoryEnemy ? (70 + currentStage * 7) : 55;
      if(Math.abs(p.x - other.x) < 110) {
        other.hp = Math.max(0, other.hp - thrustDmg);
        addParticles(other.x, other.y - 20, '#f1c40f', 30);
      }
      setTimeout(() => p.isSpecialAction = false, 250);

    } else if (wp === 'glove') {
      p.isSpecialAction = true;
      addParticles(p.x, p.y - 20, '#ff4757', 30);
      createBullet(p, other, 'glove');
      setTimeout(() => p.isSpecialAction = false, 220);

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
    let skillCooldown = 10000;
    if (pSelf.data.weapon === 'bow') {
      skillCooldown = 200;
    }

    if (now - (pSelf.lastSkillTime || 0) < skillCooldown) return;
    pSelf.lastSkillTime = now;

    executeWeaponSkill(pSelf);

    if(gameMode === 'online' && conn && conn.open) {
      if(['staff', 'bow', 'laser', 'sword', 'glove'].includes(pSelf.data.weapon)) {
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

    let moveSpeed = 4.8;
    if(pSelf.slowTimer > 0) { moveSpeed *= 0.6; pSelf.slowTimer--; }

    if (moveL) { pSelf.x -= moveSpeed; pSelf.facing = -1; pSelf.walkTimer += 0.25; }
    else if (moveR) { pSelf.x += moveSpeed; pSelf.facing = 1; pSelf.walkTimer += 0.25; }
    else { pSelf.walkTimer = 0; }
    
    pSelf.x = Math.max(20, Math.min(canvas.width - 20, pSelf.x));

    if(gameMode === 'story') {
      pEnemy.y += pEnemy.vy; pEnemy.vy += 0.58;
      if (pEnemy.y >= ground) { pEnemy.y = ground; pEnemy.vy = 0; pEnemy.isGrounded = true; }
      
      pEnemy.facing = pSelf.x < pEnemy.x ? -1 : 1;
      let speed = 2.4 + (currentStage * 0.18);
      if(pEnemy.slowTimer > 0) { speed *= 0.5; pEnemy.slowTimer--; }
      if(isBossStage) speed = 3.4;

      if (!pEnemy.isSpecialAction && Math.abs(pSelf.x - pEnemy.x) > 45 * pEnemy.scale) {
        pEnemy.x += (pSelf.x < pEnemy.x) ? -speed : speed;
        pEnemy.walkTimer += 0.3;
      }

      let now = Date.now();
      let enemyCooldown = (pEnemy.data.weapon === 'dagger') ? 100 : 150;
      let canEnemyAtk = (now - (pEnemy.lastAtkTime || 0) > enemyCooldown);

      let atkChance = 0.045 + (currentStage * 0.005);
      if (Math.random() < 0.015 && pEnemy.isGrounded) pEnemy.vy = -13;
      
      if (Math.random() < atkChance && canEnemyAtk) { 
        pEnemy.lastAtkTime = now;
        pEnemy.atk = true; 
        setTimeout(() => pEnemy.atk = false, 140); 
        if(['staff', 'bow', 'laser', 'sword', 'glove'].includes(pEnemy.data.weapon)) {
          createBullet(pEnemy, pSelf, pEnemy.data.weapon); 
        } else if(Math.abs(pSelf.x - pEnemy.x) < 75 * pEnemy.scale) {
          let meleeDmg = 16 + (currentStage * 2.5);
          pSelf.hp = Math.max(0, pSelf.hp - meleeDmg);
          addParticles(pSelf.x, pSelf.y - 20, '#ff4757', 10);
        }
      }

      let enemySkillCooldown = (pEnemy.data.weapon === 'bow') ? 200 : 10000;
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
    ctx.strokeStyle = '#45a29e'; ctx.lineWidth = 2; ctx.strokeRect(12, 12, w, 16);

    ctx.fillStyle = "rgba(31, 40, 51, 0.8)"; ctx.fillRect(canvas.width - w - 12, 12, w, 16);
    ctx.fillStyle = pEnemy.data.color;
    ctx.shadowColor = pEnemy.data.color; ctx.shadowBlur = 8;
    let enemyHpW = w * (Math.max(0, pEnemy.hp) / pEnemy.maxHp);
    ctx.fillRect(canvas.width - 12 - enemyHpW, 12, enemyHpW, 16);
    ctx.shadowBlur = 0;
    ctx.strokeStyle = '#45a29e'; ctx.lineWidth = 2; ctx.strokeRect(canvas.width - w - 12, 12, w, 16);

    ctx.fillStyle = '#fff';
    ctx.font = 'bold 11px sans-serif';
    ctx.fillText("BẠN (" + Math.max(0, Math.floor(pSelf.hp)) + "/" + pSelf.maxHp + ")", 20, 24);
    let enemyTitle = (gameMode === 'story') ? (isBossStage ? "BOSS MÀN " + currentStage : "KẺ ĐỊCH MÀN " + currentStage) : "ĐỐI THỦ";
    ctx.fillText(enemyTitle + " (" + Math.max(0, Math.floor(pEnemy.hp)) + "/" + pEnemy.maxHp + ")", canvas.width - w - 4, 24);

    if(gameMode === 'story') {
      ctx.fillStyle = '#66fcf1';
      ctx.font = 'bold 14px sans-serif';
      ctx.textAlign = 'center';
      ctx.fillText("MÀN " + currentStage + (isBossStage ? " - ⚔️ BOSS BATTLE" : ""), canvas.width / 2, 25);
      ctx.textAlign = 'left';
    }

    for(let i = bullets.length - 1; i >= 0; i--) {
      let b = bullets[i];
      b.x += b.vx;
      
      ctx.save();
      ctx.shadowColor = b.color; 
      ctx.shadowBlur = 10;
      
      if (b.type === 'tornado') {
        ctx.translate(b.x, b.y);
        ctx.rotate(animFrame * 0.3);
        ctx.strokeStyle = b.color;
        ctx.lineWidth = 3;
        ctx.beginPath();
        ctx.arc(0, 0, b.radius, 0, Math.PI * 1.5);
        ctx.stroke();
        ctx.beginPath();
        ctx.arc(0, 0, b.radius * 0.5, 0, Math.PI);
        ctx.strokeStyle = '#ffffff';
        ctx.stroke();
      } else if (b.type === 'fist') {
        ctx.translate(b.x, b.y);
        ctx.fillStyle = b.color;
        ctx.beginPath();
        ctx.arc(0, 0, b.radius, 0, Math.PI * 2);
        ctx.fill();
        ctx.lineWidth = 2;
        ctx.strokeStyle = '#ffffff';
        ctx.stroke();
        ctx.fillStyle = '#ffffff';
        ctx.fillRect(-5, -5, 10, 10);
      } else {
        ctx.fillStyle = b.color;
        ctx.beginPath(); 
        ctx.arc(b.x, b.y, b.radius, 0, Math.PI*2); 
        ctx.fill();
      }
      ctx.restore();

      let target = (b.shooter === pSelf) ? pEnemy : pSelf;
      if(Math.abs(b.x - target.x) < (b.radius + 15) * target.scale && Math.abs(b.y - target.y) < 35 * target.scale) {
        target.hp = Math.max(0, target.hp - b.dmg);
        if(b.shooter.data && b.shooter.data.element === 'ice') {
          target.slowTimer = 90;
        }
        addParticles(b.x, b.y, b.color, 8);
        bullets.splice(i, 1);
        continue;
      }

      if(b.x < 0 || b.x > canvas.width) {
        bullets.splice(i, 1);
      }
    }

    for(let i = particles.length - 1; i >= 0; i--) {
      let pt = particles[i];
      pt.x += pt.vx; pt.y += pt.vy; pt.life--;
      ctx.fillStyle = pt.color;
      ctx.globalAlpha = pt.life / 22;
      ctx.fillRect(pt.x, pt.y, 4, 4);
      ctx.globalAlpha = 1.0;
      if(pt.life <= 0) particles.splice(i, 1);
    }

    drawStickman(pSelf);
    drawStickman(pEnemy);

    if(pSelf.hp <= 0) {
      triggerEndGame(false);
      return;
    }
    if(pEnemy.hp <= 0) {
      triggerEndGame(true);
      return;
    }

    requestAnimationFrame(loop);
  }

  function drawStickman(p) {
    ctx.save();
    ctx.translate(p.x, p.y);
    ctx.scale(p.facing * p.scale, p.scale);

    let skin = p.data.color;
    let wp = p.data.weapon;
    let hat = p.data.hat;
    let cape = p.data.cape;
    let el = p.data.element;

    ctx.strokeStyle = skin;
    ctx.lineWidth = 4;
    ctx.lineCap = 'round';
    ctx.lineJoin = 'round';
    ctx.shadowColor = skin;
    ctx.shadowBlur = 8;

    if(cape !== 'none') {
      ctx.fillStyle = (cape === 'red') ? '#ff4757' : '#2f3640';
      ctx.beginPath();
      ctx.moveTo(0, -32);
      ctx.lineTo(-14, -5);
      ctx.lineTo(-4, -5);
      ctx.closePath();
      ctx.fill();
    }

    ctx.beginPath();
    ctx.arc(0, -38, 10, 0, Math.PI*2);
    ctx.stroke();

    if(hat === 'knight') {
      ctx.fillStyle = '#718093';
      ctx.fillRect(-8, -52, 16, 5);
      ctx.fillRect(-4, -58, 8, 6);
    } else if(hat === 'wizard') {
      ctx.fillStyle = '#9b59b6';
      ctx.beginPath();
      ctx.moveTo(0, -62);
      ctx.lineTo(-10, -46);
      ctx.lineTo(10, -46);
      ctx.closePath();
      ctx.fill();
    }

    ctx.beginPath();
    ctx.moveTo(0, -28);
    ctx.lineTo(0, -8);
    ctx.stroke();

    let legOffset = Math.sin(p.walkTimer) * 11;
    if(p.isGrounded && Math.abs(p.walkTimer) > 0) {
      ctx.beginPath();
      ctx.moveTo(0, -8);
      ctx.lineTo(-10 + legOffset, 0);
      ctx.stroke();
      ctx.beginPath();
      ctx.moveTo(0, -8);
      ctx.lineTo(10 - legOffset, 0);
      ctx.stroke();
    } else {
      ctx.beginPath();
      ctx.moveTo(0, -8);
      ctx.lineTo(-7, 0);
      ctx.stroke();
      ctx.beginPath();
      ctx.moveTo(0, -8);
      ctx.lineTo(7, 0);
      ctx.stroke();
    }

    if(p.isSpinning) {
      ctx.rotate(p.spinAngle * Math.PI * 2);
    }

    let armAngle = p.atk ? -Math.PI / 4 : 0;
    ctx.save();
    ctx.translate(0, -24);
    ctx.rotate(armAngle);

    ctx.beginPath();
    ctx.moveTo(0, 0);
    ctx.lineTo(18, 4);
    ctx.stroke();

    // Model vũ khí cực kỳ chi tiết & đẹp mắt kèm hiệu ứng nguyên tố
    ctx.lineWidth = 3.5;
    let weaponGlow = '#66fcf1';
    if(el === 'poison') weaponGlow = '#2ed573';
    else if(el === 'fire') weaponGlow = '#ff4757';
    else if(el === 'ice') weaponGlow = '#70a1ff';

    ctx.shadowColor = weaponGlow;
    ctx.shadowBlur = 12;

    if(wp === 'sword') {
      ctx.strokeStyle = '#ffffff';
      ctx.beginPath();
      ctx.moveTo(18, 4);
      ctx.lineTo(44, 4);
      ctx.stroke();
      ctx.fillStyle = weaponGlow;
      ctx.fillRect(15, 0, 4, 8);
      ctx.beginPath();
      ctx.arc(44, 4, 3, 0, Math.PI*2);
      ctx.fill();
    } else if(wp === 'axe') {
      ctx.strokeStyle = '#a4b0be';
      ctx.beginPath();
      ctx.moveTo(18, 4);
      ctx.lineTo(32, 4);
      ctx.stroke();
      ctx.fillStyle = weaponGlow;
      ctx.beginPath();
      ctx.moveTo(32, -4);
      ctx.lineTo(42, 4);
      ctx.lineTo(32, 12);
      ctx.closePath();
      ctx.fill();
    } else if(wp === 'dagger') {
      ctx.strokeStyle = weaponGlow;
      ctx.beginPath();
      ctx.moveTo(18, 4);
      ctx.lineTo(30, 4);
      ctx.stroke();
      ctx.fillStyle = '#ffffff';
      ctx.fillRect(28, 2, 4, 4);
    } else if(wp === 'spear') {
      ctx.strokeStyle = '#f1c40f';
      ctx.beginPath();
      ctx.moveTo(18, 4);
      ctx.lineTo(48, 4);
      ctx.stroke();
      ctx.fillStyle = weaponGlow;
      ctx.beginPath();
      ctx.moveTo(48, -1);
      ctx.lineTo(56, 4);
      ctx.lineTo(48, 9);
      ctx.closePath();
      ctx.fill();
    } else if(wp === 'staff') {
      ctx.strokeStyle = '#e67e22';
      ctx.beginPath();
      ctx.moveTo(18, 4);
      ctx.lineTo(38, 4);
      ctx.stroke();
      ctx.fillStyle = weaponGlow;
      ctx.beginPath();
      ctx.arc(38, 4, 6, 0, Math.PI*2);
      ctx.fill();
    } else if(wp === 'bow') {
      ctx.strokeStyle = '#e1b12c';
      ctx.beginPath();
      ctx.arc(24, 4, 12, -Math.PI/2, Math.PI/2);
      ctx.stroke();
      ctx.strokeStyle = weaponGlow;
      ctx.beginPath();
      ctx.moveTo(24, -8);
      ctx.lineTo(18, 4);
      ctx.lineTo(24, 16);
      ctx.stroke();
    } else if(wp === 'laser') {
      ctx.strokeStyle = weaponGlow;
      ctx.beginPath();
      ctx.moveTo(18, 4);
      ctx.lineTo(36, 4);
      ctx.stroke();
      ctx.fillStyle = '#ffffff';
      ctx.fillRect(32, 1, 6, 6);
    } else if(wp === 'muscle') {
      ctx.fillStyle = weaponGlow;
      ctx.beginPath();
      ctx.arc(22, 4, 8, 0, Math.PI*2);
      ctx.fill();
    } else if(wp === 'glove') {
      ctx.fillStyle = weaponGlow;
      ctx.beginPath();
      ctx.arc(24, 4, 8, 0, Math.PI*2);
      ctx.fill();
      ctx.strokeStyle = '#ffffff';
      ctx.lineWidth = 2;
      ctx.stroke();
    }

    ctx.restore();
    ctx.restore();
  }

  window.addEventListener('keydown', (e) => {
    if(!isRunning) return;
    if(e.key === 'a' || e.key === 'A' || e.key === 'ArrowLeft') { moveL = true; }
    if(e.key === 'd' || e.key === 'D' || e.key === 'ArrowRight') { moveR = true; }
    if(e.key === 'w' || e.key === 'W' || e.key === 'ArrowUp' || e.key === ' ') { jump(); }
    if(e.key === 'j' || e.key === 'J') { attack(); }
    if(e.key === 'k' || e.key === 'K') { useSkill(); }
  });

  window.addEventListener('keyup', (e) => {
    if(e.key === 'a' || e.key === 'A' || e.key === 'ArrowLeft') { moveL = false; }
    if(e.key === 'd' || e.key === 'D' || e.key === 'ArrowRight') { moveR = false; }
  });

  function bindTouchButton(id, startFn, endFn) {
    let el = document.getElementById(id);
    if(!el) return;
    el.addEventListener('mousedown', (e) => { e.preventDefault(); if(startFn) startFn(); el.classList.add('active'); });
    el.addEventListener('mouseup', (e) => { e.preventDefault(); if(endFn) endFn(); el.classList.remove('active'); });
    el.addEventListener('mouseleave', (e) => { e.preventDefault(); if(endFn) endFn(); el.classList.remove('active'); });
    el.addEventListener('touchstart', (e) => { e.preventDefault(); if(startFn) startFn(); el.classList.add('active'); });
    el.addEventListener('touchend', (e) => { e.preventDefault(); if(endFn) endFn(); el.classList.remove('active'); });
  }

  bindTouchButton('btnLeft', () => { moveL = true; }, () => { moveL = false; });
  bindTouchButton('btnRight', () => { moveR = true; }, () => { moveR = false; });
  bindTouchButton('btnJump', () => { jump(); }, null);
  bindTouchButton('btnAtk', () => { attack(); }, null);
  bindTouchButton('btnSkill', () => { useSkill(); }, null);

  canvas.addEventListener('mousedown', (e) => {
    if(e.button === 0) attack();
    else if(e.button === 2) useSkill();
  });
  canvas.addEventListener('contextmenu', (e) => e.preventDefault());

  window.addEventListener('resize', () => {
    if(isRunning) {
      canvas.width = window.innerWidth * 0.95;
      canvas.height = window.innerHeight * 0.75;
    }
  });
</script>
</body>
</html>
"""

st.components.v1.html(game_code, height=750, scrolling=False)
