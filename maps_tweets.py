"""
    This script creates a csv from a week game on an specific country
"""

import json
import os
import sys
import pandas as pd
from pandas import json_normalize

if len(sys.argv) > 3:
    # Setting country, season and week from system arguments
    country = sys.argv[1]
    season = sys.argv[2]
    week = sys.argv[3]
else:
    print("Wrong arguments were given, expected: --country --season --week")

# Directory to find data
dirName = country + '/' + season + '/' + week + '/'

def decode_label(label):
    if label == "positive":
        return 1
    if label == "negative":
        return -1
    if label == "neutral":
        return 0

def decode_title(title):
    txt = title.split("_")
    limit = int(len(txt[1])/2)
    home_team = txt[1][0:limit]
    away_team = txt[1][limit:]
    if len(txt) > 2:
        end = txt[2].split(".")
        pre_label = decode_label(end[0])
    else:
        pre_label = 0
    return home_team, away_team, pre_label

"""Dictionary to count the total tweets obtained per game"""
dct_counts = dict()

df = pd.DataFrame()
dirWeek = os.listdir(dirName)
for game in dirWeek:
    if game == ".DS_Store":
        continue
    home_team, away_team, pre_label = decode_title(game)
    file_to_open = dirName + game
    with open(file_to_open) as f:
        response = json.load(f)
        tweets = response["statuses"]
        code_search = home_team + away_team
        if code_search not in dct_counts:
            dct_counts[code_search] = len(tweets)
        else:
            dct_counts[code_search] += len(tweets)
        for tweet in tweets:
            tweet_update = {
                "season": season,
                "weekgame": week,
                "home_team": home_team,
                "away_team": away_team,
                "favorite_count": tweet["favorite_count"],
                "lang": tweet["lang"],
                "retweet_count": tweet["retweet_count"],
                "retweeted": tweet["retweeted"],
                "text": tweet["text"],
                "followers_count": tweet["user"]["followers_count"],
                "verified": tweet["user"]["verified"],
                "user": tweet["user"]["screen_name"],
                "pre_label": pre_label
            }
            try:
                df = df.append(json_normalize(tweet_update))
            except:
                print(tweet_update)

# csv to save
file_title = country + '/' + season + '/' + week + ".csv"
print(file_title)
df.to_csv(file_title)
print(dct_counts)