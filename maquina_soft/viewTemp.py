import requests  # Importa o módulo requests para fazer solicitações HTTP.
import matplotlib.pyplot as plt  # Importa o módulo matplotlib para criação de gráficos.
import json

BASE_URL = "https://api-flask-three.vercel.app"

def get_temperatures():
    url = f"{BASE_URL}/temperatures"
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        # Ordena os dados pela data antes de processar
        data.sort(key=lambda entry: entry[next(iter(entry))]['date'])
        dates = [entry[next(iter(entry))]['date'] for entry in data]
        temperatures = [entry[next(iter(entry))]['temperature'] for entry in data]       

        for i, temp in enumerate(temperatures):
            if isinstance(temp, str):
                temperatures[i] = float(temp.rstrip('º'))
        plt.figure(figsize=(10, 6))
        plt.plot(dates, temperatures, marker='o', linestyle='-', color='b', label='Temperatura')
        plt.xlabel('Data')
        plt.ylabel('Temperatura (°C)')
        plt.title('Temperaturas Registradas')
        plt.xticks(rotation=45)
        plt.legend()
        plt.tight_layout()
        plt.show()      
    else:
        print(f"Erro ao obter as temperaturas. Código de status: {response.status_code}")

def main():
    # Obtendo todas as temperaturas registradas.
    get_temperatures()

if __name__ == "__main__":
    main()  # Executa a função main de forma assíncrona usando o asyncio.


