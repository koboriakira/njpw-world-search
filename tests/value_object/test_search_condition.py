from njpw_world_search.value_object.search_condition import SearchCondition


def test_init():
    text = 'オカダ・カズチカ 内藤　哲也'
    actual = SearchCondition(text=text)
    assert actual.keywords == ["オカダ", "カズチカ", "内藤", "哲也"]
