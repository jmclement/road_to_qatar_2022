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
from data_01 import getKnockoutround


#Import utils for everyone
#from road_to_qatar_2022.modelling.data_01 import getKnockoutround


def prepareTrainingset():
    '''Preparing Training and Testing Data'''
    knockout_final_df, final_df = getKnockoutround()

    #split X and y and train test split (For League Matches)
    X = final_df.drop('home_team_result',axis=1)
    y = final_df['home_team_result']

    X_train, X_val, y_train, y_val = train_test_split(X, y, test_size=0.3, random_state=42)
    #Validtion and test set
    X_hold_test, X_test, y_hold_test, y_test = train_test_split(X_val, y_val, test_size=0.5, random_state=42)



    #Team_id = getWinners()
    #Team_id = Team_id.drop(['date','home_team','away_team','win_conditions'],1)
    #X = Team_id.iloc[:, 0:7].values
    #y = Team_id.iloc[:, -1].values

    #X = np.array(X, dtype = 'f')
    #y = np.array(y, dtype = 'f')

    #LabelEncoder_res=LabelEncoder()
    #y=LabelEncoder_res.fit_transform(y)

    #X, y = shuffle(X,y)

    #X_train_encoded, X_test_encoded, y_train_encoded, y_test_encoded = train_test_split(X, y, test_size = 0.3)
    #print("Encoding done")
    #return X_train_encoded, X_test_encoded, y_train_encoded, y_test_encoded
    #print(X_train,X_test,X_hold_test)
    return  X_hold_test, X_test, y_hold_test, y_test, X_train, X_val, y_train, y_val
if __name__ == "__main__":
    prepareTrainingset()
