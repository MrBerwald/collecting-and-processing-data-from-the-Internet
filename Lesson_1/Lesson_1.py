import requests
import json
url ='https://api.github.com/'
user = 'MrBerwald'
token = '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'

repos = requests.get('https://api.github.com/user/repos', auth=(user, token))


with open('data.json', 'w') as f:
    json.dump(repos.json(), f)

for i in repos.json():
    print(i['name'])