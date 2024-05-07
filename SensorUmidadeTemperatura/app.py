from datetime import datetime
import json
import dados_sensor as ds
from flask import Flask, jsonify
import os

def get_time():
    return datetime.now().strftime("%Y%m%d")

app = Flask(__name__)

@app.route('/data', methods=['GET'])
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
    download_dir = os.path.expanduser('~/Downloads')

    # Define o nome do arquivo com a data e hora atual para evitar sobreposição
    file_name = datetime.now().strftime('%Y-%m-%d_%H-%M-%S') + '.json'

    # Cria o caminho completo para o arquivo
    file_path = os.path.join(download_dir, file_name)

    with open(file_path, 'w') as f:
        json.dump(json_data, f)

    return jsonify(json_data)
    

if __name__ == '__main__':
    app.run(debug=True)