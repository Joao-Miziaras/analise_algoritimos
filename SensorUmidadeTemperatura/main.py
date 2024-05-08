import aws_integrations as awsI
import app as app
import time
from datetime import datetime
import json
import dados_sensor as ds

def get_time():
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")

def get_data():
    data = {
        'umidade': ds.get_data()['umidade'],
        'temperatura': ds.get_data()['temperatura'],
    }

    json_data ={
            "metric": "umidadeTemperatura",
            "date": get_time(),
            "data": data
    }
    return json.dumps(json_data)
    


while True:
    nome_json = f"umi_temp_{get_time()}.json"
    awsI.send_json_to_s3(get_data(), nome_json)   
    time.sleep(10)
    
