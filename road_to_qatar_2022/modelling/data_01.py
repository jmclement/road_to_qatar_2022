# Add standard imports
import requests
import csv
import os
import re
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn import shuffle
from sklearn.model_selection import train_test_split

#Add data source for vinesh
#import data as src_data

#Add data source for everyone
import road_to_qatar_2022.data as src_data

#Import utils for everyone
from road_to_qatar_2022.utils import getTeamsRanking,cleanUpCountriesName,addingMissingData
import road_to_qatar_2022.data as src_data

def getData ():
    '''Function to retrieve the fulldata set and attemp a baseline'''
    # Load the 2 files from the dataset in a pandas dataframe
    fulldataset_df = pd.read_csv('data/fulldataset.csv')
    #print(fulldataset_df.head(10))
    #print(fulldataset_df.describe())
    return fulldataset_df



def getTeams():
    '''Function to create a list of all teams playing football worlcup'''
    team_name = {}
    index = 0
    #matches = getData()
    for idx, row in getData().iterrows():
        name = row['home_team']
        if (name not in team_name.keys()):
            team_name[name] = index
            index += 1

        name = row['away_team']
        if (name not in team_name.keys()):
            team_name[name] = index
            index += 1
    #print(team_name.keys())
    return team_name

def getWinners():
    '''Determining the winner of a particular match.
    For Home team win value is 1, Away team win value is 2 and for Draw value is 0 '''

    winners_df = getData()
    winners_df['home_champion'] = ""
    winners_df['away_champion'] = ""
    winners_df['winner'] = 0

    winners_df.home_champion[winners_df.home_score > winners_df.away_score] = winners_df.home_team
    winners_df.winner[(winners_df.home_score > winners_df.away_score)] = 1
    winners_df.away_champion[winners_df.home_score < winners_df.away_score] = winners_df.away_team
    winners_df.winner[(winners_df.home_score < winners_df.away_score)] = 2
    winners_df.winner[(winners_df.win_conditions != " ")] = 0

    print("Data ready")
    return winners_df


if __name__ == "__main__":
    getWinners()
