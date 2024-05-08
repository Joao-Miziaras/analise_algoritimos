import mysql.connector
import random
import time
from datetime import datetime

def get_temp():
    return round(random.uniform(25.0, 30.0), 2)

import random

def get_umi(prev_value=None):
    interval1 = (77, 80)  
    interval2 = (80, 88)  
    interval3 = (88, 100)  
    
    # Ajuste das probabilidades para tornar os valores mais consistentes
    prob_interval1 = 0.1  
    prob_interval2 = 0.6  
    prob_interval3 = 0.1  

    if prev_value is None:
        interval_escolhido = random.choices([interval1, interval2, interval3], weights=[prob_interval1, prob_interval2, prob_interval3])[0]
        return round(random.uniform(*interval_escolhido), 2)
    else:
        if prev_value < 80:
            offset = random.uniform(-1, 1)
        elif prev_value < 88:
            offset = random.uniform(-1, 1)
        else:
            offset = random.uniform(-1, 1)
        
        new_value = prev_value + offset
        return round(max(min(new_value, 100), 77), 2)


def conectar_bd():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="urubu100",
        database="grupo6"
    )

def insert_data(temperatura, umidade, horario):
    conexao = conectar_bd()
    cursor = conexao.cursor()
    sql = "INSERT INTO dados_sensor (id_sensor, porcent_umidade, temperatura, horario_da_coleta) VALUES (%s, %s, %s, %s)"
    valores = (1, umidade, temperatura, horario)
    cursor.execute(sql, valores)
    conexao.commit()
    conexao.close()

def get_data():
    umidade= None
    temperatura = get_temp()
    umidade = get_umi(umidade)
    horario = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    return {
        'umidade': umidade,
        'temperatura': temperatura,
        'horario': horario
    }

