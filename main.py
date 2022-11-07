from libs.generator import Test4Generator
from libs.ast import *
from collections import defaultdict
import random

if __name__ == "__main__":
    gen = Test4Generator()

    split = defaultdict(int)

    for _ in range(1_000):
        try:
            ast = gen.generate()
            result = ast.evaluate()
            split[result] += 1
            print('-' * 20)
            print(ast, ' --> ', result)
        except ZeroDivisionError as e:
            print('-' * 20)
            print('Divide by Zero Error')
    
    print(split)