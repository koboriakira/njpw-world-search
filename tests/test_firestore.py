from njpw_world_search import firestore
from njpw_world_search.model.tag import Tag
from datetime import datetime as DateTime
import pytest

movie_id = 'testid'


@pytest.mark.skip(reason='firestoreを利用する')
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


@pytest.mark.skip(reason='firestoreを利用する')
def test_get_movie():
    # setup
    movie_id = 's_series_00554_25_02'

    # execute
    actual = firestore.get_movie(movie_id=movie_id)

    # verify
    title = 'SUMMER STRUGGLE 2020 Aug 26,2020 Tokyo・Korakuen Hall (English Commentary) 2ND MATCH Hiroshi Tanahashi, Kota Ibushi, Hiroyoshi Tenzan & Master Wato vs. Taichi, Zack Sabre Jr., Yoshinobu Kanemaru & DOUKI'
    assert actual['title'] == title


@pytest.mark.skip(reason='firestoreを利用する')
def test_extract_match_date():
    title = '2019年10月7日 東京・後楽園ホール 全試合'
    actual = firestore._extract_match_date(title=title)
    expect = DateTime.fromisoformat('2019-10-07 00:00:00')
    assert actual == expect

    title = 'Road to POWER STRUGGLE ～SUPER Jr. TAG LEAGUE 2019～ Oct 30,2019 Twin Messe Shizuoka (English Commentary) 5TH MATCH Hirooki Goto & Tomohiro Ishii & Toa Henare vs. Jay White & KENTA & Yujiro Takahashi'
    actual = firestore._extract_match_date(title=title)
    expect = DateTime.fromisoformat('2019-10-30 00:00:00')
    assert actual == expect
