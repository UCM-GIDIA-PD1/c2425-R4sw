import pandas as pd
import math
import os 
from PasarAP2Difdf import crearDfDif

 # Calcula una fila de estadísticas para un enfrentamiento entre dos peleadores
 # usando sus últimas 3 peleas para calcular estadísticas ponderadas y diferencias.
def calcular_fila_pelea(peleador_a, peleador_b):
    """
    Realizado por Mateo Turati.
    Calcula las estadísticas ponderadas de las tres últimas peleas previas para dos peleadores
    dados y devuelve una sola fila correspondiente al combate usando las diferencias entre ellos.
    Si no hay más de tres peleas devuelve None. (Tener en cuenta para mostrar algo en la web igual)
    """
    # Cargar dataset de peleas y normalizar nombres de peleadores
    ruta_df =  os.path.join("data","peleas.parquet")
    df = pd.read_parquet(ruta_df)
    df['DATE'] = pd.to_datetime(df['DATE'])

    peleador_a = peleador_a.lower()
    peleador_b = peleador_b.lower()
    df['Peleador_A'] = df['Peleador_A'].str.lower()
    df['Peleador_B'] = df['Peleador_B'].str.lower()
    fecha = pd.Timestamp.today()

    # Filtrar y ordenar las últimas tres peleas previas de cada peleador
    peleas_a = df[
        (df['DATE'] < fecha) &
        (
            (df['Peleador_A'] == peleador_a) |
            (df['Peleador_B'] == peleador_a)
        )
    ].sort_values(by='DATE').tail(3)

    peleas_b = df[
        (df['DATE'] < fecha) &
        (
            (df['Peleador_A'] == peleador_b) |
            (df['Peleador_B'] == peleador_b)
        )
    ].sort_values(by='DATE').tail(3)
    
    # Si alguno de los peleadores tiene menos de 3 peleas previas, no se puede calcular
    if len(peleas_a) < 3 or len(peleas_b) < 3:
        return None

    # Columnas específicas de cada peleador y sus versiones genéricas para mapear estadísticas
    columnas_a = [
        'KD_A', 'SIG_STR_A', 'TD_PORC_A', 'SUB_ATT_A', 'REV_A', 'CTRL_A',
        'TOTAL_STR_A_x', 'TOTAL_STR_A_y', 'TD_A_x', 'TD_A_y', 'STR_HEAD_A_x',
        'STR_HEAD_A_y', 'STR_BODY_A_x', 'STR_BODY_A_y', 'STR_LEG_A_x',
        'STR_LEG_A_y', 'STR_DISTANCE_A_x', 'STR_DISTANCE_A_y',
        'STR_CLINCH_A_x', 'STR_CLINCH_A_y', 'STR_GROUND_A_x', 'STR_GROUND_A_y',
        'STRIKER_A', 'GRAPPLER_A','Victorias_KO_A', 'Victorias_Sub_A', 'Victorias_Decision_A',
                                    'Derrotas_KO_A', 'Derrotas_Sub_A', 'Derrotas_Decision_A'
    ]
    
    columnas_b = [
        'KD_B', 'SIG_STR_B', 'TD_PORC_B', 'SUB_ATT_B', 'REV_B', 'CTRL_B',
        'TOTAL_STR_B_x', 'TOTAL_STR_B_y', 'TD_B_x', 'TD_B_y', 'STR_HEAD_B_x',
        'STR_HEAD_B_y', 'STR_BODY_B_x', 'STR_BODY_B_y', 'STR_LEG_B_x',
        'STR_LEG_B_y', 'STR_DISTANCE_B_x', 'STR_DISTANCE_B_y',
        'STR_CLINCH_B_x', 'STR_CLINCH_B_y', 'STR_GROUND_B_x', 'STR_GROUND_B_y',
        'STRIKER_B', 'GRAPPLER_B','Victorias_KO_B', 'Victorias_Sub_B', 'Victorias_Decision_B',
                                    'Derrotas_KO_B', 'Derrotas_Sub_B', 'Derrotas_Decision_B'
    ]
    
    columnas_gen = [
        'KD', 'SIG_STR', 'TD_PORC', 'SUB_ATT', 'REV', 'CTRL',
        'TOTAL_STR_x', 'TOTAL_STR_y', 'TD_x', 'TD_y', 'STR_HEAD_x',
        'STR_HEAD_y', 'STR_BODY_x', 'STR_BODY_y', 'STR_LEG_x',
        'STR_LEG_y', 'STR_DISTANCE_x', 'STR_DISTANCE_y',
        'STR_CLINCH_x', 'STR_CLINCH_y', 'STR_GROUND_x', 'STR_GROUND_y',
        'STRIKER', 'GRAPPLER','Victorias_KO', 'Victorias_Sub', 'Victorias_Decision',
                                    'Derrotas_KO', 'Derrotas_Sub', 'Derrotas_Decision'
    ]


    # Calcula una media ponderada exponencial de las estadísticas pasadas
    def media_ponderada(peleas, peleador, columnas_a, columnas_b, columnas_gen):
        dic = {}
        peleas = peleas.sort_values(by='DATE', ascending=False)
        for col_a, col_b, col_gen in zip(columnas_a, columnas_b, columnas_gen):
            values = []
            for _, p in peleas.iterrows():
                values.append(p[col_a] if peleador == p['Peleador_A'] else p[col_b])
            values_series = pd.Series(values)
            ewm_mean = values_series.ewm(span=4, adjust=False).mean().iloc[-1]
            dic[col_gen] = ewm_mean
        return dic

    media_a = media_ponderada(peleas_a, peleador_a, columnas_a, columnas_b, columnas_gen)
    media_b = media_ponderada(peleas_b, peleador_b, columnas_a, columnas_b, columnas_gen)

    pelea_ajustada = {
        'DATE': fecha,
        'Peleador_A': peleador_a,
        'Peleador_B': peleador_b,
    }

    for i in range(len(columnas_a)):
        pelea_ajustada[columnas_a[i]] = media_a[columnas_gen[i]]
        pelea_ajustada[columnas_b[i]] = media_b[columnas_gen[i]]

    # Actualiza el récord del peleador según el resultado de su última pelea
    def actualizar_record(peleador, ult_pelea):
        """"Actualiza el record teniendo en cuenta el resultado de su última pelea"""
        if peleador == ult_pelea["Peleador_A"] and ult_pelea["WINNER"] == 0:
            return ult_pelea["Record_A"] + 1
        elif peleador == ult_pelea["Peleador_B"] and ult_pelea["WINNER"] == 1:
            return ult_pelea["Record_B"] + 1
        elif peleador == ult_pelea["Peleador_B"]:
            return ult_pelea["Record_B"] - 1
        else:
            return ult_pelea["Record_A"] - 1

    pelea_ajustada['Record_A'] = actualizar_record(peleador_a, peleas_a.iloc[-1])
    pelea_ajustada['Record_B'] = actualizar_record(peleador_b, peleas_b.iloc[-1])

    # Actualiza la racha ganadora del peleador
    def actualizar_racha(peleador, ult_pelea):
        """"Actualiza la racha teniendo en cuenta el resultado de su última pelea"""
        if peleador == ult_pelea["Peleador_A"] and ult_pelea["WINNER"] == 0:
            return ult_pelea["Racha_A"] + 1
        elif peleador == ult_pelea["Peleador_B"] and ult_pelea["WINNER"] == 1:
            return ult_pelea["Racha_B"] + 1
        else:
            return 0

    pelea_ajustada['Racha_A'] = actualizar_racha(peleador_a, peleas_a.iloc[-1])
    pelea_ajustada['Racha_B'] = actualizar_racha(peleador_b, peleas_b.iloc[-1])

    # Calcula los puntos del peleador en base al sistema ELO modificado
    def actualizar_puntos(peleador, ult_pelea, k=20):
        """Actualiza los puntos del peleador teniendo en cuenta la diferencia de nivel y normalización."""
        A, B = ult_pelea["Peleador_A"], ult_pelea["Peleador_B"]
        Ra, Rb = ult_pelea["Puntos_A"], ult_pelea["Puntos_B"]

        ganador = (peleador == A and ult_pelea["WINNER"] == 0) or (peleador == B and ult_pelea["WINNER"] == 1)
        R_peleador = Ra if peleador == A else Rb
        R_oponente = Rb if peleador == A else Ra

        epsilon = 1e-6
        total_puntos = R_peleador + R_oponente + epsilon
        ajuste = 1 / (1 + math.exp(-abs(R_peleador - R_oponente) / 50))

        if ganador:
            return max(R_peleador + k * ajuste * (1 - (R_oponente / total_puntos)), 0)
        else:
            return max(R_peleador - k * ajuste * (R_peleador / total_puntos), 0)

    pelea_ajustada["Puntos_A"] = actualizar_puntos(peleador_a, peleas_a.iloc[-1])
    pelea_ajustada["Puntos_B"] = actualizar_puntos(peleador_b, peleas_b.iloc[-1])

    # Actualiza el número total de peleas del peleador
    def act_peleas(peleador, ult_pelea):
        return ult_pelea["Peleas_A"] + 1 if peleador == ult_pelea["Peleador_A"] else ult_pelea["Peleas_B"] + 1

    pelea_ajustada["Peleas_A"] = act_peleas(peleador_a, peleas_a.iloc[-1])
    pelea_ajustada["Peleas_B"] = act_peleas(peleador_b, peleas_b.iloc[-1])

    # Cálculo de diferencias estadísticas entre los dos peleadores
    pelea_ajustada['KD_DIFF'] = pelea_ajustada['KD_A'] - pelea_ajustada['KD_B']
    pelea_ajustada['SIG_STR_DIFF'] = pelea_ajustada['SIG_STR_A'] - pelea_ajustada['SIG_STR_B']
    pelea_ajustada['TD_DIFF'] = (pelea_ajustada['TD_A_x'] / (pelea_ajustada['TD_A_y'] + 1)) - (pelea_ajustada['TD_B_x'] / (pelea_ajustada['TD_B_y'] + 1))
    pelea_ajustada['SUB_ATT_DIFF'] = pelea_ajustada['SUB_ATT_A'] - pelea_ajustada['SUB_ATT_B']
    pelea_ajustada['REV_DIFF'] = pelea_ajustada['REV_A'] - pelea_ajustada['REV_B']
    pelea_ajustada['CTRL_DIFF'] = pelea_ajustada['CTRL_A'] - pelea_ajustada['CTRL_B']

    # Crear DataFrame con la fila de estadísticas ajustadas
    df_pond = pd.DataFrame([pelea_ajustada])

    # Calcular las diferencias finales con la función externa
    df_dif = crearDfDif(df_pond)
    
    return df_dif
