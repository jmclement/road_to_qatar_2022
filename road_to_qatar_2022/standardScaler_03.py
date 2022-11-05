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
#from road_to_qatar_2022.encoder_02 import prepareTrainingset

def standardScaler():
    '''Scalling of Data:'''
    sc = StandardScaler()
    X_train_encoded, X_test_encoded, y_train_encoded, y_test_encoded = prepareTrainingset()
    X_train_transformed = sc.fit_transform(X_train_encoded)
    X_test_transformed = sc.fit_transform(X_test_encoded)
    #print(X_train,X_test)
    print("Scaling done")
    return X_train_transformed,X_test_transformed

if __name__ == "__main__":
    standardScaler()
