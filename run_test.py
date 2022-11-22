import os
os.environ["CUDA_VISIBLE_DEVICES"] = "-1"

from libs.ast import *
from libs.generator import Task1Generator
from libs.models import model1_mlp
from libs.pipeline import dataset_generator
from libs.train import do_train
from libs.translators import BasicFeatureTranslator
import tensorflow as tf

# Constants
BATCH_SIZE = 32

if __name__ == "__main__":

    # Set seed for reproducibility
    tf.keras.utils.set_random_seed(42)

    # Create the task
    task = Task1Generator()
    trans = BasicFeatureTranslator()

    # Create the pipeline    
    pipe = dataset_generator(task, trans)
    pipe = pipe.batch(BATCH_SIZE)

    # Create the model
    model = model1_mlp((3, 2))
    print(model.summary())

    # Train the model
    do_train(model, pipe, BATCH_SIZE)
