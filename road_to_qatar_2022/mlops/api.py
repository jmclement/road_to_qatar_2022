# Importing required Modules for creating API
from fastapi import FastAPI
from fastapi.openapi.utils import get_openapi
from pydantic import BaseModel
from typing import List
from road_to_qatar_2022.interface import main_local

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

# Instantiate the FastAPI
app = FastAPI()

# Define default route
@app.get('/')
def index():
    return {'ok':True}

# Define route to get winner
@app.get('/winner')
def getWinner():
    return {'Res':'Winner called'}

# Define route for choosing the selected team
@app.post('/selected_team')
def setPreferedTeam(param:SelectedTeam):
    return {'Post':f'{param.name}'}

# Route to 'save' the results of predictions
@app.post('/update_predictions')
def updatePredictions():
    return {'Called update predictions'}

# Route to generate the predictions for a match or list of matches
@app.post('/predict')
def predictResults(param:MatchesList):
    output = "{"
    for i in param.matches:
        output += f"{i.homeTeam} v/s {i.awayTeam},"
    output += "}"
    return {output}

@app.post('/model')
def runModel():
    return {main_local.prediction_fixtures()}


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
