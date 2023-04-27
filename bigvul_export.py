from libs import generator, translators
from rich.progress import Progress
import argparse
import pandas as pd
import sys
import tensorflow as tf

def get_samples(num_samples, task, tran):
    for _ in range(num_samples):
        ast = task.generate()
        yield {
            'target': int(ast.evaluate()),
            'processed_func': tran.translate(ast),
        }


def run_task(args):
    # Set seed for reproducibility
    tf.keras.utils.set_random_seed(42)

    # # Create the task
    task_class = getattr(generator, f'Task{args.task}Generator')
    task = task_class()
    tran = translators.BasicCTranslator()

    df_train = []
    df_test = []
    df_eval = []

    with Progress() as pb:
        p_epoch = pb.add_task('Epoch', total=args.epochs)
        p_steps = pb.add_task('Steps', total=args.train_steps + args.test_steps * 2)

        for _ in range(args.epochs):
            pb.update(task_id=p_steps, completed=0)
            for _ in range(args.train_steps):
                df_train.extend(get_samples(args.step_size, task, tran))
                pb.update(task_id=p_steps, advance=1)
            
            for _ in range(args.test_steps):
                df_test.extend(get_samples(args.step_size, task, tran))
                pb.update(task_id=p_steps, advance=1)
            
            for _ in range(args.test_steps):
                df_eval.extend(get_samples(args.step_size, task, tran))
                pb.update(task_id=p_steps, advance=1)

            pb.update(task_id=p_epoch, advance=1)

    df_train = pd.DataFrame(df_train)
    df_test = pd.DataFrame(df_test)
    df_eval = pd.DataFrame(df_eval)

    df_train.to_csv('train.csv', index=False)
    df_test.to_csv('test.csv', index=False)
    df_eval.to_csv('val.csv', index=False)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(prog='Task Sampler')
    parser.add_argument('-t', '--task', type=int)
    parser.add_argument('--step_size', type=int, default=32)
    parser.add_argument('--train_steps', type=int, default=10_000)
    parser.add_argument('--test_steps', type=int, default=1_000)
    parser.add_argument('--epochs', type=int, default=10)

    parser.add_argument('--seed', type=int, default=None)

    args = parser.parse_args()
    run_task(args)
