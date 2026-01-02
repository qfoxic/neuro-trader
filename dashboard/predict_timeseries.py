import sys
from optparse import OptionParser

import pandas as pd
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
    client = Mt5Client({'common': {'mql_files_path': '/System/Volumes/Data/Users/volodymyrpaslavskyy/Library/Application Support/net.metaquotes.wine.metatrader5/drive_c/Program Files/MetaTrader 5/MQL5/Files'}})
    resp = [r for r in client.rates_all(currency, 'h4')]
    data = resp[0].rates[::-1][10:]
    sc = StandardScaler()
    scaled_data = np.array(sc.fit_transform(data))
    scaled_data = np.round(scaled_data, 5)
    rsd = scaled_data.reshape((1, 60, 4))

    input_shape = (60, 4) # 4 - because we have open, close, high, low.
    output_size = 4
    model = build_transformer_model(input_shape, output_size)
    model = tf.keras.models.load_model('eurusd_h4_model.keras', custom_objects={'PositionalEncoding': PositionalEncoding})
    # Evaluate the model
    # test_loss, test_mae = model.evaluate(X_test, y_test)
    # print(f'Test MAE: {test_mae}')

    # Step 4: Making Predictions
    y_pred = model.predict(rsd)
    y_pred = sc.inverse_transform(y_pred)
    print(y_pred)

    import matplotlib.pyplot as plt
    # Extract the open, close, high, and low values
    open_price = y_pred[0][0]
    close_price = y_pred[0][1]
    high_price = y_pred[0][2]
    low_price = y_pred[0][3]

    # Calculate the PIPs
    high_low_pips = abs(high_price - low_price) * 10000
    open_close_pips = abs(close_price - open_price) * 10000
    # Create a simple candlestick plot
    fig, ax = plt.subplots()

    # Set the width of the candlestick
    candlestick_width = 0.4

    # Determine the color of the candlestick
    if close_price >= open_price:
        color = 'green'
    else:
        color = 'red'

    # Plot the high-low line
    ax.plot([1, 1], [low_price, high_price], color='black')

    # Plot the open-close rectangle
    rect = plt.Rectangle((0.5, open_price if close_price >= open_price else close_price),
                        candlestick_width,
                        abs(close_price - open_price),
                        color=color)

    ax.add_patch(rect)

    # Add PIPs annotations
    ax.text(1.2, (high_price + low_price) / 2, f'PIPs: {high_low_pips:.2f}', verticalalignment='center')
    ax.text(1.2, (open_price + close_price) / 2, f'PIPs: {open_close_pips:.2f}', verticalalignment='center')

    # Set the limits and labels
    ax.set_xlim(0.5, 1.5)
    ax.set_ylim(low_price - 0.001, high_price + 0.001)
    ax.set_xticks([])
    ax.set_ylabel('Price')
    ax.set_title('Candlestick Chart')

    # Show the plot
    plt.show()


if __name__ == '__main__':
    parser = OptionParser()
    parser.add_option('-c', '--currency', dest='currency', default='eurusd')

    (options, args) = parser.parse_args()
    sys.exit(main(options.currency))
