# FNN model trained on just the current, voltage and SOC
# Trained on Cell 1(007) data
# Validated on last 15% of cell 2(008)
# Tested on first 85% of cell 2(008)
import numpy as np
import tensorflow as tf
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, Dropout
from sklearn.preprocessing import StandardScaler

from model_graph import *

class FNN:
    def __init__(self, xtrain, ytrain, xval, yval, xtest, ytest):
        self.xtrain = xtrain
        self.ytrain = ytrain
        self.xval = xval
        self.yval = yval
        self.xtest = xtest
        self.ytest = ytest

        
    def train(self):
        self.scaler = StandardScaler()
        x_scaled = self.scaler.fit_transform(self.xtrain)

        self.model = Sequential([
            #tf.keras.layers.Input(shape=(x_scaled.shape[1],)),
            Dense(64, activation="relu"),
            Dropout(0.1),
            Dense(32, activation='relu'),
            Dense(1, activation='linear')
        ])

        self.model.compile(
            optimizer=tf.keras.optimizers.Adam(learning_rate=0.001),
            loss='mse',
            metrics=['mae']
        )

        history = self.model.fit(
            x_scaled, self.ytrain,
            validation_data=(self.scaler.transform(self.xval), self.yval),
            epochs=50,
            batch_size=32,

        )

    def evaluate(self):
      test_loss, test_mae = self.model.evaluate(self.scaler.transform(self.xtest), self.ytest, verbose=0)

      print(f"FNN Weak:\n\tTest Loss: {test_loss}\n\tTest MAE: {test_mae}")

    def predict(self, time):
        y_pred = self.model.predict(self.scaler.transform(self.xtest))

        y_pred_clipped = np.clip(y_pred, 0.0, 1.0)

        soc_pred_vs_actual(time, self.ytest, y_pred_clipped, "FNN/")

    def save(self):
        self.model.save("output/models/FNN/fnn.keras")
        
