from fastapi import FastAPI
from pydantic import BaseModel
from typing import List
class SelectedTeam(BaseModel):
    name: str

class MatchTemplate(BaseModel):
    homeTeam: str
    awayTeam: str

class MatchesList(BaseModel):
    matches: List[MatchTemplate] = []

app = FastAPI()

@app.get('/')
def index():
    return {'ok':True}

@app.get('/winner')
def getWinner():
    return {'Res':'Winner called'}

@app.post('/selected_team')
def setPreferedTeam(param:SelectedTeam):
    return {'Post':f'{param.name}'}

@app.post('/update_predictions')
def updatePredictions():
    return {'Called update predictions'}

@app.post('/predict')
def predictResults(param:MatchesList):
    output = "{"
    for i in param.matches:
        output += f"{i.homeTeam} v/s {i.awayTeam},"
    output += "}"
    return {output}
