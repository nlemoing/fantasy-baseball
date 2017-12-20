from bs4 import BeautifulSoup
from urllib.request import urlopen

#Usage:
#parse_table(year, playertype)
#player type: True for pitcher, False for batter
#returns a dictionary of player names and their stats
#stats are dictionaries of statistics and values
#list of statistics can be imported as batter_categories and pitcher_categories

#Examples:
#batters = parse_table(2017, False)
#jose = batters["Jose Altuve"]
#kevin_pillar_avg = batters["Kevin Pillar"]["AVG"]
#print(jose)
#print(kevin_pillar_avg)
#pitchers = parse_table(2017, True)
#print(pitchers["Corey Kluber"])
pitcher_categories = ['RK', 'PLAYER', 'TEAM', 'GP', 'GS', 'IP', 'H', 'R', 'ER', 'BB', 'SO', 'W', 'L', 'SV', 'HLD', 'BLSV', 'WHIP', 'ERA']
batter_categories = ['RK', 'PLAYER', 'TEAM', 'AB', 'R', 'H', '2B', '3B', 'HR', 'RBI', 'SB', 'CS', 'BB', 'SO', 'AVG', 'OBP', 'SLG', 'OPS']

def parse_table(year, playerType, categories, count = 1, players = {}):
    url = "https://www.espn.com/mlb/stats/{}/_/year/{}/count/{}/qualified/true"
    try:
        dataPage = urlopen(url.format(playerType, year, count))
    except:
        print("Data not found")
        return 1
    soup = BeautifulSoup(dataPage, 'html.parser')
    table = soup.find('table')
    def is_player(cssclass):
        return cssclass == 'evenrow' or cssclass == 'oddrow'
    playRows = table.find_all('tr', class_=is_player)
    if len(playRows) == 0:
        return players
    for row in playRows:
        tracker = 0
        playerData = {}
        name = ""
        columns = row.find_all('td')
        for data in columns:
            text = data.text
            if tracker >= len(categories):
                break
            elif tracker == 1:
                name = text
            elif tracker == 2:
                playerData["TEAM"] = text
            elif tracker > 2: #this is where the numerical data starts
                if text.isnumeric():
                    value = int(text)
                else:
                    value = float(text)
                playerData[categories[tracker]] = value
            tracker = tracker + 1
        players[name] = playerData
    return parse_table(year, playerType, categories, count + 40, players)

def importdata(filename):
    try:
        with open(filename) as f:
            data = f.readlines()
    except IOError:
        raise
    data = [x.strip() for x in data]
    categories = data[0].split(",")[1:]
    players = {}
    for line in data[1:]:
        player = line.split(",")
        playerdata = {}
        for stat in range(len(categories)):
            text = player[stat + 1]
            if stat and text.isnumeric():
                playerdata[categories[stat]] = int(text)
            elif stat:
                playerdata[categories[stat]] = float(text)
            else:
                playerdata[categories[stat]] = text
        players[player[0]] = playerdata
    return players

def exportdata(data, filename, pitching):
    if pitching:
        categorystring = ",".join(pitcher_categories[1:])
    else:
        categorystring = ",".join(batter_categories[1:])
    targetfile = open(filename, "w")
    targetfile.write(categorystring + "\n")
    for name, playerstats in data.items():
        playerstring = name + ","
        playerdata = []
        for stat in playerstats.values():
            playerdata.append(str(stat))
        datastring = ",".join(playerdata)
        targetfile.write(playerstring + datastring + "\n")
    targetfile.close()

def playerdata(year, pitching, export = True):
    playerType = "batting"
    categories = batter_categories
    if pitching:
        playerType = "pitching"
        categories = pitcher_categories
    filename = str(year) + playerType + ".csv"
    try:
        return importdata(filename)
    except:
        data = parse_table(year, playerType, categories)
        if export:
            exportdata(data, filename, pitching)
        return data
#tests
#batters = parse_table(2017, False)
#pitchers = parse_table(2017, True)
#print(batters["Jose Altuve"])
#print(pitchers["Corey Kluber"])
#print(batters["Kevin Pillar"])
#print(pitchers["Tanner Roark"])
