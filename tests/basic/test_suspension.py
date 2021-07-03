from time import perf_counter
import pytest
from src.basic.suspension import Suspension


def fibonacci(n):
    if n <= 2:
        return 1
    else:
        return fibonacci(n - 2) + fibonacci(n - 1)


class TestSuspension:

    def test_suspension(self):
        func = (lambda: fibonacci(36))
        susp = Suspension(func)

        timestamp1 = perf_counter()
        result = susp.force()
        timestamp2 = perf_counter()
        memorized_result = susp.force()
        timestamp3 = perf_counter()

        assert result == memorized_result
        assert timestamp2 - timestamp1 >= 0.01
        assert timestamp3 - timestamp2 <= 0.01
