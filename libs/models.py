import tensorflow as tf

def model1_mlp(input_shape):
    inputs = tf.keras.Input(shape=input_shape)
    x = tf.keras.layers.Flatten()(inputs)
    x = tf.keras.layers.Dense(64, activation='relu')(x)
    x = tf.keras.layers.Dense(32, activation='relu')(x)
    x = tf.keras.layers.Dense(16, activation='relu')(x)
    outputs = tf.keras.layers.Dense(1, activation='sigmoid')(x)
    return tf.keras.Model(inputs=inputs, outputs=outputs)

def model2_cnn(input_shape):
    inputs = tf.keras.Input(shape=input_shape)
    x = tf.keras.layers.Conv1D(128, 3, activation='relu')(inputs)
    x = tf.keras.layers.Flatten()(x)
    x = tf.keras.layers.Dense(64, activation='relu')(x)
    x = tf.keras.layers.Dense(32, activation='relu')(x)
    x = tf.keras.layers.Dense(16, activation='relu')(x)
    outputs = tf.keras.layers.Dense(1, activation='sigmoid')(x)
    return tf.keras.Model(inputs=inputs, outputs=outputs)

def model3_lstm(input_shape):
    inputs = tf.keras.Input(shape=input_shape)
    x = tf.keras.layers.LSTM(128)(inputs)
    x = tf.keras.layers.Flatten()(x)
    x = tf.keras.layers.Dense(64, activation='relu')(x)
    x = tf.keras.layers.Dense(32, activation='relu')(x)
    x = tf.keras.layers.Dense(16, activation='relu')(x)
    outputs = tf.keras.layers.Dense(1, activation='sigmoid')(x)
    return tf.keras.Model(inputs=inputs, outputs=outputs)

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

def model5_gnn(n_node_features, n_edge_features):
    import spektral
    X_in = tf.keras.layers.Input(shape=(n_node_features,))
    A_in = tf.keras.layers.Input(shape=(None,), sparse=True)
    E_in = tf.keras.layers.Input(shape=(n_edge_features,))
    I_in = tf.keras.layers.Input(shape=(), dtype=tf.int64)

    X_1 = spektral.layers.ECCConv(32, activation='relu')([X_in, A_in, E_in])
    X_2 = spektral.layers.ECCConv(32, activation='relu')([X_1, A_in, E_in])
    X_3 = spektral.layers.GlobalSumPool()(X_2)
    output = tf.keras.layers.Dense(1, activation='sigmoid')(X_3)

    return tf.keras.models.Model(inputs=[X_in, A_in, E_in], outputs=output)