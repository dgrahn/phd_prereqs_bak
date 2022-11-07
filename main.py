from libs.generator import Test2Generator
from libs.ast import *
import random

if __name__ == "__main__":
    gen = Test2Generator()

    for _ in range(1_000):
        ast = gen.generate()
        print('-' * 20)
        print(ast, ' --> ', ast.evaluate())