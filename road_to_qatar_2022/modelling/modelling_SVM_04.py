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
from sklearn.svm import SVC
from sklearn.metrics import classification_report, confusion_matrix
from sklearn.model_selection import GridSearchCV
#Add data source for vinesh
# for everyone add prefix road_to_qatar_2022
from road_to_qatar_2022.standardScaler_03 import standardScaler
from road_to_qatar_2022.encoder_02 import prepareTrainingset


def SVM():

    # SVM

    X_train_transformed,X_test_transformed = standardScaler()
    X_train_encoded, X_test_encoded, y_train_encoded, y_test_encoded = prepareTrainingset()
    svm_model = SVC()
    parameters = {'C' : [ 0.1, 0.001, 1]}#, 'multi_class' :['multinomial', 'ovr'], 'solver': ['lbfgs', 'newton-cg']}
    svm_model = GridSearchCV(svm_model, param_grid= parameters ,cv=5)
    svm_model.fit(X_train_transformed, y_train_encoded)
    score_train_acc = svm_model.score(X_train_transformed, y_train_encoded)
    score_test_acc = svm_model.score(X_test_transformed, y_test_encoded)
    print(score_train_acc) # 0.50
    print(score_test_acc) # 0.47
    y_pred_SVM = svm_model.predict(X_test_transformed)
    print(classification_report(y_test_encoded, y_pred_SVM))
    print(confusion_matrix(y_test_encoded, y_pred_SVM, labels=range(3)))


    return

if __name__ == "__main__":
    SVM()
