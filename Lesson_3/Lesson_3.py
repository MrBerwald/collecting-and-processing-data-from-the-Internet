import json

from bs4 import BeautifulSoup as bs
import requests
from pprint import pprint
from pymongo import MongoClient

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.110 Safari/537.36 OPR/82.0.4227.50'
}
client = MongoClient('localhost', 27017)
main_url = 'https://hh.ru/search/vacancy'

db = client['parser_db']

series_col = db['hh_ru']

jobs_data = []

page = 0

while page != 5:
    params = {'text': 'Ruby',
              'page': page,
              'clusters': 'true',
              'ored_clusters': 'true',
              }
    response = requests.get(main_url, params=params, headers=headers)
    dom = bs(response.text, 'html.parser')
    res = dom.find('div', {'data-qa': 'vacancy-serp__results'})
    if not res:
        break

    vacancies = dom.find_all('div', {'class': 'vacancy-serp-item'})

    for vacancy in vacancies:
        data = {}
        src = vacancy.find('a', {'data-qa': 'vacancy-serp__vacancy-title'})
        name = src.text
        #company = vacancy.find('a', {'class': 'bloko-link bloko-link_kind-secondary'}).text
        url = src.get('href')
        data['name'] = name
        #data['company'] = company
        data["url"] = url

        try:
            salary = vacancy.find('span', {'data-qa': 'vacancy-serp__vacancy-compensation'}).text
            sr = salary.replace('\u202f', '').split()

            if sr[0] == 'от':
                data['salary_min'] = int(sr[1])
                data['salary_max'] = 0
                data['currency'] = sr[2]
            elif sr[0] == 'до' or '':
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

        if not dom.find('a', {'class': 'bloko-button'}):
            break


        def insert(collection, d):
            if not collection.find_one({'url': data['url']}) and data['salary_min'] is not None and data['salary_max'] is not None:
                return collection.insert_one(d).inserted_id


        insert(series_col, data)
        jobs_data.append(data)

    page += 1

    for i in series_col.find({"$or": [{'salary_min': {"$gt": 'salary'}}, {'salary_max': {"$gt": salary}}]}):
        pront(i)
pprint(jobs_data)
