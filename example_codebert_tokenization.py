from transformers import AutoTokenizer

def tokenize(tokenizer, string):
    for i in range(len(string)):
        print(string[:i], '=>')
        print('\t', tokenizer.tokenize(string[:i]))
        print('\t', tokenizer.encode(string[:i]))

def display_tokens():
    tokenizer = AutoTokenizer.from_pretrained("microsoft/codebert-base")

    pi = "3.1415926535"
    tokenize(tokenizer, pi)

    pi2 = "3.1515926535"
    tokenize(tokenizer, pi2)


if __name__ == "__main__":
    display_tokens()
