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
from sklearn.preprocessing import LabelEncoder

#Add data source for vinesh
#from data_01 import getWinners


#Import utils for everyone
from road_to_qatar_2022.data_01 import getWinners

def prepareTrainingset():
    '''Preparing Training and Testing Data'''
    Team_id = getWinners()
    Team_id = Team_id.drop(['date','home_team','away_team','win_conditions'],1)
    X = Team_id.iloc[:, 0:7].values
    y = Team_id.iloc[:, -1].values

    X = np.array(X, dtype = 'f')
    y = np.array(y, dtype = 'f')

    LabelEncoder_res=LabelEncoder()
    y=LabelEncoder_res.fit_transform(y)

    X, y = shuffle(X,y)

    X_train_encoded, X_test_encoded, y_train_encoded, y_test_encoded = train_test_split(X, y, test_size = 0.3)
    print("Encoding done")
    return X_train_encoded, X_test_encoded, y_train_encoded, y_test_encoded

if __name__ == "__main__":
    prepareTrainingset()
