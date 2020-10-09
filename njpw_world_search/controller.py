from typing import List, Dict
from njpw_world_search.requests import RequestService
from njpw_world_search.scraper import Scraper
from njpw_world_search.model.movie import Movies
from njpw_world_search.firestore import set_movie, get_movie, get_batch, set_batch, grant_seq
from njpw_world_search import elastic_search
from njpw_world_search.slack import Slack


ENDPOINT = 'https://njpwworld.com/'


def scrape_page(page: int, stop_if_exists: bool = True) -> List[str]:
    """
    指定されたページにある動画をスクレイピングしてデータベースに登録します。
    すでに存在する動画をスクレイピングした場合は、その時点でスクレイピングを終了します。
    return 登録完了した動画のIDリスト
    """
    movie_id_list: List[str] = _get_movie_id_list(page=page)

    result: List[str] = []
    for movie_id in movie_id_list:
        if get_movie(movie_id=movie_id) is not None:
            if stop_if_exists:
                break
            else:
                continue
        movie: Dict = _get_movie(movie_id=movie_id)
        set_movie(movie_id, movie)
        result.append(movie_id)
    return result


def _get_movie_id_list(page: int) -> List[str]:
    url = f'{ENDPOINT}search/latest?page={page}'
    html = RequestService(url).get()
    return Scraper(html=html).get_movie_id_list()


def _get_movie(movie_id: str) -> Dict:
    try:
        url = f'{ENDPOINT}p/{movie_id}'
        html = RequestService(url).get()
        return Scraper(html=html).get_movie_detail()
    except Exception as e:
        Slack().post_message(f'${movie_id} 動画スクレイピングに失敗しました。\n{str(e)}')
        raise e


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


def batch_execute():
    batch = get_batch()
    try:
        scrape_page(page=batch['last_page'], stop_if_exists=False)
        batch['last_page'] = batch['last_page'] + 1
        set_batch(batch=batch)
        return True
    except Exception as e:
        print(e)
        return False


def grant_seq_batch_execute():
    MAX_PAGE = 535
    seq = 0
    for idx in range(MAX_PAGE):
        page = MAX_PAGE - idx
        movie_id_list = list(reversed(_get_movie_id_list(page=page)))
        for movie_id in movie_id_list:
            if get_movie(movie_id=movie_id) is not None:
                seq = grant_seq(movie_id=movie_id, seq=seq)
            else:
                print(f'データがなかったため新規作成しました {movie_id}')
                movie: Dict = _get_movie(movie_id=movie_id)
                movie['seq'] = seq
                set_movie(movie_id, movie)
                seq = seq + 1
