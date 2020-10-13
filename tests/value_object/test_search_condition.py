from njpw_world_search.value_object.search_condition import SearchCondition, SearchConditionException
from datetime import date as Date
from datetime import datetime as DateTime
import pytest


def test_init():
    text = 'オカダ・カズチカ 内藤　哲也'
    begin_date = Date(2020, 10, 13)
    end_date = Date(2020, 10, 13)
    actual = SearchCondition(
        text=text,
        begin_date=begin_date,
        end_date=end_date)
    assert actual.keywords == ["オカダ", "カズチカ", "内藤", "哲也"]
    assert actual.begin_date == DateTime(2020, 10, 13)
    assert actual.end_date == DateTime(2020, 10, 13, 23, 59, 59)


def test_validate():
    with pytest.raises(SearchConditionException):
        SearchCondition().validate()
    with pytest.raises(SearchConditionException):
        SearchCondition(
            begin_date=Date(
                2019, 1, 1), end_date=Date(
                2018, 1, 1)).validate()
    with pytest.raises(SearchConditionException):
        SearchCondition(
            begin_date=Date(
                2017, 1, 1), end_date=Date(
                2018, 1, 2)).validate()
    SearchCondition(
        begin_date=Date(
            2017, 1, 1), end_date=Date(
            2018, 1, 1)).validate()
    SearchCondition(
        text='test',
        begin_date=Date(
            2017, 1, 1), end_date=Date(
            2018, 1, 2)).validate()
