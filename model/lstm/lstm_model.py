import keras.backend as K
import tensorflow as tf
from tensorflow.keras.layers import Bidirectional


class LSTMModel:
    def __init__(self, input_shape, num_classes):
        self.input_shape = input_shape
        # self.gru_layers=gru_layers
        self.num_classes = num_classes
        # self.projection_dims=projection_dims
        self.model = self.get_model(input_shape, num_classes)
        self.model_10_layers = self.get_model_5_layers(input_shape, num_classes)

    def recall_m(self, y_true, y_pred):
        true_positives = K.sum(K.round(K.clip(y_true * y_pred, 0, 1)))
        possible_positives = K.sum(K.round(K.clip(y_true, 0, 1)))
        recall = true_positives / (possible_positives + K.epsilon())
        return recall


    def precision_m(self, y_true, y_pred):
        true_positives = K.sum(K.round(K.clip(y_true * y_pred, 0, 1)))
        predicted_positives = K.sum(K.round(K.clip(y_pred, 0, 1)))
        precision = true_positives / (predicted_positives + K.epsilon())
        return precision


    def f1_m(self, y_true, y_pred):
        precision = self.precision_m(y_true, y_pred)
        recall = self.recall_m(y_true, y_pred)
        return 2 * ((precision * recall) / (precision + recall + K.epsilon()))


    def r2_keras(self, y_true, y_pred):
        SS_res = K.sum(K.square(y_true - y_pred))
        SS_tot = K.sum(K.square(y_true - K.mean(y_true)))
        return (1 - SS_res / (SS_tot + K.epsilon()))

    def get_model(self, input_shape, num_class):
        lstm_model = tf.keras.models.Sequential([
            tf.keras.layers.LSTM(512, input_shape=input_shape, return_sequences=True),
            tf.keras.layers.LSTM(512, dropout=0.1, return_sequences=True),
            tf.keras.layers.LSTM(512, dropout=0.1, return_sequences=True),
            tf.keras.layers.LSTM(512, dropout=0.1, return_sequences=True),
            tf.keras.layers.LSTM(256, dropout=0.1, return_sequences=True),
            tf.keras.layers.LSTM(256, dropout=0.1, return_sequences=True),
            tf.keras.layers.LSTM(256, dropout=0.1, return_sequences=True),
            tf.keras.layers.LSTM(256, dropout=0.1, return_sequences=True),
            tf.keras.layers.LSTM(128, dropout=0.1, return_sequences=True),
            tf.keras.layers.LSTM(128, dropout=0.1, return_sequences=True),
            tf.keras.layers.LSTM(128, dropout=0.1, return_sequences=True),
            tf.keras.layers.LSTM(128, dropout=0.1, return_sequences=True),
            tf.keras.layers.LSTM(64, dropout=0.1, return_sequences=True),
            tf.keras.layers.LSTM(64, dropout=0.1, return_sequences=True),
            tf.keras.layers.LSTM(64, dropout=0.1, return_sequences=True),
            tf.keras.layers.LSTM(64, dropout=0.1, return_sequences=True),
            tf.keras.layers.LSTM(32, dropout=0.1, return_sequences=True),
            tf.keras.layers.LSTM(32, dropout=0.1, return_sequences=True),
            tf.keras.layers.LSTM(16, dropout=0.1, return_sequences=True),
            tf.keras.layers.LSTM(16, dropout=0.1, return_sequences=True),
            tf.keras.layers.Dense(num_class, activation='sigmoid')
        ])
        return lstm_model

    def get_model_5_layers(self, input_shape, num_class):
        lstm_model = tf.keras.models.Sequential([
            tf.keras.layers.LSTM(512, input_shape=input_shape, return_sequences=True),
            tf.keras.layers.LSTM(512, dropout=0.2, return_sequences=True),
            tf.keras.layers.LSTM(512, dropout=0.2, return_sequences=True),
            tf.keras.layers.LSTM(512, dropout=0.2, return_sequences=True),
            tf.keras.layers.LSTM(512, dropout=0.2, return_sequences=True),
            tf.keras.layers.Dense(num_class, activation='sigmoid')
        ])
        return lstm_model

    def get_model_bi(self, input_shape, num_class):
        lstm_model = tf.keras.models.Sequential([
            Bidirectional(tf.keras.layers.LSTM(512, return_sequences=True), input_shape=input_shape),
            Bidirectional(tf.keras.layers.LSTM(512, dropout=0.2, return_sequences=True)),
            Bidirectional(tf.keras.layers.LSTM(512, dropout=0.2, return_sequences=True)),
            Bidirectional(tf.keras.layers.LSTM(512, dropout=0.2, return_sequences=True)),
            Bidirectional(tf.keras.layers.LSTM(512, dropout=0.2, return_sequences=True)),
            tf.keras.layers.Dense(num_class, activation='sigmoid')
        ])
        return lstm_model

    def get_model_2_layers(self, input_shape, num_class):
        lstm_model = tf.keras.models.Sequential([
            tf.keras.layers.LSTM(512, input_shape=input_shape, return_sequences=True),
            tf.keras.layers.LSTM(512, dropout=0.2, return_sequences=True),
            tf.keras.layers.Dense(num_class, activation='sigmoid')
        ])
        return lstm_model

    def get_model_3_layers(self, input_shape, num_class):
        lstm_model = tf.keras.models.Sequential([
            tf.keras.layers.LSTM(512, input_shape=input_shape, return_sequences=True),
            tf.keras.layers.LSTM(512, dropout=0.2, return_sequences=True),
            tf.keras.layers.LSTM(512, dropout=0.2, return_sequences=True),
            tf.keras.layers.Dense(num_class, activation='sigmoid')
        ])
        return lstm_model

    def get_model_4_layers(self, input_shape, num_class):
        lstm_model = tf.keras.models.Sequential([
            tf.keras.layers.LSTM(512, input_shape=input_shape, return_sequences=True),
            tf.keras.layers.LSTM(512, dropout=0.2, return_sequences=True),
            tf.keras.layers.LSTM(512, dropout=0.2, return_sequences=True),
            tf.keras.layers.LSTM(512, dropout=0.2, return_sequences=True),
            tf.keras.layers.Dense(num_class, activation='sigmoid')
        ])
        return lstm_model

    def get_model_custom(self, input_shape, num_class, num_layers, hidden_size):
        lstm_model = tf.keras.models.Sequential([
            tf.keras.layers.LSTM(hidden_size, input_shape=input_shape, return_sequences=True),
        ])
        for i in range(num_layers-1):
            lstm_model.add(tf.keras.layers.GRU(hidden_size, dropout=0.2,return_sequences=True))
        lstm_model.add(tf.keras.layers.Dense(num_class,activation='sigmoid'))
        return lstm_model