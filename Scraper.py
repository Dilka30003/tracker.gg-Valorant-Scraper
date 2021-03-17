from os import name
from typing import Tuple
import requests
from bs4 import BeautifulSoup
import yaml
from Player import Player
from PIL import Image, ImageFont, ImageDraw

def GetStats(name:str, tag:str, type:str):
    URL = 'https://tracker.gg/valorant/profile/riot/' + name + '%23' + tag + '/overview?playlist=' + type
    page = requests.get(URL)

    #with open("page.html", "wb") as f:
    #    f.write(page.content)

    soup = BeautifulSoup(page.content, 'html.parser')

    results = soup.find(id='app')

    pageError = results.find_all('div', class_='content content--error')
    if (len(pageError) >0):
        if "private" in pageError[0].text.lower():
            return 1, URL
        if "404" in pageError[0].text.lower():
            return 404, None





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
        player.agents[i].image = Image.open(requests.get(row.find('img').get('src'), stream=True).raw)
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
        player.weapons[i].image = Image.open(requests.get(weapon.find('img').get('src'), stream=True).raw)
        player.weapons[i].type = weapon.find('div', class_='weapon__type').text
        stats = weapon.find_all('span', class_='stat')
        player.weapons[i].headRate = int(stats[0].text[:-1])
        player.weapons[i].bodyRate = int(stats[1].text[:-1])
        player.weapons[i].legRate = int(stats[2].text[:-1])
        player.weapons[i].kills = int(weapon.find('span', class_='value').text.replace(',', ''))
        pass

    return 0, player

def GenerateAgentGraphic(player:Player) -> Image:
    img = Image.new('RGBA', (1920, 1200), (255, 0, 0, 0))
    timeFont = ImageFont.truetype("Roboto/Roboto-Medium.ttf", 100)
    subtextFont = ImageFont.truetype("Roboto/Roboto-Medium.ttf", 70)
    MARGIN = 10

    for i in range(3):
        agent = player.agents[i]
        img.paste(agent.image, (MARGIN, i*(156+256)), agent.image)
        draw = ImageDraw.Draw(img)
        draw.text((MARGIN, i*(156+agent.image.width) + agent.image.height),agent.time,(200,200,200),font=timeFont)
        draw.text((MARGIN + agent.image.width + 10, i*(156+agent.image.height) + 36),str(agent.matches) + " Matches",(255,255,255),font=timeFont)
        draw.text((MARGIN + agent.image.width + 10, i*(156+agent.image.height) + 154),str(agent.winRate) + "% Win Rate",(255,255,255),font=timeFont)
        draw.text((MARGIN + agent.image.width + 10 + 800, i*(156+agent.image.height) + 36),str(agent.kd) + " K/D",(255,255,255),font=timeFont)
        draw.text((MARGIN + agent.image.width + 10 + 800, i*(156+agent.image.height) + 154),str(agent.dmg) + " Dmg/Round",(255,255,255),font=timeFont)
        
    return img
    
def GenerateWeaponGraphic(player:Player) -> Image:
    img = Image.new('RGBA', (1000, 1200), (255, 0, 0, 0))
    nameFont = ImageFont.truetype("Roboto/Roboto-Medium.ttf", 100)
    typeFont = ImageFont.truetype("Roboto/Roboto-Medium.ttf", 60)
    headerFont = ImageFont.truetype("Roboto/Roboto-Medium.ttf", 60)
    MARGIN = 10

    weaponHeight = player.weapons[0].image.height + player.weapons[1].image.height + player.weapons[2].image.height
    spacing = (img.height - weaponHeight)/2 - 90
    positions = []
    positions.append(0)
    positions.append(player.weapons[0].image.height + spacing)
    positions.append(positions[1] + player.weapons[1].image.height + spacing)

    for i in range(3):
        weapon = player.weapons[i]
        img.paste(weapon.image, (MARGIN, int(positions[i])), weapon.image)
        draw = ImageDraw.Draw(img)
        draw.text((MARGIN+50, positions[i] + weapon.image.height + 10), weapon.name,(200,200,200),font=nameFont)
        draw.text((MARGIN+50, positions[i] + weapon.image.height + 100 + 20), weapon.type,(200,200,200),font=typeFont)
        draw.text((MARGIN+weapon.image.width + 30, positions[i]), "Headshot: " + str(weapon.headRate) + "%",(255,255,255),font=headerFont)
        draw.text((MARGIN+weapon.image.width + 30, positions[i] + 70), "Bodyshot: " + str(weapon.bodyRate) + "%",(255,255,255),font=headerFont)
        draw.text((MARGIN+weapon.image.width + 30, positions[i] + 70*2), "Legshot: " + str(weapon.legRate) + "%",(255,255,255),font=headerFont)
        draw.text((MARGIN+weapon.image.width + 30, positions[i] + 70*3), "Kills: " + str(weapon.kills),(255,255,255),font=headerFont)





    return img