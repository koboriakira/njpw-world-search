from njpw_world_search.model.tag import TagClass


class TestTagClass:
    def test_to_enum(self):
        actual = TagClass.to_enum(value='tag-mic')
        assert actual == TagClass.MIC
