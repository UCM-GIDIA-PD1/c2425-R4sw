from CalculaFilaP2Dif import calcular_fila_pelea
from fastapi import FastAPI, Request, Form
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse, RedirectResponse
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
    app.modelP1 = XGBClassifier()
    app.modelP2 = XGBClassifier()
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

    pelea_dict = pelea.dict()  # Extrae todos los valores como un diccionario

    pred_y=app.modelP1.predict([list(pelea_dict.values())])[0]
    prob_y=app.modelP1.predict_proba([list(pelea_dict.values())])[0]

    return pred_y,prob_y

def predecirP2(fila_pelea):
    """Dada una futura pelea predice quien sera el ganador"""
    print(f'Fila de pelea: {fila_pelea}')
    # Realizar la predicción
    pred_y = app.modelP2.predict(fila_pelea)[0]
    prob_y = app.modelP2.predict_proba(fila_pelea)[0]
    return pred_y,prob_y

@app.get("/", response_class=HTMLResponse)
async def index(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.get("/p1", response_class=HTMLResponse)
async def predict_p1(request: Request):
    return RedirectResponse(url='./static/PrediccionP1.html')

@app.get("/p2", response_class=HTMLResponse)
async def predict_p2(request: Request):
    return templates.TemplateResponse("predictP2.html", {"request": request})

@app.post('/PrediccionP1',response_class=HTMLResponse)
async def testGET(request: Request,       
    TIME: Annotated[int,Form()],
    KD_A: Annotated[int,Form()],
    KD_B: Annotated[int,Form()],
    SIG_STR_A: Annotated[float,Form()],
    SIG_STR_B: Annotated[float,Form()],
    TD_PORC_A: Annotated[float,Form()],
    TD_PORC_B: Annotated[float,Form()],
    SUB_ATT_A: Annotated[int,Form()],
    SUB_ATT_B: Annotated[int,Form()],
    REV_A: Annotated[int,Form()],
    REV_B: Annotated[int,Form()],
    CTRL_A: Annotated[int,Form()],
    CTRL_B: Annotated[int,Form()],
    TOTAL_STR_A_x: Annotated[int,Form()],
    TOTAL_STR_A_y: Annotated[int,Form()],
    TOTAL_STR_B_x: Annotated[int,Form()],
    TOTAL_STR_B_y: Annotated[int,Form()],
    TD_A_x: Annotated[int,Form()],
    TD_A_y: Annotated[int,Form()],
    TD_B_x: Annotated[int,Form()],
    TD_B_y: Annotated[int,Form()],
    STR_HEAD_A_x: Annotated[int,Form()],
    STR_HEAD_A_y: Annotated[int,Form()],
    STR_HEAD_B_x: Annotated[int,Form()],
    STR_HEAD_B_y: Annotated[int,Form()],
    STR_BODY_A_x: Annotated[int,Form()],
    STR_BODY_A_y: Annotated[int,Form()],
    STR_BODY_B_x: Annotated[int,Form()],
    STR_BODY_B_y: Annotated[int,Form()],
    STR_LEG_A_x: Annotated[int,Form()],
    STR_LEG_A_y: Annotated[int,Form()],
    STR_LEG_B_x: Annotated[int,Form()],
    STR_LEG_B_y: Annotated[int,Form()],
    STR_DISTANCE_A_x: Annotated[int,Form()],
    STR_DISTANCE_A_y: Annotated[int,Form()],
    STR_DISTANCE_B_x: Annotated[int,Form()],
    STR_DISTANCE_B_y: Annotated[int,Form()],
    STR_CLINCH_A_x: Annotated[int,Form()],
    STR_CLINCH_A_y: Annotated[int,Form()],
    STR_CLINCH_B_x: Annotated[int,Form()],
    STR_CLINCH_B_y: Annotated[int,Form()],
    STR_GROUND_A_x: Annotated[int,Form()],
    STR_GROUND_A_y: Annotated[int,Form()],
    STR_GROUND_B_x: Annotated[int,Form()],
    STR_GROUND_B_y: Annotated[int,Form()],
    KD_DIFF: Annotated[int,Form()],
    SIG_STR_DIFF: Annotated[int,Form()],
    TD_DIFF: Annotated[int,Form()],
    SUB_ATT_DIFF: Annotated[int,Form()],
    REV_DIFF: Annotated[int,Form()],
    CTRL_DIFF: Annotated[int,Form()],
    STRIKER_A: Annotated[int,Form()],
    STRIKER_B: Annotated[int,Form()],
    GRAPPLER_A: Annotated[int,Form()],
    GRAPPLER_B: Annotated[int,Form()],
    Record_A: Annotated[int,Form()],
    Record_B: Annotated[int,Form()],
    Peleas_A: Annotated[int,Form()],
    Peleas_B: Annotated[int,Form()],
    Puntos_A: Annotated[int,Form()],
    Puntos_B: Annotated[int,Form()],
    Racha_A: Annotated[int,Form()],
    Racha_B: Annotated[int,Form()],
    Victorias_KO_A: Annotated[int,Form()],
    Victorias_KO_B: Annotated[int,Form()],
    Victorias_Sub_A: Annotated[int,Form()],
    Victorias_Sub_B: Annotated[int,Form()],
    Victorias_Decision_A: Annotated[int,Form()],
    Victorias_Decision_B: Annotated[int,Form()],
    Derrotas_KO_A: Annotated[int,Form()],
    Derrotas_KO_B: Annotated[int,Form()],
    Derrotas_Sub_A: Annotated[int,Form()],
    Derrotas_Sub_B: Annotated[int,Form()],
    Derrotas_Decision_A: Annotated[int,Form()],
    Derrotas_Decision_B: Annotated[int,Form()]):
    """Lee datos y predice Post_Pelea"""

    pelea_obj = PeleaP1(
        TIME=TIME, KD_A=KD_A, KD_B=KD_B, SIG_STR_A=SIG_STR_A, SIG_STR_B=SIG_STR_B,
        TD_PORC_A=TD_PORC_A, TD_PORC_B=TD_PORC_B, SUB_ATT_A=SUB_ATT_A, SUB_ATT_B=SUB_ATT_B,
        REV_A=REV_A, REV_B=REV_B, CTRL_A=CTRL_A, CTRL_B=CTRL_B, 
        TOTAL_STR_A_x=TOTAL_STR_A_x, TOTAL_STR_A_y=TOTAL_STR_A_y, TOTAL_STR_B_x=TOTAL_STR_B_x, TOTAL_STR_B_y=TOTAL_STR_B_y,
        TD_A_x=TD_A_x, TD_A_y=TD_A_y, TD_B_x=TD_B_x, TD_B_y=TD_B_y,
        STR_HEAD_A_x=STR_HEAD_A_x, STR_HEAD_A_y=STR_HEAD_A_y, STR_HEAD_B_x=STR_HEAD_B_x, STR_HEAD_B_y=STR_HEAD_B_y,
        STR_BODY_A_x=STR_BODY_A_x, STR_BODY_A_y=STR_BODY_A_y, STR_BODY_B_x=STR_BODY_B_x, STR_BODY_B_y=STR_BODY_B_y,
        STR_LEG_A_x=STR_LEG_A_x, STR_LEG_A_y=STR_LEG_A_y, STR_LEG_B_x=STR_LEG_B_x, STR_LEG_B_y=STR_LEG_B_y,
        STR_DISTANCE_A_x=STR_DISTANCE_A_x, STR_DISTANCE_A_y=STR_DISTANCE_A_y, STR_DISTANCE_B_x=STR_DISTANCE_B_x, STR_DISTANCE_B_y=STR_DISTANCE_B_y,
        STR_CLINCH_A_x=STR_CLINCH_A_x, STR_CLINCH_A_y=STR_CLINCH_A_y, STR_CLINCH_B_x=STR_CLINCH_B_x, STR_CLINCH_B_y=STR_CLINCH_B_y,
        STR_GROUND_A_x=STR_GROUND_A_x, STR_GROUND_A_y=STR_GROUND_A_y, STR_GROUND_B_x=STR_GROUND_B_x, STR_GROUND_B_y=STR_GROUND_B_y,
        KD_DIFF=KD_DIFF, SIG_STR_DIFF=SIG_STR_DIFF, TD_DIFF=TD_DIFF, SUB_ATT_DIFF=SUB_ATT_DIFF, REV_DIFF=REV_DIFF, CTRL_DIFF=CTRL_DIFF,
        STRIKER_A=STRIKER_A, STRIKER_B=STRIKER_B, GRAPPLER_A=GRAPPLER_A, GRAPPLER_B=GRAPPLER_B,
        Record_A=Record_A, Record_B=Record_B, Peleas_A=Peleas_A, Peleas_B=Peleas_B,
        Puntos_A=Puntos_A, Puntos_B=Puntos_B, Racha_A=Racha_A, Racha_B=Racha_B,
        Victorias_KO_A=Victorias_KO_A, Victorias_KO_B=Victorias_KO_B, Victorias_Sub_A=Victorias_Sub_A, Victorias_Sub_B=Victorias_Sub_B,
        Victorias_Decision_A=Victorias_Decision_A, Victorias_Decision_B=Victorias_Decision_B,
        Derrotas_KO_A=Derrotas_KO_A, Derrotas_KO_B=Derrotas_KO_B, Derrotas_Sub_A=Derrotas_Sub_A, Derrotas_Sub_B=Derrotas_Sub_B,
        Derrotas_Decision_A=Derrotas_Decision_A, Derrotas_Decision_B=Derrotas_Decision_B
    )

    print(f'Predección de la pelea P1: {pelea_obj}')
    y_pred, probs = predecirP1(pelea_obj)
       
    # Informacion del ganador
    winner = "Peleador A" if y_pred == 0 else "Peleador B"
    probabilidad = probs[0] if y_pred == 0 else probs[1]
    
    context = {
        'winner': winner,
        'probability': probabilidad,
    }
    return templates.TemplateResponse(request, name='response.html', context=context)

@app.post('/POSTP2',response_class=HTMLResponse)
def testGET(request: Request, 
            Peleador_A: Annotated[str, Form()], Peleador_B: Annotated[str,Form()]):
    print(f'POSTP2 Pelador_A: {Peleador_A} Peleador_B: {Peleador_B}')
    return templates.TemplateResponse(request, name='predictP2.html', context={'Peleador_A': Peleador_A, 'Peleador_B': Peleador_B})


@app.post("/predictP2_json", response_model=Prediccion)
def predict(pelea: PeleaP2):
    '''Predicción JSON para determinar el ganador de la pelea'''

    print(f'Predicción de la pelea P2: {pelea}')
    
    y_pred, probs = predecirP2(pelea)
    
    winner = pelea.Peleador_A if y_pred == 0 else pelea.Peleador_B
    probability = probs[0] if y_pred == 0 else probs[1]
    
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
    probabilidad = probs[0] if y_pred == 0 else probs[1]
    print("Winner:", winner)
    
    # Pasar datos a la plantilla
    context = {
        'winner': winner,
        'probability': probabilidad,
    }
    
    return templates.TemplateResponse(request,'response.html', context=context)

print('Fin')