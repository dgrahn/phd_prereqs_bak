from .ast import *

class TestAssignmentNode:
    def test_str(self):
        assert str(AssignmentNode(VariableNode('x'), ValueNode(1))) == 'x = 1'
        assert str(AssignmentNode(VariableNode('y'), ValueNode(2))) == 'y = 2'

    def test_evaluate(self):
        node = AssignmentNode(VariableNode('x'), ValueNode(1))

        env = {}
        assert node.evaluate(env)
        assert 'x' in env
        assert env['x'] == 1

class TestComparisonNode:
    def setup_method(self):
        self.one = ValueNode(1)
        self.two = ValueNode(2)
    
    def test_evaluate(self):
        assert ComparisonNode(self.one, '<', self.two).evaluate()
        assert not ComparisonNode(self.two, '<', self.one).evaluate()

        assert ComparisonNode(self.one, '<=', self.two).evaluate()
        assert ComparisonNode(self.two, '<=', self.two).evaluate()

        assert not ComparisonNode(self.one, '>', self.two).evaluate()
        assert ComparisonNode(self.two, '>', self.one).evaluate()

        assert not ComparisonNode(self.one, '>=', self.two).evaluate()
        assert ComparisonNode(self.two, '>=', self.two).evaluate()

        assert not ComparisonNode(self.one, '==', self.two).evaluate()
        assert ComparisonNode(self.two, '==', self.two).evaluate()

        assert ComparisonNode(self.one, '!=', self.two).evaluate()
        assert not ComparisonNode(self.two, '!=', self.two).evaluate()

    def test_str(self):
        assert str(ComparisonNode(self.one, '<', self.two)) == '1 < 2'
        assert str(ComparisonNode(self.one, '<=', self.two)) == '1 <= 2'
        assert str(ComparisonNode(self.one, '>', self.two)) == '1 > 2'
        assert str(ComparisonNode(self.one, '>=', self.two)) == '1 >= 2'
        assert str(ComparisonNode(self.one, '==', self.two)) == '1 == 2'
        assert str(ComparisonNode(self.one, '!=', self.two)) == '1 != 2'

class TestValueNode:
    def test_str(self):
        assert str(ValueNode('a')) == 'a'
        assert str(ValueNode(1)) == '1'
    
    def test_eq(self):
        assert ValueNode('a') == ValueNode('a')
        assert ValueNode('a') != ValueNode('b')
        assert ValueNode(1) == ValueNode(1)
        assert ValueNode(1) != ValueNode(2)
    
    def test_evaluate(self):
        assert ValueNode('a').evaluate() == 'a'
        assert ValueNode(1).evaluate() == 1
    
    def test_random_int(self):
        assert isinstance(ValueNode.random_int().value, int)

        for _ in range(1_000):
            node = ValueNode.random_int(0, 10)
            assert 0 <= node.value and node.value <= 10

class TestVariableNode:
    def test_str(self):
        assert str(VariableNode('x')) == 'x'
        assert str(VariableNode('y')) == 'y'
        assert str(VariableNode('z')) == 'z'

    def test_evaluate(self):
        val = random.random()
        node = VariableNode('x')
        env = { 'x': val }
        assert node.evaluate(env) == val

class TestSequenceNode:
    def test_simple_false(self):
        x = VariableNode('x')
        y = VariableNode('y')

        x_assign = AssignmentNode(x, ValueNode(1))
        y_assign = AssignmentNode(y, ValueNode(2))
        compare = ComparisonNode(x, '>', y)
        sequence = SequenceNode([x_assign, y_assign, compare])

        assert str(sequence) == 'x = 1\ny = 2\nx > y'
        assert not sequence.evaluate()
    
    def test_simple_true(self):
        x = VariableNode('x')
        y = VariableNode('y')

        x_assign = AssignmentNode(x, ValueNode(3))
        y_assign = AssignmentNode(y, ValueNode(2))
        compare = ComparisonNode(x, '>', y)
        sequence = SequenceNode([x_assign, y_assign, compare])

        assert str(sequence) == 'x = 3\ny = 2\nx > y'
        assert sequence.evaluate()
        
