# Add standard imports
import requests
import csv
import os


def getTeamsRanking():
    '''
    Function to connect to FIFA and extract list of Men Team ranking with
    current and previous points
    '''

    # Path to output csv
    csvFile = os.path.join(os.getcwd(),os.path.dirname(__file__),'../raw_data/teamsranking.csv')

    # Store url to scrape
    url = "https://www.fifa.com/api/ranking-overview?locale=en&dateId=id13792"

    # Set the appropriate headers for request to succeed
    headers = {
        'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/106.0.0.0 Safari/537.36',
    }

    # Inititate the request and get the response
    response = requests.get(url, headers=headers)
    jsonResponse = response.json()

    # Prepare output to csv
    fields = ['rank','countryCode','countryName','totalPoints','previousPoints']
    rows = []

    for ranking in jsonResponse['rankings']:
        team = ranking['rankingItem']
        #print(team['rank'],team['countryCode'],team['name'],team['totalPoints'],ranking['previousPoints'])
        rows.append([team['rank'],team['countryCode'],team['name'],team['totalPoints'],ranking['previousPoints']])


    # data rows of csv file
    with open(csvFile, 'w') as f:

        # using csv.writer method from CSV package
        write = csv.writer(f)

        write.writerow(fields)

        write.writerows(rows)

# print(csvFile)
# print(os.getcwd())
# print(os.path.dirname(__file__))

if __name__ == '__main__':
    getTeamsRanking()
