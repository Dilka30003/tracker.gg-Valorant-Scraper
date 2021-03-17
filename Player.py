from requests.api import head


class Player:
    def __init__(self):
        self.damage = Damage()
        self.game = Game()
        self.agents = [ Agent(), Agent(), Agent() ]
        self.accuracy = Accuracy()
        self.weapons = [ Weapon(), Weapon(), Weapon() ]

    
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
    playtime = None
    matches = None

class Agent:
    name = None
    image = None
    time = None
    matches = None
    winRate = None
    kd = None
    dmg = None

class Accuracy:
    headRate = None
    head = None
    bodyRate = None
    body = None
    legRate = None
    leg = None

class Weapon:
    name = None
    image = None
    type = None
    headRate = None
    bodyRate = None
    legRate = None
    kills = None