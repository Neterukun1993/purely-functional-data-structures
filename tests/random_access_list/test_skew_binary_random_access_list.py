import pytest
from src.random_access_list.skew_binary_random_access_list import (
    SkewBinaryRandomAccessList
)


@pytest.fixture
def empty_list():
    return SkewBinaryRandomAccessList()


class TestList:

    def test_truth_value(self, empty_list):
        assert not empty_list

        not_empty_list = empty_list.cons(0)
        assert not_empty_list

    def test_cons(self, empty_list):
        list_ = empty_list.cons(0).cons(1).cons(2)
        assert [list_.lookup(i) for i in range(3)] == [2, 1, 0]

    def test_cons_if_list_is_branching(self, empty_list):
        #             <- 3 <- 4 : branch1
        #            /
        # 0 <- 1 <- 2
        #            \
        #             <- 5 <- 6 : branch2
        stem = empty_list.cons(0).cons(1).cons(2)
        branch1 = stem.cons(3).cons(4)
        branch2 = stem.cons(5).cons(6)
        assert [branch1.lookup(i) for i in range(5)] == [4, 3, 2, 1, 0]
        assert [branch2.lookup(i) for i in range(5)] == [6, 5, 2, 1, 0]

    def test_head(self, empty_list):
        list_ = empty_list.cons(0).cons(1).cons(2)
        assert list_.head() == 2

    def test_head_failed_if_list_is_empty(self, empty_list):
        with pytest.raises(IndexError):
            empty_list.head()

    def test_tail(self, empty_list):
        list_ = empty_list.cons(0).cons(1).cons(2)
        tail = list_.tail()
        assert [tail.lookup(i) for i in range(2)] == [1, 0]

    def test_tail_if_list_is_branching(self, empty_list):
        # 0 <- 1 <- 2 <- 3 <- 4 : branch1
        #            \
        #             <- 5 <- 6 : branch2
        branch1 = empty_list.cons(0).cons(1).cons(2).cons(3).cons(4)
        branch2 = branch1.tail().tail().cons(5).cons(6)
        assert [branch1.lookup(i) for i in range(5)] == [4, 3, 2, 1, 0]
        assert [branch2.lookup(i) for i in range(5)] == [6, 5, 2, 1, 0]

    def test_tail_failed_if_list_is_empty(self, empty_list):
        with pytest.raises(IndexError):
            empty_list.tail()

    def test_update(self, empty_list):
        list_ = empty_list.cons(0).cons(1).cons(2).cons(3).cons(4)

        new = list_
        new = new.update(0, -4)
        assert [new.lookup(i) for i in range(5)] == [-4, 3, 2, 1, 0]
        new = new.update(1, -3) 
        assert [new.lookup(i) for i in range(5)] == [-4, -3, 2, 1, 0]
        new = new.update(2, -2)
        assert [new.lookup(i) for i in range(5)] == [-4, -3, -2, 1, 0]
        new = new.update(3, -1)
        assert [new.lookup(i) for i in range(5)] == [-4, -3, -2, -1, 0]
        new = new.update(4, 100)
        assert [new.lookup(i) for i in range(5)] == [-4, -3, -2, -1, 100]

        # list_ is persistent after update.
        assert [list_.lookup(i) for i in range(5)] == [4, 3, 2, 1, 0]
