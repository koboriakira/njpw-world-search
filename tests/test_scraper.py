from njpw_world_search.scraper import Scraper
from njpw_world_search.requests import RequestService


@pytest.mark.skip(reason='firestoreを利用する')
def test_get_movie_id_list():
    # setup
    url = 'https://front.njpwworld.com/search/latest?page=534'
    html = RequestService(url=url).get()

    # execute
    actual = Scraper(html=html).get_movie_id_list()

    # verify
    expect = ['s_series_00005_1_1',
              's_series_00021_1_1',
              's_series_00004_2_1',
              's_series_00004_1_1',
              's_series_00003_1_1',
              's_series_00002_1_1',
              's_series_00001_1_1',
              'o_original_0093_92',
              'enc_test_1',
              'o_original_0001_2',
              'o_original_0055_1_01']

    assert actual == expect


@pytest.mark.skip(reason='firestoreを利用する')
def test_get_movie_detail():
    # setup
    url: str = 'https://njpwworld.com/p/s_series_00001_1_1'
    html = RequestService(url=url).get()

    # execute
    actual = Scraper(html=html).get_movie_detail()

    # verify
    assert actual['title'] == '闘魂シリーズ＆世界最強タッグ戦 1973年10月14日 蔵前国技館 世界最強タッグ戦 アントニオ猪木＆坂口征二 VS ルー・テーズ＆カール・ゴッチ'
    assert actual['tags'][0]['id'] == 'box_1'
    assert actual['tags'][0]['name'] == '東京・蔵前国技館'
    assert actual['tags'][0]['div'] == 'tag-box'
