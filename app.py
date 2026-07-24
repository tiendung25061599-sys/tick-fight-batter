import streamlit as st

# Cấu hình giao diện trang
st.set_page_config(page_title="Găng Tay Bão Táp - Trận Chiến", page_icon="🥊", layout="centered")

# Khởi tạo trạng thái game trong session_state để lưu trữ qua các lượt bấm nút
if "initialized" not in st.session_state:
    st.session_state.hero_hp = 1000
    st.session_state.hero_max_hp = 1000
    st.session_state.hero_mana = 150
    st.session_state.hero_max_mana = 150
    st.session_state.hero_atk = 380  # (200 gốc + 180 từ Găng Tay Bão Táp)
    
    st.session_state.monster_hp = 800
    st.session_state.monster_max_hp = 800
    st.session_state.monster_stunned = False
    
    st.session_state.logs = ["[Hệ thống] Đã trang bị Găng Tay Bão Táp (+180 Tấn công). Trận chiến bắt đầu!"]
    st.session_state.initialized = True

# Giao diện tiêu đề
st.markdown("<h2 style='text-align: center; color: #4facfe;'>🥊 GĂNG TAY BÃO TÁP - THẬP ẢNH CUỒNG PHONG</h2>", unsafe_allow_html=True)

# Hiển thị thông số nhân vật và quái vật
col1, col2 = st.columns(2)

with col1:
    st.markdown("### 🛡️ Chiến Binh Gió")
    st.write(f"**HP:** {max(0, float(st.session_state.hero_hp)):.0f} / {st.session_state.hero_max_hp}")
    st.write(f"**Mana:** {max(0, float(st.session_state.hero_mana)):.0f} / {st.session_state.hero_max_mana}")
    st.write(f"**Tấn công:** {st.session_state.hero_atk} (Đã cộng găng)")

with col2:
    st.markdown("### 👹 Quái Vật Goblin")
    st.write(f"**HP:** {max(0, float(st.session_state.monster_hp)):.0f} / {st.session_state.monster_max_hp}")
    status_text = "Choáng (Stun)" if st.session_state.monster_stunned else "Bình thường"
    st.write(f"**Trạng thái:** {status_text}")

st.markdown("---")

# Kiểm tra điều kiện thắng/thua để khóa/mở nút bấm
game_over = st.session_state.monster_hp <= 0 or st.session_state.hero_hp <= 0

# Các nút hành động
col_btn1, col_btn2, col_btn3 = st.columns(3)

with col_btn1:
    if st.button("⚔️ Đánh Thường", disabled=game_over):
        dmg = st.session_state.hero_atk * 0.4
        st.session_state.monster_hp -= dmg
        st.session_state.logs.append(f"[Đánh thường] Chiến Binh Gió tấn công gây {dmg:.1f} sát thương.")
        st.rerun()

with col_btn2:
    if st.button("⚡ Thập Ảnh Cuồng Phong", disabled=game_over):
        if st.session_state.hero_mana < 60:
            st.session_state.logs.append("⚠️ Không đủ Mana để dùng chiêu!")
        else:
            st.session_state.hero_mana -= 60
            st.session_state.logs.append(f"⚡ [KỸ NĂNG] Chiến Binh Gió tung chiêu Thập Ảnh Cuồng Phong!")
            
            total_dmg = 0
            # 9 cú đấm đầu
            for i in range(1, 10):
                if st.session_state.monster_hp <= 0:
                    break
                hit_dmg = st.session_state.hero_atk * 0.15
                total_dmg += hit_dmg
                st.session_state.logs.append(f"  • Cú đấm thứ {i}: Lao tới gây gián đoạn và {hit_dmg:.1f} sát thương.")
            
            # Cú đấm thứ 10
            if st.session_state.monster_hp > 0:
                finisher_dmg = st.session_state.hero_atk * 1.50
                total_dmg += finisher_dmg
                st.session_state.monster_hp -= finisher_dmg
                st.session_state.monster_stunned = True
                st.session_state.logs.append(f"  💥 Cú đấm thứ 10 (ĐÒN KẾT LIỄU): Bùng nổ gây {finisher_dmg:.1f} sát thương chí mạng!")
                st.session_state.logs.append(f"  🌪️ Quái Vật Goblin bị đánh văng ra xa 5 mét và dính hiệu ứng Choáng trong 1.5 giây!")
            
            st.session_state.logs.append(f"✨ Tổng sát thương chuỗi kỹ năng: {total_dmg:.1f}")
        st.rerun()

with col_btn3:
    if st.button("🔄 Chơi Lại"):
        st.session_state.hero_hp = 1000
        st.session_state.hero_mana = 150
        st.session_state.monster_hp = 800
        st.session_state.monster_stunned = False
        st.session_state.logs = ["[Hệ thống] Trò chơi đã được thiết lập lại. Trận chiến bắt đầu!"]
        st.rerun()

# Hiển thị thông báo kết quả nếu trận đấu kết thúc
if st.session_state.monster_hp <= 0:
    st.success("🏆 Chúc mừng! Quái Vật Goblin đã bị tiêu diệt hoàn toàn bởi Găng Tay Bão Táp!")

# Khung nhật ký trận đấu
st.markdown("### 📜 Nhật Ký Trận Đấu")
log_container = st.container(height=250)
with log_container:
    for log in reversed(st.session_state.logs):
        st.write(log)
