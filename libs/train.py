import spektral
import tensorflow as tf

def do_train(model, pipe, batch_size, epochs=10, steps_per_epoch=10_000,
    validation_steps=1_000):
    # Compile the model
    model.compile(optimizer='adam',
                loss='binary_crossentropy',
                metrics=[
                    'binary_accuracy',
                    tf.keras.metrics.TruePositives(name='tp'),
                    tf.keras.metrics.TrueNegatives(name='tn'),
                    tf.keras.metrics.FalsePositives(name='fp'),
                    tf.keras.metrics.FalseNegatives(name='fn'),
                ])

    if isinstance(pipe, spektral.data.loaders.Loader):
        print('-' * 30)
        print('Spektral loader identified, changing batch size to 1.')
        print('-' * 30)
        batch_size = 1

    # Train the model
    model.fit(
        pipe,
        batch_size=batch_size,
        epochs = epochs,
        steps_per_epoch = steps_per_epoch,
        validation_data = pipe,
        validation_steps = validation_steps,
    )