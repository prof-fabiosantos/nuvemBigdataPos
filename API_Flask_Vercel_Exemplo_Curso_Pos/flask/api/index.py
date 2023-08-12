import firebase_admin
from firebase_admin import credentials, firestore
from flask import Flask, request, jsonify
import datetime

app = Flask(__name__)

# Use um arquivo de credenciais para autenticação no Firebase.
cred = credentials.Certificate('./api/nuvem-96e92-firebase-adminsdk-36ihj-8a8e7c4a05.json')
firebase_admin.initialize_app(cred)
db = firestore.client()

@app.route('/')
def home():
    return 'Hello, World!'

# Rota para obter todas as temperaturas.
@app.route('/temperatures', methods=['GET'])
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
@app.route('/temperatures', methods=['POST'])
def add_temperature():
    data = request.get_json()
    temperature = data.get('temperature')  # Use get para evitar KeyError

    if temperature is None:
        return jsonify({"error": "Temperature value missing"}), 400

    timestamp = datetime.datetime.now().timestamp()
    date = datetime.datetime.now().strftime('%Y-%m-%d')

    temperature_data = {
        "temperature": temperature,
        "timestamp": timestamp,
        "date": date
    }

    temperatures_ref = db.collection("temperatures")
    new_temperature_ref = temperatures_ref.add(temperature_data)

    return jsonify({"message": "Temperature added successfully!", "document_id": new_temperature_ref.id})

if __name__ == "__main__":
    app.run(debug=True)
