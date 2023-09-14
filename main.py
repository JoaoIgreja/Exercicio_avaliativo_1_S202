# Importa as bibliotecas necessárias para o código.
import threading  # Para criar threads concorrentes.
import random     # Para gerar números aleatórios.
import time       # Para trabalhar com pausas e atrasos no código.
from pymongo import MongoClient  # Para interagir com o MongoDB.

# Função para gerar temperatura aleatória entre 30 e 40 graus.
def gerar_temperatura():
    return round(random.uniform(30, 40), 2)

# Função para atualizar o banco de dados MongoDB com valores de temperatura e verificar alarmes.
def atualizar_banco(sensor_id, nome_sensor, db):
    while True:
        temperatura = gerar_temperatura()  # Gera uma temperatura aleatória.
        sensor_alarmado = temperatura > 38   # Verifica se a temperatura é maior que 38 graus.

        # Atualiza um documento no banco de dados MongoDB com os valores gerados.
        db.sensores.update_one(
            {"_id": sensor_id},
            {
                "$set": {
                    "valorSensor": temperatura,
                    "sensorAlarmado": sensor_alarmado
                }
            }
        )

        print(f"{nome_sensor}: {temperatura}C")  # Exibe a temperatura no console.
        if sensor_alarmado:
            print(
                f"atencao! Temperatura muito alta! Verificar Sensor {nome_sensor}!")
            break  # Se o alarme estiver ativado, interrompe a atualização.
        time.sleep(10)  # Aguarda 10 segundos antes da próxima atualização.

# Função principal do programa.
def main():
    # Conexão com o MongoDB.
    cliente = MongoClient('localhost', 27017)
    banco = cliente.bancoiot
    sensores = banco.sensores

    # Criação de três sensores no banco de dados (você pode criar manualmente).
    sensores.insert_many([
        {"nomeSensor": "Temp1", "valorSensor": 0.0,
            "unidadeMedida": "C", "sensorAlarmado": False},
        {"nomeSensor": "Temp2", "valorSensor": 0.0,
            "unidadeMedida": "C", "sensorAlarmado": False},
        {"nomeSensor": "Temp3", "valorSensor": 0.0,
            "unidadeMedida": "C", "sensorAlarmado": False},
    ])

    # Inicia threads para atualizar os sensores no banco de dados.
    sensores_info = [
        {"_id": 1, "nome_sensor": "Temp1"},
        {"_id": 2, "nome_sensor": "Temp2"},
        {"_id": 3, "nome_sensor": "Temp3"}
    ]

    threads = []
    for sensor_info in sensores_info:
        thread = threading.Thread(target=atualizar_banco, args=(
            sensor_info["_id"], sensor_info["nome_sensor"], sensores))
        threads.append(thread)
        thread.start()

    # Espera que todas as threads terminem.
    for thread in threads:
        thread.join()

# Verifica se o script está sendo executado como o programa principal.
if __name__ == "__main__":
    main()
