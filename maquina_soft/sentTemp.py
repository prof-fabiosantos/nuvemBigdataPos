import asyncio  # Importa o módulo asyncio para suporte a programação assíncrona.
from asyncua import Client  # Importa a classe Client do módulo asyncua para se conectar a um servidor OPC UA.
import requests  # Importa o módulo requests para fazer solicitações HTTP.

url = "opc.tcp://localhost:4840/freeopcua/server/"  # Define a URL do servidor OPC UA.
namespace = "http://examples.freeopcua.github.io"  # Define o namespace utilizado pelo servidor OPC UA.

BASE_URL = "https://api-flask-three.vercel.app" # Define a URL base da API.

def sent_temperature(temperature):
    url = f"{BASE_URL}/temperatures"  # Monta a URL completa para a rota de adição de temperaturas.
    data = {"temperature": temperature}  # Cria um dicionário com os dados da temperatura.
    response = requests.post(url, json=data)  # Faz uma solicitação POST com os dados JSON.

    if response.status_code == 200:  # Verifica se a solicitação foi bem-sucedida (status code 200).
        print("Temperatura adicionada com sucesso!")
    else:
        print(f"Erro ao adicionar temperatura. Código de status: {response.status_code}")

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
        sent_temperature(new_temperature)

if __name__ == "__main__":
    asyncio.run(main())  # Executa a função main de forma assíncrona usando o asyncio.