from libs.ast import *
from libs.generator import Task1Generator
from libs.model import model1_mlp
from libs.pipeline import dataset_generator
from libs.translators import BasicFeatureTranslator
import tensorflow as tf


if __name__ == "__main__":

    # Set seed for reproducibility
    tf.keras.utils.set_random_seed(42)

    # Create the task
    task1 = Task1Generator()
    trans = BasicFeatureTranslator()

    # Create the pipeline    
    pipe = dataset_generator(task1, trans)
    pipe = pipe.batch(32)

    # Create the model
    model = model1_mlp((3, 2))
    print(model.summary())

    # Compile the model
    model.compile(optimizer='adam',
                loss='binary_crossentropy',
                metrics=[
                    'binary_accuracy',
                    tf.keras.metrics.TruePositives(name='tp'),
                    tf.keras.metrics.TrueNegatives(name='tn'),
                    tf.keras.metrics.FalsePositives(name='fp'),
                    tf.keras.metrics.FalseNegatives(name='fn'),
                ])

    # Train the model
    model.fit(
        pipe,
        batch_size=32,
        epochs = 10,
        steps_per_epoch = 10_000,
        validation_data = pipe,
        validation_steps = 1_000,
    )