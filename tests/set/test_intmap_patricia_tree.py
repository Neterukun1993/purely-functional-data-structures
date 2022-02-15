import pytest
from src.set.intmap_patricia_tree import IntMapPatriciaTree


@pytest.fixture
def empty_set():
    return IntMapPatriciaTree()


class TestIntmapPatriciaTree:

    def test_truth_value(self, empty_set):
        assert not empty_set
        set_ = empty_set.insert(0, 10)
        assert set_

    def test_insert_when_branching(self, empty_set):
        # (1, 100) + (2, 200) + (8, 800) - (3, 300) + (5, 500) : branch1
        #                                \
        #                                  (4, 400) + (6, 600) : branch2
        branch1 = empty_set.insert(1, 100).insert(2, 200).insert(8, 800)
        branch2 = branch1
        branch1 = branch1.insert(3, 300).insert(5, 500)
        branch2 = branch2.insert(4, 400).insert(6, 600)

        ephemeral_branch1 = {1: 100, 2: 200, 8: 800, 3: 300, 5: 500}
        ephemeral_branch2 = {1: 100, 2: 200, 8: 800, 4: 400, 6: 600}

        for key in range(10):
            if key in ephemeral_branch1:
                assert branch1.lookup(key) is not None
                assert branch1.lookup(key) == ephemeral_branch1[key]
            else:
                # key not in ephemeral_branch1
                assert branch1.lookup(key) is None

            if key in ephemeral_branch2:
                assert branch2.lookup(key) is not None
                assert branch2.lookup(key) == ephemeral_branch2[key]

    def test_insert_and_overwrite_value(self, empty_set):
        # (1, 100)   : branch1
        #          \
        #            (1, 999) overwrite : branch2
        branch1 = empty_set.insert(1, 100)
        branch2 = branch1.insert(1, 999)

        assert branch1.lookup(1) == 100
        assert branch2.lookup(1) == 999
