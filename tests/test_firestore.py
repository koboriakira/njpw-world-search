from njpw_world_search import firestore
from njpw_world_search.model.tag import Tag

movie_id = 'testid'


def test_set_movie():
    # setup
    tag = Tag(div='tag-man', id='tagtest', name='タグテスト')
    movie = {
        "id": movie_id,
        "title": 'test',
        "tags": [tag.to_dict()],
        "like_count": 0
    }

    # execute
    # データがないときはTrueを返す
    actual = firestore.set_movie(movie_id=movie_id, movie=movie)
    assert actual

    # データが存在するとFalseを返す
    actual = firestore.set_movie(movie_id=movie_id, movie=movie)
    assert not actual

    # データのクリーニング
    firestore.delete_movie(movie_id=movie_id)


def test_get_movie():
    # setup
    movie_id = 's_series_00554_25_02'

    # execute
    actual = firestore.get_movie(movie_id=movie_id)

    # verify
    title = 'SUMMER STRUGGLE 2020 Aug 26,2020 Tokyo・Korakuen Hall (English Commentary) 2ND MATCH Hiroshi Tanahashi, Kota Ibushi, Hiroyoshi Tenzan & Master Wato vs. Taichi, Zack Sabre Jr., Yoshinobu Kanemaru & DOUKI'
    assert actual['title'] == title
