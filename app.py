class Character:
    def __init__(self, name, hp, mana, physical_attack):
        self.name = name
        self.hp = hp
        self.max_mana = mana
        self.mana = mana
        self.physical_attack = physical_attack
        self.is_stunned = False

    def take_damage(self, amount, is_crit=False):
        crit_text = " (CHÍ MẠNG!)" if is_crit else ""
        self.hp -= amount
        print(f"-> {self.name} nhận {amount:.1f} sát thương{crit_text}. HP còn lại: {max(0, self.hp):.1f}")


class StormGauntlets:
    def __init__(self):
        self.name = "Găng Tay Bão Táp (Storm Gauntlets)"
        self.rarity = "Huyền Thoại"
        # Chỉ số cơ bản
        self.bonus_attack = 180
        self.attack_speed_bonus = 0.30  # +30%
        self.crit_rate = 0.15           # +15%
        
        # Thông tin kỹ năng
        self.skill_name = "Thập Ảnh Cuồng Phong"
        self.cooldown = 12.0  # giây
        self.mana_cost = 60
        self.range = 12.0     # mét
        self.current_cooldown = 0.0

    def equip(self, player):
        """Trang bị găng tay cho nhân vật, cộng dồn chỉ số."""
        player.physical_attack += self.bonus_attack
        print(f"[{player.name}] đã trang bị **{self.name}**! Tấn công tăng thêm +{self.bonus_attack}.")

    def cast_ten_shadow_gale(self, user, target):
        """Kích hoạt kỹ năng: 10 cú đấm lao tới."""
        if self.current_cooldown > 0:
            print(f"Kỹ năng '{self.skill_name}' đang hồi chiêu! Còn lại {self.current_cooldown:.1f} giây.")
            return False

        if user.mana < self.mana_cost:
            print(f"Không đủ năng lượng! Cần {self.mana_cost} Mana.")
            return False

        # Tiêu hao tài nguyên
        user.mana -= self.mana_cost
        self.current_cooldown = self.cooldown

        print(f"\n⚡ [{user.name}] gầm lên và tung chiêu **{self.skill_name}**!")
        print(f"Giải phóng bão táp lao tới mục tiêu {target.name} trong phạm vi {self.range}m!\n")

        total_damage_dealt = 0

        # Thực hiện 9 cú đấm đầu tiên
        for i in range(1, 10):
            if target.hp <= 0:
                print(f"Mục tiêu {target.name} đã bị hạ gục trước khi hoàn tất chuỗi đấm!")
                break
            
            hit_damage = user.physical_attack * 0.15
            total_damage_dealt += hit_damage
            print(f"  • Cú đấm thứ {i}: Lao tới đánh trúng, gây gián đoạn và {hit_damage:.1f} sát thương vật lý.")

        # Cú đấm thứ 10 (Đòn kết liễu)
        if target.hp > 0:
            print(f"  💥 Cú đấm thứ 10 (ĐÒN KẾT LIỄU): Năng lượng bão táp bùng nổ toàn lực!")
            finisher_damage = user.physical_attack * 1.50
            total_damage_dealt += finisher_damage
            
            # Áp dụng hiệu ứng khống chế và đẩy lùi
            target.take_damage(finisher_damage, is_crit=True)
            target.is_stunned = True
            print(f"  🌪️ {target.name} bị đánh văng ra xa 5 mét và dính hiệu ứng **Choáng (Stun)** trong 1.5 giây!")
        
        print(f"\n✨ Tổng sát thương chuỗi kỹ năng: {total_damage_dealt:.1f}\n")
        return True


# ==================== MÔ PHỎNG KIỂM TRA (TEST GAME) ====================
if __name__ == "__main__":
    # Khởi tạo Người chơi và Kẻ địch mẫu
    hero = Character(name="Chiến Binh Gió", hp=1000, mana=150, physical_attack=200)
    monster = Character(name="Quái Vật Goblin", hp=800, mana=50, physical_attack=50)

    # Nhận trang bị
    gloves = StormGauntlets()
    gloves.equip(hero)

    # Sử dụng kỹ năng
    gloves.cast_ten_shadow_gale(hero, monster)
