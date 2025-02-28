from characters.characters import Characters

class Oliver:
    def __init__(self):
        self.character_config = Characters(
            character = "Oliver",
            health = 100
        )
        attack_func = [self.super_attack, self.normal_attack, self.fast_attack]
        for attack in attack_func:
            attack()
        print(self.character_config.characteristic)
        
    def super_attack(self) -> dict: # loggings
        self.character_config.get_attack(
            attack_type = "super_attack",
            attack_name = "Blazing Fury",
            damage_caused = 50,
            cooldown_rounds = 2
        )
        return self.character_config.characteristic

    def normal_attack(self) -> dict:
        self.character_config.get_attack(
            attack_type = "normal_attack",
            attack_name = "Thunderstorm",
            damage_caused = 12,
            cooldown_rounds = 1
        )
        return self.character_config.characteristic
    
    def fast_attack(self) -> dict:
        self.character_config.get_attack(
            attack_type = "fast_attack",
            attack_name = "Thunder Kick",
            damage_caused = 32,
            cooldown_rounds = 0
        ) 
        return self.character_config.characteristic

    # def add_characters(
    #         self, 
    #         character_name: str, 
    #         character_health: int, 
    #         character_moves: dict,
    #     ) -> None:
    #         self.characters[character_name] = {}
    #         self.characters[character_name]["HEALTH"] = character_health
    #         self.characters[character_name]["MOVES"] = character_moves



