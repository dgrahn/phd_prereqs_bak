import numpy as np
import tensorflow as tf

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