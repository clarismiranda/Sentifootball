import json
import os
import sys
import urllib.parse
import requests
from requests.auth import AuthBase
from datetime import datetime

if len(sys.argv) > 3:
    # Setting country, league and season from system arguments
    # Main is a boolean to represent this league as principal
    home_team = sys.argv[1]
    away_team = sys.argv[2]
    match = sys.argv[3]
else:
    print("Wrong arguments were given, expected: --home_team --away_team --match")

# Fill these in. Generate tokens at https://developer.twitter.com/en/apps
# Retrieve key and host from terminal
CONSUMER_KEY = os.getenv('TW_KEY')
CONSUMER_SECRET = os.getenv('TW_SECRET')

country = 'GB'
season = '2020'

direcName = country + '/'
teams_json = direcName + country + "_twitter.json"

hashtag = "#"+home_team+away_team

sentiment = "neutral"

try:
    with open(teams_json) as json_file:
        dct_teams = json.load(json_file)
except:
    print("Cannot open json.")
    raise
try:
    home_h = dct_teams[home_team]["hashtag"]
    home_u = dct_teams[home_team]["mention"]
except:
    print("Cannot find home team.")
    raise

try:
    away_h = dct_teams[away_team]["hashtag"]
    away_u = dct_teams[away_team]["mention"]
except:
    print("Cannot find away team.")
    raise

q = "(" + hashtag + " OR " + home_h + " OR " + away_h + " OR " + home_u + " OR " + away_u

query_h = q + ") -filter:links -filter:replies -filter:retweets -filter:media"

query = urllib.parse.quote(query_h)

url= f"https://api.twitter.com/1.1/search/tweets.json?q={query}&result_type=recent&lang=en&count=100"

headers = {
    "Accept-Encoding": "gzip"
}

# Generates a bearer token with consumer key and secret
# via https://api.twitter.com/oauth2/token


class BearerTokenAuth(AuthBase):
    def __init__(self, consumer_key, consumer_secret):
        self.bearer_token_url = "https://api.twitter.com/oauth2/token"
        self.consumer_key = consumer_key
        self.consumer_secret = consumer_secret
        self.bearer_token = self.get_bearer_token()

    def get_bearer_token(self):
        response = requests.post(
            self.bearer_token_url,
            auth=(self.consumer_key, self.consumer_secret),
            data={'grant_type': 'client_credentials'},
            headers={'User-Agent': 'LabsRecentSearchQuickStartPython'})

        if response.status_code is not 200:
            raise Exception("Cannot get a Bearer token (HTTP %d): %s" %
                            (response.status_code, response.text))

        body = response.json()
        return body['access_token']

    def __call__(self, r):
        r.headers['Authorization'] = f"Bearer %s" % self.bearer_token
        r.headers['User-Agent'] = 'LabsRecentSearchQuickStartPython'
        return r

# Script starts here

# Create Bearer Token for authenticating with recent search
bearer_token = BearerTokenAuth(CONSUMER_KEY, CONSUMER_SECRET)

# Make a GET request to the Labs recent search endpoint
response = requests.get(url, auth=bearer_token, headers=headers)

if response.status_code is not 200:
    raise Exception(f"Request returned an error: %s" %
                    (response.status_code, response.text))

# Display the returned Tweet JSON
parsed = json.loads(response.text)
pretty_print = json.dumps(parsed, indent=2, sort_keys=True)
print(pretty_print)

now = datetime.now()
timestamp = int(datetime.timestamp(now))

direcName = direcName + season + '/' + match

try:
    # Create target Directory
    os.mkdir(direcName)
    print("Directory " , direcName ,  " Created ")
except FileExistsError:
    print("Directory " , direcName ,  " already exists")

file_search = direcName + '/'+ str(timestamp) + "_" + hashtag.strip("#") + "_" + sentiment + ".json"
with open(file_search, "w") as outfile: 
    outfile.write(pretty_print)