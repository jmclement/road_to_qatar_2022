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
import xgboost as xgb
from sklearn.metrics import classification_report, confusion_matrix
from sklearn.model_selection import GridSearchCV
#Add data source for vinesh
#import data as src_data
# for other add the prefix folder road_t0....
from standardScaler_03 import standardScaler
from encoder_02 import prepareTrainingset


def XGBoost():

    X_train_transformed,X_test_transformed = standardScaler()
    X_train_encoded, X_test_encoded, y_train_encoded, y_test_encoded = prepareTrainingset()

    # XGBoost

    XGB = xgb.XGBClassifier(base_score=0.5, booster='gbtree', colsample_bylevel=1,
        colsample_bytree=0.8, gamma=0.4, learning_rate=0.01,
        max_delta_step=0, max_depth=3, min_child_weight=1, missing=None,
        n_estimators=40, n_jobs=1, nthread=None, objective='multi:softprob',
        random_state=0, reg_alpha=1e-05, reg_lambda=1, scale_pos_weight=1,
        seed=2, silent=True, subsample=0.8)
    XGB.fit(X_train_transformed, y_train_encoded)
    score_train_acc = XGB.score(X_train_transformed, y_train_encoded)
    score_test_acc = XGB.score(X_test_transformed, y_test_encoded)
    print(score_train_acc) #
    print(score_test_acc)  #
    y_pred_XGB = XGB.predict(X_test_transformed)
    print(classification_report(y_test_encoded, y_pred_XGB))
    print(confusion_matrix(y_test_encoded, y_pred_XGB, labels=range(3)))

    return

if __name__ == "__main__":
    XGBoost()
