import pytest
from njpw_world_search import controller


@pytest.mark.skip(reason='tmp')
def test_scrape_page():
    actual = controller.scrape_page(page=1)
    assert actual.length() == 24


def test_cooperate_to_elasticsearch():
    controller.cooperate_to_elasticsearch()
    assert False
