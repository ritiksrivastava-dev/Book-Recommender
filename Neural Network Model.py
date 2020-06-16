# -*- coding: utf-8 -*-
"""Untitled

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1mg4wn9QkzIZ06flonHTyjP1QriZziM65
"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import os
import warnings

from keras.layers import Input, Embedding, Flatten, Dot, Dense, Concatenate
from keras.models import Model

warnings.filterwarnings('ignore')


#importing user ratings of books from dataset
dataset = pd.read_csv('https://raw.githubusercontent.com/ritiksrivastava-dev/Book-Recommender/master/ratings.csv')

from sklearn.model_selection import train_test_split
train, test = train_test_split(dataset, test_size = 0.2, random_state = 42)
#test_size = dataset split for testing (20% in this case) approx 1,96,351 ratings of 9,81,756
#random_state = randomizes the data taken for the test and training set split

n_users = len(dataset.user_id.unique())
n_books = len(dataset.book_id.unique())

conc = Concatenate()([book_vec, user_vec])

#Densely Connected Layer comprised of Weight, Bias, and Activation.
fc1 = Dense(128, activation = 'relu')(conc)
fc2 = Dense(32, activation = 'relu')(fc1)
out = Dense(1)(fc2)

model = Model([user_input, book_input], out)
model.compile('adam', 'mean_squared_error')

from keras.models import load_model

history = model.fit([train.user_id, train.book_id], train.rating, epochs=20, verbose=1)
plt.plot(history.history['loss'])
plt.xlabel("Epochs")
plt.ylabel("Training Error")

model.evaluate([test.user_id, test.book_id], test.rating)

predictions = model.predict([test.user_id.head(10), test.book_id.head(10)])
[print(predictions[i], test.rating.iloc[i]) for i in range(0,10)]

#dataset used for predictions
book_data = np.array(list(set(dataset.book_id)))
user = np.array([1 for i in range(len(book_data))])

predictions = model.predict([user, book_data])
predictions = np.array([a[0] for a in predictions])
recommended_book_ids = (-predictions).argsort()[:5]

books = pd.read_csv('https://raw.githubusercontent.com/ritiksrivastava-dev/Book-Recommender/master/books.csv')
books[books['id'].isin(recommended_book_ids)]