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

class PeleaP1(BaseModel):
    """Datos de una pelea"""
    Peleador_A: str
    Peleador_B: str
    DATE: str
    CATEGORY: str
    WINNER: bool
    METHOD: str
    TIME: int
    ROUND: int
    KD_A: int
    KD_B: int
    SIG_STR_A: float
    SIG_STR_B: float
    TD_PORC_A: float
    TD_PORC_B: float
    SUB_ATT_A: int
    SUB_ATT_B: int
    REV_A: int
    REV_B: int
    CTRL_A: int
    CTRL_B: int
    TOTAL_STR_A_x: int
    TOTAL_STR_A_y: int
    TOTAL_STR_B_x: int
    TOTAL_STR_B_y: int
    TD_A_x: int
    TD_A_y: int
    TD_B_x: int
    TD_B_y: int
    STR_HEAD_A_x: int
    STR_HEAD_A_y: int
    STR_HEAD_B_x: int
    STR_HEAD_B_y: int
    STR_BODY_A_x: int
    STR_BODY_A_y: int
    STR_BODY_B_x: int
    STR_BODY_B_y: int
    STR_LEG_A_x: int
    STR_LEG_A_y: int
    STR_LEG_B_x: int
    STR_LEG_B_y: int
    STR_DISTANCE_A_x: int
    STR_DISTANCE_A_y: int
    STR_DISTANCE_B_x: int
    STR_DISTANCE_B_y: int
    STR_CLINCH_A_x: int
    STR_CLINCH_A_y: int
    STR_CLINCH_B_x: int
    STR_CLINCH_B_y: int
    STR_GROUND_A_x: int
    STR_GROUND_A_y: int
    STR_GROUND_B_x: int
    STR_GROUND_B_y: int
    KD_DIFF: int
    SIG_STR_DIFF: int
    TD_DIFF: int
    SUB_ATT_DIFF: int
    REV_DIFF: int
    CTRL_DIFF: int
    STRIKER_A: int
    STRIKER_B: int
    GRAPPLER_A: int
    GRAPPLER_B: int
    TITLE_FIGHT: int
    WOMEN: int
    Record_A: int
    Record_B: int
    Peleas_A: int
    Peleas_B: int
    Puntos_A: int
    Puntos_B: int
    Racha_A: int
    Racha_B: int
    Victorias_KO_A: int
    Victorias_KO_B: int
    Victorias_Sub_A: int
    Victorias_Sub_B: int
    Victorias_Decision_A: int
    Victorias_Decision_B: int
    Derrotas_KO_A: int
    Derrotas_KO_B: int
    Derrotas_Sub_A: int
    Derrotas_Sub_B: int
    Derrotas_Decision_A: int
    Derrotas_Decision_B: int

class PeleaP2(BaseModel):
    """Datos de una pelea"""
    DATE: str
    Peleador_A: str
    Peleador_B: str
    WINNER: bool
    KD_A: float
    KD_B: float
    SIG_STR_A: float
    SIG_STR_B: float
    TD_PORC_A: float
    TD_PORC_B: float
    SUB_ATT_A: float
    SUB_ATT_B: float
    REV_A: float
    REV_B: float
    CTRL_A: float
    CTRL_B: float
    TOTAL_STR_A_x: float
    TOTAL_STR_B_x: float
    TOTAL_STR_A_y: float
    TOTAL_STR_B_y: float
    TD_A_x: float
    TD_B_x: float
    TD_A_y: float
    TD_B_y: float
    STR_HEAD_A_x: float
    STR_HEAD_B_x: float
    STR_HEAD_A_y: float
    STR_HEAD_B_y: float
    STR_BODY_A_x: float
    STR_BODY_B_x: float
    STR_BODY_A_y: float
    STR_BODY_B_y: float
    STR_LEG_A_x: float
    STR_LEG_B_x: float
    STR_LEG_A_y: float
    STR_LEG_B_y: float
    STR_DISTANCE_A_x: float
    STR_DISTANCE_B_x: float
    STR_DISTANCE_A_y: float
    STR_DISTANCE_B_y: float
    STR_CLINCH_A_x: float
    STR_CLINCH_B_x: float
    STR_CLINCH_A_y: float
    STR_CLINCH_B_y: float
    STR_GROUND_A_x: float
    STR_GROUND_B_x: float
    STR_GROUND_A_y: float
    STR_GROUND_B_y: float
    STRIKER_A: float
    STRIKER_B: float
    GRAPPLER_A: float
    GRAPPLER_B: float
    Victorias_KO_A: float
    Victorias_KO_B: float
    Victorias_Sub_A: float
    Victorias_Sub_B: float
    Victorias_Decision_A: float
    Victorias_Decision_B: float
    Derrotas_KO_A: float
    Derrotas_KO_B: float
    Derrotas_Sub_A: float
    Derrotas_Sub_B: float
    Derrotas_Decision_A: float
    Derrotas_Decision_B: float
    Record_A: float
    Record_B: float
    Racha_A: float
    Racha_B: float
    Puntos_A: float
    Puntos_B: float
    Peleas_A: float
    Peleas_B: float
    KD_DIFF: float
    SIG_STR_DIFF: float
    TD_DIFF: float
    SUB_ATT_DIFF: float
    REV_DIFF: float
    CTRL_DIFF: float

