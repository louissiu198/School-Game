from characters.characters import Characters
from characters.emma import Emma
from characters.mason import Mason
from characters.noah import Noah
from characters.oliver import Oliver
# hello ss
class Game:
    def __init__(self, game_name: str = "default"): # no idea what this could be if value is blank
        self.current_player = 0
        self.game_name = game_name
        self.game_table = {}
        self.setup_players()
    
    def setup_players(self) -> None:
        for _ in range(1, 5):
            self.game_table[f"player_{_}"] = {}
    
    @staticmethod
    def fetch_character(charcater_name: str) -> object:
        character_list = {
            "emma": Emma,
            "noah": Noah,
            "mason": Mason,
            "oliver": Oliver,
        }
        return character_list[charcater_name]
        # match charcater_name: # dumb method
        #     case "emma":
        #         return Emma
        #     case "noah" 
        
    def join_game(
            self, 
            username: str = "bot",
            character: str = "noah"
        ) -> None:
        if self.current_player < 4 or username in str(self.game_table):
            if username in str(self.game_table):
                return True, ""
            self.current_player += 1
            self.game_table[f"player_{self.current_player}"]["username"] = username
            print(Game.fetch_character(character)().character_config.characteristic)
            self.game_table[f"player_{self.current_player}"]["character_stats"] = Game.fetch_character(character)().character_config.characteristic # dict object
            return True, str(self.current_player)
            # {'player_1': {'username': 'saqwde', 'character_stats': {'name': 'Noah', 'health': 90, 'actions': [{'name': 'Phoenix Dash', 'damage': 32, 'cooldown': 1}, {'name': 'Phoenix Dash', 'damage': 10, 'cooldown': 1}, {'name': 'Phoenix Dash', 'damage': 9, 'cooldown': 0}]}}, 'player_2': {}, 'player_3': {}, 'player_4': {}}
            # {'name': 'Emma', 'health': 75, 'actions': [{'super_attack': {'name': 'Shadow Strike', 'damage': 59, 'cooldown': 2}}, {'normal_attack': {'name': 'Shadow Crawl', 'damage': 12, 'cooldown': 1}}, {'fast_attack': {'name': 'Shadow Wind', 'damage': 9, 'cooldown': 0}}]}
        else:
            return False
