import streamlit as st

st.title("🎮 Cấu Hình Vũ Khí & Kỹ Năng Game")
st.write("Dưới đây là thông số chi tiết của các loại vũ khí đã được cập nhật:")

# Dữ liệu vũ khí chuẩn Python
weapons = [
    {
        "name": "Cung & Súng Laser",
        "cooldown": 0.5,
        "effect": "Đánh thường cơ bản"
    },
    {
        "name": "Trượng Ma Thuật",
        "cooldown": 1.0,
        "effect": "Gây nhiễm độc, trừ máu theo thời gian (Đòn đánh & Kỹ năng)",
        "poison_damage_over_time": True
    },
    {
        "name": "Rìu Chiến",
        "damage_nerfed": True,
        "special_skill": {
            "name": "Bay lên xoay vòng dập xuống",
            "cooldown": 30.0
        }
    },
    {
        "name": "Dao Độc",
        "skill": {
            "name": "Phun độc",
            "effect": "Trừ máu liên tục mỗi giây"
        }
    },
    {
        "name": "Giáo Dài",
        "skill": {
            "name": "Lao tới",
            "cooldown": 15.0
        }
    }
]

# Hiển thị danh sách vũ khí lên giao diện Streamlit
for weapon in weapons:
    with st.expander(f"⚔️ {weapon['name']}"):
        if "cooldown" in weapon:
            st.write(f"- **Hồi chiêu đánh thường:** {weapon['cooldown']} giây")
        if "effect" in weapon:
            st.write(f"- **Hiệu ứng:** {weapon['effect']}")
        if weapon.get("damage_nerfed"):
            st.write("- **Trạng thái:** Đã giảm sát thương đánh thường")
        if "special_skill" in weapon:
            skill = weapon["special_skill"]
            st.write(f"- **Kỹ năng đặc biệt:** {skill['name']} (Hồi chiêu: {skill['cooldown']} giây)")
        if "skill" in weapon:
            skill = weapon["skill"]
            st.write(f"- **Kỹ năng:** {skill['name']} ({skill.get('effect', '')})")

st.success("Khởi tạo lại mã nguồn thành công! Bạn có thể tiếp tục phát triển các tính năng tiếp theo.")
