import pytest
from src.set.unbalanced_set import UnbalancedSet


@pytest.fixture
def empty_set():
    return UnbalancedSet[int]()


class TestUnbalancedSet:

    def test_empty(self, empty_set):
        assert not empty_set

    def test_not_empty(self, empty_set):
        not_empty_set = empty_set.insert(0)
        assert not_empty_set

    def test_add_ascending(self, empty_set):
        set_ = empty_set
        naive_set = set()
        for v in range(10):
            set_ = set_.insert(v)
            naive_set.add(v)
            for match_v in range(10):
                assert (match_v in naive_set) == set_.member(match_v)

    def test_add_descending(self, empty_set):
        set_ = empty_set
        naive_set = set()
        for v in reversed(range(10)):
            set_ = set_.insert(v)
            naive_set.add(v)
            for match_v in range(10):
                assert (match_v in naive_set) == set_.member(match_v)
