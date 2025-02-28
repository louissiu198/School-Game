from characters.characters import Characters

class Mason:
    def __init__(self):
        self.character_config = Characters(
            character = "Mason",
            health = 110
        )
        attack_func = [self.super_attack, self.normal_attack, self.fast_attack]
        for attack in attack_func:
            attack()
        # print(self.character_config.characteristic)
        
    def super_attack(self) -> dict: # loggings
        self.character_config.get_attack(
            attack_type = "super_attack",
            attack_name = "Titan Slam",
            damage_caused = 46,
            cooldown_rounds = 2
        )
        return self.character_config.characteristic

    def normal_attack(self) -> dict:
        self.character_config.get_attack(
            attack_type = "normal_attack",
            attack_name = "Rock fall",
            damage_caused = 12,
            cooldown_rounds = 1
        )
        return self.character_config.characteristic
    
    def fast_attack(self) -> dict:
        self.character_config.get_attack(
            attack_type = "fast_attack",
            attack_name = "Earthquake",
            damage_caused = 7,
            cooldown_rounds = 0
        ) 
        return self.character_config.characteristic

