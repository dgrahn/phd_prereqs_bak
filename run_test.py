import os
os.environ["CUDA_VISIBLE_DEVICES"] = "-1"

from libs import generator, models, translators
from libs.pipeline import dataset_generator, codebert_dataset
from libs.train import do_train
import argparse
import sys
import tensorflow as tf

# Constants
BATCH_SIZE = 32

def task1_basic():
    task = generator.Task1Generator()
    trans = translators.BasicFeatureTranslator()
    return dataset_generator(task, trans)

def task2_basic():
    task = generator.Task2Generator()
    trans = translators.BasicFeatureTranslator()
    return dataset_generator(task, trans)

def task3_basic():
    task = generator.Task3Generator()
    trans = translators.BasicFeatureTranslator()
    return dataset_generator(task, trans, max_size=34)

def task4_basic():
    task = generator.Task4Generator()
    trans = translators.BasicFeatureTranslator()
    return dataset_generator(task, trans)

def model4(task):
    trans = translators.PythonTranslator()
    pipe = codebert_dataset(task, trans, BATCH_SIZE)
    return models.model4_codebert(), pipe

model1_task1 = lambda: models.model1_mlp((3, 2)), task1_basic()
model1_task2 = lambda: models.model1_mlp((9, 2)), task2_basic()
model1_task3 = lambda: models.model1_mlp((34, 2)), task3_basic()
model1_task4 = lambda: models.model1_mlp((26, 2)), task4_basic()
model2_task1 = lambda: models.model2_cnn((3, 2)), task1_basic()
model2_task2 = lambda: models.model2_cnn((9, 2)), task2_basic()
model2_task3 = lambda: models.model2_cnn((34, 2)), task3_basic()
model2_task4 = lambda: models.model2_cnn((26, 2)), task4_basic()
model3_task1 = lambda: models.model3_lstm((3, 2)), task1_basic()
model3_task2 = lambda: models.model3_lstm((9, 2)), task2_basic()
model3_task3 = lambda: models.model3_lstm((34, 2)), task3_basic()
model3_task4 = lambda: models.model3_lstm((26, 2)), task4_basic()
model4_task1 = lambda: model4(generator.Task1Generator())
model4_task2 = lambda: model4(generator.Task2Generator())
model4_task3 = lambda: model4(generator.Task3Generator())
model4_task4 = lambda: model4(generator.Task4Generator())

def model5_task1():
    task = generator.Task1Generator()
    trans = translators.NetworkXTranslator()
    pipe = dataset_generator(task, trans)


    return model, pipe


def model5_task2(): raise NotImplementedError()
def model5_task3(): raise NotImplementedError()
def model5_task4(): raise NotImplementedError()


def run_test(args):
    # Set seed for reproducibility
    tf.keras.utils.set_random_seed(42)

    # Create the task
    func_name = f'model{args.model}_task{args.task}'
    model, pipe = getattr(sys.modules[__name__], func_name)()

    # Batch the pipeline
    pipe = pipe.batch(BATCH_SIZE)

    # Describe the model
    print(model.summary())

    # Train the model
    do_train(model, pipe, BATCH_SIZE)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(prog='Prereq Task Runner')
    parser.add_argument('--task', type=int)
    parser.add_argument('--model', type=int)

    args = parser.parse_args()
    run_test(args)