from espnscraper import parse_table
import numpy as np

#Goal: Predict players fantasy contributions based on previous seasons
#Methodology: Aggregate data from previous years and build a neural network to predict data from current years
#A player's "fantasy value" is the sum of their standardized scores in "fantasy categories"

batter_fantasy_categories = ['R', 'HR', 'RBI', 'SB', 'AVG']
pitcher_fantasy_categories = ['W', 'SV', 'SO', 'ERA', 'WHIP']
print("Collecting data...")
batters = []
startyear = 2017
endyear = 2017
statistics = []
for year in range(endyear - startyear + 1):
    print("Year: " + str(year + startyear))
    batters.append(parse_table(year + startyear, False))
    print("Aggregating yearly data...")
    yearstats = {}
    count = float(len(batters[year]))
    for name, playerstats in batters[year].items():
        for stat, value in playerstats.items():
            if not isinstance(value, str):
                if stat in yearstats:
                    yearstats[stat] += (value/count)
                else:
                    yearstats[stat] = (value/count)
    statistics.append(yearstats)
print("Data collection complete!")

print("Standardizing player data...")

#Outputs
for year in range(endyear - startyear + 1):
    for playerstats in batters[year].values():
        for stat, value in playerstats.items():
            if stat in statistics[year]:
                playerstats[stat] /= statistics[year][stat]
        playerstats["Fantasy"] = 0
        for cat in batter_fantasy_categories:
            playerstats["Fantasy"] += playerstats[cat]
print("Player data standardized!")
#print("Getting data for NN...")
#plan: convert batter data to a numpy array
#input array is the standardized data we scraped
#output array is the standardized fantasy data
rank = 1
for key in sorted(batters[endyear-startyear], key = lambda x: batters[endyear-startyear][x]["Fantasy"], reverse=True):
    print(str(rank) + ". " + key + " (" + str(batters[endyear-startyear][key]["Fantasy"]) + ")")
    rank += 1
