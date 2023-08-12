import asyncio  # Importa o módulo asyncio para suporte a programação assíncrona.
import requests  # Importa o módulo requests para fazer solicitações HTTP.
import matplotlib.pyplot as plt  # Importa o módulo matplotlib para criação de gráficos.

#BASE_URL = "http://localhost:5000"  # Define a URL base da API.
BASE_URL = "https://flask-ecru-theta.vercel.app"

def get_temperatures():
    url = f"{BASE_URL}/temperatures"  # Monta a URL completa para a rota de obtenção das temperaturas.
    response = requests.get(url)  # Faz uma solicitação GET para obter os dados das temperaturas.

    if response.status_code == 200:  # Verifica se a solicitação foi bem-sucedida (status code 200).
        data = response.json()  # Converte a resposta JSON em um dicionário Python.
        print("Temperaturas registradas:")
        print(data)

        # Extrai dados para plotagem do gráfico.
        dates = [entry[next(iter(entry))]['date'] for entry in data]  # Obtém as datas das temperaturas.
        temperatures = [entry[next(iter(entry))]['temperature'] for entry in data]  # Obtém as temperaturas.
        timestamps = [entry[next(iter(entry))]['timestamp'] for entry in data]  # Obtém os timestamps.

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

async def main():
    # Obtendo todas as temperaturas registradas.
    get_temperatures()

if __name__ == "__main__":
    asyncio.run(main())  # Executa a função main de forma assíncrona usando o asyncio.

    

    
