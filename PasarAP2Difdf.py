def crearDfDif(df_peleas):
    """
    Crea un DataFrame con las diferencias entre las estadísticas de los peleadores A y B.
    Se eliminan las columnas originales y se devuelven las diferencias.
    """

    df = df_peleas.copy()

    # Lista de columnas que tienen contraparte en A y B
    columnas_a = ['KD_A', 'SIG_STR_A', 'TD_PORC_A', 'SUB_ATT_A', 'REV_A', 'CTRL_A', 
                'TOTAL_STR_A_x', 'TOTAL_STR_A_y', 'TD_A_x', 'TD_A_y', 
                'STR_HEAD_A_x', 'STR_HEAD_A_y', 'STR_BODY_A_x', 'STR_BODY_A_y', 
                'STR_LEG_A_x', 'STR_LEG_A_y', 'STR_DISTANCE_A_x', 'STR_DISTANCE_A_y', 
                'STR_CLINCH_A_x', 'STR_CLINCH_A_y', 'STR_GROUND_A_x', 'STR_GROUND_A_y', 
                'STRIKER_A', 'GRAPPLER_A', 'Record_A', 'Peleas_A', 'Puntos_A', 
                'Racha_A', 'Victorias_KO_A', 'Victorias_Sub_A', 'Victorias_Decision_A', 
                'Derrotas_KO_A', 'Derrotas_Sub_A', 'Derrotas_Decision_A']

    columnas_b = ['KD_B', 'SIG_STR_B', 'TD_PORC_B', 'SUB_ATT_B', 'REV_B', 'CTRL_B', 
                'TOTAL_STR_B_x', 'TOTAL_STR_B_y', 'TD_B_x', 'TD_B_y', 
                'STR_HEAD_B_x', 'STR_HEAD_B_y', 'STR_BODY_B_x', 'STR_BODY_B_y', 
                'STR_LEG_B_x', 'STR_LEG_B_y', 'STR_DISTANCE_B_x', 'STR_DISTANCE_B_y', 
                'STR_CLINCH_B_x', 'STR_CLINCH_B_y', 'STR_GROUND_B_x', 'STR_GROUND_B_y', 
                'STRIKER_B', 'GRAPPLER_B', 'Record_B', 'Peleas_B', 'Puntos_B', 
                'Racha_B', 'Victorias_KO_B', 'Victorias_Sub_B', 'Victorias_Decision_B', 
                'Derrotas_KO_B', 'Derrotas_Sub_B', 'Derrotas_Decision_B']

    # Calcular las diferencias
    for col_a, col_b in zip(columnas_a, columnas_b):
        if col_a in df.columns and col_b in df.columns:
            df[f'{col_a[:-2]}_DIFF'] = df[col_a] - df[col_b]

    # Eliminar las columnas originales
    df.drop(columns=columnas_a + columnas_b, inplace=True)

    # Mostrar el DataFrame resultante
    df.head()
    
    return df
