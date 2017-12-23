from espnscraper import playerdata
import numpy as np

#Goal: Predict players fantasy contributions based on previous seasons
#Methodology: Aggregate data from previous years and build a neural network to predict data from current years
#A player's "fantasy value" is the sum of their standardized scores in "fantasy categories"
#fantasy categories
batter_fantasy_categories = ['R', 'HR', 'RBI', 'SB', 'AVG']
pitcher_fantasy_categories = ['W', 'SV', 'SO', 'ERA', 'WHIP']
#data containers
players = {}
mean = []
exsqr = []
#inputs
mode = False
startyear = 2017
endyear = startyear
fantasycategories = []

def initialize(s, e, m, exp = True, std = True):
    global mode, startyear, endyear, fantasycategories, players
    mode = m
    startyear = s
    endyear = e
    if endyear < startyear:
        endyear = startyear
    if mode:
        fantasycategories = pitcher_fantasy_categories
    else:
        fantasycategories = batter_fantasy_categories
    collect(exp)
    if std:
        standardize()

def collect(exp):
    for year in range(startyear, endyear + 1):
        print("Collecting data for {}...".format(year))
        players[year] = playerdata(year, mode, exp)
        yearmean = {}
        yearexsqr = {}
        count = float(len(players[year]))
        for name, playerstats in players[year].items():
            for stat, value in playerstats.items():
                if not isinstance(value, str):
                    if stat in yearmean:
                        yearmean[stat] += (value/count)
                        yearexsqr[stat] += ((value**2)/count)
                    else:
                        yearmean[stat] = (value/count)
                        yearexsqr[stat] = ((value**2)/count)
        mean.append(yearmean)
        exsqr.append(yearexsqr)

def standardize():
    for year in range(endyear - startyear + 1):
        for playerstats in players[year + startyear].values():
            for stat, value in playerstats.items():
                if stat in mean[year]:
                    playerstats[stat] -= mean[year][stat]
                    playerstats[stat] /= (exsqr[year][stat] - (mean[year][stat]**2))**0.5
                if stat == "ERA" or stat == "WHIP":
                    playerstats[stat] *= -1

#plan: convert batter data to a numpy array
#input array is the standardized data we scraped
#output array is the standardized fantasy data
def fantasy(year):
    for player in players[year].values():
        player["Fantasy"] = 0
        for cat in fantasycategories:
            playerstats["Fantasy"] += playerstats[cat]

def search(year, category, count = 10):
    rank = 1
    for key in sorted(players[year], key = lambda x: players[year][x][category], reverse=True):
        if rank > count:
            break
        print(str(rank) + ". " + key + " (" + str(players[year][key][category]) + ")")
        rank += 1

#transform target year to dictionary of lists (just raw data)
def converttolist(year, fantasyonly):
    ret = {}
    for name, playerstats in players[year].items():
        data = []
        for stat, value in playerstats.items():
            if isinstance(value, str) or (fantasyonly and not stat in fantasycategories):
                continue
            data.append(value)
        ret[name] = data
    return ret

def getoutput():
    return converttolist(endyear, True)

def getinput():
    inp = []
    for year in range(startyear, endyear):
        inp.append(converttolist(year, False))
    return inp

