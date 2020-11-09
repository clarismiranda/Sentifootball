"""
    Analyzing Tweets
"""

import stanza
import emoji
import json
import pandas as pd
import re
from nltk.tokenize import TweetTokenizer

# Tokenizes text using TweetTokenizer
def emoji_tokenization(text):
    tknzr = TweetTokenizer()
    return tknzr.tokenize(text)

# Return 0 when both teams where mentioned
# -1 when away team only, 1 when home team only
def support(df, dct):
    label = []
    for index, row in df.iterrows():
        home_team = row["home_team"]
        away_team = row["away_team"]
        home_info = dct[home_team]
        away_info = dct[away_team]
        current_label = 0
        if home_info["mention"] in row["text"] or home_info["hashtag"] in row["text"]:
            current_label = 1
            if away_info["mention"] in row["text"] or away_info["hashtag"] in row["text"]:
                current_label = 0
        elif away_info["mention"] in row["text"] or away_info["hashtag"] in row["text"]:
            current_label = -1
        label.append(current_label)
    return label

# Using Stanford NLP to classify sentiment
def stanza_check(txt):
    txt = emoji_tokenization(txt)
    sentiment = nlp([txt]).sentences[0].sentiment
    # Negative
    if sentiment == 0:
        return -1
    # Neutral
    if sentiment == 1:
        return 0
    # Positive
    if sentiment == 2:
        return 1

# duplicates: number of records delete if it already exists in dataset
# multilingual: number of records delete if multilingual
# empty tweets: tweets deleted because were just mentions
def clean_data(df):
    resp = {
        "duplicates":0,
        "multilingual":0,
        "empty_tweets":0
    }
    act_rows = df.shape[0]
    df = df.drop(df.columns[0], axis=1)
    # Duplicates
    df = df.drop_duplicates()
    resp["duplicates"] = act_rows - df.shape[0]
    act_rows = df.shape[0]
    # Delete Mentions and replace hashtags
    df["no_mentions"] = df["text"].apply(lambda x: ' '.join(re.sub("(@[A-Za-z0-9]+)|([^0-9A-Za-z \t])|(\w+:\/\/\S+)"," ",x).split()))
    # Multilingual (To check if a tweet has multiple languages)
    df["multilingual"] = df["no_mentions"].apply(multilingual)
    # After deleting mention the tweet length was 0
    df = df[(df["multilingual"] != 2)]
    df = df.drop(columns=["multilingual"], axis=1)
    resp["empty_tweets"] = act_rows - df.shape[0]
    act_rows = df.shape[0]
    return df, resp

# Process create the cleanest text for use in Stanza
def get_sentiment(df, dct):
    # Support column
    df["support"] = support(df, dct)
    # Cleanest text and replace hashtags
    df["with_emojis"] = df["text"].apply(lambda x: ' '.join(re.sub("(\w+:\/\/\S+)"," ",x).split()))
    # Replaced unicode to emojis code
    df["with_emojis"] = df["with_emojis"].apply(lambda x: ' '.join(re.sub(u'[\U0001F1E6-\U0001F1FF]', " ", ' '.join(emoji.demojize(x, use_aliases=True, delimiters=("", "")).split('_')).strip()).split()))
    # Replace happy and sad strings with word happy or sad
    df["with_emojis"] = df["with_emojis"].apply(lambda x: ' '.join(re.sub("(?::|;|=)(?:-)?(?:\)|\|D|P)","good",x).split()))
    df["with_emojis"] = df["with_emojis"].apply(lambda x: ' '.join(re.sub("(?::|;|=)(?:-)?(?:\()","bad",x).split()))
    # Evaluate sentiment with stanza library from Stanford
    df["sentiment"] = df["with_emojis"].apply(stanza_check)
    return df

# Finds a score in the text either 0-0 or 0:0
def match_score(text):
    m = re.search(r'([0-9]+)\s*(:|-)\s*([0-9]+)', text)
    # If no match returns a neutral sentiment
    if m == None:
        return 0
    # If match favor home
    if m.group(1) > m.group(3):
        return 1
    # Favor against
    if m.group(3) > m.group(1):
        return -1
    # Draw
    return 0

# If a score is found change sentiment according to score favor and support
# if draw sentiment and support remains the same
def absolute_sentiment(df):
    support = []
    sentiment = []
    for index, row in df.iterrows():
        if row["score"] != 0:
            support.append(row["score"])
            sentiment.append(1)
        else:
            support.append(row["support"])
            sentiment.append(row["sentiment"])
    return support, sentiment

# Returns an absolute support when scores 0-0 are found
def get_scores(df):
    df["score"] = df["text"].apply(lambda x: match_score(x))
    df["m_support"], df["m_sentiment"] = absolute_sentiment(df)
    return df

if len(sys.argv) > 3:
    # Setting country, season and week from system arguments
    country = sys.argv[1]
    season = sys.argv[2]
    week = sys.argv[3]
else:
    print("Wrong arguments were given, expected: --country --season --week")

nlp = stanza.Pipeline('en', tokenize_no_ssplit=True, tokenize_pretokenized=True)

file_title = country + '/' + season + '/' + week + ".csv"

df = pd.read_csv(file_title)
print("Original dataset size: %s", str(df.shape))

# Load the dictionary of the current teams
file_title = country + '/' + country + '_twitter.json'
dct = dict()
with open(file_title, 'r') as j:
     dct = json.loads(j.read())

df_clean, resp = clean_data(df)
print("Removed tweets: %s", str(resp))
df_final = get_sentiment(df_clean, dct)
df_score = get_scores(df_final)

# Saving the clean and processed dataset
file_title = country + '/' + season + '/' + week + "_analysis.csv"
df_score.to_csv(file_title)
print(file_title)