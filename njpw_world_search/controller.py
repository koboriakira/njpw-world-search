from njpw_world_search.value_object.search_condition import SearchCondition, SearchConditionException
from typing import List, Dict
from njpw_world_search.requests import RequestService
from njpw_world_search.scraper import Scraper
from njpw_world_search.firestore import set_movie, get_movie, grant_seq
from njpw_world_search.slack import Slack
from njpw_world_search.whoosh import search_whoosh


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
        movie: Dict = scrape_movie(movie_id=movie_id)
        set_movie(movie_id, movie)
        result.append(movie_id)
    return result


def _get_movie_id_list(page: int) -> List[str]:
    url = f'{ENDPOINT}search/latest?page={page}'
    html = RequestService(url).get()
    return Scraper(html=html).get_movie_id_list()


def scrape_movie_list(movie_id_list: List[str]):
    result: List[str] = []
    for movie_id in movie_id_list:
        url = f'{ENDPOINT}p/{movie_id}'
        try:
            html = RequestService(url).get()
            movie = Scraper(html=html).get_movie_detail()
            set_movie(movie_id, movie)
            result.append(movie_id)
        except Exception as e:
            Slack().post_message(f'{url}\n動画スクレイピングに失敗しました。\n{str(e)}')
            return result
    return result


def scrape_movie(movie_id: str) -> Dict:
    url = f'{ENDPOINT}p/{movie_id}'
    try:
        html = RequestService(url).get()
        movie = Scraper(html=html).get_movie_detail()
        set_movie(movie_id, movie)
        return movie
    except Exception as e:
        Slack().post_message(f'{url}\n動画スクレイピングに失敗しました。\n{str(e)}')
        raise e


def search_unregisted_movies(
        begin_page: int = 1,
        end_page: int = 10) -> List[str]:
    """
    未登録の動画を検索し、idのリストを返却します。
    """
    registed_movie_id_list: List[str] = _get_all_movie_id_by_json()
    result: List[str] = []
    for page in list(map(lambda p: p + begin_page,
                         range(end_page - begin_page + 1))):
        for movie_id in _get_movie_id_list(page=page):
            if movie_id not in registed_movie_id_list:
                result.append(movie_id)
    # Slackに共有
    if len(result) > 0:
        title = '未登録の動画IDリスト\n'
        movie_list = "\n".join(result)
        text = f'{title}{movie_list}'
        Slack().post_message(text=text)
    return result


def search_movies(cond: SearchCondition) -> Dict:
    """
    指定されたオプションをもとに動画を検索して返却します。
    """
    try:
        cond.validate()
    except SearchConditionException as e:
        return {"error": str(e)}

    result = search_whoosh(keywords=cond.keywords)['result']
    if 'error' in result and result['error']:
        messege = f'検索中に失敗がありました\n{result["error"]}\n{str(cond)}'
        Slack().post_message(messege)
        return result

    if cond.has_begin_date():
        result = list(filter(lambda r: 'datetime' in r and r['datetime'].astimezone(
        ) >= cond.begin_date, result))
    if cond.has_end_date():
        result = list(
            filter(
                lambda r: 'datetime' in r and r['datetime'].astimezone() <= cond.end_date,
                result))
    return {"movies": result}


# def cooperate_to_elasticsearch():
#     movie_id = 's_series_00553_1_01'
#     movie = get_movie(movie_id=movie_id)
#     res = elastic_search.insert(movie_id=movie_id, movie=movie)
#     return res['result'] == 'created'


def batch_execute():
    try:
        scrape_page(page=1, stop_if_exists=True)
        return True
    except Exception as e:
        print(e)
        return False
    finally:
        search_unregisted_movies(begin_page=1, end_page=5)


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
                movie: Dict = scrape_movie(movie_id=movie_id)
                movie['seq'] = seq
                set_movie(movie_id, movie)
                seq = seq + 1


def _only_in_japan():
    """
    これだけローカルで処理する
    """
    url = 'https://front.njpwworld.com/search?query=BRITISH%20J%20CUP'
    html = RequestService(url).get()
    movie_id_list = Scraper(html=html).get_movie_id_list()

    result: List[str] = []
    for movie_id in movie_id_list:
        print(movie_id)
        if get_movie(movie_id=movie_id) is not None:
            continue
        movie: Dict = scrape_movie(movie_id=movie_id)
        set_movie(movie_id, movie)
        result.append(movie_id)
    return result


def _get_all_movie_id_by_json() -> List[str]:
    import json
    import glob
    result: List[str] = []
    for filepath in glob.glob('json/*'):
        with open(filepath, 'r') as f:
            data = json.loads(f.read())
            result.extend(list(map(lambda m: m['id'], data['movies'])))
    return result
