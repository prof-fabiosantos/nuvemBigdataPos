import requests  # Importa o módulo requests para fazer solicitações HTTP.
BASE_URL = "https://flask-ecru-theta.vercel.app" # Define a URL base da API.

def sent_temperature(temperature):
    url = f"{BASE_URL}/temperatures"  # Monta a URL completa para a rota de adição de temperaturas.
    data = {"temperature": temperature}  # Cria um dicionário com os dados da temperatura.
    response = requests.post(url, json=data)  # Faz uma solicitação POST com os dados JSON.

    if response.status_code == 200:  # Verifica se a solicitação foi bem-sucedida (status code 200).
        print("Temperatura adicionada com sucesso!")
    else:
        print(f"Erro ao adicionar temperatura. Código de status: {response.status_code}")

def main():
          
    new_temperature = 90  
    print(f"Valor da variavel de temperatura: {new_temperature}")

    # Envia uma nova temperatura (altere o valor da temperatura conforme necessário).
    sent_temperature(new_temperature)
      

if __name__ == "__main__":
    main()  # Executa a função main de forma assíncrona usando o asyncio.

    

    
