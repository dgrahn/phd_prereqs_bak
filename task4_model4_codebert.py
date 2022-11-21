from libs.ast import *
from libs.generator import Task4Generator
from libs.models import model4_codebert
from libs.pipeline import codebert_dataset
from libs.translators import PythonTranslator
import tensorflow as tf

# Constants
BATCH_SIZE = 32

if __name__ == "__main__":

    # Set seed for reproducibility
    tf.keras.utils.set_random_seed(42)

    # Create the task
    task = Task4Generator()
    trans = PythonTranslator()  

    # Create the pipeline    
    pipe = codebert_dataset(task, trans, BATCH_SIZE)

    # Create the model
    model = model4_codebert()
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
        batch_size=BATCH_SIZE,
        epochs = 10,
        steps_per_epoch = 10_000,
        validation_data = pipe,
        validation_steps = 1_000,
    )