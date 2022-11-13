# Importing required Modules for creating API
from fastapi import FastAPI
from pydantic import BaseModel
from typing import List

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
