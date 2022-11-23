# Importing required Modules for creating API
from fastapi import FastAPI
from fastapi.openapi.utils import get_openapi
from pydantic import BaseModel
from typing import List
import road_to_qatar_2022.interface.main_local as main_local
import pandas as pd

# Define a class to model the request body content expected in POST requests
# Team selection request body model
class SelectedTeam(BaseModel):
    name: str


# Match request body model
class MatchTemplate(BaseModel):
    homeTeam: str
    awayTeam: str


# Matches list request body model
class MatchesList(BaseModel):
    matches: List[MatchTemplate] = []

model_df = pd.DataFrame()
model_output = pd.DataFrame()


# Instantiate the FastAPI
app = FastAPI()


# Define default route
@app.get('/')
def index():
    return {'status':True,
            'Note': 'API up and running'
            }


# Define route to get winner
@app.get('/winner')
def getWinner():
    return {'Res':'Winner called'}


# Define route for choosing the selected team
@app.post('/selected_team')
def setPreferedTeam(param:SelectedTeam):

    matches = model_output[(model_output['Home_team'] == param.name) | (model_output['Away_team'] == param.name)]

    matches['Winner'] = matches['Winner'].map(int)

    return matches.to_dict(orient='index')


# Route to 'save' the results of predictions
@app.post('/update_predictions')
def updatePredictions():
    return {'Called update predictions'}


# Route to generate the predictions for a match or list of matches
@app.post('/predict')
def predictResults(param:MatchesList):
    number_of_matches = len(param.matches)
    match = param.matches[0]
    # output = "{"
    # for i in param.matches:
    #     output += f"{i.homeTeam} v/s {i.awayTeam},"
    # output += "}"

    table = main_local.createRewriteTable()

    probs,txt_output,table = main_local.prediction(match.homeTeam,match.awayTeam,table)

    print(f"{'Probabilities':-^20}")
    print(f"Draw: {probs[0]}")
    print(f"Home Team ({match.homeTeam}): {probs[1]}")
    print(f"Away Team ({match.awayTeam}): {probs[2]}")


    table['Winner'] = table['Winner'].map(int)

    tblWinValue = table['Winner'][0]

    if tblWinValue == 0:
        retVal = f"{match.homeTeam} draws {match.awayTeam}"
    elif tblWinValue == 1:
        retVal = f"{match.homeTeam} wins over {match.awayTeam}"
    else:
        retVal = f"{match.homeTeam} loses against {match.awayTeam}"


    print(txt_output)
    return {'result': retVal}


# Route to get all the match results from the model
@app.get('/model')
def runModel():

    # output_df, rewrite_df = main_local.prediction_fixtures()

    matches = model_output

    matches['Winner'] = matches['Winner'].map(int)

    return matches.to_dict(orient='index')


# Running on startup - Initiating the model, and generating the initial predictions
@app.on_event('startup')
def startup_event():
    print(f'{"Running startup":-^25}')
    global model_df
    global model_output

    for i in range(1,4):
        print(f'{"Model DF":*^20}')
        print(model_df)
        print(f'{"Model Output":.^20}')
        print(model_output)
        model_df, rewrite_df = main_local.prediction_fixtures(i)
        model_output = model_output.append(model_df,ignore_index=True)

    print(f'{"Finishing startup":-^25}')


# Customising the API doc
def custom_openapi():
    if app.openapi_schema:
        return app.openapi_schema

    openapi_schema = get_openapi(
        title="Road to Qatar 2022",
        version="1.0.0",
        description="OpenAPI schema to the Road to Qatar Data Science Project",
        routes=app.routes,
    )

    openapi_schema['info']['x-logo'] = {
        "url": "https://img.freepik.com/premium-vector/fifa-world-cup-qatar-2022-logo-stylized-vector-isolated-illustration-with-football_633888-121.jpg?w=2000"
    }

    app.openapi_schema  = openapi_schema
    return app.openapi_schema

app.openapi = custom_openapi
