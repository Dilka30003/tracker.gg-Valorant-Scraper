class Player:
    def __init__(self):
        self.damage = Damage()
        self.game = Game()
    
class Damage:
    dmg = None
    kda = None
    kd = None
    headshotRate = None
    kills = None
    Headshots = None
    deaths = None
    assists = None
    killsPerRound = None
    
class Game:
    winRate = None
    wins = None
    scorePerRound = None
    firstBlood = None
    ace = None
    clutch = None
    flawless = None
    mostKills = None

class Agent:
    name = None
    time = None
    matches = None
    winRate = None
    kd = None
    dmg = None
    