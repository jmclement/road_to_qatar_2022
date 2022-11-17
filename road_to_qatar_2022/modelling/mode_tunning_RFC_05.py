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


from sklearn.model_selection import GridSearchCV
from sklearn.ensemble import RandomForestClassifier
#Add data source for vinesh
import data as src_data
from encoder_02 import prepareTrainingset
from standardScaler_03 import standardScaler
from modelling_XGBoost_04 import XGBoost

# for other add the prefix folder road_t0....
#from road_to_qatar_2022.modelling.standardScaler_03 import standardScaler
#from road_to_qatar_2022.modelling.encoder_02 import prepareTrainingset
#from road_to_qatar_2022.modelling.modelling_XGBoost_04 import XGBoost

# Parameters list for tuning

def modelTuning():
    X_train_transformed,X_test_transformed = standardScaler()
    X_train_encoded, X_test_encoded, y_train_encoded, y_test_encoded = prepareTrainingset()

    param_grid = {
    'bootstrap': [True],
    'max_depth': [80, 90, 100, 110],
    'max_features': [2, 3],
    'min_samples_leaf': [3, 4, 5],
    'min_samples_split': [8, 10, 12],
    'n_estimators': [100, 200, 300, 1000]
}


    clf_1 = RandomForestClassifier()

    grid_obj1 = GridSearchCV(estimator = clf_1, param_grid = param_grid,
                            cv = 3, n_jobs = -1, verbose = 2)
    grid_obj1 = grid_obj1.fit(X_train_transformed,y_train_encoded)
    clf_1 = grid_obj1.best_estimator_
    print(clf_1)

    return
if __name__ == "__main__":
    modelTuning()
