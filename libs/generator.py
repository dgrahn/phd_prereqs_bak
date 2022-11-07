from .ast import *
from dataclasses import dataclass
import random

class Generator:
    def generate(self):
        raise NotImplementedError()

    def random_comparison(self, values):
        a_var, b_var = random.sample(values, 2)
        return ComparisonNode.random(a_var, b_var)

    def random_calculation(self, variables):
        var = random.choice(variables)
        
        # Swap where the variable and ints appear
        a = var
        b = ValueNode.random_int()
        if random.random() < 0.5: b, a = a, b

        # Build the node
        calc_node = CalculationNode.random(a, b)
        return AssignmentNode(var, calc_node)


class Task1Generator(Generator):
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


class Task2Generator(Generator):
    def generate(self):
        x_var, y_var = VariableNode.random_variables(2)

        x_asn = AssignmentNode.random_int(x_var)
        y_asn = AssignmentNode.random_int(y_var)
        compare = self.random_comparison([ x_var, y_var ])

        assignments = [ x_asn, y_asn ]
        random.shuffle(assignments)

        extra = self.extend(x_var, y_var)

        sequence = SequenceNode(assignments + extra + [compare])
        return sequence
    
    def extend(self, x_var, y_var):
        return []

@dataclass
class Task3Generator(Task2Generator):
    min_calcs: int = 1
    max_calcs: int = 5
    
    def extend(self, x_var, y_var):
        variables = [ x_var, y_var ]
        num_calcs = random.randint(self.min_calcs, self.max_calcs)

        return [
            self.random_calculation(variables)
            for _ in range(num_calcs)
        ]


class Task4Generator(Task2Generator):
    def extend(self, x_var, y_var):
        condition = self.random_comparison([
            x_var, y_var, ValueNode.random_int()
        ])
        if_node = self.random_calculation([ x_var, y_var ])
        else_node = self.random_calculation([ x_var, y_var ])

        return [ ConditionalNode(condition, if_node, else_node) ]
