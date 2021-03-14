import requests
from bs4 import BeautifulSoup
import yaml
from Player import Player

URL = 'https://tracker.gg/valorant/profile/riot/Dilka30003%230000/overview?playlist=unrated'
page = requests.get(URL)

#with open("page.html", "wb") as f:
#    f.write(page.content)

soup = BeautifulSoup(page.content, 'html.parser')

results = soup.find(id='app')

player = Player()                                                                               # Initialise Player
player.damage.kda = float(results.find_all('span', class_='valorant-highlighted-stat__value')[-1].next) # Get KDA

big_stats = results.find('div', class_='giant-stats')                                           # Get the 4 big stats from main page
stats = []
for stat in big_stats.find_all('div', class_='numbers'):
    stats.append(stat.find('span', class_='value').next)

player.damage.dmg = float(stats[0])                                                             # Extract Stats from big 4
player.damage.kd = float(stats[1])
player.damage.headshotRate = float(stats[2])
player.game.winRate = float(stats[3][:-1])

main_stats = results.find('div', class_="main")                                                 # Get the main 8 stats
stats = []
for stat in main_stats.find_all('div', class_='numbers'):
    stats.append(stat.find('span', class_='value').next.replace(',', ''))

player.game.wins = int(stats[0])                                                                # Extract stats from the main 8
player.damage.kills = int(stats[1])
player.damage.Headshots = int(stats[2])
player.damage.deaths  = int(stats[3])
player.damage.assists = int(stats[4])
player.game.scorePerRound = float(stats[5])
player.damage.killsPerRound = float(stats[6])
player.game.firstBlood = int(stats[7])
player.game.ace = int(stats[8])
player.game.clutch = int(stats[9])
player.game.flawless = int(stats[10])
player.game.mostKills = int(stats[11])

print(stats)


#print(player.kda)
