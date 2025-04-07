from fastapi import FastAPI, Request, Form
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
from pydantic import BaseModel
from joblib import load
from typing import Annotated

app=FastAPI()

# Servir ficheros HTML en la carpeta static
app.mount('/static', StaticFiles(directory='static', html = True), name='static')

# Usar templates para devolver páginas HTML parametrizadas
templates = Jinja2Templates(directory="templates")

class Pelea(BaseModel):
    """Datos de una pelea"""


class Prediccion(BaseModel):
    """Predicción sobre la pelea"""
    winner: str           # Nombre del peleador ganador
    probability: float    # Probabilidad de la victoria

@app.on_event("startup")
def startup_event():
    """Se ejecuta al principio. Carga los modelos necesarios para nuestras predicciones"""
    #app.modelP1=load(modelos/P1)
    #app.modelP2=load(modelos/P2)

def predecirP1(pelea: Pelea):
    """Dada una pelea ya dada indica el justo ganador"""
       # Combinar los datos de los dos peleadores en una sola entrada

    pred_y=app.modelP1.predict(pelea)[0]
    prob_y=app.modelP1.predict_proba(pelea)[0]
    return pred_y,prob_y

def predecirP2(pelea: Pelea):
    """Dada una futura pelea predice quien sera el ganador"""
    pred_y=app.modelP2.predict(pelea)[0]
    prob_y=app.modelP2.predict_proba(pelea)[0]
    return pred_y,prob_y

@app.post("/predictP1_json", response_model=Prediccion)
def predict(pelea: Pelea):
    '''Predicción JSON para determinar el ganador de la pelea'''

    print(f'Predicción de la pelea {pelea}')
    
    y_pred, probs = predecirP1(pelea)
    
    winner = pelea.peleadorA if y_pred == 0 else pelea.peleadorB
    probability = probs[0] if y_pred == 0 else probs[1]
    
    return Prediccion(winner=winner, probability=probability)

@app.post("/predictP1_html",response_class=HTMLResponse)
def predict(request: Request, 
            pelea: Annotated[Pelea, Form()]):
    '''Predicción JSON para determinar el ganador de la pelea'''

    print(f'Predección de la pelea: {pelea}')

    y_pred, probs = predecirP1(pelea)
       
          # Determinar el nombre del ganador
    winner = pelea.peleadorA if y_pred == 0 else pelea.peleadorB
    probabilidad = probs[0] if y_pred == 0 else probs[1]
    
    context = {
        'winner': winner,
        'probability': probabilidad,
    }
    return templates.TemplateResponse(request, name='response.html', context=context)

print('Fin')