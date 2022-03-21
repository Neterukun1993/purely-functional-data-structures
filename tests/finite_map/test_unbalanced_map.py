import pytest
from src.finite_map.unbalanced_map import UnbalancedMap


@pytest.fixture
def empty_map():
    return UnbalancedMap[int, int]()


class TestUnbalancedMap:

    def test_empty(self, empty_map):
        assert not empty_map

    def test_not_empty(self, empty_map):
        not_empty_map = empty_map.bind(0, 0)
        assert not_empty_map

    def test_bind_ascending(self, empty_map):
        map_ = empty_map
        naive_map = dict()
        for key, value in zip(range(10), range(10)):
            map_ = map_.bind(key, value)
            naive_map[key] = value
            for match_key in range(10):
                if match_key in naive_map:
                    assert naive_map[match_key] == map_.lookup(match_key)

    def test_bind_descending(self, empty_map):
        map_ = empty_map
        naive_map = dict()
        for key, value in zip(reversed(range(10)), reversed(range(10))):
            map_ = map_.bind(key, value)
            naive_map[key] = value
            for match_key in range(10):
                if match_key in naive_map:
                    assert naive_map[match_key] == map_.lookup(match_key)

    def test_bind_when_branching(self, empty_map):
        # (0, 0) <- (1, 1) <- (2, 2) <- (3, 3): branch1
        #           (1, -1)             (3, -3): branch2
        branch1 = empty_map.bind(0, 0).bind(1, 1).bind(2, 2).bind(3, 3)
        branch2 = branch1.bind(1, -1).bind(3, -3)
        assert branch1.lookup(0) == 0
        assert branch1.lookup(1) == 1
        assert branch1.lookup(2) == 2
        assert branch1.lookup(3) == 3
        assert branch2.lookup(0) == 0
        assert branch2.lookup(1) == -1
        assert branch2.lookup(2) == 2
        assert branch2.lookup(3) == -3

    def test_lookup_failed_if_key_is_not_binded(self, empty_map):
        with pytest.raises(KeyError):
            empty_map.lookup(0)
