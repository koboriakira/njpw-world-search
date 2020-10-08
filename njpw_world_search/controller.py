from typing import List, Dict
from njpw_world_search.requests import RequestService
from njpw_world_search.scraper import Scraper
from njpw_world_search.model.movie import Movie, Movies
from njpw_world_search.firestore import set_movie, delete_movie, get_movie
from njpw_world_search import elastic_search

ENDPOINT = 'https://njpwworld.com/'


def scrape_page(page: int, stop_if_exists: bool = True) -> List[str]:
    """
    指定されたページにある動画をスクレイピングしてデータベースに登録します。
    すでに存在する動画をスクレイピングした場合は、その時点でスクレイピングを終了します。
    return 登録完了した動画のIDリスト
    """
    url = f'{ENDPOINT}search/latest?page={page}'
    html = RequestService(url).get()
    movie_id_list: List[str] = Scraper(html=html).get_movie_id_list()

    result: List[str] = []
    for movie_id in movie_id_list:
        if get_movie(movie_id=movie_id) is not None:
            if stop_if_exists:
                break
            else:
                continue
        url = f'{ENDPOINT}p/{movie_id}'
        html = RequestService(url).get()
        movie: Dict = Scraper(html=html).get_movie_detail()
        set_movie(movie_id, movie)
        result.append(movie_id)
    return result


def search_movies(options: Dict) -> Dict:
    """
    指定されたオプションをもとに動画を検索して返却します。
    """
    movies: Movies = elastic_search.search(options=options)
    return movies.to_dict()


def sample():
    movie_id = 's_series_00559_11_1'
    # delete_movie(movie_id=movie_id)

    url = 'https://njpwworld.com/p/s_series_00559_11_1'
    html = RequestService(url).get()
    movie = Scraper(html=html).get_movie_detail()
    print(set_movie(movie_id=movie_id, movie=movie))


def cooperate_to_elasticsearch():
    movie_id = 's_series_00553_1_01'
    movie = get_movie(movie_id=movie_id)
    res = elastic_search.insert(movie_id=movie_id, movie=movie)
    return res['result'] == 'created'
