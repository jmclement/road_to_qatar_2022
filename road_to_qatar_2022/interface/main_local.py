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
from pathlib import Path

#Add data source for everyone
#import road_to_qatar_2022.data as src_data
#Import utils for everyone
#from road_to_qatar_2022.utils import (addingMissingData, cleanUpCountriesName,
 #                                     getTeamsRanking)
#from road_to_qatar_2022.modelling import (data_01)

#Add data source for vinesh
import road_to_qatar_2022.data as src_data
# from modelling import (data_01,encoder_02,standardScaler_03, modelling_XGBoost_04,mode_tunning_XGB_05, tune_model_with_params_06)
import road_to_qatar_2022.modelling.data_01 as data_01
import road_to_qatar_2022.modelling.tune_model_with_params_06 as tune_model_with_params_06
import road_to_qatar_2022.dataprep as dataprep
import road_to_qatar_2022.utils as utils
import pickle

import warnings
warnings.filterwarnings("ignore")


def getTeams (teamX):
    '''Get the Team Id from the inputted team names'''

    team_name=data_01.getTeams()
    team_id=team_name[teamX]

    return team_id

def getChampions (teamX):
    '''Get the Team number of wins of the FIFA world CUP from the inputted team names'''


    winners_df = dataprep.handlingMissingData()[2]
    winners = winners_df['Winner'].map(lambda n: 'Germany' if n == 'Germany FR' else n).value_counts()
    championship = winners.get(teamX) if winners.get(teamX) != None else 0

    return championship

def getTeamRankings (teamX):
    '''Get the Team number of wins of the FIFA world CUP from the inputted team names'''
    team1=teamX
    teams_ranking_df = data_01.getTeamRankings()
    team1_rank_1=teams_ranking_df[teams_ranking_df['countryName']==team1]['rank']
    team1_totalPoints_1=teams_ranking_df[teams_ranking_df['countryName']==team1]['totalPoints']
    team1_previousPoints_1=teams_ranking_df[teams_ranking_df['countryName']==team1]['previousPoints']
    team1_rank_1=team1_rank_1.values[0]
    team1_totalPoints_1=team1_totalPoints_1.values[0]
    team1_previousPoints_1=team1_previousPoints_1.values[0]
    #print(team1_rank_4)
    #print(team1_totalPoints_1.values)
    #print(team1_previousPoints_1.values)
    return (team1_rank_1,team1_totalPoints_1,team1_previousPoints_1)
    #return (team1_rank_4)

def callTeams(X):
    test_input1= X
    #team1_rank_1,team1_totalPoints_1,team1_previousPoints_1= getTeamRankings(test_input1)
    team1_rank_3= getTeamRankings(test_input1)
    print(team1_rank_3)
    #print(team1_totalPoints_1)
    #print(team1_previousPoints_1)
    return

def createRewriteTable ():
    '''The rewritetable is used to temporarily store the results of a prediction that would be used to append to the team_id data frame
    to update the source dataframe from which the model is trained, for basing the predictions on the source table along with previous
    predicted data as well
    '''
    ReWrite_pred_df=pd.DataFrame(columns = ['Home Team Name',
                                        'Away Team Name',
                                        'home_team_rank',
                                        'home_team_points',
                                        'home_team_previous_points',
                                        'away_team_rank',
                                        'away_team_points',
                                        'away_team_previous_points',
                                        'Home Team Champion',
                                        'Away Team Champion',
                                        'Winner'])

    return ReWrite_pred_df

def prediction(team1,team2,df):
    '''This function predicts the matches for two teams playing against each othre'''

    # input data
    test_input1= team1
    test_input2 = team2

    # Team ids
    id1=getTeams(test_input1)
    id2=getTeams(test_input2)

    # Team past FIFA wins
    championship1 = getChampions(test_input1)
    championship2 = getChampions(test_input2)

    # Team rankings
    team1_rank_1,team1_totalPoints_1,team1_previousPoints_1= getTeamRankings(test_input1)
    team2_rank,team2_totalPoints,team2_previousPoints= getTeamRankings(test_input2)

    # Storing the data that will be needed for the input to calling the model
    t = np.array([id1, id2, team1_rank_1, team1_totalPoints_1, team1_previousPoints_1, team2_rank, team2_totalPoints, team2_previousPoints, championship1, championship2]).astype('float64')
    t = np.reshape(t, (1,-1))

    # Instantiating the tuned model and calling it with the teams data for which a prediciton is required
    loaded_model = pickle.load(open(os.path.join(src_data.__path__[0],'model_tuned'), 'rb'))
    XGB = loaded_model
    #XGB = tune_model_with_params_06.new_tuned_model()

    y_rc = XGB.predict_proba(t)[0]
    #print(XGB.get_params())
    #return XGB
    # collecting the data used for the prediction and its resulting prediction to be stored in a temporary dataframe
    home_team_rank=team1_rank_1
    home_team_points=team1_totalPoints_1
    home_team_previous_points=team1_previousPoints_1
    away_team_rank=team2_rank
    away_team_points=team2_totalPoints
    away_team_previous_points=team2_previousPoints
    Home_Team_Champion=championship1
    Away_Team_Champion=championship2
    # Determining the outcome of the prediciton if its a win, loss or draw
    conditions = [y_rc[0]> y_rc[1] and y_rc[0]> y_rc[2],
                y_rc[1]> y_rc[2],
                y_rc[2]>y_rc[1]]
    values =[0,1,2]

    Winner=np.select(conditions,values)
    # Intantiating the temporaty table and writing the data to it
    #ReWrite_pred_df = createRewriteTable()
    ReWrite_pred_df = df
    ReWrite_pred_df=ReWrite_pred_df.append({'Home Team Name':id1,
                                'Away Team Name':id2,
                                'home_team_rank':home_team_rank,
                                'home_team_points':home_team_points,
                                'home_team_previous_points':home_team_previous_points,
                                'away_team_rank':away_team_rank,
                                'away_team_points':away_team_points,
                                'away_team_previous_points':away_team_previous_points,
                                'Home Team Champion':Home_Team_Champion,
                                'Away Team Champion':Away_Team_Champion,
                                'Winner':Winner},
                                ignore_index = True)






    text = ('Chance for '+test_input1+' to win against '+test_input2+' is {}\nChance for '+test_input2+' to win against '+test_input1+' is {}\nChance for '+test_input1+' and '+test_input2+' draw is {}').format(y_rc[1]*100,y_rc[2]*100,y_rc[0]*100)
    #print(y_rc,text)
    #print(ReWrite_pred_df.head())
    return y_rc, text, ReWrite_pred_df
    #print(test_input1,id1,championship1,home_team_rank,home_team_points,home_team_previous_points)
    #return test_input1,id1,championship1,home_team_rank,home_team_points,home_team_previous_points

