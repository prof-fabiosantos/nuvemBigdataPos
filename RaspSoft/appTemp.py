# Carrega as bibliotecas
import Adafruit_DHT
import requests  # Importa o módulo requests para fazer solicitações HTTP.
import time
import sys

BASE_URL = "https://flask-ecru-theta.vercel.app" # Define a URL base da API.

sensor = Adafruit_DHT.DHT22
# Define a GPIO conectada ao pino de dados do sensor
pino_sensor = 4

def sent_temperature(temperature):
    url = f"{BASE_URL}/temperatures"  # Monta a URL completa para a rota de adição de temperaturas.
    data = {"temperature": temperature}  # Cria um dicionário com os dados da temperatura.
    response = requests.post(url, json=data)  # Faz uma solicitação POST com os dados JSON.

    if response.status_code == 200:  # Verifica se a solicitação foi bem-sucedida (status code 200).
        print("Temperatura adicionada com sucesso!")
    else:
        print(f"Erro ao adicionar temperatura. Código de status: {response.status_code}")

while(1):
    time.sleep(5) # Pausa o programa por 10 segundos
    # Efetua a leitura do sensor
    umid, temp = Adafruit_DHT.read_retry(sensor, pino_sensor);
    if umid is not None and temp is not None:
        print('Temp={0:0.1f}*  Humidity={1:0.1f}%'.format(temp, umid))
        sent_temperature(temp)
    else:
        print('Sensor não obteve a temperatura. Try again!')
        sys.exit(1)
 