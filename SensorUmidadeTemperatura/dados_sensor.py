import mysql.connector
import random
import time
from datetime import datetime

def gerar_temperatura():
    return round(random.uniform(25.0, 30.0), 2)

def gerar_umidade():
    return round(random.uniform(77, 88))
    
def conectar_bd():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="urubu100",
        database="grupo6"
    )

def inserir_dados_temperatura(temperatura, umidade, horario):
    conexao = conectar_bd()
    cursor = conexao.cursor()
    sql = "INSERT INTO dados_sensor (id_sensor, porcent_umidade, temperatura, horario_da_coleta) VALUES (%s, %s, %s, %s)"
    valores = (1, umidade, temperatura, horario)
    cursor.execute(sql, valores)
    conexao.commit()
    conexao.close()

while True:
    temperatura = gerar_temperatura()
    umidade = gerar_umidade()
    horario = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    print("Id do sensor: 1")
    print(f"Percentual de umidade: {umidade}%")
    print("Temperatura:", temperatura)
    print("Horário da coleta:", horario)
    #inserir_dados_temperatura(temperatura, umidade, horario)
    time.sleep(5)
