import pytest
from src.sortable.bottom_up_merge_sort import BottomUpMergeSort


@pytest.fixture
def empty_sortable():
    return BottomUpMergeSort[int]()


class TestBottomUpMergeSort:

    def test_empty(self, empty_sortable):
        assert not empty_sortable

    def test_not_empty(self, empty_sortable):
        not_empty_sortable = empty_sortable.add(0)
        assert not_empty_sortable

    def test_add_ascending(self, empty_sortable):
        sortable = empty_sortable
        naive_list = []
        for v in range(5):
            sortable = sortable.add(v)
            naive_list.append(v)
            assert [v for v in sortable.sort()] == [v for v in sorted(naive_list)]

    def test_add_descending(self, empty_sortable):
        sortable = empty_sortable
        naive_list = []
        for v in reversed(range(5)):
            sortable = sortable.add(v)
            naive_list.append(v)
            assert [v for v in sortable.sort()] == [v for v in sorted(naive_list)]

    @pytest.mark.parametrize(('input_value', 'expected'), [
        ([1, 3, 2, 4, 5], [1, 2, 3, 4, 5]),
        ([2, 5, 4, 3, 1], [1, 2, 3, 4, 5]),
        ([3, 4, 5, 1, 2], [1, 2, 3, 4, 5]),
        ([5, 2, 1, 4, 3], [1, 2, 3, 4, 5]),
    ])
    def test_add_random(self, empty_sortable, input_value, expected):
        sortable = empty_sortable
        for v in input_value:
            sortable = sortable.add(v)
        assert [v for v in sortable.sort()] == expected
