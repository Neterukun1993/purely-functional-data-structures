from time import perf_counter
import pytest
from src.basic.stream import Stream


@pytest.fixture
def empty_stream():
    return Stream()


class TestStream:

    def test_truth_value(self, empty_stream):
        assert not empty_stream

        not_empty_stream = empty_stream.cons(0)
        assert not_empty_stream

    def test_cons(self, empty_stream):
        stream = empty_stream.cons(0).cons(1).cons(2)
        assert [v for v in stream] == [2, 1, 0]

    def test_cons_when_branching(self, empty_stream):
        #             <- 3 <- 4 : branch1
        #            /
        # 0 <- 1 <- 2
        #            \
        #             <- 5 <- 6 : branch2
        stem = empty_stream.cons(0).cons(1).cons(2)
        branch1 = stem.cons(3).cons(4)
        branch2 = stem.cons(5).cons(6)
        assert [v for v in branch1] == [4, 3, 2, 1, 0]
        assert [v for v in branch2] == [6, 5, 2, 1, 0]

    def test_head(self, empty_stream):
        stream = empty_stream.cons(0).cons(1).cons(2)
        assert stream.head() == 2

    def test_head_failed_stream_is_empty(self, empty_stream):
        with pytest.raises(IndexError):
            empty_stream.head()

    def test_tail(self, empty_stream):
        stream = empty_stream.cons(0).cons(1).cons(2)
        tail = stream.tail()
        assert [v for v in tail] == [1, 0]

    def test_tail_when_branching(self, empty_stream):
        # 0 <- 1 <- 2 <- 3 <- 4 : branch1
        #            \
        #             <- 5 <- 6 : branch2
        branch1 = empty_stream.cons(0).cons(1).cons(2).cons(3).cons(4)
        branch2 = branch1.tail().tail().cons(5).cons(6)
        assert [v for v in branch1] == [4, 3, 2, 1, 0]
        assert [v for v in branch2] == [6, 5, 2, 1, 0]

    def test_tail_failed_if_stream_is_empty(self, empty_stream):
        with pytest.raises(IndexError):
            empty_stream.tail()

    def test_reverse(self, empty_stream):
        stream = empty_stream.cons(0).cons(1).cons(2)
        reversed_stream = stream.reverse()
        assert [v for v in reversed_stream] == [0, 1, 2]

        # strem is persistent after reversed.
        assert [v for v in stream] == [2, 1, 0]

    def test_concat_two_list(self, empty_stream):
        front = empty_stream.cons(0).cons(1).cons(2)
        rear = empty_stream.cons(3).cons(4).cons(5)
        concatenated_stream = front.concat(rear)
        assert [v for v in concatenated_stream] == [2, 1, 0, 5, 4, 3]

        # rear and front are persistent after concatenated.
        assert [v for v in front] == [2, 1, 0]
        assert [v for v in rear] == [5, 4, 3]

    def test_take(self, empty_stream):
        stream = empty_stream.cons(0).cons(1).cons(2).cons(3).cons(4)
        front3 = stream.take(3)
        assert [v for v in front3] == [4, 3, 2]

        # stream is persistent after take.
        assert [v for v in stream] == [4, 3, 2, 1, 0]

    def test_drop(self, empty_stream):
        stream = empty_stream.cons(0).cons(1).cons(2).cons(3).cons(4)
        rear2 = stream.drop(5 - 2)
        assert [v for v in rear2] == [1, 0]

        # stream is persistent after drop.
        assert [v for v in stream] == [4, 3, 2, 1, 0]


class TestStreamSuspention:

    def test_reverse(self, empty_stream):
        n = 10 ** 5

        stream = empty_stream
        for value in range(n):
            stream = stream.cons(value)

        # O(1): make suspension of reverse.
        start = perf_counter()
        stream = stream.reverse()
        end = perf_counter()
        assert end - start < 0.01

        # O(N): head from stream by proceeding suspension of reverse.
        #       reverse function is monolithic.
        start = perf_counter()
        head = stream.head()
        end = perf_counter()
        assert end - start > 0.01

        # O(1): head from stream.
        #       calculation result of reverse is memorized.
        start = perf_counter()
        head = stream.head()
        end = perf_counter()
        assert end - start < 0.01

    def test_concat(self, empty_stream):
        n = 10 ** 5
        m = 10 ** 5

        front = empty_stream
        for value in range(n):
            front = front.cons(value)
        rear = empty_stream
        for value in range(m):
            rear = rear.cons(value)

        # O(1): make suspension of concat.
        start = perf_counter()
        concatenated_stream = front.concat(rear)
        end = perf_counter()
        assert end - start < 0.01

        # O(1): tail from concatenated stream by proceeding suspension of concat.
        #       concat function is incremental.
        for _ in range(n + m):
            start = perf_counter()
            concatenated_stream = concatenated_stream.tail()
            end = perf_counter()
            assert end - start < 0.01

    def test_take(self, empty_stream):
        n = 10 ** 5
        k = 5 * 10 ** 4  # size of take elements

        stream = empty_stream
        for value in range(n):
            stream = stream.cons(value)

        # O(1): make suspension of take.
        start = perf_counter()
        stream = stream.take(k)
        end = perf_counter()
        assert end - start < 0.01

        # O(1): tail from concatenated stream by proceeding suspension of take.
        #       take function is incremental.
        for _ in range(k):
            start = perf_counter()
            stream = stream.tail()
            end = perf_counter()
            assert end - start < 0.01

    def test_drop(self, empty_stream):
        n = 10 ** 5
        k = 5 * 10 ** 4  # size of drop elements

        stream = empty_stream
        for value in range(n):
            stream = stream.cons(value)

        # O(1): make suspension of drop.
        start = perf_counter()
        stream = stream.drop(k)
        end = perf_counter()
        assert end - start < 0.01

        # O(k): head from stream by proceeding suspension of drop.
        #       drop function is monolithic.
        start = perf_counter()
        head = stream.head()
        end = perf_counter()
        assert end - start > 0.01

        # O(1): head from stream.
        #       calculation result of reverse is memorized.
        start = perf_counter()
        head = stream.head()
        end = perf_counter()
        assert end - start < 0.01
