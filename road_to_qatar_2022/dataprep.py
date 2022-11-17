import os
import pandas as pd
import numpy as np
# for everyone import utils path issues
#from road_to_qatar_2022.utils import getTeamsRanking,cleanUpCountriesName,addingMissingData
#import road_to_qatar_2022.data as src_data
# for vinesh import utils path issues
from utils import getTeamsRanking,cleanUpCountriesName,addingMissingData
import data as src_data

def loadData():
    '''Importing the datasets from the data folders'''
    # Importing Files
    data_matches = pd.read_csv('../raw_data/data/FIFA World Cup/WorldCupMatches.csv')
    data_players = pd.read_csv('../raw_data/data/FIFA World Cup/WorldCupPlayers.csv')
    data_cups = pd.read_csv('../raw_data/data/FIFA World Cup/WorldCups.csv')
    # Adding international Matches for Qatar first participation in the World Cup 2022 as Host country
    international_matches = pd.read_csv('../raw_data/data/International football results from 1872 to 2022/results.csv')

    return (data_matches,data_players,data_cups,international_matches)

def handlingMissingData():
    '''Cleaning of the null values for the datasets'''

    data_matches,data_players,data_cups,international_matches = loadData()

    x1 = np.array(data_players['Event'].isna())
    x2 = (data_players['Position'].isna())   #True = 0

    for i in range(len(x1)):
        if x1[i] == False:
            x2[i] = x2.replace(True, False).all()

    x2_value = x2.astype(int)
    x2_value = x2_value.replace([0,1], ['C','GK'])
    # Replaciing Position column with x2_value in the dataset
    data_players = data_players.drop('Position', axis = 1)
    data_players_new = pd.concat([data_players, x2_value], axis = 1)

    # Cleaning data_matches
    data_matches_new = data_matches.loc[0:851,:]
    data_matches_new['Attendance'] = data_matches_new['Attendance'].fillna(data_matches_new['Attendance'].value_counts().idxmax())

    # Cleaning data_cups
    data_cups['Attendance'] = data_cups['Attendance'].str.replace('.', '')

    return (data_players_new,data_matches_new,data_cups,international_matches)

def replaceCountryName():
    data_matches_new=handlingMissingData()[1]
    data_matches_new=cleanUpCountriesName(data_matches_new)

    return data_matches_new


def prepInternational():
    '''
    Function that loads the downloaded International dataset and merge the two
    files. Additionally renaming/processing the information by limiting the data
    to teams participating in the 2022 World Cup
    '''
    data_matches_new = replaceCountryName()

    # Load the 1 international matches files from the dataset in a pandas dataframe
    international_results_df = pd.read_csv('raw_data/international-football-results-from-1872-to-2017/results.csv')
    international_shootouts_df = pd.read_csv('raw_data/international-football-results-from-1872-to-2017/shootouts.csv')

    # Merging the content of the 2 dataframes into a merged df
    international_merge_df = international_results_df.merge(international_shootouts_df,left_on=['date','home_team','away_team'],right_on=['date','home_team','away_team'])

    # Renaming the columns
    international_merge_df.rename(columns={
        "Date": "date",
        "home_team": "home_team",
        "away_team": "away_team",
        "home_score": "home_score",
        "away_score": "away_score",
        "tournament": "tournament",
        "city":"city",
        "country": "country",
        "neutral": "neutral",
        "winner": "win_conditions"
    }, inplace=True)

    # Filtering the dataframe to have only the participating countries
    # Creating a list of all teams playing football worlcup:
    team_name = {}
    index = 0
    for idx, row in data_matches_new.iterrows():
        name = row['Home Team Name']
        if (name not in team_name.keys()):
            team_name[name] = index
            index += 1

        name = row['Away Team Name']
        if (name not in team_name.keys()):
            team_name[name] = index
            index += 1
    team_name['Qatar']= 80

    A_list = list(team_name.keys())

    international_merge_df = cleanUpCountriesName(international_merge_df)
    international_merge_df = international_merge_df[international_merge_df['home_team'].isin(A_list) |
                         international_merge_df['away_team'].isin(A_list) ]

    # Final DF filtered to drop columns not needed

    international_merge_df=international_merge_df[['date','home_team','away_team','home_score','away_score','win_conditions']]

    #final_international_merge_df = cleanUpCountriesName(final_international_merge_df)

    print(data_matches_new.info())
    return (international_merge_df,data_matches_new)
