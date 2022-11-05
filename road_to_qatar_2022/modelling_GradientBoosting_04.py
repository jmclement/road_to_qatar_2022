# Add standard imports
import requests
import csv
import os
import re
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.utils import shuffle
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler

# Building ANN
import tensorflow as tf
from tensorflow import keras
from keras.models import Sequential
from keras.layers import Dense
from keras.wrappers.scikit_learn import KerasClassifier
from sklearn.ensemble import GradientBoostingClassifier
from sklearn.metrics import classification_report, confusion_matrix
from sklearn.model_selection import GridSearchCV
#Add data source for vinesh
#import data as src_data
# for other add the prefix folder road_t0....
from standardScaler_03 import standardScaler
from encoder_02 import prepareTrainingset


def GradientBoosting():

    X_train_transformed,X_test_transformed = standardScaler()
    X_train_encoded, X_test_encoded, y_train_encoded, y_test_encoded = prepareTrainingset()

    # Gradient Boosting

    gbc = GradientBoostingClassifier(n_estimators=100, learning_rate=0.1)
    gbc.fit(X_train_transformed, y_train_encoded)
    score_train_acc = gbc.score(X_train_transformed, y_train_encoded)
    score_test_acc = gbc.score(X_test_transformed, y_test_encoded)
    print(score_train_acc) #0.71
    print(score_test_acc)  #0.42
    y_pred_gbc = gbc.predict(X_test_transformed)
    print(classification_report(y_test_encoded, y_pred_gbc))
    print(confusion_matrix(y_test_encoded, y_pred_gbc, labels=range(3)))

    return

if __name__ == "__main__":
    GradientBoosting()
