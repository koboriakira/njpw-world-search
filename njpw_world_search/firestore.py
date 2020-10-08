from google.cloud import firestore
from typing import Dict, Any

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
    doc_ref.set(movie)
    print(f'{movie_id}を記録しました')
    return True


def delete_movie(movie_id: str) -> None:
    """
    指定されたデータを削除します
    """
    db.collection(MOVIES).document(movie_id).delete()


def get_movie(movie_id: str) -> Dict[str, Any]:
    doc_ref = db.collection(MOVIES).document(movie_id)
    if doc_ref.get().exists:
        return doc_ref.get().to_dict()
    return {}


def get_all_movies() -> Dict[str, Any]:
    docs = db.collection(MOVIES).stream()
    result = {}
    for doc in docs:
        result[doc.id] = doc.to_dict()
    return result
