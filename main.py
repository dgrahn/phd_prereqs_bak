from libs.generator import *
from libs.translators import BasicCTranslator, PythonTranslator
from tqdm import trange


if __name__ == "__main__":
    generators = [
        ( 'Task 1', Task1Generator() ),
        ( 'Task 2', Task2Generator() ),
        ( 'Task 3', Task3Generator() ),
        ( 'Task 4', Task4Generator() ),
    ]

    trans = BasicCTranslator()
    # trans = PythonTranslator()

    # Iterate over the generators
    for name, gen in generators:

        for _ in range(1):
            ast = gen.generate()
            python = trans.translate(ast)

            print('-' * 20)
            print(python, '=>', ast.evaluate())


        # print(name)
        # for _ in trange(250_000):
        #     try:
        #         # Generate a new AST and evaluate it
        #         ast = gen.generate()
        #         result = ast.evaluate()
                
        #         # Convert the same AST to a function and evaluate it
        #         code = convert_to_python(ast)
        #         exec(code)
        #         exec_result = task_fn()

        #         # Make sure the results are the same
        #         assert exec_result == result

        #     except ZeroDivisionError as e:
        #         pass