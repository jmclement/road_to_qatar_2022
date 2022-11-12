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


#Add data source for vinesh
#import data as src_data
from encoder_02 import prepareTrainingset


#Import utils for everyone

#import road_to_qatar_2022.data as src_data
#from road_to_qatar_2022.modelling.encoder_02 import prepareTrainingset

def standardScaler():
    '''Scalling of Data:'''

    #Scaling
    X_hold_test, X_test, y_hold_test, y_test, X_train, X_val, y_train, y_val = prepareTrainingset()
    scaler = StandardScaler()
    X_train = scaler.fit_transform(X_train)
    X_test = scaler.transform(X_test)
    X_hold_test = scaler.transform(X_hold_test)



    #sc = StandardScaler()
    #X_train_encoded, X_test_encoded, y_train_encoded, y_test_encoded = prepareTrainingset()
    #X_train_transformed = sc.fit_transform(X_train_encoded)
    #X_test_transformed = sc.fit_transform(X_test_encoded)
    print(X_train,X_test,X_hold_test)
    #print("Scaling done")
    return X_train,X_test,X_hold_test

if __name__ == "__main__":
    standardScaler()
