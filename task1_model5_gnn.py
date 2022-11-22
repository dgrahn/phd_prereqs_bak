import os
os.environ["CUDA_VISIBLE_DEVICES"] = "-1"

from libs.generator import Task4Generator
from libs.models import model4_codebert
from libs.pipeline import codebert_dataset
from libs.translators import Translator, PythonTranslator
import tensorflow as tf
import numpy as np

# Constants
BATCH_SIZE = 32

from libs.ast import *
from typing import Any
import networkx as nx

class NetworkXTranslator(Translator):
    def translate(self, node):
        print('Translating')
        self.G = nx.DiGraph()
        self.node = 0
        self._translate(node)
        return self.G

    def add_node(self, label, **kwargs):
        self.node += 1
        self.G.add_node(self.node, label=label, **kwargs)
        return self.node

    def _assignment(self, node:AssignmentNode, **kwargs) -> Any:
        assign = self.add_node('ASSIGN', **kwargs)
        variable = self._translate(node.variable, order=0)
        value = self._translate(node.value, order=1)

        self.G.add_edge(assign, variable)
        self.G.add_edge(assign, value)
        return assign
        # return f'{node.variable} = {node.value}'
    
    def _conditional(self, node:ConditionalNode, **kwargs) -> Any:
        if_id = self.add_node('IFELSE')
        cond_id = self._translate(node.condition)
        if_node = self._translate(node.if_node)
        else_node = self._translate(node.else_node)

        self.G.add_edge(if_id, cond_id, label='CONDITION')
        self.G.add_edge(if_id, if_node, label='IF')
        self.G.add_edge(if_id, else_node, label='ELSE')
        return if_id

    def _operator(self, node:OperatorNode, **kwargs) -> Any:
        op_node = self.add_node('OPERATOR')
        l_node = self._translate(node.left, order=0)
        r_node = self._translate(node.right, order=1)

        self.G.add_edge(op_node, l_node)
        self.G.add_edge(op_node, r_node)
        return op_node
        # l_val = self._translate(node.left)
        # r_val = self._translate(node.right)
        # return f'{l_val} {node.operator} {r_val}'
    
    def _sequence_node(self, node:SequenceNode) -> Any:
        block = self.add_node('BLOCK')
        for i, node in enumerate(node.nodes):
            statement = self._translate(node, order=i)
            self.G.add_edge(block, statement)
        return block
        # return '\n'.join(self._translate(n) for n in node.nodes)
    
    def _value_node(self, node:ValueNode, **kwargs) -> Any:
        return self.add_node('VALUE', value=node.value, **kwargs)
        # return str(node.value)
    
    def _variable_node(self, node:VariableNode, **kwargs) -> Any:
        return self.add_node('VARIABLE', var=node.name, **kwargs)
        # return node.name

if __name__ == "__main__":

    # Set seed for reproducibility
    tf.keras.utils.set_random_seed(42)

    # Create the task
    task = Task4Generator()
    ast = task.generate()
    print('-' * 20)
    print(ast)


    python = PythonTranslator().translate(ast)
    print('-' * 20)
    print(python)

    print('-' * 20)
    g = NetworkXTranslator().translate(ast)
    print(g)
    from networkx.drawing.nx_pydot import write_dot
    write_dot(g, 'network.dot')


    # # Create the pipeline    
    # pipe = codebert_dataset(task, trans, BATCH_SIZE)

    # # Create the model
    # model = model4_codebert()
    # print(model.summary())

    # # Compile the model
    # model.compile(optimizer='adam',
    #             loss='binary_crossentropy',
    #             metrics=[
    #                 'binary_accuracy',
    #                 tf.keras.metrics.TruePositives(name='tp'),
    #                 tf.keras.metrics.TrueNegatives(name='tn'),
    #                 tf.keras.metrics.FalsePositives(name='fp'),
    #                 tf.keras.metrics.FalseNegatives(name='fn'),
    #             ])

    # # Train the model
    # model.fit(
    #     pipe,
    #     batch_size=BATCH_SIZE,
    #     epochs = 10,
    #     steps_per_epoch = 10_000,
    #     validation_data = pipe,
    #     validation_steps = 1_000,
    # )