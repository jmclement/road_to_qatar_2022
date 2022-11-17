# Add standard imports
import csv
import os
import re

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import requests
import seaborn as sns
from sklearn.utils import shuffle
from sklearn.model_selection import train_test_split

#Add data source for everyone
#import road_to_qatar_2022.data as src_data
#Import utils for everyone
#from road_to_qatar_2022.utils import (addingMissingData, cleanUpCountriesName,
                                      #getTeamsRanking)

#Add data source for vinesh
import data as src_data



def getData ():
    '''Function to retrieve the fulldata set and attemp a baseline'''
    # Load the 2 files from the dataset in a pandas dataframe
    fulldataset_df = pd.read_csv('data/fulldataset.csv')
    #print(fulldataset_df.info())
    #print(fulldataset_df.describe())
    return fulldataset_df



def getTeams():
    '''Function to create a list of all teams playing football worlcup'''
    team_name = {}
    index = 0
    #matches = getData()
    for idx, row in getData().iterrows():
        name = row['Home Team Name']
        if (name not in team_name.keys()):
            team_name[name] = index
            index += 1

        name = row['Away Team Name']
        if (name not in team_name.keys()):
            team_name[name] = index
            index += 1
    #print(team_name['Indonesia'])
    return team_name

def replace_name():
    '''Function for replacing the team names by id'''
    Team_id=getData()
    team_name = getTeams()

    for index_label, row_series in Team_id.iterrows():
    # For each row update the 'Team Name' value to it's matching ID value from the team_name
        Team_id.at[index_label , 'Home Team Name'] =  (team_name.get( Team_id.at[index_label , 'Home Team Name']))
        Team_id.at[index_label , 'Away Team Name'] =  (team_name.get( Team_id.at[index_label , 'Away Team Name']))
    # Now we dont need number of goals and year

    Team_id = Team_id.drop(['Date','Home Team Goals', 'Away Team Goals'], 1)

    #Team_id.replace(np.nan,0)
    Team_id=Team_id.fillna(0)
    Team_id= Team_id[['Home Team Name',
                 'Away Team Name',
                 'home_team_rank',
                 'home_team_points',
                 'home_team_previous_points',
                 'away_team_rank',
                 'away_team_points',
                 'away_team_previous_points',
                 'Home Team Champion',
                 'Away Team Champion',
                 'Winner']]
    #print(Team_id.isnull().sum().sum())
    return Team_id

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

def getKnockoutround():
    '''From Sample Model notebook: ## Make dataset for knockout round'''


    #Filter the teams participating in World cup 22
    list_2022 = ['Qatar', 'Germany', 'Denmark', 'Brazil', 'France', 'Belgium', 'Croatia', 'Spain', 'Serbia', 'England', 'Switzerland', 'Netherlands', 'Argentina', 'IR Iran', 'Korea Republic', 'Japan', 'Saudi Arabia', 'Ecuador', 'Uruguay', 'Canada', 'Ghana', 'Senegal', 'Portugal', 'Poland', 'Tunisia', 'Morocco', 'Cameroon', 'USA', 'Mexico', 'Wales', 'Australia', 'Costa Rica']


    full_df = getData()

    #ADD winner column on dataset
    winner = []
    for i in range (len(full_df['home_team'])):
        if full_df ['home_score'][i] > full_df['away_score'][i]:
            winner.append('win')
        elif full_df['home_score'][i] < full_df ['away_score'][i]:
            winner.append('lose')
        else:
            winner.append('Draw')
    full_df['home_team_result'] = winner

    final_df = full_df[(full_df["home_team"].apply(lambda x: x in list_2022)) | (full_df["away_team"].apply(lambda x: x in list_2022))]
    final_df = final_df.drop(['date','win_conditions','home_team_previous_points','away_team_previous_points','home_score','away_score'], axis=1)
    final_df['home_team_result'] = final_df['home_team_result'].map({'win':1, 'Draw':2, 'lose':0})
    #Holdout another DF for pipeline
    pipe_DF = final_df
    #Create dummies for categorical columns
    final_df = pd.get_dummies(final_df)


    full_df = full_df.copy()
    #change draw result to win depending on win conditions
    full_df['knockout_result'] = np.where((full_df['home_team_result'] == 'Draw') & (full_df['win_conditions']  == full_df['home_team']), 'win', full_df['home_team_result'])
    #change draw result to lose depending on win conditions
    full_df['knockout_result'] = np.where((full_df['knockout_result'] == 'Draw'), 'lose',
                                      full_df['knockout_result'])
    #filter teams qualified for world cup 2022
    final_knockout_df = full_df[(full_df["home_team"].apply(lambda x: x in list_2022)) |
                            (full_df["away_team"].apply(lambda x: x in list_2022))]
    #change win, lose into numerical
    final_knockout_df['knockout_result'] = final_knockout_df['knockout_result'].map({'win':1, 'lose':0})
    #drop unecessary column for knockout dataset
    final_knockout_df = final_knockout_df.drop(['date','win_conditions','home_team_previous_points',
                                            'away_team_previous_points','home_team_result','home_score','away_score'], axis=1)

    #Knockout Round
    #Holdout another DF for pipeline
    pipe_DF_knockout = final_knockout_df
    #Create dummies for categorical columns
    knockout_final_df = pd.get_dummies(final_knockout_df)



    #print(final_df['home_team_result'])
    return final_knockout_df, final_df

if __name__ == "__main__":
    replace_name()
