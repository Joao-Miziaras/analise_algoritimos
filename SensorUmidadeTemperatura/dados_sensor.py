import mysql.connector
import random
import time
import matplotlib as plt
from datetime import datetime

def get_temp():
    return round(random.uniform(25.0, 30.0), 2)

def get_umi():
    interval1 = (77, 80)  
    interval2 = (80, 88)  
    interval3 = (88, 100)  
    
    prob_interval1 = 0.3  
    prob_interval2 = 0.4  
    prob_interval3 = 0.1  

    interval_escolhido = random.choices([interval1, interval2, interval3], weights=[prob_interval1, prob_interval2, prob_interval3])[0]

    return round(random.uniform(*interval_escolhido), 2)

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

contador_alerta = 0
id_dado = 0
try:
    while id_dado < 10:
        id_dado += 1
        temperatura = get_temp()
        umidade = get_umi()
        horario = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        print("-" * 30)
        print("Id do sensor: 1")
        print("ID do dado:", id_dado)
        print(f"Percentual de umidade: {umidade}%")
        print("Temperatura:", temperatura)
        print("Horário da coleta:", horario)
        insert_data(temperatura, umidade, horario)
        if umidade > 88.0:
            print("ALERTA: Condições climáticas desfavoráveis")
            contador_alerta += 1
        time.sleep(5)
except KeyboardInterrupt:
    print("Contador de alert de umidade alta:", contador_alerta)