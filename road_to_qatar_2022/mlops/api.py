from fastapi import FastAPI
from pydantic import BaseModel

class SelectedTeam(BaseModel):
    name: str

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
