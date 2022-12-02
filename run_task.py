from libs import generator, translators
import argparse
import sys


def run_task(args):
    # Set seed for reproducibility
    if args.seed:
        import tensorflow as tf
        tf.keras.utils.set_random_seed(args.seed)

    # # Create the task
    task_class = getattr(generator, f'Task{args.task}Generator')
    task = task_class()
    tran = translators.PythonTranslator()

    for _ in range(args.num):
        print('-' * 40)
        ast = task.generate()
        print(tran.translate(ast))
        print('----->', ast.evaluate())

if __name__ == "__main__":
    parser = argparse.ArgumentParser(prog='Task Sampler')
    parser.add_argument('-t', '--task', type=int)
    parser.add_argument('-n', '--num', type=int, default=10)
    parser.add_argument('--seed', type=int, default=None)

    args = parser.parse_args()
    run_task(args)
