import streamlit as st
import random

st.title("⚔️ Game Chiến Đấu: Cập Nhật Vũ Khí & Kỹ Năng")

# Khởi tạo trạng thái game nếu chưa có
if "player_hp" not in st.session_state:
    st.session_state.player_hp = 100
    st.session_state.enemy_hp = 100
    st.session_state.game_log = []
    st.session_state.selected_weapon = "Cung & Súng Laser"

# Danh sách vũ khí và thông số cập nhật mới
weapons_data = {
    "Cung & Súng Laser": {
        "type": "normal",
        "cooldown": 0.5,
        "damage": 15,
        "desc": "Đánh thường nhanh (Hồi chiêu: 0.5s)"
    },
    "Trượng Ma Thuật": {
        "type": "poison",
        "cooldown": 1.0,
        "damage": 10,
        "desc": "Đánh thường & Skill gây nhiễm độc trừ máu theo thời gian (Hồi chiêu: 1.0s)"
    },
    "Rìu Chiến": {
        "type": "heavy_skill",
        "cooldown": 2.0,
        "damage": 12, # Đã giảm sát thương đánh thường
        "special_name": "Bay lên xoay vòng dập xuống",
        "special_cooldown": 30.0,
        "desc": "Sát thương thường giảm, có skill đặc biệt dập xuống (CD: 30s)"
    },
    "Dao Độc": {
        "type": "skill",
        "cooldown": 1.0,
        "damage": 10,
        "skill_name": "Phun độc",
        "desc": "Có kỹ năng phun độc gây trừ máu liên tục mỗi giây"
    },
    "Giáo Dài": {
        "type": "skill",
        "cooldown": 1.0,
        "damage": 12,
        "skill_name": "Lao tới",
        "skill_cooldown": 15.0,
        "desc": "Có kỹ năng lao tới tấn công (CD: 15s)"
    }
}

# Giao diện chọn vũ khí
st.sidebar.header("Chọn Vũ Khí")
chosen_weapon = st.sidebar.selectbox("Vũ khí của bạn:", list(weapons_data.keys()))
st.session_state.selected_weapon = chosen_weapon

weapon_info = weapons_data[chosen_weapon]

# Hiển thị thông tin trận đấu
col1, col2 = st.columns(2)
with col1:
    st.metric("❤️ HP Người Chơi", st.session_state.player_hp)
with col2:
    st.metric("💀 HP Kẻ Địch", st.session_state.enemy_hp)

st.info(f"**Vũ khí hiện tại:** {chosen_weapon}\n\n_{weapon_info['desc']}_")

# Nút hành động trong game
col_action1, col_action2 = st.columns(2)

with col_action1:
    if st.button("⚔️ Tấn Công Thường"):
        dmg = weapon_info["damage"]
        st.session_state.enemy_hp = max(0, st.session_state.enemy_hp - dmg)
        st.session_state.game_log.insert(0, f"Bạn dùng **{chosen_weapon}** đánh thường gây **{dmg}** sát thương.")

with col_action2:
    # Nút kỹ năng đặc biệt tùy theo vũ khí
    if chosen_weapon in ["Rìu Chiến", "Dao Độc", "Giáo Dài"]:
        skill_btn_name = weapon_info.get("special_name", weapon_info.get("skill_name"))
        if st.button(f"🔥 Dùng Kỹ Năng: {skill_btn_name}"):
            skill_dmg = weapon_info["damage"] * 2
            st.session_state.enemy_hp = max(0, st.session_state.enemy_hp - skill_dmg)
            st.session_state.game_log.insert(0, f"Bạn sử dụng kỹ năng **{skill_btn_name}** gây **{skill_dmg}** sát thương và hiệu ứng đặc biệt!")
    else:
        st.write("*(Vũ khí này không có kỹ năng kích hoạt riêng)*")

# Kẻ địch phản công đơn giản
if st.button("🤖 Kẻ Địch Phản Công"):
    if st.session_state.enemy_hp > 0:
        enemy_dmg = random.randint(5, 15)
        st.session_state.player_hp = max(0, st.session_state.player_hp - enemy_dmg)
        st.session_state.game_log.insert(0, f"Kẻ địch phản công gây **{enemy_dmg}** sát thương cho bạn.")
    else:
        st.success("Kẻ địch đã bị hạ gục!")

# Nút reset game
if st.button("🔄 Chơi Lại Từ Đầu"):
    st.session_state.player_hp = 100
    st.session_state.enemy_hp = 100
    st.session_state.game_log = []
    st.rerun()

# Nhật ký trận đấu
st.markdown("### 📜 Nhật Ký Trận Đấu")
for log in st.session_state.game_log[:5]:
    st.write(f"- {log}")
