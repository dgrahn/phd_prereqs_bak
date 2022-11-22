from .ast import *
from typing import Any
import numpy as np
import string


class Translator:
    def translate(self, node:Node) -> Any:
        return self._translate(node)

    def _translate(self, node:Node, **kwargs) -> Any:
        if isinstance(node, AssignmentNode): return self._assignment(node, **kwargs)
        if isinstance(node, CalculationNode): return self._calculation(node, **kwargs)
        if isinstance(node, ComparisonNode): return self._comparison(node, **kwargs)
        if isinstance(node, ConditionalNode): return self._conditional(node, **kwargs)
        if isinstance(node, OperatorNode): return self._operator(node, **kwargs)
        if isinstance(node, SequenceNode): return self._sequence_node(node, **kwargs)
        if isinstance(node, ValueNode): return self._value_node(node, **kwargs)
        if isinstance(node, VariableNode): return self._variable_node(node, **kwargs)
        raise NotImplementedError(f'Invalid type: {type(node)}')

    def _calculation(self, node:CalculationNode, **kwargs) -> Any:
        return self._operator(node, **kwargs)
    
    def _comparison(self, node:ComparisonNode, **kwargs) -> Any:
        return self._operator(node, **kwargs)

    def _assignment(self, node:AssignmentNode) -> Any:
        raise NotImplementedError('_assignment')        
    
    def _conditional(self, node:ConditionalNode) -> Any:
        raise NotImplementedError('_conditional')

    def _operator(self, node:OperatorNode) -> Any:
        raise NotImplementedError('_operator')
    
    def _sequence_node(self, node:SequenceNode) -> Any:
        raise NotImplementedError('_value_node')
    
    def _value_node(self, node:ValueNode) -> Any:
        raise NotImplementedError('_value_node')
    
    def _variable_node(self, node:VariableNode) -> Any:
        raise NotImplementedError('_variable_node')


class BasicCTranslator(Translator):
    def _assignment(self, node:AssignmentNode) -> Any:
        return f'{node.variable} = {node.value};'
    
    def _conditional(self, node:ConditionalNode) -> Any:
        r = f'if ({self._translate(node.condition)}) {{\n'
        r += f'\t{self._translate(node.if_node)}\n'
        r += '} else {\n'
        r += f'\t{self._translate(node.else_node)}\n'
        r += '}'
        return r

    def _operator(self, node:OperatorNode) -> Any:
        l_val = self._translate(node.left)
        r_val = self._translate(node.right)
        return f'{l_val} {node.operator} {r_val}'
    
    def _sequence_node(self, node:SequenceNode) -> Any:
        return '\n'.join(self._translate(n) for n in node.nodes)
    
    def _value_node(self, node:ValueNode) -> Any:
        return str(node.value)
    
    def _variable_node(self, node:VariableNode) -> Any:
        return node.name


class PythonTranslator(Translator):
    def _assignment(self, node:AssignmentNode) -> Any:
        return f'{node.variable} = {node.value}'
    
    def _conditional(self, node:ConditionalNode) -> Any:
        r = f'if {self._translate(node.condition)}:\n'
        r += f'\t{self._translate(node.if_node)}\n'
        r += 'else:\n'
        r += f'\t{self._translate(node.else_node)}'
        return r

    def _operator(self, node:OperatorNode) -> Any:
        l_val = self._translate(node.left)
        r_val = self._translate(node.right)
        return f'{l_val} {node.operator} {r_val}'
    
    def _sequence_node(self, node:SequenceNode) -> Any:
        return '\n'.join(self._translate(n) for n in node.nodes)
    
    def _value_node(self, node:ValueNode) -> Any:
        return str(node.value)
    
    def _variable_node(self, node:VariableNode) -> Any:
        return node.name


class BasicFeatureTranslator(Translator):
    IDS = { k:v for v, k in enumerate([
            '<', '<=', '>', '>=', '==', '!=',
            '=',
            '+', '-', '*', '/', '%',
            'if', 'do', 'else', 'end',
    ]) }

    VARS = { k:v for v, k in enumerate(string.ascii_lowercase) }
    OPERATOR = 0
    NUMBER = 1
    VARIABLE = 2

    def _get_operator(self, op):
        return [[ self.OPERATOR, self.IDS[op] ]]

    def _assignment(self, node:AssignmentNode) -> Any:
        return self._translate(node.variable) \
            + self._get_operator('=') \
            + self._translate(node.value)
    
    def _conditional(self, node:ConditionalNode) -> Any:
        return self._get_operator('if') \
            + self._translate(node.condition) \
            + self._get_operator('do') \
            + self._translate(node.if_node) \
            + self._get_operator('else') \
            + self._translate(node.else_node) \
            + self._get_operator('end')

    def _operator(self, node:OperatorNode) -> Any:
        return self._translate(node.left) \
            + self._get_operator(node.operator) \
            + self._translate(node.right)
    
    def _sequence_node(self, node:SequenceNode) -> Any:
        feats = []
        for child in node.nodes:
            feats += self._translate(child)

        return feats
    
    def _value_node(self, node:ValueNode) -> Any:
        return [[ self.NUMBER, node.value ]]
    
    def _variable_node(self, node:VariableNode) -> Any:
        return [[ self.VARIABLE, self.VARS[node.name] ]]
    
    def normalize(self, feats):
        # FIXME How do we handle unbounded numbers?
        feats = np.array(feats, dtype=np.float64)
        feats[feats[:, 0] == self.NUMBER, 1] /= 10_000
        # feats[feats[:, 0] == self.NUMBER, 1] += 0.5
        feats[feats[:, 0] == self.OPERATOR, 1] /= len(self.IDS)
        feats[feats[:, 0] == self.VARIABLE, 1] /= len(self.VARS)
        feats[:, 0] /= 2
        return feats
