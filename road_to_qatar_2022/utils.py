# Add standard imports
import requests
import csv
import os
import re
import pandas as pd

def getTeamsRanking():
    '''
    Function to connect to FIFA website and extract latest list of men's team
    ranking with current and previous points. The list is then saved to the
    data folder
    '''

    # Path to output csv
    csvFile = os.path.join(os.getcwd(),os.path.dirname(__file__),'data/teamsranking.csv')

    # Urls used to query the FIFA website
    initialUrl = "https://www.fifa.com/fifa-world-ranking/men"
    url = "https://www.fifa.com/api/ranking-overview?locale=en&dateId="

    # Set the appropriate headers for request to succeed
    headers = {
        'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/106.0.0.0 Safari/537.36',
    }

    # Inititate the request and get the response to find the latest id
    response = requests.get(initialUrl, headers=headers)
    id_ = re.search(b'dates":\[\{"id":"(.*?)"',response.content).group(1).decode('utf-8')

    # Store url to scrape
    url = url + id_

    # Inititate the request and get the response
    response = requests.get(url, headers=headers)
    jsonResponse = response.json()

    # Prepare output to csv
    fields = ['rank','countryCode','countryName','totalPoints','previousPoints']
    rows = []

    for ranking in jsonResponse['rankings']:
        team = ranking['rankingItem']
        rows.append([team['rank'],team['countryCode'],team['name'],team['totalPoints'],ranking['previousPoints']])


    # data rows of csv file
    with open(csvFile, 'w') as f:

        # using csv.writer method from CSV package
        write = csv.writer(f)

        write.writerow(fields)

        write.writerows(rows)


def getKaggleDataSets():
    '''
    Function that connects to Kaggle using it's API and download a series of
    datasets required as data source.
    Actual datasets are stored in a list that function will loop over and
    download.
    '''

    # Import Kaggle package to leverage it's API
    from kaggle.api.kaggle_api_extended import KaggleApi
    import zipfile

    # Initialise API connection and authenticate using environment variables
    api = KaggleApi()
    resp = api.authenticate()

    # Datasets list
    datasets = [
        'martj42/international-football-results-from-1872-to-2017', # International Matches
        'abecklas/fifa-world-cup' # World Cup matches
        ]

    # Loop over all datasets in list, download and extract each to their
    # corresponding folder

    for dataset in datasets:
        dsName = dataset.split("/")[1]
        api.dataset_download_files(dataset,path=f'raw_data/{dsName}',unzip=True)


def cleanUpCountriesName(df:pd.DataFrame):
    '''
    Function that takes a dataframe as input and cleans up the series
    looking for specific values found in countries dictionary below and
    replacing them with corresponding values.

    Allows for standardising the naming of different countries

    Arguments:
        df: Pandas Dataframe
    Returns:
        Cleaned dataframe
    '''
    countries = {
        "Côte d'Ivoire": "Ivory Coast",
        "C�te d'Ivoire": "Ivory Coast",
        "United States": "USA",
        'rn">Republic of Ireland':"Republic of Ireland",
        'rn">United Arab Emirates':"United Arab Emirates",
        'rn">Trinidad and Tobago':"Trinidad and Tobago",
        'rn">Serbia and Montenegro':"Serbia and Montenegro",
        'rn">Bosnia and Herzegovina':"Bosnia and Herzegovina",
        'IR Iran':"Iran",
        'DR Congo': "Congo DR",
        'Türkiye':"Turkey",
        'Zaire': "Congo DR",
        'North Korea':'Korea DPR',
        'South Korea':'Korea Republic',
        'Soviet Union': "Russia",
        'Vietnam Republic':"Vietnam",
        'Czech Republic':'Czechia',
        'Dutch East Indies':'Indonesia',
        'Germany FR':'Germany',
        'Martinique':'France'
    }

    new_df = pd.DataFrame(df)
    new_df.replace(to_replace=countries,inplace=True)

    return new_df


def addingMissingData(df:pd.DataFrame):
    '''
    Assumptions are being made regarding the 'missing' countries' data.
    Countries that don't exist anymore. We've researched and found their
    highest ranking where possible and adding it to the teamsranking dataframe.
    '''

    '''
    19,,Serbia and Montenegro,674,674
    6,,Yugoslavia,64,64
    64,,Czechoslovakia,24,24
    45,,German DR,,
    '''

    data = {
        'rank':[19,6,64,45],
        'countryCode':['','','',''],
        'countryName':['Serbia and Montenegro','Yugoslavia','Czechoslovakia','German DR'],
        'totalPoints':[674,64,24,0],
        'previousPoints':[674,64,24,0],
    }

    df_additional = pd.DataFrame(data)

    result = pd.concat([df,df_additional])
    return result

if __name__ == '__main__':
    getTeamsRanking()
    getKaggleDataSets()
