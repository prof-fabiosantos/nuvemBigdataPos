import requests
import matplotlib.pyplot as plt
import json
from matplotlib.animation import FuncAnimation
import firebase_admin
from firebase_admin import credentials, firestore, initialize_app

BASE_URL = "https://api-flask-three.vercel.app"


fig, ax = plt.subplots(figsize=(10, 6))  # Defina fig e ax como globais

def update_plot(i):
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

        ax.clear()
        ax.plot(dates, temperatures, marker='o', linestyle='-', color='b', label='Temperatura')
        ax.set_xlabel('Data')
        ax.set_ylabel('Temperatura (°C)')
        ax.set_title('Temperaturas Registradas')
        ax.xaxis.set_tick_params(rotation=45)
        ax.legend()
        plt.tight_layout()

def main():
    ani = FuncAnimation(fig, update_plot, interval=5000)  # Atualiza a cada 10 segundos (10000 ms)
    plt.show()

if __name__ == "__main__":
    main()


if __name__ == "__main__":
    main()

