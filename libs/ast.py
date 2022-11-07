import random
import string

class Node:
    def evaluate(self, env=None):
        raise NotImplementedError()
    
    def _get_env(self, env):
        if env is None: return {}
        return env


class AssignmentNode(Node):
    @staticmethod
    def random_int(variable, min=-10_000, max=10_000):
        value = ValueNode.random_int(min, max)
        return AssignmentNode(variable, value)

    def __init__(self, variable, value):
        assert isinstance(variable, VariableNode)
        self.variable = variable
        self.value = value
    
    def __str__(self):
        return f'{self.variable} = {self.value}'
    
    def evaluate(self, env):
        self._get_env(env)[self.variable.name] = self.value.evaluate()
        return True


class ComparisonNode(Node):
    RELATIONAL = [ '<', '<=', '>', '>=' ]
    EQUALITY = [ '==', '!=' ]
    ALL_OPERATORS = RELATIONAL + EQUALITY

    @staticmethod
    def random(left, right, include_equality=False):
        op = ComparisonNode.random_operator(include_equality)
        return ComparisonNode(left, op, right)

    @staticmethod
    def random_operator(include_equality=False):
        if include_equality:
            return random.choice(ComparisonNode.ALL_OPERATORS)
        else:
            return random.choice(ComparisonNode.RELATIONAL)

    def __init__(self, left, operator, right):
        assert operator in ComparisonNode.ALL_OPERATORS, 'Invalid Operator'
        self.left = left
        self.right = right
        self.operator = operator

    def __str__(self):
        return f'{self.left} {self.operator} {self.right}'

    def evaluate(self, env=None):
        l_val = self.left.evaluate(env)
        r_val = self.right.evaluate(env)

        if self.operator == '<' : return l_val <  r_val
        if self.operator == '<=': return l_val <= r_val
        if self.operator == '>' : return l_val >  r_val
        if self.operator == '>=': return l_val >= r_val
        if self.operator == '==': return l_val == r_val
        if self.operator == '!=': return l_val != r_val


class SequenceNode(Node):
    def __init__(self, nodes):
        self.nodes = nodes
    
    def __str__(self):
        return '\n'.join(str(n) for n in self.nodes)
    
    def evaluate(self, env=None):
        env = self._get_env(env)

        result = None
        for node in self.nodes:
            result = node.evaluate(env)
        
        return result


class ValueNode(Node):
    def __init__(self, value):
        self.value = value
    
    def __str__(self):
        return str(self.value)

    def __eq__(self, other):
        return self.value == other.value

    def evaluate(self, env=None):
        return self.value
    
    @staticmethod
    def random_int(min=-10_000, max=10_000):
        return ValueNode(random.randint(min, max))

class VariableNode(Node):
    VARS = string.ascii_lowercase

    @staticmethod
    def random_variables(count=1):
        if count == 1:
            name = random.choice(VariableNode.VARS)
            return VariableNode(name)

        assert count < len(VariableNode.VARS), 'Too many vars'
        valid = list(VariableNode.VARS)
        random.shuffle(valid)
        return [ VariableNode(valid.pop()) for _ in range(count) ]

    def __init__(self, name):
        self.name = name
    
    def __str__(self):
        return self.name
    
    def evaluate(self, env):
        return env[self.name]

