from lib.generator import Test1Generator

if __name__ == "__main__":
    gen = Test1Generator()

    for _ in range(1_000):
        ast = gen.generate()
        print(ast.evaluate(), ast)