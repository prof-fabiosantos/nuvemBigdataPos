# client.py
import asyncio
from asyncua import Client
import requests
import matplotlib.pyplot as plt

url = "opc.tcp://localhost:4840/freeopcua/server/"
namespace = "http://examples.freeopcua.github.io"

BASE_URL = "http://localhost:5000"  

def get_temperatures():
    url = f"{BASE_URL}/temperatures"
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        print("Temperaturas registradas:")
        print(data)

        # Extrair dados para plotagem
        dates = [entry[next(iter(entry))]['date'] for entry in data]
        temperatures = [entry[next(iter(entry))]['temperature'] for entry in data]
        timestamps = [entry[next(iter(entry))]['timestamp'] for entry in data]

        # Converter a temperatura para float se for uma string
        for i, temp in enumerate(temperatures):
            if isinstance(temp, str):
                temperatures[i] = float(temp.rstrip('º'))

        # Criar o gráfico
        plt.figure(figsize=(10, 6))
        plt.plot(dates, temperatures, marker='o', linestyle='-', color='b', label='Temperatura')
        plt.xlabel('Data')
        plt.ylabel('Temperatura (°C)')
        plt.title('Temperaturas Registradas')
        plt.xticks(rotation=45)
        plt.legend()
        plt.tight_layout()

        # Exibir o gráfico
        plt.show()
        
    else:
        print(f"Erro ao obter as temperaturas. Código de status: {response.status_code}")

def add_temperature(temperature):
    url = f"{BASE_URL}/temperatures"
    data = {"temperature": temperature}
    response = requests.post(url, json=data)
    if response.status_code == 200:
        print("Temperatura adicionada com sucesso!")
    else:
        print(f"Erro ao adicionar temperatura. Código de status: {response.status_code}")

async def main():

    print(f"Connecting to {url} ...")
    async with Client(url=url) as client:
        # Find the namespace index
        nsidx = await client.get_namespace_index(namespace)
        print(f"Namespace Index for '{namespace}': {nsidx}")

        # Get the variable node for read / write
        var = await client.nodes.root.get_child(
            ["0:Objects", f"{nsidx}:MyObject", f"{nsidx}:MyVariable"]
        )
        new_temperature = await var.read_value()
        print(f"Valor da variavel de temperatura: {new_temperature}")

        # Adicionando uma nova temperatura (altere o valor da temperatura conforme necessário)
        # add_temperature(new_temperature)
        # Obtendo todas as temperaturas registradas
        get_temperatures()

        

if __name__ == "__main__":    
    asyncio.run(main())
    

    
