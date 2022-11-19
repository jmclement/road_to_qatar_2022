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
# Seed
#np.random(47)
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report, confusion_matrix
from sklearn.model_selection import GridSearchCV
#Add data source for vinesh
#import data as src_data
from modelling.encoder_02 import prepareTrainingset
from modelling.standardScaler_03 import standardScaler
#from modelling_RandomForest_04 import RandomForest
from modelling.modelling_XGBoost_04 import XGBoost
#from mode_tunning_RFC_05 import modelTuning
from modelling.mode_tunning_XGB_05 import modelTuning
# for everyone add the prefix folder road_t0....
#from road_to_qatar_2022.modelling.standardScaler_03 import standardScaler
#from road_to_qatar_2022.modelling.encoder_02 import prepareTrainingset
#from sklearn.externals import joblib
import pickle



def importModelParams():
    '''loading the initial trained model and tuning the model then saving the new tuned mdel'''
    model_tuning = modelTuning()
    p=model_tuning.get_params()
    tuned_model = XGBoost(**p)
    tuned_model_file = open('data/model_tuned', 'wb')
    pickle.dump(tuned_model,tuned_model_file)
    # close the file
    tuned_model_file.close()
    #loaded_model = pickle.load(open('data/model_tuned', 'rb'))
    #print(loaded_model.get_params())

    return tuned_model


def new_tuned_model():
    '''Saving the model that was tuned'''

    loaded_model = pickle.load(open('data/model_tuned', 'rb'))
    #file = open('data/model_tuned', 'wb')
    #pickle.dumps(tuned_model,file)
    #tunedModel= importModelParams()
    print(loaded_model.get_params())
    return loaded_model

if __name__ == "__main__":
    importModelParams()
