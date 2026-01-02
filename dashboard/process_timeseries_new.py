import sys
from optparse import OptionParser

import numpy as np
import tensorflow as tf
from sklearn.preprocessing import StandardScaler
from trader_corelib.mt5client import Mt5Client


def create_sequences(data, seq_length):
    xs, ys = [], []
    for i in range(len(data) - seq_length):
        x = data[i:i + seq_length]
        y = data[i + seq_length]
        xs.append(x)
        ys.append(y)
    return np.array(xs), np.array(ys)

@tf.keras.utils.register_keras_serializable()
class PositionalEncoding(tf.keras.layers.Layer):
    def __init__(self, sequence_length, d_model, **kwargs):
        super(PositionalEncoding, self).__init__(**kwargs)
        self.pos_encoding = self.positional_encoding(sequence_length, d_model)

    def positional_encoding(self, position, d_model):
        angle_rads = self.get_angles(np.arange(position)[:, np.newaxis],
                                     np.arange(d_model)[np.newaxis, :],
                                     d_model)
        angle_rads[:, 0::2] = np.sin(angle_rads[:, 0::2])
        angle_rads[:, 1::2] = np.cos(angle_rads[:, 1::2])
        pos_encoding = angle_rads[np.newaxis, ...]
        return tf.cast(pos_encoding, dtype=tf.float32)

    def get_angles(self, pos, i, d_model):
        angle_rates = 1 / np.power(10000, (2 * (i // 2)) / np.float32(d_model))
        return pos * angle_rates

    def call(self, inputs):
        return inputs + self.pos_encoding[:, :tf.shape(inputs)[1], :]


def build_transformer_model(input_shape, output_size, num_heads=8, ff_dim=128, num_transformer_blocks=4, dropout_rate=0.1):
    inputs = tf.keras.layers.Input(shape=input_shape)
    x = PositionalEncoding(input_shape[0], input_shape[1])(inputs)

    for _ in range(num_transformer_blocks):
        attention_output = tf.keras.layers.MultiHeadAttention(num_heads=num_heads, key_dim=input_shape[1])(x, x)
        attention_output = tf.keras.layers.Dropout(dropout_rate)(attention_output)
        x = tf.keras.layers.LayerNormalization(epsilon=1e-6)(x + attention_output)

        ffn_output = tf.keras.layers.Dense(ff_dim, activation='relu')(x)
        ffn_output = tf.keras.layers.Dense(input_shape[1])(ffn_output)
        ffn_output = tf.keras.layers.Dropout(dropout_rate)(ffn_output)
        x = tf.keras.layers.LayerNormalization(epsilon=1e-6)(x + ffn_output)

    x = tf.keras.layers.Flatten()(x)
    x = tf.keras.layers.Dense(128, activation='relu')(x)
    x = tf.keras.layers.Dropout(dropout_rate)(x)
    outputs = tf.keras.layers.Dense(output_size)(x)

    model = tf.keras.models.Model(inputs, outputs)
    return model


def main(currency):
    print(f'Preprocessing {currency.upper()}')
    timeframe = 'd1'
    points = 5
    sliding_window = 60

    client = Mt5Client({'common': {'mql_files_path': '/System/Volumes/Data/Users/volodymyrpaslavskyy/Library/Application Support/net.metaquotes.wine.metatrader5/drive_c/Program Files/MetaTrader 5/MQL5/Files'}})
    resp = [r for r in client.rates_all(currency, timeframe)]
    data = resp[0].rates[::-1]
    sc = StandardScaler()
    scaled_data = np.array(sc.fit_transform(data))
    scaled_data = np.round(scaled_data, 5)
    X, y = create_sequences(scaled_data, sliding_window)

    # Split the data into training, validation, and test sets
    split1 = int(0.7 * len(X))
    split2 = int(0.9 * len(X))
    X_train, X_val, X_test = X[:split1], X[split1:split2], X[split2:]
    y_train, y_val, y_test = y[:split1], y[split1:split2], y[split2:]
    print(X_test.shape)
    print(y_test.shape)
    input_shape = (sliding_window, X.shape[2])
    output_size = y.shape[1]
    model = build_transformer_model(input_shape, output_size)

    # Step 3: Training and Evaluation
    model.compile(optimizer=tf.keras.optimizers.Adam(learning_rate=0.001), loss='mse', metrics=['mae'])

    early_stopping = tf.keras.callbacks.EarlyStopping(monitor='val_loss', patience=10, restore_best_weights=True)
    reduce_lr = tf.keras.callbacks.ReduceLROnPlateau(monitor='val_loss', factor=0.2, patience=5, min_lr=1e-6)
    model.fit(X_train, y_train, validation_data=(X_val, y_val), epochs=100, batch_size=32, callbacks=[early_stopping, reduce_lr])
    model.save(f'eurusd_{timeframe}_model.keras')
    model = tf.keras.models.load_model(f'eurusd_{timeframe}_model.keras', custom_objects={'PositionalEncoding': PositionalEncoding})
    # Now, predict the next 10 points
    last_sequence = X_test[-1]  # Start with the last sequence from your test set
    predictions = []
    for _ in range(points):
        # Predict the next point
        next_pred = model.predict(last_sequence[np.newaxis, :, :])[0]

        # Append the prediction to the list of predictions
        predictions.append(next_pred)

        # Update the last_sequence to include this prediction
        last_sequence = np.vstack([last_sequence[1:], next_pred])  # Drop the oldest and add the latest

    # Convert predictions to the original scale
    predictions = sc.inverse_transform(predictions)

    # Display the predicted points
    print(f"Predicted next {points} points (open, close, high, low):")
    print(predictions)

    # Plot the predictions
    import matplotlib.pyplot as plt

    plt.figure(figsize=(12, 6))

    # Plot each component of the prediction
    for i, label in enumerate(['Open', 'Close', 'High', 'Low']):
        plt.plot(range(len(predictions)), predictions[:, i], label=f'Predicted {label}')

    plt.xlabel('Future Points')
    plt.ylabel('Price')
    plt.title(f'Predicted Next {points} Points')
    plt.legend()
    plt.show()


if __name__ == '__main__':
    parser = OptionParser()
    parser.add_option('-c', '--currency', dest='currency', default='eurusd')

    (options, args) = parser.parse_args()
    sys.exit(main(options.currency))
# TODO, use percentage normalizer
# TODO, use different sequencer