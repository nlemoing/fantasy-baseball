from espnscraper import parse_table
import numpy as np

#Goal: Predict players fantasy contributions based on previous seasons
#Methodology: Aggregate data from previous years and build a neural network to predict data from current years
#A player's "fantasy value" is the sum of their standardized scores in "fantasy categories"

batter_fantasy_categories = ['R', 'HR', 'RBI', 'SB', 'AVG']
pitcher_fantasy_categories = ['W', 'SV', 'SO', 'ERA', 'WHIP']
batters = []
startyear = 2017
endyear = 2017
mean = []
exsqr = []

def collect():
    for year in range(endyear - startyear + 1):
        batters.append(parse_table(year + startyear, False))
        yearmean = {}
        yearexsqr = {}
        count = float(len(batters[year]))
        for name, playerstats in batters[year].items():
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
        for playerstats in batters[year].values():
            for stat, value in playerstats.items():
                if stat in mean[year]:
                    playerstats[stat] -= mean[year][stat]
                    playerstats[stat] /= (exsqr[year][stat] - (mean[year][stat]**2))**0.5
            playerstats["Fantasy"] = 0
            for cat in batter_fantasy_categories:
                playerstats["Fantasy"] += playerstats[cat]

#plan: convert batter data to a numpy array
#input array is the standardized data we scraped
#output array is the standardized fantasy data
def fantasy_rank():
    rank = 1
    for key in sorted(batters[endyear-startyear], key = lambda x: batters[endyear-startyear][x]["Fantasy"], reverse=True):
        print(str(rank) + ". " + key + " (" + str(batters[endyear-startyear][key]["Fantasy"]) + ")")
        rank += 1

collect()
standardize()
fantasy_rank()
