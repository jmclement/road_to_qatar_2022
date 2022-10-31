import os
import pandas as pd

def prepInternational():
    international_results_df = pd.read_csv('raw_data/international-football-results-from-1872-to-2017/results.csv')
    international_shootouts_df = pd.read_csv('raw_data/international-football-results-from-1872-to-2017/shootouts.csv')

    international_merge_df = international_results_df.merge(international_shootouts_df,left_on=['date','home_team','away_team'],right_on=['date','home_team','away_team'])

    print(international_results_df[international_results_df['date']=='1973-04-21'])
    print(international_shootouts_df[international_shootouts_df['date']=='1973-04-21'])
    print(international_merge_df[international_merge_df['date']=='1973-04-08'])

    # print(international_results_df[international_results_df['home_team']=='Ghana'][international_results_df['away_team']=='Senegal'])

if __name__ == '__main__':
    prepInternational()
