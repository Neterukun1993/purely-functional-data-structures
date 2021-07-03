import pytest
from src.heap.leftist_heap import LeftistHeap


@pytest.fixture
def empty_heap():
    return LeftistHeap()


class TestList:

    def test_truth_value(self, empty_heap):
        assert not empty_heap

        not_empty_heap = empty_heap.insert(0)
        assert not_empty_heap

    def test_insert_in_descending_order(self, empty_heap):
        heap = empty_heap
        for i in reversed(range(5)):
            heap = heap.insert(i)
            assert heap.find_min() == i

    def test_insert_in_ascending_order(self, empty_heap):
        heap = empty_heap
        for i in range(5):
            heap = heap.insert(i)
            assert heap.find_min() == 0

    def test_insert_same_values(self, empty_heap):
        heap = empty_heap
        for _ in range(5):
            heap = heap.insert(0)
            assert heap.find_min() == 0
        for _ in range(5):
            assert heap.find_min() == 0
            heap = heap.delete_min()

    def test_delete_min(self, empty_heap):
        heap = empty_heap
        for i in range(5):
            heap = heap.insert(i)
        for i in range(5):
            assert heap.find_min() == i
            heap = heap.delete_min()

    def test_delete_min_if_heap_is_branching(self, empty_heap):
        stem = empty_heap.insert(0).insert(1).insert(2)
        branch1 = stem.insert(3).insert(4)
        branch2 = stem.insert(-3).insert(-4)

        for v in [0, 1, 2, 3, 4]:
            assert branch1.find_min() == v
            branch1 = branch1.delete_min()

        for v in [-4, -3, 0, 1, 2]:
            assert branch2.find_min() == v
            branch2 = branch2.delete_min()

    def test_find_min_failed_if_heap_is_empty(self, empty_heap):
        with pytest.raises(IndexError):
            empty_heap.find_min()

    def test_delete_min_failed_if_heap_is_empty(self, empty_heap):
        with pytest.raises(IndexError):
            empty_heap.delete_min()