class PeleaP2_dif(BaseModel):
    """Datos de una pelea con diferencias estadísticas entre peleadores."""
    DATE: str
    Peleador_A: str
    Peleador_B: str
    WINNER: bool
    KD_DIFF: float
    SIG_STR_DIFF: float
    TD_DIFF: float
    SUB_ATT_DIFF: float
    REV_DIFF: float
    CTRL_DIFF: float
    TD_PORC_DIFF: float
    TOTAL_STR_A_DIFF: float
    TD_A_DIFF: float
    STR_HEAD_A_DIFF: float
    STR_BODY_A_DIFF: float
    STR_LEG_A_DIFF: float
    STR_DISTANCE_A_DIFF: float
    STR_CLINCH_A_DIFF: float
    STR_GROUND_A_DIFF: float
    STRIKER_DIFF: float
    GRAPPLER_DIFF: float
    Record_DIFF: float
    Peleas_DIFF: float
    Puntos_DIFF: float
    Racha_DIFF: float
    Victorias_KO_DIFF: float
    Victorias_Sub_DIFF: float
    Victorias_Decision_DIFF: float
    Derrotas_KO_DIFF: float
    Derrotas_Sub_DIFF: float
    Derrotas_Decision_DIFF: float

class Prediccion(BaseModel):
    """Predicción sobre la pelea"""
    winner: str           # Nombre del peleador ganador
    probability: float    # Probabilidad de la victoria

@app.on_event("startup")
def startup_event():
    """Se ejecuta al principio. Carga los modelos necesarios para nuestras predicciones"""
    app.modelP1=load(modelos/P1)
    app.modelP2=load(modelos/P2)
    app.modelP2_dif=load(modelos/P2_dif)

def predecirP1(pelea: PeleaP1):
    """Dada una pelea ya dada indica el justo ganador"""
       # Combinar los datos de los dos peleadores en una sola entrada

    pred_y=app.modelP1.predict(pelea)[0]
    prob_y=app.modelP1.predict_proba(pelea)[0]
    return pred_y,prob_y

def predecirP2(pelea: PeleaP2):
    """Dada una futura pelea predice quien sera el ganador"""
    pred_y=app.modelP2.predict(pelea)[0]
    prob_y=app.modelP2.predict_proba(pelea)[0]
    return pred_y,prob_y

def predecirP2_dif(pelea: PeleaP2_dif):
    """Dada una futura pelea predice quien sera el ganador"""
    pred_y=app.modelP2_dif.predict(pelea)[0]
    prob_y=app.modelP2_dif.predict_proba(pelea)[0]
    return pred_y,prob_y

@app.post("/predictP1_json", response_model=Prediccion)
def predict(pelea: PeleaP1):
    '''Predicción JSON para determinar el ganador de la pelea'''

    print(f'Predicción de la pelea P1:{pelea}')
    
    y_pred, probs = predecirP1(pelea)
    
    winner = pelea.Peleador_A if y_pred == 0 else pelea.Peleador_B
    probability = probs[0] if y_pred == 0 else probs[1]
    
    return Prediccion(winner=winner, probability=probability)

@app.post("/predictP1_html",response_class=HTMLResponse)
def predict(request: Request, 
            pelea: Annotated[PeleaP1, Form()]):
    '''Predicción JSON para determinar el ganador de la pelea'''

    print(f'Predección de la pelea P1: {pelea}')

    y_pred, probs = predecirP1(pelea)
       
    # Determinar el nombre del ganador
    winner = pelea.Peleador_A if y_pred == 0 else pelea.Peleador_B
    probabilidad = probs[0] if y_pred == 0 else probs[1]
    
    context = {
        'winner': winner,
        'probability': probabilidad,
    }
    return templates.TemplateResponse(request, name='response.html', context=context)

@app.post("/predictP2_json", response_model=Prediccion)
def predict(pelea: PeleaP2):
    '''Predicción JSON para determinar el ganador de la pelea'''

    print(f'Predicción de la pelea P2: {pelea}')
    
    y_pred, probs = predecirP2(pelea)
    
    winner = pelea.Peleador_A if y_pred == 0 else pelea.Peleador_B
    probability = probs[0] if y_pred == 0 else probs[1]
    
    return Prediccion(winner=winner, probability=probability)

@app.post("/predictP2_html",response_class=HTMLResponse)
def predict(request: Request, 
            pelea: Annotated[PeleaP2, Form()]):
    '''Predicción JSON para determinar el ganador de la pelea'''

    print(f'Predección de la pelea P2: {pelea}')

    y_pred, probs = predecirP2(pelea)
       
    # Determinar el nombre del ganador
    winner = pelea.Peleador_A if y_pred == 0 else pelea.Peleador_B
    probabilidad = probs[0] if y_pred == 0 else probs[1]
    
    context = {
        'winner': winner,
        'probability': probabilidad,
    }
    return templates.TemplateResponse(request, name='response.html', context=context)

@app.post("/predictP2_dif_json", response_model=Prediccion)
def predict(pelea: PeleaP2):
    '''Predicción JSON para determinar el ganador de la pelea'''

    print(f'Predicción de la pelea P2_dif: {pelea}')
    
    y_pred, probs = predecirP2_dif(pelea)
    
    winner = pelea.Peleador_A if y_pred == 0 else pelea.Peleador_B
    probability = probs[0] if y_pred == 0 else probs[1]
    
    return Prediccion(winner=winner, probability=probability)

@app.post("/predictP2_dif_html",response_class=HTMLResponse)
def predict(request: Request, 
            pelea: Annotated[PeleaP2, Form()]):
    '''Predicción JSON para determinar el ganador de la pelea'''

    print(f'Predección de la pelea P2_dif: {pelea}')

    y_pred, probs = predecirP2_dif(pelea)
       
    # Determinar el nombre del ganador
    winner = pelea.Peleador_A if y_pred == 0 else pelea.Peleador_B
    probabilidad = probs[0] if y_pred == 0 else probs[1]
    
    context = {
        'winner': winner,
        'probability': probabilidad,
    }
    return templates.TemplateResponse(request, name='response.html', context=context)

print('Fin')