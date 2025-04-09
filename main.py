from CalculaFilaP2Dif import calcular_fila_pelea
from fastapi import FastAPI, Request, Form
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
from pydantic import BaseModel
from joblib import load
from typing import Annotated
from contextlib import asynccontextmanager
from xgboost import XGBClassifier
import xgboost as xgb

@asynccontextmanager
async def lifespan(app: FastAPI):
    """Se ejecuta al inicio y al final del ciclo de vida de la aplicación."""
    # Código de inicialización (antes de que la aplicación comience a aceptar solicitudes)
    app.modelP1 = xgb.Booster()
    app.modelP2 = xgb.Booster()
    app.modelP1.load_model("models/modelP1.xgb")
    app.modelP2.load_model("models/modelP2.xgb")
    print("Modelos cargados")

    yield  # Aquí la aplicación estará en ejecución

    # Código de limpieza (después de que la aplicación deje de aceptar solicitudes)
    print("Aplicación finalizada")

# Configurar el manejador de ciclo de vida
app = FastAPI(lifespan=lifespan)

# Servir ficheros HTML en la carpeta static
app.mount('/static', StaticFiles(directory='static', html = True), name='static')

# Usar templates para devolver páginas HTML parametrizadas
templates = Jinja2Templates(directory="templates")

class PeleaP1(BaseModel):
    """Datos de una pelea"""
    TIME: int
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
    Peleador_A: str
    Peleador_B: str


class Prediccion(BaseModel):
    """Predicción sobre la pelea"""
    winner: str           # Nombre del peleador ganador
    probability: float    # Probabilidad de la victoria


def predecirP1(pelea: PeleaP1):
    """Dada una pelea ya dada indica el justo ganador"""
       # Combinar los datos de los dos peleadores en una sola entrada

    pred_y=app.modelP1.predict(pelea)[0]
    prob_y=app.modelP1.predict_proba(pelea)[0]
    return pred_y,prob_y

def predecirP2(fila_pelea):
    """Dada una futura pelea predice quien sera el ganador"""
    print(f'Fila de pelea: {fila_pelea}')
    dmatrix = xgb.DMatrix(fila_pelea)
    print(f'Dmatrix: {dmatrix}')
    print(f'Dmatrix data: {dmatrix.get_data()}')
    # Realizar la predicción
    pred_y = app.modelP2.predict(dmatrix)[0]
    prob_y = app.modelP2.predict(dmatrix, output_margin=False)[0]
    return pred_y,prob_y

@app.post('/POSTP2',response_class=HTMLResponse)
def testGET(request: Request, 
            Peleador_A: Annotated[str, Form()], Peleador_B: Annotated[str,Form()]):
    print(f'POSTP2 Pelador_A: {Peleador_A} Peleador_B: {Peleador_B}')
    return templates.TemplateResponse(request, name='predictP2.html', context={'Peleador_A': Peleador_A, 'Peleador_B': Peleador_B})

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
    probability = probs if y_pred == 0 else probs
    
    return Prediccion(winner=winner, probability=probability)

@app.post("/predictP2_html", response_class=HTMLResponse)
def predict(request: Request, 
            pelea: Annotated[PeleaP2, Form()]):
    '''Predicción HTML para determinar el ganador de la pelea'''
    print(f'POSTP2 Pelador_A:{pelea.Peleador_A} b: {pelea.Peleador_B}')
    print(f'Predicción de la pelea P2: {pelea}')

    # Calcular la fila de datos para la pelea
    df = calcular_fila_pelea(pelea.Peleador_A, pelea.Peleador_B)
    df.drop(columns=['Peleador_A', 'Peleador_B','DATE'], inplace=True)
    print(f'Fila de datos: {df}')
    print(f'Columnas: {df.columns}')    
    print(df.info())
    y_pred, probs = predecirP2(df)
    
    # Determinar el nombre del ganador
    winner = pelea.Peleador_A if y_pred == 0 else pelea.Peleador_B
    print(probs)
    probabilidad = probs if y_pred == 0 else probs
    print("Winner:", winner)
    
    # Pasar datos a la plantilla
    context = {
        'winner': winner,
        'probability': probabilidad,
    }
    
    return templates.TemplateResponse(request,'response.html', context=context)


print('Fin')