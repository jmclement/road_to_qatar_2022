import os
import pandas as pd

def prepInternational():
    '''
    Function that loads the downloaded Internation dataset and merge the two
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

    return final_international_merge_df


if __name__ == '__main__':
    prepInternational()
