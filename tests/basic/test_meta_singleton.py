import pytest
from src.basic.meta_singleton import MetaSingleton


class TestMetaSingleton:

    class SampleSingleton(metaclass=MetaSingleton):
        def __init__(self):
            pass

    class InheritedSampleSingleton(SampleSingleton):
        def __init__(self):
            pass

    def test_singleton(self):
        obj_a = TestMetaSingleton.SampleSingleton()
        obj_b = TestMetaSingleton.SampleSingleton()
        assert obj_a is obj_b

    def test_singleton_instance(self):
        obj_a = TestMetaSingleton.InheritedSampleSingleton()
        obj_b = TestMetaSingleton.InheritedSampleSingleton()
        assert obj_a is obj_b
