from google.cloud import firestore
from typing import Dict, Any, Optional
from datetime import datetime as DateTime
import re

MOVIES = 'movies'

db = firestore.Client()


def set_movie(movie_id: str, movie: Dict[str, Any]) -> bool:
    """
    指定されたデータを登録してTrueを返却します。
    すでに存在するデータの場合はFalseを返却します。
    """
    doc_ref = db.collection(MOVIES).document(movie_id)
    if doc_ref.get().exists:
        return False
    date: DateTime = _extract_match_date(movie['title'])
    movie['date'] = date
    doc_ref.set(movie)
    print(f'{movie_id}を記録しました')
    return True


def delete_movie(movie_id: str) -> None:
    """
    指定されたデータを削除します
    """
    db.collection(MOVIES).document(movie_id).delete()


def get_movie(movie_id: str) -> Optional[Dict[str, Any]]:
    doc_ref = db.collection(MOVIES).document(movie_id)
    if doc_ref.get().exists:
        return doc_ref.get().to_dict()
    return None


def get_all_movies() -> Dict[str, Any]:
    docs = db.collection(MOVIES).stream()
    result = {}
    for doc in docs:
        result[doc.id] = doc.to_dict()
    return result


def get_batch() -> Dict[str, Any]:
    return db.collection('batch').document('batch').get().to_dict()


def set_batch(batch: Dict) -> None:
    db.collection('batch').document('batch').set(batch)


def grant_seq(movie_id: str, seq: int) -> int:
    movie = db.collection(MOVIES).document(movie_id).get().to_dict()
    seq = seq + 1
    movie['seq'] = seq
    db.collection(MOVIES).document(movie_id).set(movie)
    return seq


def _update_movie_date(movie_id: str, movie: Dict[str, Any]) -> None:
    date: DateTime = _extract_match_date(movie['title'])
    movie['date'] = date
    db.collection(MOVIES).document(movie_id).set(movie)
    print(f'{movie_id}: {date}')


def _extract_match_date(title: str) -> Optional[DateTime]:
    match = re.search(r'\d{4}年\d{1,2}月\d{1,2}日', title)
    if match is not None:
        date_str = match.group()
        el = re.sub(r'(年|月|日)', '-', date_str).split('-')
        return DateTime(int(el[0]), int(el[1]), int(el[2]))

    match = re.search(
        r'\w{3,5}\s\d{1,2},\s*\d{4}',
        title)
    if match is not None:
        print(match)
        date_str = match.group()
        el = re.sub(r'(\s|,\s*)', '-', date_str).split('-')
        print(el)
        return DateTime(int(el[2]), _convert_month(el[0]), int(el[1]))

    return None


def _convert_month(month_str: str) -> int:
    values = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'June',
              'July', 'Aug', 'Sept', 'Oct', 'Nov', 'Dec']
    for idx, value in enumerate(values):
        if value == month_str:
            return idx + 1
    if month_str == 'Sep':
        return 9
    if month_str == 'Jul':
        return 7
    if month_str == 'Jun':
        return 6
    if month_str == 'March':
        return 3
    raise ValueError


# if __name__ == '__main__':
#     # 日付を作成するのに使う。今後は自動で入るようになっている
#     for movie_id, movie in get_all_movies().items():
#         movie = get_movie(movie_id=movie_id)
#         _update_movie_date(movie_id=movie_id, movie=movie)
