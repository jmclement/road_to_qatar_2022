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
from sklearn.metrics import classification_report,ConfusionMatrixDisplay

#Add data source for vinesh
#import data as src_data
from encoder_02 import prepareTrainingset


#Import utils for everyone

#import road_to_qatar_2022.data as src_data
#from road_to_qatar_2022.modelling.encoder_02 import prepareTrainingset
#Add data source for vinesh
#import data as src_data
# for other add the prefix folder road_t0....
from road_to_qatar_2022.modelling.standardScaler_03 import standardScaler
from road_to_qatar_2022.modelling.encoder_02 import prepareTrainingset
#function to fit different model and vizualize them
def metrics_display(model):
    X_hold_test_encoded, X_test_encoded, y_hold_test_encoded, y_test_encoded, X_train_encoded, X_val_encoded, y_train_encoded, y_val_encoded = prepareTrainingset()
    X_train_scaled,X_test_scaled,X_hold_test_scaled = standardScaler()

    model.fit(X_train_scaled,y_train_encoded)
    y_pred = model.predict(X_test_scaled)
    print(classification_report(y_test_encoded,y_pred))
    ConfusionMatrixDisplay.from_predictions(y_test_encoded,y_pred)
    return
