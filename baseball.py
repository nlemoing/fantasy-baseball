from espnscraper import playerdata, batter_categories, pitcher_categories
import numpy as np
import sys

#Goal: Predict players fantasy contributions based on previous seasons
#Methodology: Aggregate data from previous years and build a neural network to predict data from current years
#A player's "fantasy value" is the sum of their standardized scores in "fantasy categories"
#fantasy categories
batter_fantasy_categories = ['R', 'HR', 'RBI', 'SB', 'AVG']
pitcher_fantasy_categories = ['W', 'SV', 'SO', 'ERA', 'WHIP']
#data containers
players = []
mean = []
exsqr = []
#inputs
mode = False
exporting = True
startyear = 2017
endyear = startyear
#handle command line arguments
for count in range(len(sys.argv)):
    arg = sys.argv[count]
    if arg == "noexp":
        exporting = False
    elif arg == "pitching":
        mode = True
    elif arg == "batting":
        mode = False
    elif arg == "start":
        try:
            startyear = int(sys.argv[count + 1])
        except:
            pass
    elif arg == "end":
        try:
            endyear = int(sys.argv[count + 1])
        except:
            pass
if endyear < startyear:
    endyear = startyear
if mode:
    print("Mode selected: Pitching")
else:
    print("Mode selected: Batting")

def collect():
    data = []
    for year in range(endyear - startyear + 1):
        print("Collecting data for " + str(year + startyear))
        players.append(playerdata(year + startyear, mode, exporting))
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
        print(yearmean)
        print(yearexsqr)
        mean.append(yearmean)
        exsqr.append(yearexsqr)

def standardize():
    for year in range(endyear - startyear + 1):
        for playerstats in players[year].values():
            for stat, value in playerstats.items():
                if stat in mean[year]:
                    playerstats[stat] -= mean[year][stat]
                    playerstats[stat] /= (exsqr[year][stat] - (mean[year][stat]**2))**0.5
                if stat == "ERA" or stat == "WHIP":
                    playerstats[stat] *= -1
            playerstats["Fantasy"] = 0
            if mode:
                fantasycategories = pitcher_fantasy_categories
            else:
                fantasycategories = batter_fantasy_categories
            for cat in fantasycategories:
                playerstats["Fantasy"] += playerstats[cat]

#plan: convert batter data to a numpy array
#input array is the standardized data we scraped
#output array is the standardized fantasy data
def fantasyrank(year):
    rank = 1
    for key in sorted(players[year-startyear], key = lambda x: players[endyear-startyear][x]["Fantasy"], reverse=True):
        print(str(rank) + ". " + key + " (" + str(players[endyear-startyear][key]["Fantasy"]) + ")")
        rank += 1


