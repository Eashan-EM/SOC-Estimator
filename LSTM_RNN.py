import numpy as np
import tensorflow as tf
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, LSTM, Input
import keras

from model_graph import *

class LSTM_RNN:
    def __init__(self, xtrain, ytrain, xval, yval, xtest, ytest):
        self.xtrain = xtrain
        self.ytrain = ytrain
        self.xval = xval
        self.yval = yval
        self.xtest = xtest
        self.ytest = ytest

    def load_module(self):
        self.model = keras.saving.load_model("./output/models/LSTM-RNN/lstm-rnn.keras")
        
    def train(self):
        self.model = Sequential([
            Input(shape=(50, 2)),
            LSTM(units=50, activation='relu', return_sequences=False),
            Dense(1)
        ])

        self.model.compile(
            optimizer=tf.keras.optimizers.Adam(learning_rate=0.001),
            loss='mse',
            metrics=['mae']
        )

        self.history = self.model.fit(
            self.xtrain, self.ytrain,
            validation_data=(self.xval, self.yval),
            epochs=50,
            batch_size = 32
        )

    def evaluate(self):
        test_loss, test_mae = self.model.evaluate(self.xtest, self.ytest, verbose=0)

        print(f"LSTM_RNN:\n\tTest Loss: {test_loss}\n\tTest MAE: {test_mae}")

    def predict(self, time):
        y_pred = self.model.predict(self.xtest)
        y_pred_clipped = np.clip(y_pred, 0.0, 1.0)

        ytest = [sample[-1] for sample in self.ytest]
        
        soc_pred_vs_actual(time, ytest, y_pred_clipped, "LSTM-RNN/")

    def save(self):
        self.model.save("output/models/LSTM-RNN/lstm-rnn.keras")