# print('Importing tensorflow...')
# import tensorflow as tf
# print('Done')
from libs.generator import Task1Generator
from libs.translators import CodeTranslator

from libs.ast import *
from typing import Any

class MLPFeatureTranslator(CodeTranslator):
    IDS = {
        k:v
        for v, k in enumerate([
            '<', '<=', '>', '>=', '==', '!='
        ])
    }

    def _assignment(self, node:AssignmentNode) -> Any:
        raise NotImplementedError('_assignment')        
    
    def _conditional(self, node:ConditionalNode) -> Any:
        raise NotImplementedError('_conditional')

    def _operator(self, node:OperatorNode) -> Any:
        return self.translate(node.left) \
            + [ MLPFeatureTranslator.IDS[node.operator] ] \
            + self.translate(node.right)
        # raise NotImplementedError('_operator')
    
    def _sequence_node(self, node:SequenceNode) -> Any:
        raise NotImplementedError('_sequence_node')
    
    def _value_node(self, node:ValueNode) -> Any:
        return [ node.value ]
    
    def _variable_node(self, node:VariableNode) -> Any:
        raise NotImplementedError('_variable_node')


if __name__ == "__main__":

    task1 = Task1Generator()
    trans = MLPFeatureTranslator()

    
    
    print('Generating...')
    for i, r in enumerate(task1.generator()):
        t = trans.translate(r)
        print(r, len(t))
        # print(t)

        if i > 10: break
