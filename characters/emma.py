from characters.characters import Characters

class Emma:
    def __init__(self):
        self.character_config = Characters(
            character = "Emma",
            health = 75
        )
        attack_func = [self.super_attack, self.normal_attack, self.fast_attack]
        for attack in attack_func:
            attack()
        # print(self.character_config.characteristic)
        
    def super_attack(self) -> dict: # loggings
        self.character_config.get_attack(
            attack_type = "super_attack",
            attack_name = "Shadow Strike",
            damage_caused = 59,
            cooldown_rounds = 2
        )
        return self.character_config.characteristic

    def normal_attack(self) -> dict:
        self.character_config.get_attack(
            attack_type = "normal_attack",
            attack_name = "Shadow Crawl",
            damage_caused = 12,
            cooldown_rounds = 1
        )
        return self.character_config.characteristic
    
    def fast_attack(self) -> dict:
        self.character_config.get_attack(
            attack_type = "fast_attack",
            attack_name = "Shadow Wind",
            damage_caused = 9,
            cooldown_rounds = 0
        ) 
        return self.character_config.characteristic

