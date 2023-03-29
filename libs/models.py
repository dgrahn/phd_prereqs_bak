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

def model2_textcnn(input_shape):
    feature_size, embed_size = input_shape
    num_filters = 128
    dropout_rate=0.5

    inputs = tf.keras.Input(shape=input_shape, name='input_data')
    embed = tf.keras.layers.Reshape((input_shape[0], input_shape[1], 1), name='add_channel')(inputs)#(embed)

    pool_outputs = []
    for filter_size in [3]:#[3, 4, 5]:
        filter_shape = (filter_size, embed_size)
        conv = tf.keras.layers.Conv2D(num_filters, filter_shape, strides=(1, 1), padding='valid',
                                   data_format='channels_last', activation='relu',
                                   kernel_initializer='glorot_normal',
                                   bias_initializer=tf.keras.initializers.Constant(0.1),
                                   name='convolution_{:d}'.format(filter_size))(embed)
        max_pool_shape = (feature_size - filter_size + 1, 1)
        pool = tf.keras.layers.MaxPool2D(pool_size=max_pool_shape,
                                      strides=(1, 1), padding='valid',
                                      data_format='channels_last',
                                      name='max_pooling_{:d}'.format(filter_size))(conv)
        pool_outputs.append(pool)

    pool_outputs = tf.keras.layers.concatenate(pool_outputs, axis=-1, name='concatenate')
    pool_outputs = tf.keras.layers.Flatten(data_format='channels_last', name='flatten')(pool_outputs)
    pool_outputs = tf.keras.layers.Dropout(dropout_rate, name='dropout')(pool_outputs)

    x = tf.keras.layers.Dense(64, activation='relu')(pool_outputs)
    x = tf.keras.layers.Dense(32, activation='relu')(x)
    x = tf.keras.layers.Dense(16, activation='relu')(x)

    outputs = tf.keras.layers.Dense(1, activation='sigmoid',
                                 kernel_initializer='glorot_normal',
                                 bias_initializer=tf.keras.initializers.Constant(0.1),
                                 kernel_regularizer='l2',
                                 bias_regularizer='l2',
                                 name='output')(x)
    model = tf.keras.Model(inputs=inputs, outputs=outputs)
    return model

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

    x = tf.keras.layers.Dense(64, activation='relu')(X_3)
    x = tf.keras.layers.Dense(32, activation='relu')(x)
    x = tf.keras.layers.Dense(16, activation='relu')(x)
    output = tf.keras.layers.Dense(1, activation='sigmoid')(x)

    return tf.keras.models.Model(inputs=[X_in, A_in, E_in], outputs=output)
