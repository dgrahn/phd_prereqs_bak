import tensorflow as tf
import tensorflow_addons as tfa
import numpy as np
from libs.generator import Task1Generator
from libs.translators import Translator

from libs.ast import *
from typing import Any

class MLPFeatureTranslator(Translator):
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

    def gen_easy():
        while True:
            ast = task1.generate()
            features = trans.translate(ast)
            features[0] = (features[0] + 10_000) / 20_000
            features[1] /= 5
            features[2] = (features[2] + 10_000) / 20_000
            yield features, int(features[1] < 0.5)

    def gen():
        while True:
            ast = task1.generate()
            features = trans.translate(ast)
            features[0] = (features[0] + 10_000) / 20_000
            features[1] /= 5
            features[2] = (features[2] + 10_000) / 20_000
            yield features, int(ast.evaluate())
    
    pipe = tf.data.Dataset.from_generator(gen, output_types=(tf.float64, tf.int32))
    pipe = pipe.batch(32)


    inputs = tf.keras.Input(shape=(3,))
    x = tf.keras.layers.Dense(16, activation='relu')(inputs)
    x = tf.keras.layers.Dense(32, activation='relu')(x)
    x = tf.keras.layers.Dense(64, activation='relu')(x)
    outputs = tf.keras.layers.Dense(1, activation='sigmoid')(x)
    model = tf.keras.Model(inputs=inputs, outputs=outputs)
    print(model.summary())

    model.compile(optimizer='adam',
                loss='binary_crossentropy',
                metrics=[
                    'binary_accuracy',
                    tf.keras.metrics.TruePositives(name='tp'),
                    tf.keras.metrics.TrueNegatives(name='tn'),
                    tf.keras.metrics.FalsePositives(name='fp'),
                    tf.keras.metrics.FalseNegatives(name='fn'),
                ])

    model.fit(
        pipe,
        batch_size=32,
        epochs = 10,
        steps_per_epoch = 10_000,
        validation_data = pipe,
        validation_steps = 1_000,
    )

    for x, y in pipe:
        z = model.predict(x)
        for xi, yi, zi in zip(x, y, z):
            print(xi.numpy(), yi.numpy(), int(zi[0] > 0.5))
        break
