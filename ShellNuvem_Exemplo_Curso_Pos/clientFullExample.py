import firebase_admin  # Importa o módulo firebase_admin para interagir com o Firebase.
from firebase_admin import credentials, db  # Importa classes do módulo para autenticação e banco de dados em tempo real.
from firebase_admin import firestore  # Importa a classe para interagir com o Firestore.
import asyncio  # Importa o módulo asyncio para suporte a programação assíncrona.
from asyncua import Client  # Importa a classe Client do módulo asyncua para se conectar a um servidor OPC UA.
import requests  # Importa o módulo requests para fazer solicitações HTTP.
import datetime  # Importa o módulo datetime para trabalhar com datas e horários.
import matplotlib.pyplot as plt  # Importa o módulo matplotlib para criação de gráficos.

# Usa um arquivo de credenciais para autenticação no Firebase.
cred = credentials.Certificate('nuvem-96e92-firebase-adminsdk-36ihj-8a8e7c4a05.json')
app = firebase_admin.initialize_app(cred)  # Inicializa o aplicativo Firebase com as credenciais.
db = firestore.client()  # Cria uma instância do cliente Firestore para interagir com o Firestore.

def get_temperatures():
    users_ref = db.collection("temperatures")  # Obtém a referência à coleção "temperatures" no Firestore.
    docs = users_ref.stream()  # Obtém um iterável com todos os documentos na coleção.

    temperatures_list = []  # Inicializa uma lista vazia para armazenar os dados das temperaturas.

    # Itera sobre todos os documentos na coleção "temperatures".
    for doc in docs:
        temperature_data = doc.to_dict()  # Converte o documento para um dicionário Python.
        temperatures_list.append({doc.id: temperature_data})  # Adiciona o dicionário à lista.

    return temperatures_list  # Retorna a lista de temperaturas como JSON.


def add_temperature(_temperature):
    temperature = _temperature  # Obtém a temperatura do JSON.
    timestamp = datetime.datetime.now().timestamp()  # Obtém o timestamp atual.
    date = datetime.datetime.now().strftime('%Y-%m-%d')  # Obtém a data atual no formato desejado.

    # Cria um dicionário Python com os dados da nova temperatura.
    temperature_data = {
        "temperature": temperature,
        "timestamp": timestamp,
        "date": date
    }

    doc_ref = db.collection("temperatures").add(temperature_data)  # Adiciona os dados como um novo documento na coleção.

    print("Temperatura adicionada com sucesso!")  # Retorna uma mensagem de sucesso como JSON.

def show_temperatures():
    response = get_temperatures()  # Faz uma solicitação GET para obter os dados das temperaturas.

    if response != '':  # Verifica se a solicitação foi bem-sucedida 
        
        print("Temperaturas registradas:")
        data = response
       
        # Extrai dados para plotagem do gráfico.
        entries = [entry[next(iter(entry))] for entry in data]
        entries.sort(key=lambda x: x['date'])  # Ordena as entradas com base nas datas.

        dates = [entry['date'] for entry in entries]  # Obtém as datas das temperaturas.
        temperatures = [entry['temperature'] for entry in entries]  # Obtém as temperaturas.

        # Converte as temperaturas para float se forem strings.
        for i, temp in enumerate(temperatures):
            if isinstance(temp, str):
                temperatures[i] = float(temp.rstrip('º'))

        # Criação e configuração do gráfico.
        plt.figure(figsize=(10, 6))
        plt.plot(dates, temperatures, marker='o', linestyle='-', color='b', label='Temperatura')
        plt.xlabel('Data')
        plt.ylabel('Temperatura (°C)')
        plt.title('Temperaturas Registradas')
        plt.xticks(rotation=45)
        plt.legend()
        plt.tight_layout()

        # Exibe o gráfico.
        plt.show()

    else:
        print(f"Erro ao obter as temperaturas. Código de status: {response.status_code}")


url = "opc.tcp://localhost:4840/freeopcua/server/"  # Define a URL do servidor OPC UA.
namespace = "http://examples.freeopcua.github.io"  # Define o namespace utilizado pelo servidor OPC UA.

async def main():
    print(f"Connecting to {url} ...")
    
    # Cria uma conexão assíncrona com o servidor OPC UA.
    async with Client(url=url) as client:
        # Encontra o índice do namespace.
        nsidx = await client.get_namespace_index(namespace)
        print(f"Namespace Index for '{namespace}': {nsidx}")

        # Obtém o nó da variável para leitura / gravação.
        var = await client.nodes.root.get_child(
            ["0:Objects", f"{nsidx}:MyObject", f"{nsidx}:MyVariable"]
        )
        new_temperature = await var.read_value()  # Lê o valor da variável do servidor OPC UA.
        print(f"Valor da variavel de temperatura: {new_temperature}")

        # Envia uma nova temperatura (altere o valor da temperatura conforme necessário).
        add_temperature(new_temperature)

        show_temperatures()

if __name__ == "__main__":
    asyncio.run(main())  # Executa a função main de forma assíncrona usando o asyncio.


