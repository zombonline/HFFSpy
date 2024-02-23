import requests
from steam import Steam
from decouple import config
from datetime import datetime

KEY = config('STEAM_API_KEY')
game_app_id = '477160'
steam = Steam(KEY)


# The ID of the workshop item you want to get details about
published_file_id = '3011262911'

# The URL of the GetPublishedFileDetails endpoint
url = f"https://api.steampowered.com/ISteamRemoteStorage/GetPublishedFileDetails/v1/"

# The parameters for the request
params = {
    'key': KEY,
    'itemcount': 1,
    'publishedfileids[0]': published_file_id
}

# Send a POST request to the GetPublishedFileDetails endpoint
response = requests.post(url, data=params)

# Parse the JSON response
data = response.json()
user = data['response']['publishedfiledetails'][0]['creator']
print("tt" + user)
# Get the details of the workshop item
details = data['response']['publishedfiledetails'][0]

if('time_created' not in details):
    print("Date not available")
    time_created = "N/A"
else:
    time_created = datetime.fromtimestamp(details['time_created'])


user_player = user['player']
user_name = user_player['personaname']
if('loccountrycode' not in user_player):
    country = "N/A"
else:
    country = user_player['loccountrycode']
if('realname' not in user_player):
    user_bio = "N/A"
else:
    user_bio = user_player['realname']


# Print the name, author, and time created of the workshop item
print(f"Name: {details['title']}")
print(f"Author: {details['creator']}")
print(f"Time Created: {time_created}")
print(f"Country: {country}")
print(f"Tags: {details['tags']}")
print(f"Description: {details['description']}")
print(f"Author Name: {user_name}")
print(f"Author Bio: {user_bio}")
