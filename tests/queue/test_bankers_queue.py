import pytest
from src.queue.bankers_queue import BankersQueue


@pytest.fixture
def empty_queue():
    return BankersQueue()


class TestList:

    def test_truth_value(self, empty_queue):
        assert not empty_queue

        not_empty_queue = empty_queue.snoc(0)
        assert not_empty_queue

    def test_snoc_and_tail(self, empty_queue):
        queue = empty_queue.snoc(0).snoc(1).snoc(2).snoc(3).snoc(4)
        for i in range(5):
            assert queue.head() == i
            queue = queue.tail()

        assert not queue

    def test_snoc_and_tail_if_queue_is_branching(self, empty_queue):
        stem = empty_queue.snoc(0).snoc(1).snoc(2)
        branch1 = stem.snoc(3).snoc(4)
        branch2 = stem.snoc(-3).snoc(-4)

        for v in [0, 1, 2, 3, 4]:
            assert branch1.head() == v
            branch1 = branch1.tail()

        for v in [0, 1, 2, -3, -4]:
            assert branch2.head() == v
            branch2 = branch2.tail()

    def test_head_failed_if_queue_is_empty(self, empty_queue):
        with pytest.raises(IndexError):
            empty_queue.head()

    def test_tail_failed_if_queue_is_empty(self, empty_queue):
        with pytest.raises(IndexError):
            empty_queue.tail()
