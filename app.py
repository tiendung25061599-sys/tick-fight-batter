import streamlit as st
import random

st.title("⚔️ Game Đánh Nhau Cơ Bản")

# Khởi tạo trạng thái game gốc
if "player_hp" not in st.session_state:
    st.session_state.player_hp = 100
    st.session_state.enemy_hp = 100
    st.session_state.player_gold = 0
    st.session_state.game_log = []

# Chọn nhân vật ban đầu
st.sidebar.header("Chọn Nhân Vật")
character = st.sidebar.selectbox("Nhân vật của bạn:", ["Chiến Binh", "Cung Thủ", "Pháp Sư"])

# Hiển thị chỉ số
col1, col2, col3 = st.columns(3)
with col1:
    st.metric("❤️ HP Người Chơi", st.session_state.player_hp)
with col2:
    st.metric("💀 HP Kẻ Địch", st.session_state.enemy_hp)
with col3:
    st.metric("🪙 Vàng", st.session_state.player_gold)

st.markdown("---")

# Các nút hành động gốc của game
col_action1, col_action2 = st.columns(2)

with col_action1:
    if st.button("⚔️ Tấn Công"):
        if st.session_state.player_hp > 0 and st.session_state.enemy_hp > 0:
            player_dmg = random.randint(10, 20)
            st.session_state.enemy_hp = max(0, st.session_state.enemy_hp - player_dmg)
            st.session_state.game_log.insert(0, f"Bạn tấn công kẻ địch gây **{player_dmg}** sát thương.")

with col_action2:
    if st.button("🛡️ Phòng Thủ"):
        if st.session_state.player_hp > 0 and st.session_state.enemy_hp > 0:
            st.session_state.game_log.insert(0, "Bạn chọn phòng thủ để giảm sát thương nhận vào.")

# Nút phản công của kẻ địch
if st.button("🤖 Kẻ Địch Phản Công"):
    if st.session_state.enemy_hp > 0 and st.session_state.player_hp > 0:
        enemy_dmg = random.randint(5, 15)
        st.session_state.player_hp = max(0, st.session_state.player_hp - enemy_dmg)
        st.session_state.game_log.insert(0, f"Kẻ địch phản công gây **{enemy_dmg}** sát thương cho bạn.")
    elif st.session_state.enemy_hp <= 0:
        st.success("🎉 Kẻ địch đã bị hạ gục! Bạn nhận được 50 vàng.")
        st.session_state.player_gold += 50
    else:
        st.error("💀 Bạn đã thua trận!")

# Nút chơi lại
if st.button("🔄 Chơi Lại"):
    st.session_state.player_hp = 100
    st.session_state.enemy_hp = 100
    st.session_state.game_log = []
    st.rerun()

# Nhật ký trận đấu
st.markdown("### 📜 Nhật Ký Trận Đấu")
for log in st.session_state.game_log[:5]:
    st.write(f"- {log}")
