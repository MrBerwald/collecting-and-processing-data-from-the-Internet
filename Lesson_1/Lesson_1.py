import requests
import json
url ='https://api.github.com/'
user = 'MrBerwald'
token = ''

repos = requests.get('https://api.github.com/user/repos', auth=(user, token))


with open('data.json', 'w') as f:
    json.dump(repos.json(), f)

for i in repos.json():
    print(i['name'])