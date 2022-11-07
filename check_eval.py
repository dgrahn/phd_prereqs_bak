from libs.generator import *
from tqdm import trange

def convert_to_python(ast):
    """Converts the code to Python"""
    code = str(ast)
    code = code.replace(' {', ':')
    code = code.replace('} ', '')
    code = code.replace('}', '')

    lines = code.split('\n')
    lines[-1] = f'return {lines[-1]}'
    code = '\n\t'.join(lines)
    code = 'def task_fn():\n\t' + code
    return code

if __name__ == "__main__":
    generators = [
        ( 'Task 1', Task1Generator() ),
        ( 'Task 2', Task2Generator() ),
        ( 'Task 3', Task3Generator() ),
        ( 'Task 4', Task4Generator() ),
    ]

    # Iterate over the generators
    for name, gen in generators:

        print(name)
        for _ in trange(250_000):
            try:
                # Generate a new AST and evaluate it
                ast = gen.generate()
                result = ast.evaluate()
                
                # Convert the same AST to a function and evaluate it
                code = convert_to_python(ast)
                exec(code)
                exec_result = task_fn()

                # Make sure the results are the same
                assert exec_result == result

            except ZeroDivisionError as e:
                pass