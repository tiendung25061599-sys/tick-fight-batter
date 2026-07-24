le = "#66fcf1"; ctx.lineWidth = 2; ctx.strokeRect(12, 12, w, 16);
    ctx.fillStyle = "white"; ctx.font = "bold 13px 'Segoe UI'";
    ctx.fillText(`BẠN (MÀN ${currentStage})` if gameMode === 'story' else "BẠN", 15, 42);

    ctx.fillStyle = "rgba(31, 40, 51, 0.8)"; ctx.fillRect(canvas.width - w - 12, 12, w, 16); 
    ctx.fillStyle = pEnemy.data.color; 
    ctx.shadowColor = pEnemy.data.color; ctx.shadowBlur = 8;
    ctx.fillRect(canvas.width - 12 - w * (Math.max(0, pEnemy.hp) / pEnemy.maxHp), 12, w * (Math.max(0, pEnemy.hp) / pEnemy.maxHp), 16);
    ctx.shadowBlur = 0;
    ctx.strokeStyle = "#ff4757"; ctx.strokeRect(canvas.width - w - 12, 12, w, 16);
    ctx.fillStyle = "white"; ctx.textAlign = "right";
    ctx.fillText(isBossStage ? "BOSS" : (gameMode === 'story' ? "QUÁI VẬT" : "ĐỐI THỦ"), canvas.width - 15, 42);
    ctx.textAlign = "left";

    for(let i=bullets.length-1; i>=0; i--) {
      let b = bullets[i];
      b.x += b.vx;
      ctx.fillStyle = b.color;
      ctx.shadowColor = b.color;
      ctx.shadowBlur = 10;
      ctx.beginPath();
      
      if (b.type === 'arrow') {
        ctx.fillRect(b.x, b.y - b.radius, b.radius*4, b.radius*1.5);
      } else if (b.type === 'laser') {
        ctx.fillRect(b.x, b.y - b.radius, b.radius*12, b.radius*2);
      } else {
        ctx.arc(b.x, b.y, b.radius, 0, Math.PI*2);
      }
      ctx.fill();
      ctx.shadowBlur = 0;

      let target = (b.shooter === pSelf) ? pEnemy : pSelf;
      if (Math.abs(b.x - target.x) < 20*target.scale && Math.abs(b.y - target.y) < 40*target.scale) {
        target.hp = Math.max(0, target.hp - b.dmg);
        addParticles(target.x, target.y - 20*target.scale, b.color, 12);
        bullets.splice(i, 1);
        continue;
      }
      if (b.x < -100 || b.x > canvas.width + 100) bullets.splice(i, 1);
    }

    for(let i=particles.length-1; i>=0; i--) {
      let pt = particles[i];
      pt.x += pt.vx; pt.y += pt.vy; pt.life--;
      ctx.fillStyle = pt.color;
      ctx.globalAlpha = pt.life / 22;
      ctx.fillRect(pt.x, pt.y, 4, 4);
      if(pt.life <= 0) particles.splice(i, 1);
    }
    ctx.globalAlpha = 1;

    drawStickman(pSelf);
    drawStickman(pEnemy);

    if (pSelf.hp <= 0 || pEnemy.hp <= 0) {
      setTimeout(() => triggerEndGame(pEnemy.hp <= 0), 200);
    } else {
      requestAnimationFrame(loop);
    }
  }

  function drawStickman(p) {
    ctx.save();
    ctx.translate(p.x, p.y);
    ctx.scale(p.facing * p.scale, p.scale);
    
    if (p.isSpinning) {
      ctx.translate(0, -25);
      ctx.rotate(p.spinAngle);
      ctx.translate(0, 25);
    }

    ctx.strokeStyle = p.data.color;
    ctx.lineWidth = 4;
    ctx.lineCap = "round";
    ctx.lineJoin = "round";
    ctx.shadowColor = p.data.color;
    ctx.shadowBlur = 6;

    let legAnim = Math.sin(p.walkTimer) * 12;
    let armAnim = p.atk ? -30 : Math.cos(p.walkTimer) * 10;

    if (p.data.cape !== 'none') {
      ctx.fillStyle = p.data.cape === 'red' ? '#ff4757' : '#2f3542';
      ctx.beginPath();
      ctx.moveTo(-6, -38);
      ctx.lineTo(-18 - Math.sin(animFrame*0.1)*5, -5);
      ctx.lineTo(-6, -10);
      ctx.fill();
    }

    ctx.beginPath(); ctx.arc(0, -42, 9, 0, Math.PI*2); ctx.stroke();
    ctx.fillStyle = "#050508"; ctx.fill();

    if (p.data.hat === 'knight') {
      ctx.fillStyle = '#a4b0be'; ctx.fillRect(-11, -54, 22, 12);
      ctx.fillStyle = '#ff4757'; ctx.fillRect(-2, -62, 4, 10);
    } else if (p.data.hat === 'wizard') {
      ctx.fillStyle = '#3742fa';
      ctx.beginPath(); ctx.moveTo(-12, -48); ctx.lineTo(12, -48); ctx.lineTo(0, -68); ctx.fill();
    }

    ctx.beginPath(); ctx.moveTo(0, -33); ctx.lineTo(0, -15); ctx.stroke();

    ctx.beginPath(); ctx.moveTo(0, -15); ctx.lineTo(-8 + legAnim, 0); ctx.stroke();
    ctx.beginPath(); ctx.moveTo(0, -15); ctx.lineTo(8 - legAnim, 0); ctx.stroke();

    ctx.beginPath(); ctx.moveTo(0, -28); ctx.lineTo(12, -22 + armAnim); ctx.stroke();
    ctx.beginPath(); ctx.moveTo(0, -28); ctx.lineTo(-12, -22 - armAnim); ctx.stroke();

    // THÊM GĂNG TAY
    ctx.fillStyle = "#ffffff";
    ctx.lineWidth = 1;
    ctx.beginPath(); ctx.arc(12, -22 + armAnim, 4.5, 0, Math.PI*2); ctx.fill(); ctx.stroke();
    ctx.beginPath(); ctx.arc(-12, -22 - armAnim, 4.5, 0, Math.PI*2); ctx.fill(); ctx.stroke();
    ctx.lineWidth = 4; // Trả lại độ dày nét vẽ cũ

    let wpX = 14, wpY = -22 + armAnim;
    ctx.save();
    ctx.translate(wpX, wpY);
    if(p.atk) {
      if(p.data.weapon === 'sword') ctx.rotate(Math.PI/3);
      else if(p.data.weapon === 'axe') ctx.rotate(Math.PI/2);
      else if(p.data.weapon === 'dagger') ctx.translate(10, 0);
      else if(p.data.weapon === 'spear') ctx.translate(18, 0);
      else if(p.data.weapon === 'muscle') ctx.scale(1.5, 1.5);
    }

    if (p.data.weapon === 'sword') {
      ctx.strokeStyle = '#f1f2f6'; ctx.lineWidth = 3;
      ctx.beginPath(); ctx.moveTo(0, 5); ctx.lineTo(25, -25); ctx.stroke();
      ctx.strokeStyle = '#f7b731'; ctx.beginPath(); ctx.moveTo(-4, 0); ctx.lineTo(8, -6); ctx.stroke();
    } else if (p.data.weapon === 'axe') {
      ctx.strokeStyle = '#a4b0be'; ctx.lineWidth = 4;
      ctx.beginPath(); ctx.moveTo(-5, 10); ctx.lineTo(18, -22); ctx.stroke();
      ctx.fillStyle = '#ff6b81';
      ctx.beginPath(); ctx.arc(15, -18, 12, -Math.PI/2, Math.PI/2); ctx.fill();
    } else if (p.data.weapon === 'dagger') {
      ctx.strokeStyle = '#7bed9f'; ctx.lineWidth = 2;
      ctx.beginPath(); ctx.moveTo(0,0); ctx.lineTo(14, -8); ctx.stroke();
    } else if (p.data.weapon === 'spear') {
      ctx.strokeStyle = '#f1c40f'; ctx.lineWidth = 3;
      ctx.beginPath(); ctx.moveTo(-15, 10); ctx.lineTo(35, -15); ctx.stroke();
      ctx.fillStyle = '#ff4757';
      ctx.beginPath(); ctx.moveTo(35, -15); ctx.lineTo(45, -15); ctx.lineTo(35, -8); ctx.fill();
    } else if (p.data.weapon === 'staff') {
      ctx.strokeStyle = '#8B4513'; ctx.lineWidth = 4;
      ctx.beginPath(); ctx.moveTo(-5, 15); ctx.lineTo(10, -25); ctx.stroke();
      ctx.fillStyle = '#fffa65';
      ctx.beginPath(); ctx.arc(10, -28, 6 + Math.sin(animFrame*0.2)*2, 0, Math.PI*2); ctx.fill();
    } else if (p.data.weapon === 'bow') {
      ctx.strokeStyle = '#d1ccc0'; ctx.lineWidth = 2;
      ctx.beginPath(); ctx.arc(8, -5, 15, -Math.PI/2, Math.PI/2); ctx.stroke();
      ctx.strokeStyle = '#ffffff'; ctx.lineWidth = 1;
      ctx.beginPath(); ctx.moveTo(8, -20); ctx.lineTo(8, 10); ctx.stroke();
    } else if (p.data.weapon === 'laser') {
      ctx.fillStyle = '#2f3542'; ctx.fillRect(0, -8, 20, 8);
      ctx.fillStyle = '#66fcf1'; ctx.fillRect(20, -6, 5, 4);
    } else if (p.data.weapon === 'muscle') {
      ctx.fillStyle = '#ffa502'; ctx.beginPath(); ctx.arc(8, -8, 12, 0, Math.PI*2); ctx.fill();
      ctx.fillStyle = p.data.color; ctx.beginPath(); ctx.arc(14, -8, 8, 0, Math.PI*2); ctx.fill();
    }

    ctx.restore();
    ctx.restore();
  }

  // EVENTS BÀN PHÍM
  window.addEventListener("keydown", (e) => {
    if(e.key.toLowerCase() === 'a') { moveL = true; document.getElementById('btnLeft').classList.add('active'); }
    if(e.key.toLowerCase() === 'd') { moveR = true; document.getElementById('btnRight').classList.add('active'); }
    if(e.key.toLowerCase() === 'w') { jump(); document.getElementById('btnJump').classList.add('active'); }
    if(e.key.toLowerCase() === 'j') { attack(); document.getElementById('btnAtk').classList.add('active'); }
    if(e.key.toLowerCase() === 'k') { useSkill(); document.getElementById('btnSkill').classList.add('active'); }
  });

  window.addEventListener("keyup", (e) => {
    if(e.key.toLowerCase() === 'a') { moveL = false; document.getElementById('btnLeft').classList.remove('active'); }
    if(e.key.toLowerCase() === 'd') { moveR = false; document.getElementById('btnRight').classList.remove('active'); }
    if(e.key.toLowerCase() === 'w') document.getElementById('btnJump').classList.remove('active');
    if(e.key.toLowerCase() === 'j') document.getElementById('btnAtk').classList.remove('active');
    if(e.key.toLowerCase() === 'k') document.getElementById('btnSkill').classList.remove('active');
  });

  // EVENTS CHUỘT
  window.addEventListener("mousedown", (e) => {
    if(isRunning) {
      if(e.button === 0) { attack(); document.getElementById('btnAtk').classList.add('active'); }
      if(e.button === 2) { useSkill(); document.getElementById('btnSkill').classList.add('active'); }
    }
  });
  window.addEventListener("mouseup", (e) => {
    if(e.button === 0) document.getElementById('btnAtk').classList.remove('active');
    if(e.button === 2) document.getElementById('btnSkill').classList.remove('active');
  });
  window.addEventListener("contextmenu", e => e.preventDefault());

  // EVENTS CẢM ỨNG
  function touchBind(id, onDown, onUp) {
    let el = document.getElementById(id);
    if(!el) return;
    el.addEventListener('touchstart', (e) => { e.preventDefault(); onDown(); el.classList.add('active'); });
    el.addEventListener('touchend', (e) => { e.preventDefault(); onUp(); el.classList.remove('active'); });
  }

  touchBind('btnLeft', () => moveL = true, () => moveL = false);
  touchBind('btnRight', () => moveR = true, () => moveR = false);
  touchBind('btnJump', jump, () => {});
  touchBind('btnAtk', attack, () => {});
  touchBind('btnSkill', useSkill, () => {});
</script>
</body>
</html>
"""

components.html(game_code, height=900, scrolling=False)
