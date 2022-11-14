import tensorflow as tf

def model1_mlp(input_shape):
    inputs = tf.keras.Input(shape=input_shape)
    x = tf.keras.layers.Flatten()(inputs)
    x = tf.keras.layers.Dense(64, activation='relu')(x)
    x = tf.keras.layers.Dense(32, activation='relu')(x)
    x = tf.keras.layers.Dense(16, activation='relu')(x)
    outputs = tf.keras.layers.Dense(1, activation='sigmoid')(x)
    model = tf.keras.Model(inputs=inputs, outputs=outputs)
    print(model.summary())

def model4_codebert(seq_length=512):
    from transformers import TFRobertaModel

    # Inputs
    input_word_ids = tf.keras.layers.Input(shape=(seq_length,), name='input_ids', dtype=tf.int32)
    input_mask = tf.keras.layers.Input(shape=(seq_length,), name='attention_mask', dtype=tf.int32)

    # Load pretrained core
    roberta_core = TFRobertaModel.from_pretrained("microsoft/codebert-base")
    roberta_core.trainable = False

    # Create a short classification MLP
    out = roberta_core([input_word_ids, input_mask])
    out = tf.keras.layers.Flatten()(out[0])
    out = tf.keras.layers.Dense(32, activation='tanh', name='dense1')(out)
    out = tf.keras.layers.Dense(16, activation='tanh', name='dense2')(out)
    out = tf.keras.layers.Dense(1, name='output', activation='sigmoid')(out)

    return tf.keras.Model(inputs=[input_word_ids, input_mask], outputs=out)