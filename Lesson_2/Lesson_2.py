import json

from bs4 import BeautifulSoup as bs
import requests

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.110 Safari/537.36 OPR/82.0.4227.50'
}

main_url = 'https://hh.ru/search/vacancy'

params = {'text': 'C++ junior',
          'page': 1,
          'salary': 'true',
          'clusters': 'true',
          'ored_clusters': 'true',
          }

jobs_data = []
response = requests.get(main_url, params=params, headers=headers)


while response.ok:
    dom = bs(response.text, 'html.parser')
    res = dom.find('div', {'data-qa': 'vacancy-serp__results'})
    if not res:
        break

    vacancies = dom.find_all('div', {'class': 'vacancy-serp-item'})

    for vacancy in vacancies:
        data = {}
        src = vacancy.find('a', {'data-qa': 'vacancy-serp__vacancy-title'})
        name = src.text
        company = vacancy.find('a', {'class': 'bloko-link bloko-link_secondary'}).text
        url = src.get('href')

        try:
            salary = vacancy.find('span', {'data-qa': 'vacancy-serp__vacancy-compensation'}).text
            sr = salary.replace('\u202f', '').split()

            if sr[0] == 'от':
                data['salary_min'] = int(sr[1])
                data['salary_max'] = 0
                data['currency'] = sr[2]
            elif sr[0] == 'до':
                data['salary_min'] = None
                data['salary_max'] = int(sr[1])
                data['currency'] = sr[2]
            else:
                data['salary_min'] = int(sr[0])
                data['salary_max'] = int(sr[2])
                data['currency'] = sr[3]
        except:
            data['salary_min'] = None
            data['salary_max'] = None
            data['currency'] = None
        data['name'] = name
        data['company'] = company
        data["url"] = url

        jobs_data.append(data)
    if not dom.find('a', {'data-qa': 'data-qa'}):
        break
    params['page'] += 1

print(jobs_data)

with open('result.json', 'w', encoding='utf-8') as f:
    json.dump(jobs_data, f)
