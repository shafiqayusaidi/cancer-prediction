# -*- coding: utf-8 -*-
"""Project 1.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1dvrDRGDMS2qR2G_zxUoUTXDHeECqBTUT
"""

import pandas as pd
from sklearn import preprocessing
from tensorflow.keras.callbacks import TensorBoard
import time

NAME = "Breast-cancer-neural-network-{}".format(int(time.time()))

tensorboard = TensorBoard(log_dir='logs/{}'.format(NAME))

df = pd.read_csv('data.csv', skiprows=0)
print(df.head())
df.info()
df.drop(["Unnamed: 32"], axis = 1, inplace=True)
df.drop(["id"], axis = 1, inplace = True)

# Checking if the column has dropped
df.info()

# Split data into features and labels
df_features = df.copy()
df_label = df_features.pop('diagnosis')

# Splitting the features into three parts of severity
features_mean= list(df.columns[1:11])
features_se= list(df.columns[11:21])
features_worst=list(df.columns[21:31])

import matplotlib.pyplot as plt
import seaborn as sns

corr = df[features_mean].corr() # .corr is used for find corelation
plt.figure(figsize=(14,14))
sns.heatmap(corr, cbar = True,  square = True, annot=True, fmt= '.2f',annot_kws={'size': 15},
           xticklabels= features_mean, yticklabels= features_mean,
           cmap= 'coolwarm')

# One hot encoding label
df_label_OH = pd.get_dummies(df_label)
print(df_label_OH)

import tensorflow as tf
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler

SEED = 12345

# Split the data set into train-validation-test sets
x_train, x_iter, y_train, y_iter = train_test_split(df_features, df_label_OH, test_size=0.4,random_state=SEED)
x_val, x_test, y_val, y_test = train_test_split(x_iter, y_iter, test_size=0.5,random_state=SEED)

# Normalize the features, fit the training set
scaler = StandardScaler()
scaler.fit(x_train)
x_train = scaler.transform(x_train)
x_iter = scaler.transform(x_iter)
x_test = scaler.transform(x_test)

# Data preparation is completed

# Create a feed neural network using Tensorflow Keras

model = tf.keras.Sequential()

model.add(tf.keras.layers.InputLayer(input_shape=(x_train.shape[-1],)))
model.add(tf.keras.layers.Dense(128,activation='elu'))
model.add(tf.keras.layers.Dense(64,activation='elu'))
model.add(tf.keras.layers.Dense(32,activation='elu'))
model.add(tf.keras.layers.Dropout(0.3))
model.add(tf.keras.layers.Dense(y_train.shape[-1], activation='softmax'))

model.compile(optimizer='adam',loss='categorical_crossentropy'
              ,metrics=['accuracy'])

# Commented out IPython magic to ensure Python compatibility.
# Load the TensorBoard notebook extension
# %load_ext tensorboard

import tensorflow as tf
import datetime

log_dir = "logs/fit/" + datetime.datetime.now().strftime("%Y%m%d-%H%M%S")
tensorboard_callback = tf.keras.callbacks.TensorBoard(log_dir=log_dir, histogram_freq=1)

history = model.fit(x_train, 
          y_train.values,
          validation_data=(x_val,y_val),
          epochs=100,
          batch_size=128,
          callbacks = [tensorboard_callback]
          )

# Evaluate the data

test_result = model.evaluate(x_test, y_test, batch_size = 128)
print(f"Test loss = {test_result[0]}")
print(f"Test accuracy = {test_result[1]}")

# Make predictions
import numpy as np

predictions_softmax = model.predict(x_test)
predictions = np.argmax(predictions_softmax, axis = 1)
y_test_element, y_test_index = np.where(np.array(y_test) == 1)
for prediction, label in zip(predictions, y_test_index):
    print(f"Prediction: {prediction} Label: {label}")

# Commented out IPython magic to ensure Python compatibility.
# %tensorboard --logdir logs/fit