from lxml import html
import requests
from pprint import pprint
from datetime import datetime

main_url = 'https://yandex.ru/news'

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.110 Safari/537.36 OPR/82.0.4227.50'
}

response = requests.get(main_url, headers = headers)

dom = html.fromstring(response.text)

news_res = dom.xpath("//div[contains(@class, 'news-top-flexible')]//div[contains(@class, 'mg-card ')]")

data = []

for i in news_res:
    news = {}
    title_result = i.xpath(".//h2[contains(@class, 'mg-card__title')]/a/text()")
    link_result = i.xpath(".//h2[contains(@class, 'mg-card__title')]/a/@href")
    source_result = i.xpath(".//span[contains(@class, 'mg-card-source__source')]/a/text()")
    time_result = i.xpath(".//span[contains(@class, 'mg-card-source__time')]/text()")

    news['title'] = title_result[0].replace('\xa0', ' ') if len(title_result) else None
    news['link'] = link_result[0] if len(link_result) else None
    news['source'] = source_result[0] if len(source_result) else None
    news['datetime'] = datetime.now().strftime("%Y-%m-%d") + ' ' + time_result[0] if len(time_result) else None

    data.append(news)

pprint(data)