def match_winner(df:pd.DataFrame):
    conditions = [
    ((df['Home Team Goals'].astype(int)) == (df['Away Team Goals'].astype(int))),
    ((df['Home Team Goals'].astype(int)) > (df['Away Team Goals'].astype(int))),
    ((df['Home Team Goals'].astype(int)) < (df['Away Team Goals'].astype(int))),
    ]
    values = [0, 1, 2]

    df['Win conditions'] = np.select(conditions, values)
    return df

def prepWorldCupDF():
    '''
    Function that loads the downloaded Worldcup matches dataset and merge the three
    files. Additionally renaming/processing the information.
    '''
    # load the cleaned data world cup matches and international matches data from
    international_merge_df,data_matches_new = prepInternational()

    # Load the three files from downloaded csv

    #worldCupMatches_df = pd.read_csv('raw_data/fifa-world-cup/WorldCupMatches.csv')
    #worldCupPlayers_df = pd.read_csv('raw_data/fifa-world-cup/WorldCupPlayers.csv')
    #worldCups_df = pd.read_csv('raw_data/fifa-world-cup/WorldCups.csv')

    # Cleaning up the worldCupMatches df
    data_matches_new['Date'] = (pd.to_datetime(data_matches_new['Datetime']))
    data_matches_new['Date'] = data_matches_new['Date'].dt.date
    data_matches_new['Date'] = pd.to_datetime(data_matches_new['Date'])
    #worldCupMatches_df = cleanUpCountriesName(worldCupMatches_df)

    data_matches_new = match_winner(data_matches_new)

    # Find the dates for World Cup matches only
    worldCupDates = (data_matches_new['Date'].unique())

    # Filter down to get unique World Cup matches dates
    uniqueWorldCupDates = [str(i)[:10] for i in worldCupDates]

    # Call to prepInternational to get the Internation matches dataframe
    #finalInternational_df = prepInternational()

    # From the international matches filter to obtain only matches that were not
    # worldcup games and settings appropriate date format
    nonWorldCupInternationalMatches = international_merge_df[~international_merge_df['date'].isin(uniqueWorldCupDates)]
    nonWorldCupInternationalMatches['date'] = pd.to_datetime(nonWorldCupInternationalMatches['date'])

    # Rename the columns for the international matches so that they align for the merge with FIFA world cup matches(data_matches_to_use)
    nonWorldCupInternationalMatches.rename(columns = {'date':'Date','home_team':'Home Team Name','home_score':'Home Team Goals','away_score':'Away Team Goals','away_team':'Away Team Name','win_conditions':'Win conditions'},inplace=True)

    # Call the function to convert the scores columns to a winners column for prediction purposes (W,L,D)
    nonWorldCupInternationalMatches = match_winner(nonWorldCupInternationalMatches)

    # Drop unwanted data from data_new_matches
    data_matches_to_use = data_matches_new.drop(['Year','Datetime', 'Stage', 'Stadium', 'City',
                                                'Attendance', 'Half-time Home Goals', 'Half-time Away Goals',
                                                'Referee', 'Assistant 1', 'Assistant 2',
                                                'RoundID', 'MatchID', 'Home Team Initials', 'Away Team Initials'], 1)
    nonWorldCupInternationalMatches.rename(columns = {'Win conditions':'Winner'},inplace = True)

    # Rename the columns for the world cup matches so that they align for the merge with international matches(nonWorldCupInternationalMatches)
    data_matches_to_use.rename(columns = {'Win conditions':'Winner'},inplace = True)
    data_matches_to_use = data_matches_to_use[['Date','Home Team Name','Home Team Goals','Away Team Goals','Away Team Name','Winner']]

    # Merging World Cup matches with Non World Cup Internation matches with an append
    #mergedWorlCupMatches_df = data_matches_to_use.merge(nonWorldCupInternationalMatches, left_on='Date', right_on='date', how='outer')

    mergedWorlCupMatches_df = data_matches_to_use.append(nonWorldCupInternationalMatches,ignore_index = True)


    # Filter WorldCup matches
    #filtered_WorldCupMatches_df = mergedWorlCupMatches_df[mergedWorlCupMatches_df[[
        #'Date',
        #'Home Team Name',
        #'Away Team Name',
        #'Home Team Goals',
        #'Away Team Goals'
        #]].notnull().all(1)]

    #finalWorldCupMatches_df =filtered_WorldCupMatches_df[[
        #'Date',
        #'Home Team Name',
        #'Away Team Name',
        #'Home Team Goals',
        #'Away Team Goals',
        #'Win conditions']]


    # Renaming the columns
    #finalWorldCupMatches_df.rename(columns={"Date": "date",
                    #"Home Team Name": "home_team",
                    #"Away Team Name": "away_team",
                    #"Home Team Goals": "home_score",
                    #"Away Team Goals": "away_score",
                    #"Win conditions": "win_conditions"}, inplace=True)


    # Merging the WorldCup matches with the non WorldCup international matches
    #frames = [data_matches_to_use,nonWorldCupInternationalMatches]
    #mergedWorldCupMatches_df_1 = pd.concat(frames)

    #print(mergedWorldCupMatches_df_1.shape)
    #print(mergedWorlCupMatches_df.info())
    return mergedWorlCupMatches_df



