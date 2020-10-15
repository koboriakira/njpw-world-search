from typing import List
import requests
import json

complete_pages = 465

endpoint = 'http://localhost:8000/movies/unregisted/'
endpoint_movie = 'http://localhost:8000/scrape/movie/'


def check():
    for page in list(map(lambda i: i + complete_pages + 1,
                         range(540 - complete_pages))):
        url = f'{endpoint}?begin_page={page}&end_page={page}'
        res = requests.get(url)
        if res.status_code != 200:
            print(res.status_code)
            print(res.text)
            exit()
        else:
            print(page, end=' ')
            movie_id_list: List[str] = json.loads(res.content)['result']
            print(movie_id_list)
            for movie_id in movie_id_list:
                url = f'{endpoint_movie}{movie_id}'
                res = requests.post(url)
                print(movie_id, json.loads(res.content)['result']['title'])


def scrape():
    from gazpacho import get, Soup
    url = 'https://front.njpwworld.com/search/latest?page=465'
    soup = Soup(get(url))
    movie_areas = soup.find('div', {'class': 'movieArea'})
    links = list(map(lambda m: m.find('a'), movie_areas))
    for link in links:
        movie_id = link[0].attrs['href'].replace('/p/', '')
        url = f'{endpoint_movie}{movie_id}'
        res = requests.post(url)


check()
