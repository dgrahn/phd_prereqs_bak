from libs.ast import *
from libs.generator import Task2Generator
from libs.pipeline import dataset_generator
from libs.translators import BasicFeatureTranslator
import tensorflow as tf


if __name__ == "__main__":

    # Set seed for reproducability
    tf.keras.utils.set_random_seed(42)

    # Create the task
    task1 = Task2Generator()
    trans = BasicFeatureTranslator()

    # Create the pipeline    
    pipe = dataset_generator(task1, trans)
    pipe = pipe.batch(32)

    # Create the model
    inputs = tf.keras.Input(shape=(9, 2))
    x = tf.keras.layers.Conv1D(64, 3, activation='relu')(inputs)
    x = tf.keras.layers.Conv1D(128, 3, activation='relu')(inputs)
    x = tf.keras.layers.Flatten()(x)
    x = tf.keras.layers.Dense(64, activation='relu')(x)
    x = tf.keras.layers.Dense(32, activation='relu')(x)
    x = tf.keras.layers.Dense(16, activation='relu')(x)
    outputs = tf.keras.layers.Dense(1, activation='sigmoid')(x)
    model = tf.keras.Model(inputs=inputs, outputs=outputs)
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