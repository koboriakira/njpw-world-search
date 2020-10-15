import pytest
from njpw_world_search import controller


@pytest.mark.skip(reason='firestoreを利用する')
def test_scrape_page():
    actual = controller.scrape_page(page=1)
    assert actual.length() == 24


@pytest.mark.skip(reason='firestoreを利用する')
def test_cooperate_to_elasticsearch():
    controller.cooperate_to_elasticsearch()
    assert False


def test_get_all_movie_id_by_json():
    print(controller._get_all_movie_id_by_json())
    assert False