def prediction_fixtures():
    '''This function calls the prediction function'''

    fixtures_wc = pd.read_csv(os.path.join(src_data.__path__[0],'fixtures_2_perGrp.csv'))

    # fixtures_wc = pd.read_csv('../data/fixtures_2_perGrp.csv')
    fixtures_wc = fixtures_wc.drop(['Round Number', 'Date', 'Location', 'Result'], 1)
    output_df = pd.DataFrame(columns = ['Group','Home_team','Away_team','Home_win','Away_win','Draw','Winner'])
    fix = fixtures_wc.loc[0:17, :]
    ReWrite_pred_df = createRewriteTable()
    #prediction = prediction()
    #Group A

    # output_df = groupPrediction(fix,'A',ReWrite_pred_df,output_df)
    '''
    # for i in range(len(fix)):
    #     array = (fix['Group'] == 'Group A')
    #     index = []
    #     for ar in range(len(array)):
    #         if array[ar] == True:
    #             index.append(ar)

    # for indx in range(len(index)):
    #     corr_row = fix.loc[index[indx]]

    #     probs, text, ReWrite_pred_df = prediction(corr_row['Home Team'], corr_row['Away Team'],ReWrite_pred_df)
    #     print('Results \n', text)
    #     conditions = [probs[0]> probs[1] and probs[0]> probs[2],
    #            probs[1]> probs[2],
    #            probs[2]>probs[1]]
    #     values =[0,1,2]

    #     Winner=np.select(conditions,values)
    #     output_df=output_df.append({'Group':'Group A',
    #                             'Home_team':corr_row['Home Team'],
    #                             'Away_team':corr_row['Away Team'],
    #                             'Home_win':probs[1],
    #                             'Away_win':probs[2],
    #                             'Draw':probs[0],
    #                             'Winner':Winner},
    #                             ignore_index = True)
    '''

    groups = ['A','B','C','D','E','F','G','H']

    for group in groups:
        output_df = groupPrediction(fix,group,ReWrite_pred_df,output_df)


    # Save to csv
    output_df.to_csv(os.path.join(src_data.__path__[0],'output_fixtures_2_perGrp.csv'),index=False,header=True)
    #ReWrite_pred_df.to_csv(os.path.join(src_data.__path__[0],'ReWrite_pred_df.csv'),index=False,header=True)
    #print(ReWrite_pred_df.head())
    return output_df,ReWrite_pred_df


def groupPrediction(fix,grp,ReWrite_pred_df,output_df):
    grpVal = f'Group {grp}'
    for i in range(len(fix)):
        array = (fix['Group'] == grpVal)
        index = []
        for ar in range(len(array)):
            if array[ar] == True:
                index.append(ar)

    for indx in range(len(index)):
        corr_row = fix.loc[index[indx]]

        probs, text, ReWrite_pred_df = prediction(corr_row['Home Team'], corr_row['Away Team'],ReWrite_pred_df)
        print('Results \n', text)
        conditions = [probs[0] > probs[1] and probs[0] > probs[2],
               probs[1] > probs[2],
               probs[2] > probs[1]]
        values =[0,1,2]

        Winner=np.select(conditions,values)
        output_df = output_df.append({'Group':grpVal,
                                'Home_team':corr_row['Home Team'],
                                'Away_team':corr_row['Away Team'],
                                'Home_win':probs[1],
                                'Away_win':probs[2],
                                'Draw':probs[0],
                                'Winner':Winner},
                                ignore_index = True)

    return output_df





def appendToTeamId():
    '''This function appendds to the source data for the model and retrains and tunes the model'''
    # read the last predicted matches
    output_df,ReWrite_pred_df=prediction_fixtures
    #ReWrite_pred_df = pd.read_csv('data/ReWrite_pred_df.csv')
    # read the source data for the model training
    Team_id=data_01.replace_name()
    # append the predicted to the source, here i used a new df, temporarily for testing and validation, until its validated, the we can simply append to the team_id
    Team_id_updated = Team_id.append(ReWrite_pred_df,ignore_index = True)
    # calling the module to load the model and tuning the model
    reTrainTuneModel= tune_model_with_params_06.importModelParams()
    ReWrite_pred_df.truncate()
    output_df.truncate()
    return

if __name__ == "__main__":
    prediction_fixtures()
    #callTeams('Iran')
