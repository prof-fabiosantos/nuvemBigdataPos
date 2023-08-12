import firebase_admin  # Importa o módulo firebase_admin para interagir com o Firebase.
from firebase_admin import credentials, db  # Importa classes do módulo para autenticação e banco de dados em tempo real.
from firebase_admin import firestore  # Importa a classe para interagir com o Firestore.
from flask import Flask, request, jsonify  # Importa classes do Flask para criar a API e processar solicitações HTTP.
import datetime  # Importa o módulo datetime para trabalhar com datas e horários.

api = Flask(__name__)  # Cria uma instância da aplicação Flask.

# Usa um arquivo de credenciais para autenticação no Firebase.
cred = credentials.Certificate('nuvem-96e92-firebase-adminsdk-36ihj-8a8e7c4a05.json')
app = firebase_admin.initialize_app(cred)  # Inicializa o aplicativo Firebase com as credenciais.
db = firestore.client()  # Cria uma instância do cliente Firestore para interagir com o Firestore.

# Rota para obter todas as temperaturas.
@api.route('/temperatures', methods=['GET'])
def get_temperatures():
    users_ref = db.collection("temperatures")  # Obtém a referência à coleção "temperatures" no Firestore.
    docs = users_ref.stream()  # Obtém um iterável com todos os documentos na coleção.

    temperatures_list = []  # Inicializa uma lista vazia para armazenar os dados das temperaturas.

    # Itera sobre todos os documentos na coleção "temperatures".
    for doc in docs:
        temperature_data = doc.to_dict()  # Converte o documento para um dicionário Python.
        temperatures_list.append({doc.id: temperature_data})  # Adiciona o dicionário à lista.

    return jsonify(temperatures_list)  # Retorna a lista de temperaturas como JSON.

# Rota para adicionar uma nova temperatura.
@api.route('/temperatures', methods=['POST'])
def add_temperature():
    data = request.get_json()  # Obtém os dados JSON da solicitação.
    temperature = data['temperature']  # Obtém a temperatura do JSON.
    timestamp = datetime.datetime.now().timestamp()  # Obtém o timestamp atual.
    date = datetime.datetime.now().strftime('%Y-%m-%d')  # Obtém a data atual no formato desejado.

    # Cria um dicionário Python com os dados da nova temperatura.
    temperature_data = {
        "temperature": temperature,
        "timestamp": timestamp,
        "date": date
    }

    doc_ref = db.collection("temperatures").add(temperature_data)  # Adiciona os dados como um novo documento na coleção.

    return jsonify({"message": "Temperatura adicionada com sucesso!"})  # Retorna uma mensagem de sucesso como JSON.

if __name__ == '__main__':
    api.run()  # Inicia a execução da aplicação Flask.
