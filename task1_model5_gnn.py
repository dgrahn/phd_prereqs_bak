import os
os.environ["CUDA_VISIBLE_DEVICES"] = "-1"

from libs.generator import Task4Generator
from libs.translators import NetworkXTranslator
# import tensorflow as tf
import numpy as np

# Constants
BATCH_SIZE = 32

if __name__ == "__main__":

    # Set seed for reproducibility
    # tf.keras.utils.set_random_seed(42)

    # Create the task
    task = Task4Generator()
    trans = NetworkXTranslator()

    
    for _ in range(10):
        ast = task.generate()
        graph = trans.translate(ast)
        print(graph)


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