from .ast import *
from typing import Any


class Translator:
    def translate(self, node:Node) -> Any:
        raise NotImplementedError()


class CodeTranslator(Translator):
    def translate(self, node:Node) -> Any:
        if isinstance(node, AssignmentNode): return self._assignment(node)
        if isinstance(node, CalculationNode): return self._calculation(node)
        if isinstance(node, ComparisonNode): return self._comparison(node)
        if isinstance(node, ConditionalNode): return self._conditional(node)
        if isinstance(node, OperatorNode): return self._operator(node)
        if isinstance(node, SequenceNode): return self._sequence_node(node)
        if isinstance(node, ValueNode): return self._value_node(node)
        if isinstance(node, VariableNode): return self._variable_node(node)
        raise NotImplementedError(f'Invalid type: {type(node)}')

    def _calculation(self, node:CalculationNode) -> Any:
        return self._operator(node)
    
    def _comparison(self, node:ComparisonNode) -> Any:
        return self._operator(node)

    def _assignment(self, node:AssignmentNode) -> Any:
        raise NotImplementedError('_assignment')        
    
    def _conditional(self, node:ConditionalNode) -> Any:
        raise NotImplementedError('_conditional')

    def _operator(self, node:OperatorNode) -> Any:
        raise NotImplementedError('_operator')
    
    def _sequence_node(self, node:SequenceNode) -> Any:
        raise NotImplementedError('_sequence_node')
    
    def _value_node(self, node:ValueNode) -> Any:
        raise NotImplementedError('_value_node')
    
    def _variable_node(self, node:VariableNode) -> Any:
        raise NotImplementedError('_variable_node')


class BasicCTranslator(CodeTranslator):
    def _assignment(self, node:AssignmentNode) -> Any:
        return f'{node.variable} = {node.value};'
    
    def _conditional(self, node:ConditionalNode) -> Any:
        r = f'if ({self.translate(node.condition)}) {{\n'
        r += f'\t{self.translate(node.if_node)}\n'
        r += '} else {\n'
        r += f'\t{self.translate(node.else_node)}\n'
        r += '}'
        return r

    def _operator(self, node:OperatorNode) -> Any:
        l_val = self.translate(node.left)
        r_val = self.translate(node.right)
        return f'{l_val} {node.operator} {r_val}'
    
    def _sequence_node(self, node:SequenceNode) -> Any:
        return '\n'.join(self.translate(n) for n in node.nodes)
    
    def _value_node(self, node:ValueNode) -> Any:
        return str(node.value)
    
    def _variable_node(self, node:VariableNode) -> Any:
        return node.name


class PythonTranslator(CodeTranslator):
    def _assignment(self, node:AssignmentNode) -> Any:
        return f'{node.variable} = {node.value}'
    
    def _conditional(self, node:ConditionalNode) -> Any:
        r = f'if {self.translate(node.condition)}:\n'
        r += f'\t{self.translate(node.if_node)}\n'
        r += 'else:\n'
        r += f'\t{self.translate(node.else_node)}'
        return r

    def _operator(self, node:OperatorNode) -> Any:
        l_val = self.translate(node.left)
        r_val = self.translate(node.right)
        return f'{l_val} {node.operator} {r_val}'
    
    def _sequence_node(self, node:SequenceNode) -> Any:
        return '\n'.join(self.translate(n) for n in node.nodes)
    
    def _value_node(self, node:ValueNode) -> Any:
        return str(node.value)
    
    def _variable_node(self, node:VariableNode) -> Any:
        return node.name

