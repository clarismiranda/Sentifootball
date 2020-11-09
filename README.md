# SentiFootball
This library performs sentiment analysis from a graph theory perspective on fan's tweets before a football match.

## Python packages
SentiFootball needs the next libraries to work:
- [Emoji] - Emoji library for python
- [Matplotlib] - 2D graphics library
- [Networkx] - Complex networks package
- [Nltk] - Natural language processing with python
- [Numpy] - Scientific computation package
- [Scipy] - Mathematics and science environment
- [Seaborn] - Data visualization library
- [Stanza] - Stanford NLP package
- [WordCloud] - Word cloud generator with python

[Emoji]: <https://github.com/carpedm20/emoji/>
[Matplotlib]: <https://matplotlib.org/>
[Networkx]: <https://networkx.org/>
[Nltk]: <https://www.nltk.org/>
[Numpy]: <https://numpy.org/>
[Scipy]: <https://www.scipy.org/>
[Seaborn]: <https://seaborn.pydata.org/>
[Stanza]: <https://stanfordnlp.github.io/stanza/>
[WordCloud]: <https://github.com/amueller/word_cloud>

## Environmental Vars
export TW_KEY=""\
export TW_SECRET=""

## Files Structure
```bash
├── GB
│   ├── 2019
│   │   ├── 38
│   │   │   ├── 1595772340_ARSWAT_neutral.json
│   │   │   ├── 1595772552_ARSWAT_positive.json
│   │   │   ├── 1595772607_ARSWAT_negative.json
│   │   │   ├── 1595773332_BURBHA_negative.json
│   │   │   ├── 1595773344_BURBHA_positive.json
│   │   │   ├── 1595773360_BURBHA_neutral.json

```

## Data Retrieval
Querying Twitter before a match can be performed by running.\
python search_twitter.py --home_team_id --away_team_id --week
```bash
python search_twitter.py CHE LIV 2
```
> Note: GB/GB_twitter.json contains the 3 letter code of the teams. 

## Dataset for Tweets
This command creates a whole dataset of all tweets in a week.\
python maps_tweets.py --country --season --week
```bash
python maps_tweets.py GB 2020 2
```

## Dataset Extras
This command creates a clean dataset and classifies tweet's polarity and support to a team.\
python process_tweets.py --country --season --week
```bash
python process_tweets.py GB 2020 2
```

## Frequencies Visualization
[visualization_sentiment.ipynb](https://github.com/clarismiranda/Sentifootball/blob/master/visualization_sentiment.ipynb) contains some visualizations of the weekgame.

## Graph Visualization
[graph_sentiment.ipynb](https://github.com/clarismiranda/Sentifootball/blob/master/graph_sentiment.ipynb) contains some visualizations of the weekgame from a graph theory perspective.