import requests
from bs4 import BeautifulSoup
import yaml
from Player import Player

URL = 'https://tracker.gg/valorant/profile/riot/Dilka30003%230000/overview'
page = requests.get(URL)

#with open("page.html", "wb") as f:
#    f.write(page.content)

soup = BeautifulSoup(page.content, 'html.parser')

results = soup.find(id='app')

player = Player()                                                                               # Initialise Player
player.kda = float(results.find('span', class_='valorant-highlighted-stat__value').next)        # Get KDA

big_stats = results.find('div', class_='giant-stats')                                           # Get the 4 big stats from main page
stats = []
for stat in big_stats.find_all('div', class_='numbers'):
    stats.append(stat.find('span', class_='value').next)

player.dmg = float(stats[0])                                                                    # Extract Stats from big 4
player.kd = float(stats[1])
player.headshotRate = float(stats[2])
player.winRate = float(stats[3][:-1])


print(stats)


#print(player.kda)
