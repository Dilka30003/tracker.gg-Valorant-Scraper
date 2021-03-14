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
player.damage.kda = float(results.find_all('span', class_='valorant-highlighted-stat__value')[-1].text) # Get KDA

big_stats = results.find('div', class_='giant-stats')                                           # Get the 4 big stats from main page
stats = []
for stat in big_stats.find_all('div', class_='numbers'):
    stats.append(stat.find('span', class_='value').text)

player.damage.dmg = float(stats[0])                                                             # Extract Stats from big 4
player.damage.kd = float(stats[1])
player.damage.headshotRate = float(stats[2])
player.game.winRate = float(stats[3][:-1])

main_stats = results.find('div', class_="main")                                                 # Get the main 8 stats
stats = []
for stat in main_stats.find_all('div', class_='numbers'):
    stats.append(stat.find('span', class_='value').text.replace(',', ''))

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

agent_stats = results.find('div', class_='top-agents__table-container')                         # Get table of top 3 agents
rows = agent_stats.next.find_all('tr')
rows.pop(0)                                                                                     # Remove top label row
for i in range(len(rows)):
    row = rows[i]
    player.agents[i].name = row.find('span', class_='agent__name').text
    data = row.find_all('span', class_='name')
    player.agents[i].time = data[0].text
    player.agents[i].matches = int(data[1].text)
    player.agents[i].winRate = float(data[2].text[:-1])
    player.agents[i].kd = float(data[3].text)
    player.agents[i].dmg = float(data[4].text)

player.game.playtime = results.find('span', class_='playtime').text.strip()[:-10]
player.game.matches = int(results.find('span', class_='matches').text.strip()[:-8])

accuracy_stats = results.find('div', class_='accuracy__content')                                # Get table of accuracy stats
rows = accuracy_stats.find_all('tr')
stats = []
for row in rows:
    data = row.find_all('span', 'stat__value')
    stats.append(data)

player.accuracy.headRate = float(stats[0][0].text[:-1])
player.accuracy.head = int(stats[0][1].text)
player.accuracy.bodyRate = float(stats[1][0].text[:-1])
player.accuracy.body = int(stats[1][1].text)
player.accuracy.legRate = float(stats[2][0].text[:-1])
player.accuracy.leg = int(stats[2][1].text)

weapon_stats = results.find('div', class_='top-weapons__weapons')
weapons = results.find_all('div', class_='weapon')
for i in range(len(weapons)):
    weapon = weapons[i]
    player.weapons[i].name = weapon.find('div', class_='weapon__name').text
    player.weapons[i].type = weapon.find('div', class_='weapon__type').text
    stats = weapon.find_all('span', class_='stat')
    player.weapons[i].headRate = int(stats[0].text[:-1])
    player.weapons[i].bodyRate = int(stats[1].text[:-1])
    player.weapons[i].legRate = int(stats[2].text[:-1])
    player.weapons[i].kills = int(weapon.find('span', class_='value').text.replace(',', ''))
    pass





print(stats)


#print(player.kda)
