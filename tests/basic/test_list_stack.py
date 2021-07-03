import pytest
from src.basic.list_stack import ListStack


@pytest.fixture
def empty_list():
    return ListStack()


class TestList:

    def test_truth_value(self, empty_list):
        assert not empty_list

        not_empty_list = empty_list.cons(0)
        assert not_empty_list

    def test_cons(self, empty_list):
        list_ = empty_list.cons(0).cons(1).cons(2)
        assert [v for v in list_] == [2, 1, 0]

    def test_cons_when_branching(self, empty_list):
        stem = empty_list.cons(0).cons(1).cons(2)
        branch1 = stem.cons(3).cons(4)
        branch2 = stem.cons(-3).cons(-4)

        assert [v for v in branch1] == [4, 3, 2, 1, 0]
        assert [v for v in branch2] == [-4, -3, 2, 1, 0]

    def test_head(self, empty_list):
        list_ = empty_list.cons(0).cons(1).cons(2)
        assert list_.head() == 2

    def test_head_failed_if_list_is_empty(self, empty_list):
        with pytest.raises(IndexError):
            empty_list.head()

    def test_tail(self, empty_list):
        list_ = empty_list.cons(0).cons(1).cons(2)
        tail = list_.tail()

        assert [v for v in tail] == [1, 0]

    def test_tail_when_branching(self, empty_list):
        branch1 = empty_list.cons(0).cons(1).cons(2).cons(3).cons(4)
        branch2 = branch1.tail().tail().cons(-3).cons(-4)

        assert [v for v in branch1] == [4, 3, 2, 1, 0]
        assert [v for v in branch2] == [-4, -3, 2, 1, 0]

    def test_tail_failed_if_list_is_empty(self, empty_list):
        with pytest.raises(IndexError):
            empty_list.tail()

    def test_reverse(self, empty_list):
        list_ = empty_list.cons(0).cons(1).cons(2)
        reversed_list = list_.reverse()

        assert [v for v in reversed_list] == [0, 1, 2]

        # list_ are persistent after reversed
        assert [v for v in list_] == [2, 1, 0]

    def test_concat_two_list(self, empty_list):
        front = empty_list.cons(0).cons(1).cons(2)
        rear = empty_list.cons(3).cons(4).cons(5)

        concatenated_list = front.concat(rear)
        assert [v for v in concatenated_list] == [2, 1, 0, 5, 4, 3]

        # rear and front are persistent after concatenated
        assert [v for v in front] == [2, 1, 0]
        assert [v for v in rear] == [5, 4, 3]
