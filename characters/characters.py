
class Characters:
    def __init__(self, character: str = "Frank", health: int = 120):
        self.health = health
        self.character = character
        self.get_character()

    def get_character(self) -> dict:
        self.characteristic = {
            "name": self.character,
            "health": self.health,
            "actions": []
        }
        return self.characteristic

    def get_attack(
            self, 
            attack_type: str = "super_attack",
            attack_name: str = "horrible person",
            damage_caused: int = 0,
            cooldown_rounds: int = 0
        ) -> dict:
        attack_options = ["super_attack", "normal_attack", "fast_attack"]
        if attack_type in attack_options:
            attack_data = {
                "name":         attack_name,
                "damage":       damage_caused,
                "cooldown":     cooldown_rounds, 
            }
            print({attack_type: attack_data})
            self.characteristic["actions"].append({
                attack_type: attack_data
            })
        return self.characteristic

    
    # def add_characters(
    #         self, 
    #         character_name: str, 
    #         character_health: int, 
    #         character_moves: dict,
    #     ) -> None:
    #         self.characters[character_name] = {}
    #         self.characters[character_name]["HEALTH"] = character_health
    #         self.characters[character_name]["MOVES"] = character_moves



