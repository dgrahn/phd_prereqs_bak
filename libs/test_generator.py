from collections import defaultdict
from .generator import Test1Generator
from .ast import *
import pytest

class TestTest1Generator():
    def setup_method(self):
        self.gen = Test1Generator()
        self.max_rand = 100_000

    def test_is_50_50(self):
        # This tests to make sure each operator is 50/50
        is_true = defaultdict(int)
        totals = defaultdict(int)
        
        for _ in range(self.max_rand):
            node = self.gen.generate()
            totals[node.operator] += 1
            is_true[node.operator] += int(node.evaluate())
        
        assert sum(totals.values()) == self.max_rand
        assert pytest.approx(sum(is_true.values()) / sum(totals.values()), 0.1) == 0.5

        for op in totals.keys():
            assert pytest.approx(is_true[op] / totals[op], 0.1) == 0.5
