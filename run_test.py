from libs import generator, models, translators
from libs.pipeline import dataset_generator, codebert_dataset, spektral_loader
from libs.train import do_train
import argparse
import spektral
import sys
import tensorflow as tf

# Constants
BATCH_SIZE = 32
EPOCHS = 10
STEPS_PER_EPOCH = 10_000
VALIDATION_STEPS = 1_000

def basic(task, **kwargs):
    trans = translators.BasicFeatureTranslator()
    return dataset_generator(task, trans, **kwargs)
 
task1_basic = lambda: basic(generator.Task1Generator())
task2_basic = lambda: basic(generator.Task2Generator())
task3_basic = lambda: basic(generator.Task3Generator(), max_size=34)
task4_basic = lambda: basic(generator.Task4Generator())
task5_basic = lambda: basic(generator.Task5Generator())

def model4(task):
    trans = translators.PythonTranslator()
    pipe = codebert_dataset(task, trans, BATCH_SIZE)
    return models.model4_codebert(), pipe

def model5(task):
    trans = translators.SpektralTranslator()
    dataset, loader = spektral_loader(task, trans,
        batch_size=BATCH_SIZE, epochs=EPOCHS,
        train_size=STEPS_PER_EPOCH, test_size=VALIDATION_STEPS)

    model = models.model5_gnn(dataset.n_node_features, dataset.n_edge_features)
    return model, loader

TASK1_SHAPE = (3, 2)
TASK2_SHAPE = (9, 2)
TASK3_SHAPE = (34, 2)
TASK4_SHAPE = (26, 2)
TASK5_SHAPE = (25, 2)

model1_task1 = lambda: (models.model1_mlp(TASK1_SHAPE), task1_basic())
model1_task2 = lambda: (models.model1_mlp(TASK2_SHAPE), task2_basic())
model1_task3 = lambda: (models.model1_mlp(TASK3_SHAPE), task3_basic())
model1_task4 = lambda: (models.model1_mlp(TASK4_SHAPE), task4_basic())
model1_task5 = lambda: (models.model1_mlp(TASK5_SHAPE), task5_basic())
model2_task1 = lambda: (models.model2_textcnn(TASK1_SHAPE), task1_basic())
model2_task2 = lambda: (models.model2_textcnn(TASK2_SHAPE), task2_basic())
model2_task3 = lambda: (models.model2_textcnn(TASK3_SHAPE), task3_basic())
model2_task4 = lambda: (models.model2_textcnn(TASK4_SHAPE), task4_basic())
model2_task5 = lambda: (models.model2_textcnn(TASK5_SHAPE), task5_basic())
model3_task1 = lambda: (models.model3_lstm(TASK1_SHAPE), task1_basic())
model3_task2 = lambda: (models.model3_lstm(TASK2_SHAPE), task2_basic())
model3_task3 = lambda: (models.model3_lstm(TASK3_SHAPE), task3_basic())
model3_task4 = lambda: (models.model3_lstm(TASK4_SHAPE), task4_basic())
model3_task5 = lambda: (models.model3_lstm(TASK5_SHAPE), task5_basic())
model4_task1 = lambda: model4(generator.Task1Generator())
model4_task2 = lambda: model4(generator.Task2Generator())
model4_task3 = lambda: model4(generator.Task3Generator())
model4_task4 = lambda: model4(generator.Task4Generator())
model4_task5 = lambda: model4(generator.Task5Generator())
model5_task1 = lambda: model5(generator.Task1Generator())
model5_task2 = lambda: model5(generator.Task2Generator())
model5_task3 = lambda: model5(generator.Task3Generator())
model5_task4 = lambda: model5(generator.Task4Generator())
model5_task5 = lambda: model5(generator.Task5Generator())


def run_test(args):
    # Set seed for reproducibility
    tf.keras.utils.set_random_seed(42)

    # Create the task
    func_name = f'model{args.model}_task{args.task}'
    model, pipe = getattr(sys.modules[__name__], func_name)()

    # Batch the pipeline
    try:
        pipe = pipe.batch(BATCH_SIZE)
    except:
        print('Not batching, usually expected.')

    # Describe the model
    print(model.summary())

    # Train the model
    do_train(model, pipe, BATCH_SIZE,
        epochs = EPOCHS,
        steps_per_epoch = STEPS_PER_EPOCH,
        validation_steps = VALIDATION_STEPS,
    )

    print(f'Complete model={args.model}, task={args.task}')

    model.save(f'models/model{args.model}_task{args.task}')


if __name__ == "__main__":
    parser = argparse.ArgumentParser(prog='Prereq Task Runner')
    parser.add_argument('--task', type=int)
    parser.add_argument('--model', type=int)

    args = parser.parse_args()
    run_test(args)
