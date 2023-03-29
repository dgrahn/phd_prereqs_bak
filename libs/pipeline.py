from tqdm import tqdm
from transformers import RobertaTokenizer
import numpy as np
import spektral
import tensorflow as tf

class SpektralTaskDataset(spektral.data.dataset.Dataset):
    def __init__(self, task, trans, epochs, train_size, test_size):
        self.task = task
        self.trans = trans
        self.num_examples = epochs * (train_size + test_size)

        self.graphs = []

        with tqdm(total=self.num_examples) as pbar:
            while len(self.graphs) < self.num_examples:
                try:
                    ast = self.task.generate()
                    g = self.trans.translate(ast)
                    self.graphs.append(g)
                    pbar.update(1)
                except ZeroDivisionError:
                    pass
    
    def read(self):
        return self.graphs

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
            retry = True
            while retry:
                try:
                    ast = task.generate()
                    labels[i] = int(ast.evaluate())
                    python = trans.translate(ast)
                    record = tokenizer(python, padding="max_length", truncation=True)
                    input_ids[i, :] = record['input_ids']
                    attention_mask[i, :] = record['attention_mask']
                    retry = False
                except ZeroDivisionError:
                    pass


        yield {
            'input_ids': np.array(input_ids),
            'attention_mask': np.array(attention_mask),
        }, np.array(labels)

def spektral_loader(task, trans, batch_size, epochs, train_size, test_size):
    dataset = SpektralTaskDataset(task, trans, epochs=epochs, train_size=batch_size * train_size, test_size=batch_size * test_size)
    print('# Graphs:', dataset.n_graphs)
    print('# Labels:', dataset.n_labels)
    print('# Node Features:', dataset.n_node_features)
    print('# Edge Features:', dataset.n_edge_features)
    # print('# Nodes:', dataset.n_nodes)
    print('# Examples:', dataset.num_examples)
    print(dataset)

    return dataset, spektral.data.BatchLoader(dataset, batch_size=batch_size, shuffle=False)
