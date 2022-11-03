import os
import pandas as pd
from road_to_qatar_2022.utils import getTeamsRanking,cleanUpCountriesName
import road_to_qatar_2022.data as src_data

def prepInternational():
    '''
    Function that loads the downloaded International dataset and merge the two
    files. Additionally renaming/processing the information by limiting the data
    to teams participating in the 2022 World Cup
    '''

    # List of countries participating in the Qatar 2022 World Cup
    participating_countries = ('Quatar',
                           'Qatar'
                           'Ecuador',
                           'Senegal',
                           'Netherlands',
                           'England',
                           'IR Iran',
                           'Iran'
                           'USA',
                           'Wales',
                           'Argentina',
                           'Saudi Arabia',
                           'Mexico',
                           'Poland',
                           'France',
                           'Australia',
                           'Denmark',
                           'Tunisia',
                           'Spain',
                           'Costa Rica',
                           'Germany',
                           'Japan',
                           'Belgium',
                           'Canada',
                           'Morocco',
                           'Croatia',
                           'Brazil',
                           'Serbia',
                           'Switzerland',
                           'Cameroon',
                           'Portugal',
                           'Ghana',
                           'Uruguay'
                           'Korea Republic',
                           'South Korea',
                           'North Korea')

    # Load the 2 files from the dataset in a pandas dataframe
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
    international_merge_filtered_df = international_merge_df[international_merge_df['home_team'].isin(participating_countries) |
                         international_merge_df['away_team'].isin(participating_countries) ]

    # Final DF filtered to drop columns not needed
    final_international_merge_df=international_merge_filtered_df[['date','home_team','away_team','home_score','away_score','win_conditions']]

    final_international_merge_df = cleanUpCountriesName(final_international_merge_df)

    return final_international_merge_df


def prepWorldCupDF():
    '''
    Function that loads the downloaded Worldcup matches dataset and merge the three
    files. Additionally renaming/processing the information.
    '''

    # Load the three files from downloaded csv
    worldCupMatches_df = pd.read_csv('raw_data/fifa-world-cup/WorldCupMatches.csv')
    worldCupPlayers_df = pd.read_csv('raw_data/fifa-world-cup/WorldCupPlayers.csv')
    worldCups_df = pd.read_csv('raw_data/fifa-world-cup/WorldCups.csv')

    # Cleaning up the worldCupMatches df
    worldCupMatches_df['Date'] = (pd.to_datetime(worldCupMatches_df['Datetime']))
    worldCupMatches_df['Date'] = worldCupMatches_df['Date'].dt.date
    worldCupMatches_df['Date'] = pd.to_datetime(worldCupMatches_df['Date'])
    worldCupMatches_df = cleanUpCountriesName(worldCupMatches_df)

    # Find the dates for World Cup matches only
    worldCupDates = (worldCupMatches_df['Date'].unique())

    # Filter down to get unique World Cup matches dates
    uniqueWorldCupDates = [str(i)[:10] for i in worldCupDates]

    # Call to prepInternational to get the Internation matches dataframe
    finalInternational_df = prepInternational()

    # From the international matches filter to obtain only matches that were not
    # worldcup games and settings appropriate date format
    nonWorldCupInternationalMatches = finalInternational_df[~finalInternational_df['date'].isin(uniqueWorldCupDates)]
    nonWorldCupInternationalMatches['date'] = pd.to_datetime(nonWorldCupInternationalMatches['date'])

    # Merging World Cup matches with Non World Cup Internation matches
    # mergedWorlCupMatches_df = worldCupMatches_df.merge(nonWorldCupInternationalMatches, left_on='Date', right_on='date', how='outer')

    # Filter WorldCup matches
    filtered_WorldCupMatches_df = worldCupMatches_df[worldCupMatches_df[[
        'Date',
        'Home Team Name',
        'Away Team Name',
        'Home Team Goals',
        'Away Team Goals'
        ]].notnull().all(1)]

    finalWorldCupMatches_df =filtered_WorldCupMatches_df[[
        'Date',
        'Home Team Name',
        'Away Team Name',
        'Home Team Goals',
        'Away Team Goals',
        'Win conditions']]

    # Renaming the columns
    finalWorldCupMatches_df.rename(columns={"Date": "date",
                    "Home Team Name": "home_team",
                    "Away Team Name": "away_team",
                    "Home Team Goals": "home_score",
                    "Away Team Goals": "away_score",
                    "Win conditions": "win_conditions"}, inplace=True)

    # Merging the WorldCup matches with the non WorldCup international matches
    frames = [finalWorldCupMatches_df,nonWorldCupInternationalMatches]
    mergedWorldCupMatches_df = pd.concat(frames)

    return mergedWorldCupMatches_df


def prepDataEng():
    '''
    Function to combine data from the teams ranking dataset with the final
    output dataframe from prepWorldCupDF
    '''
    worldCup_DF = prepWorldCupDF()

    if not os.path.exists(os.path.join(src_data.__path__[0],'teamsranking.csv')):
        getTeamsRanking()

    teamsRanking_DF = pd.read_csv(os.path.join(src_data.__path__[0],'teamsranking.csv'))

    teamsRanking_DF = cleanUpCountriesName(teamsRanking_DF)

    fullMerge_DF = worldCup_DF.merge(teamsRanking_DF,
                                     left_on='home_team',
                                     right_on='countryName',
                                     how='left').merge(teamsRanking_DF,
                                                       left_on='away_team',
                                                       right_on='countryName',
                                                       how='left',
                                                       suffixes=('_home','_away'))
    fullMerge_DF.rename(columns={
        'rank_home': 'home_team_rank',
        'totalPoints_home': 'home_team_points',
        'previousPoints_home': 'home_team_previous_points',
        'rank_away': 'away_team_rank',
        'totalPoints_away': 'away_team_points',
        'previousPoints_away': 'away_team_previous_points',
    },inplace=True)

    fullMerge_DF.drop(['countryCode_home',
                       'countryName_home',
                       'countryCode_away',
                       'countryName_away'],axis=1,inplace=True)

    fullMerge_DF.to_csv(os.path.join(src_data.__path__[0],'fulldataset.csv'),index=False,header=True)



if __name__ == '__main__':
    prepDataEng()
