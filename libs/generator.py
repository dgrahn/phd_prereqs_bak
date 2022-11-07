from .ast import *
import random

class Generator:
    def generate(self):
        raise NotImplementedError()


class Test1Generator(Generator):
    """Test 1 - Comparison of ints
    > Test performance of models on simple relational operations.
    ```c
    [number 1] > [number 2]
    ```
    """
    def generate(self):
        left = ValueNode.random_int()
        right = ValueNode.random_int()
        operator = ComparisonNode.random_operator(include_equality=True)
        
        if operator in ComparisonNode.EQUALITY and random.random() > 0.5:
            right = left

        return ComparisonNode(left, operator, right)

class Test2Generator(Generator):
    def generate(self):
        x_var, y_var = VariableNode.random_variables(2)

        x_asn = AssignmentNode.random_int(x_var)
        y_asn = AssignmentNode.random_int(y_var)
        compare = ComparisonNode.random(x_var, y_var)


        assignments = [ x_asn, y_asn ]
        random.shuffle(assignments)

        sequence = SequenceNode(assignments + [compare])
        return sequence