def prepDataEng():
    '''
    Function to combine data from the teams ranking dataset with the final
    output dataframe from prepWorldCupDF
    '''

    # Get world cup dataframe from prepWorldCupDF
    worldCup_DF = prepWorldCupDF()

    # Check if teamsranking data is present, else download it
    if not os.path.exists(os.path.join(src_data.__path__[0],'teamsranking.csv')):
        getTeamsRanking()

    # Process the data, adding missing countries and cleaning up the names
    teamsRanking_DF = pd.read_csv(os.path.join(src_data.__path__[0],'teamsranking.csv'))
    teamsRanking_DF = addingMissingData(teamsRanking_DF)
    teamsRanking_DF = cleanUpCountriesName(teamsRanking_DF)
    teamsRanking_DF.to_csv(os.path.join(src_data.__path__[0],'teamsranking.csv'),index=False,header=True)
    # Merge the two datasets
    fullMerge_DF = worldCup_DF.merge(teamsRanking_DF,
                                     #left_on='home_team',
                                     left_on='Home Team Name',
                                     right_on='countryName',
                                     how='left').merge(teamsRanking_DF,
                                                       #left_on='away_team',
                                                       left_on='Away Team Name',
                                                       right_on='countryName',
                                                       how='left',
                                                       suffixes=('_home','_away'))
    # Rename the columns in the dataset
    fullMerge_DF.rename(columns={
        'rank_home': 'home_team_rank',
        'totalPoints_home': 'home_team_points',
        'previousPoints_home': 'home_team_previous_points',
        'rank_away': 'away_team_rank',
        'totalPoints_away': 'away_team_points',
        'previousPoints_away': 'away_team_previous_points',
    },inplace=True)

    # Drop unused columns
    fullMerge_DF.drop(['countryCode_home',
                       'countryName_home',
                       'countryCode_away',
                       'countryName_away'],axis=1,inplace=True)

    # Save to csv
    #fullMerge_DF.to_csv(os.path.join(src_data.__path__[0],'fulldataset.csv'),index=False,header=True)

    return fullMerge_DF,teamsRanking_DF

def countChampions():

    '''Count the past world cup champions'''
    df = prepDataEng()[0]

    df['Home Team Champion'] = 0
    df['Away Team Champion'] = 0

    winners_df = handlingMissingData()[2]

    winners = winners_df['Winner'].map(lambda n: 'Germany' if n == 'Germany FR' else n).value_counts()
    # iterate over the dataframe row by row
    for index_label, row_series in df.iterrows():
    # For each row update the 'Champion' value to it's matching value from the winners list of past FIFA world cup champions
        df.at[index_label , 'Home Team Champion'] =  (winners.get( df.at[index_label , 'Home Team Name']))
        df.at[index_label , 'Away Team Champion'] =  (winners.get( df.at[index_label , 'Away Team Name']))

    #Replace the NaN for teams with no past championship wons to 0
    df=df.fillna(0)

    #print(df[df['Home Team Champion']==0][['Home Team Name','Home Team Champion']])
    fullMerge_DF = df
    #print(fullMerge_DF.info())
    # Save to csv
    fullMerge_DF.to_csv(os.path.join(src_data.__path__[0],'fulldataset.csv'),index=False,header=True)
    winners.to_csv(os.path.join(src_data.__path__[0],'winners.csv'),index=False,header=True)
    return fullMerge_DF


if __name__ == '__main__':
    countChampions()
