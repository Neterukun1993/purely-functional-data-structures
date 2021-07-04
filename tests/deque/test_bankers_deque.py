import pytest
from src.deque.bankers_deque import BankersDeque


@pytest.fixture
def empty_deque():
    return BankersDeque()


class TestBatchedDeque:

    def test_empty(self, empty_deque):
        assert not empty_deque

    def test_not_empty_after_cons(self, empty_deque):
        not_empty = empty_deque.cons(0)
        assert not_empty

    def test_not_empty_after_snoc(self, empty_deque):
        not_empty = empty_deque.snoc(0)
        assert not_empty

    def test_empty_after_tail(self, empty_deque):
        empty = empty_deque.cons(0).tail()
        assert not empty
        empty = empty_deque.snoc(0).tail()
        assert not empty

    def test_empty_after_init(self, empty_deque):
        empty = empty_deque.cons(0).init()
        assert not empty
        empty = empty_deque.snoc(0).init()
        assert not empty

    def test_cons(self, empty_deque):
        deque = empty_deque
        for value in range(100):
            deque = deque.cons(value)
            assert deque.head() == value
            assert deque.last() == 0

    def test_snoc(self, empty_deque):
        deque = empty_deque
        for value in range(100):
            deque = deque.snoc(value)
            assert deque.head() == 0
            assert deque.last() == value

    def test_cons_and_tail(self, empty_deque):
        deque = empty_deque
        for value in range(100):
            deque = deque.cons(value)
        for value in range(100):
            assert deque.head() == 99 - value
            assert deque.last() == 0
            deque = deque.tail()

    def test_cons_and_init(self, empty_deque):
        deque = empty_deque
        for value in range(100):
            deque = deque.cons(value)
        for value in range(100):
            assert deque.head() == 99
            assert deque.last() == value
            deque = deque.init()

    def test_snoc_and_tail(self, empty_deque):
        deque = empty_deque
        for value in range(100):
            deque = deque.snoc(value)
        for value in range(100):
            assert deque.head() == value
            assert deque.last() == 99
            deque = deque.tail()

    def test_snoc_and_init(self, empty_deque):
        deque = empty_deque
        for value in range(100):
            deque = deque.snoc(value)
        for value in range(100):
            assert deque.head() == 0
            assert deque.last() == 99 - value
            deque = deque.init()

    def test_if_deque_is_branching(self, empty_deque):
        stem = empty_deque.cons(0).cons(1).cons(2)
        branch1 = stem.cons(3).cons(4)
        branch2 = stem.cons(-3).cons(-4)
        branch3 = stem.snoc(3).snoc(4)
        branch4 = stem.snoc(-3).snoc(-4)
        branch5 = stem.cons(3).snoc(4)

        for v in [4, 3, 2, 1, 0]:
            assert branch1.head() == v
            assert branch1.last() == 0
            branch1 = branch1.tail()

        for v in [-4, -3, 2, 1, 0]:
            assert branch2.head() == v
            assert branch2.last() == 0
            branch2 = branch2.tail()

        for v in [2, 1, 0, 3, 4]:
            assert branch3.head() == v
            assert branch3.last() == 4
            branch3 = branch3.tail()

        for v in [2, 1, 0, -3, -4]:
            assert branch4.head() == v
            assert branch4.last() == -4
            branch4 = branch4.tail()

        for v in [3, 2, 1, 0, 4]:
            assert branch5.head() == v
            assert branch5.last() == 4
            branch5 = branch5.tail()

    def test_head_failed_if_deque_is_empty(self, empty_deque):
        with pytest.raises(IndexError):
            empty_deque.head()

    def test_tail_failed_if_deque_is_empty(self, empty_deque):
        with pytest.raises(IndexError):
            empty_deque.tail()

    def test_last_failed_if_deque_is_empty(self, empty_deque):
        with pytest.raises(IndexError):
            empty_deque.last()

    def test_init_failed_if_deque_is_empty(self, empty_deque):
        with pytest.raises(IndexError):
            empty_deque.init()
