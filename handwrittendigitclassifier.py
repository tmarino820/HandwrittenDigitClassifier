# -*- coding: utf-8 -*-
"""HandwrittenDigitClassifer.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1EZziYiXmFyotHAJ06fe3n6eUfG-4tAn5
"""

"""
Author: Antonio Marino

This file loads data from the MNIST dataset, initializes 
a neural to classify handwritten digits, and saves the 
weights of that model to a directory where they can be 
easily accessed by future executions of this program. 
Much of the code originates from tutorials in the book 
Deep Learning Illustrated, Stack Overflow, and Tensorflow.

Beyleveld, G. & Krohn, J.. Deep Learning Illustrated. Pearson’s Addison-Wesley imprint (2019). https://www.amazon.com/Deep-Learning-Illustrated-Intelligence-Addison-Wesley/dp/0135116694.

Anonymous. Save and load models. Tensorflow (2022). https://www.tensorflow.org/tutorials/keras/save_and_load.

Ramadan, Lucas. Where do I call the BatchNormalization function in Keras?. Stackoverflow (2021). https://stackoverflow.com/questions/34716454/where-do-i-call-the-batchnormalization-function-in-keras.

Creative Commons Attribution 4.0 License:
Attribution 4.0 International (CC BY 4.0)
This is a human-readable summary of (and not a substitute for) the license. Disclaimer.
You are free to:
Share — copy and redistribute the material in any medium or format
Adapt — remix, transform, and build upon the material
for any purpose, even commercially.
This license is acceptable for Free Cultural Works.
The licensor cannot revoke these freedoms as long as you follow the license terms.
Under the following terms:
Attribution — You must give appropriate credit, provide a link to the license, and indicate if changes were made. You may do so in any reasonable manner, but not in any way that suggests the licensor endorses you or your use.

No additional restrictions — You may not apply legal terms or technological measures that legally restrict others from doing anything the license permits.
Notices:
You do not have to comply with the license for elements of the material in the public domain or where your use is permitted by an applicable exception or limitation.
No warranties are given. The license may not give you all of the permissions necessary for your intended use. For example, other rights such as publicity, privacy, or moral rights may limit how you use the material.
https://creativecommons.org/licenses/by/4.0/
"""
import os
import keras
from keras.datasets import mnist
from keras.models import Sequential
from keras.layers import Dense
from keras.utils import np_utils
from tensorflow.keras.optimizers import SGD
from matplotlib import pyplot as plt
from tensorflow.keras.layers import BatchNormalization

# loading the the mnist dataset from the keras built-in datasets

(X_train, y_train), (X_valid, y_valid) = mnist.load_data()

# showing the data to the user

plt.figure(figsize=(5,5))
for k in range(12):
  plt.subplot(3, 4, k+1)
  plt.imshow(X_train[k], cmap='Greys')
  plt.axis('off')
plt.tight_layout()
plt.show()

# flattening two-dimensional images to one dimension

X_train = X_train.reshape(60000, 784).astype('float32')
X_valid = X_valid.reshape(10000, 784).astype('float32')

# converting pixels to floats

X_train /= 255
X_valid /= 255

# converting integer labels to one-hot encodings

n_classes = 10
y_train = keras.utils.np_utils.to_categorical(y_train, n_classes)
y_valid = keras.utils.np_utils.to_categorical(y_valid, n_classes)

# initialize the architecture of the neural network

model = Sequential()
model.add(Dense(64, activation='sigmoid', input_shape=(784,)))
model.add(BatchNormalization())
model.add(Dense(64, activation='sigmoid', input_shape=(784,)))
model.add(BatchNormalization())
model.add(Dense(10, activation='softmax'))
model.compile(loss='categorical_crossentropy', optimizer='adam', metrics=['accuracy'])


checkpoint_path = "training_1/cp.ckpt"
checkpoint_dir = os.path.dirname(checkpoint_path)

try:
  # Loading the weights
  model.load_weights(checkpoint_path)
except:
  # Creating a callback that saves the model's weights
  cp_callback = keras.callbacks.ModelCheckpoint(filepath=checkpoint_path,
                                                  save_weights_only=True,
                                                  verbose=1)
  # Training the model with the new callback
  model.fit(X_train, y_train, 
            batch_size=128, epochs=200,
            verbose=1,
            validation_data=(X_valid, y_valid),
            callbacks=[cp_callback])  # Pass callback to training
  

# Evaluating the model
loss, acc = model.evaluate(X_valid, y_valid, verbose=2)
print("Trained model, accuracy: {:5.2f}%".format(100 * acc))