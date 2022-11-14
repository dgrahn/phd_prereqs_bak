import numpy as np
import tensorflow as tf
from transformers import RobertaTokenizer

def dataset_generator(gen, trans, max_size=None, do_normalize=True):
    def gen_fn():
        while True:
            ast = gen.generate()
            feats = trans.translate(ast)

            if do_normalize:
                feats = trans.normalize(feats)
            
            if max_size is not None:
                shape = list(feats.shape)
                shape[0] = max_size

                f2 = np.zeros(shape)
                f2[-len(feats):] = feats
                feats = f2
            
            try:
                yield feats, int(ast.evaluate())
            except ZeroDivisionError:
                pass
    
    return tf.data.Dataset.from_generator(gen_fn,\
        output_types=(tf.float64, tf.int32))

def codebert_dataset(task, trans, batch_size):
    tokenizer = RobertaTokenizer.from_pretrained("microsoft/codebert-base")

    while True:
        input_ids = np.zeros((batch_size, 512))
        attention_mask = np.zeros((batch_size, 512))
        labels = np.zeros((batch_size,))

        for i in range(batch_size):
            ast = task.generate()
            python = trans.translate(ast)
            record = tokenizer(python, padding="max_length", truncation=True)
            input_ids[i, :] = record['input_ids']
            attention_mask[i, :] = record['attention_mask']
            labels[i] = int(ast.evaluate())

        yield {
            'input_ids': np.array(input_ids),
            'attention_mask': np.array(attention_mask),
        }, np.array(labels)