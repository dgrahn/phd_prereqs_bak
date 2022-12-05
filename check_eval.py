#!/usr/bin/env python3
"""check_eval.py: Validate the evaluation of ASTs.

For this project, we needed

Author: Dan Grahn
"""
from libs import generator, translators
from tqdm import trange

def convert_to_function(code, task):
    # """Converts the code to a Python function"""
    lines = code.split('\n')

    if task == 5:
        lines[-1] = f'\treturn {lines[-1]}'
        lines[-3] = f'\treturn {lines[-3]}'
    else:
        lines[-1] = f'return {lines[-1]}'

    code = '\n\t'.join(lines)
    code = 'def task_fn():\n\t' + code
    return code

if __name__ == "__main__":
    generators = [
        (1, generator.Task1Generator() ),
        (2, generator.Task2Generator() ),
        (3, generator.Task3Generator() ),
        (4, generator.Task4Generator() ),
        (5, generator.Task5Generator() ),
    ]

    trans = translators.PythonTranslator()

    # Iterate over the generators
    for num, gen in generators:

        print(f'Task {num}')
        for _ in trange(250_000):
            try:
                # Generate a new AST and evaluate it
                ast = gen.generate()
                result = ast.evaluate()
                
                # Convert the same AST to a function and evaluate it
                code = trans.translate(ast)
                code = convert_to_function(code, num)
                exec(code)
                exec_result = task_fn()

                # Make sure the results are the same
                assert exec_result == result

            except ZeroDivisionError as e:
                pass

    print(f'AST evaluation is correct for all tasks.')