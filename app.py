<!DOCTYPE html>
<html lang="vi">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Găng Tay Bão Táp - Trận Chiến</title>
    <style>
        body {
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background-color: #121212;
            color: #e0e0e0;
            max-width: 600px;
            margin: 40px auto;
            padding: 20px;
            border-radius: 12px;
            box-shadow: 0 4px 20px rgba(0,0,0,0.5);
        }
        h2 { color: #4facfe; text-align: center; }
        .stats-box {
            display: flex;
            justify-content: space-between;
            background: #1e1e1e;
            padding: 15px;
            border-radius: 8px;
            margin-bottom: 20px;
            border: 1px solid #333;
        }
        .character { width: 48%; }
        .controls {
            display: flex;
            gap: 10px;
            margin-bottom: 20px;
        }
        button {
            flex: 1;
            padding: 12px;
            font-size: 16px;
            font-weight: bold;
            border: none;
            border-radius: 6px;
            cursor: pointer;
            transition: 0.2s;
        }
        #btn-attack { background-color: #ff9800; color: white; }
        #btn-attack:hover { background-color: #f57c00; }
        #btn-skill { background-color: #4facfe; color: white; }
        #btn-skill:hover { background-color: #00f2fe; color: #121212; }
        button:disabled { background-color: #444; color: #888; cursor: not-allowed; }
        #log {
            background: #181818;
            border: 1px solid #333;
            padding: 15px;
            border-radius: 8px;
            height: 250px;
            overflow-y: auto;
            font-family: monospace;
            font-size: 14px;
            line-height: 1.5;
        }
        .log-hit { color: #ffb74d; }
        .log-crit { color: #ff5252; font-weight: bold; }
        .log-skill { color: #4facfe; font-weight: bold; }
    </style>
</head>
<body>

    <h2>🥊 GĂNG TAY BÃO TÁP - THẬP ẢNH CUỒNG PHONG</h2>

    <div class="stats-box">
        <div class="character">
            <h3>Chiến Binh Gió</h3>
            <p>HP: <span id="hero-hp">1000</span>/1000</p>
            <p>Mana: <span id="hero-mana">150</span>/150</p>
            <p>Tấn công: <span id="hero-atk">380</span> (Đã cộng găng)</p>
        </div>
        <div class="character">
            <h3>Quái Vật Goblin</h3>
            <p>HP: <span id="monster-hp">800</span>/800</p>
            <p>Trạng thái: <span id="monster-status" style="color: #4caf50;">Bình thường</span></p>
        </div>
    </div>

    <div class="controls">
        <button id="btn-attack" onclick="normalAttack()">Đánh Thường</button>
        <button id="btn-skill" onclick="castSkill()">Dùng Chiêu: Thập Ảnh Cuồng Phong (60 Mana)</button>
    </div>

    <div id="log">
        [Hệ thống] Đã trang bị Găng Tay Bão Táp (+180 Tấn công). Trận chiến bắt đầu!<br>
    </div>

    <script>
        let hero = { name: "Chiến Binh Gió", hp: 1000, maxHp: 1000, mana: 150, maxMana: 150, atk: 380 };
        let monster = { name: "Quái Vật Goblin", hp: 800, maxHp: 800, isStunned: false };

        function updateUI() {
            document.getElementById("hero-hp").innerText = Math.max(0, hero.hp);
            document.getElementById("hero-mana").innerText = Math.max(0, hero.mana);
            document.getElementById("monster-hp").innerText = Math.max(0, monster.hp);
            document.getElementById("monster-status").innerText = monster.isStunned ? "Choáng (Stun)" : "Bình thường";
            document.getElementById("monster-status").style.color = monster.isStunned ? "#ff5252" : "#4caf50";
        }

        function logMessage(msg, className = "") {
            let logDiv = document.getElementById("log");
            logDiv.innerHTML += `<span class="${className}">${msg}</span><br>`;
            logDiv.scrollTop = logDiv.scrollHeight;
        }

        function normalAttack() {
            if (monster.hp <= 0) {
                logMessage("Quái vật đã bị hạ gục! Hãy reset lại trang.", "log-crit");
                return;
            }
            let dmg = hero.atk * 0.4;
            monster.hp -= dmg;
            logMessage(`[Đánh thường] ${hero.name} tấn công gây ${dmg.toFixed(1)} sát thương.`, "log-hit");
            
            checkWin();
            updateUI();
        }

        function castSkill() {
            if (monster.hp <= 0) {
                logMessage("Quái vật đã bị hạ gục!", "log-crit");
                return;
            }
            if (hero.mana < 60) {
                logMessage("Không đủ Mana để dùng chiêu!", "log-crit");
                return;
            }

            hero.mana -= 60;
            logMessage(`⚡ [KỸ NĂNG] ${hero.name} tung chiêu Thập Ảnh Cuồng Phong!`, "log-skill");

            let totalDmg = 0;
            // 9 cú đấm đầu
            for (let i = 1; i <= 9; i++) {
                if (monster.hp <= 0) break;
                let hitDmg = hero.atk * 0.15;
                totalDmg += hitDmg;
                logMessage(`  • Cú đấm thứ ${i}: Lao tới gây gián đoạn và ${hitDmg.toFixed(1)} sát thương.`, "log-hit");
            }

            // Cú đấm thứ 10
            if (monster.hp > 0) {
                let finisherDmg = hero.atk * 1.50;
                totalDmg += finisherDmg;
                monster.hp -= finisherDmg;
                monster.isStunned = true;
                logMessage(`  💥 Cú đấm thứ 10 (ĐÒN KẾT LIỄU): Bùng nổ gây ${finisherDmg.toFixed(1)} sát thương chí mạng!`, "log-crit");
                logMessage(`  🌪️ ${monster.name} bị đánh văng ra xa 5 mét và dính hiệu ứng **Choáng** trong 1.5 giây!`, "log-skill");
            }

            logMessage(`✨ Tổng sát thương chuỗi kỹ năng: ${totalDmg.toFixed(1)}`, "log-skill");
            checkWin();
            updateUI();
        }

        function checkWin() {
            if (monster.hp <= 0) {
                logMessage(`🏆 Chúc mừng! ${monster.name} đã bị tiêu diệt hoàn toàn bởi Găng Tay Bão Táp!`, "log-crit");
                document.getElementById("btn-attack").disabled = true;
                document.getElementById("btn-skill").disabled = true;
            }
        }
    </script>
</body>
</html>
