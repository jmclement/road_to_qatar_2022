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
import xgboost as xgb
#Add data source for vinesh
import data as src_data
from modelling.encoder_02 import prepareTrainingset
from modelling.standardScaler_03 import standardScaler
from modelling.modelling_XGBoost_04 import XGBoost

# for other add the prefix folder road_t0....
#from road_to_qatar_2022.modelling.standardScaler_03 import standardScaler
#from road_to_qatar_2022.modelling.encoder_02 import prepareTrainingset
#from road_to_qatar_2022.modelling.modelling_XGBoost_04 import XGBoost

# Parameters list for tuning

def modelTuning():
    X_train_transformed,X_test_transformed = standardScaler()
    X_train_encoded, X_test_encoded, y_train_encoded, y_test_encoded = prepareTrainingset()
    XGB = XGBoost()

    parameters = { 'learning_rate' : [0.001,0.01, 0.1, 1],
                'n_estimators' : [40, 100],
                'max_depth': [3, 6],
                'min_child_weight': [1, 3],
                'gamma':[0.4],
                'subsample' : [0.5, 0.8],
                'colsample_bytree' : [0.8],
                'scale_pos_weight' : [1],
                'reg_alpha':[1e-5]
                }
    clf = XGB

    grid_obj = GridSearchCV(clf,
                            param_grid=parameters,
                            cv=5
                            )
    grid_obj = grid_obj.fit(X_train_transformed,y_train_encoded)
    clf = grid_obj.best_estimator_
    #tuned_xgb_params= clf.get_params()
    #print(tuned_xgb_params)
    #print(estimator)

    return clf
if __name__ == "__main__":
    modelTuning()
