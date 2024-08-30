import struct
import numpy as np
from enlace import *
import time

#serialName = "/dev/cu.usbmodem101"  # Mudar conforme Sistema operacional e porta usada
serialName = "COM7"  

def main():
    try:
        print("Iniciou o main")
        com1 = enlace(serialName)
        com1.enable()
        print("Abriu a comunicação")
        time.sleep(.2)
        com1.sendData(b'00')
        print("byte de sacrfifício enviado")
        time.sleep(1)

        # Lê os números do arquivo listaEnvio.txt com codificação UTF-8
        with open('listaEnvio.txt', 'r', encoding='utf-8') as file:
            numeros = file.readlines()

        soma = 0
        timeout_flag = False

        for numero in numeros:
            numero = numero.strip()
            try:
                numero_float = float(numero) # Converte a string para float
                print(f"Enviando o número: {numero_float}")
                soma += numero_float
                ieee754_bytes = np.float32(numero_float)  # Converte para IEEE 754 em formato binário (big-endian float)
                time.sleep(0.5)
                com1.sendData(ieee754_bytes)  # Envia os bytes diretamente
                print("Número enviado")
                
                while com1.tx.threadMutex == True:
                    time.sleep(0.01)
                txSize = com1.tx.getStatus()
                print(f'Enviou = {txSize}')

            except ValueError as ve:
                print(f"Erro ao converter '{numero}' para float: {ve}")
                continue  # Pula para o próximo número

        print("Todos os números foram enviados")
        print(f"A soma correta é: {soma}")

        # Espera resposta do server
        print("Esperando resposta do server")
        timeout = time.time() + 5  # Define o tempo limite de 30 segundos

        while com1.rx.getIsEmpty():
            if time.time() > timeout:  # Verifica se o tempo limite foi atingido
                print("Timeout: Nenhuma resposta do server em 5 segundos.")
                timeout_flag = True
                break
            time.sleep(0.01)

        if not timeout_flag:
            print("recebendo soma do server")
            time.sleep(0.5)
            rxBuffer, nRx = com1.getData(4)
            print("soma recebida")
            soma_server = np.frombuffer(rxBuffer, dtype=np.float32)[0]
            soma += 10e21
            delta = abs(soma - soma_server)
            if delta <= (0.01 * soma):
                print("Soma correta")
                joinha = """
                ⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢰⣦⣤⡀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
                ⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣼⣿⣿⣿⡆⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
                ⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣠⣿⣿⣿⣿⡇⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
                ⠀⠀⠀⠀⠀⠀⠀⠀⣠⣾⣿⣿⣿⣿⣿⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
                ⢠⣤⣤⣤⡀⠀⢀⣼⣿⣿⣿⣿⣿⣿⣧⣤⣤⣤⣤⣤⣤⣤⣤⣄⡀⠀
                ⢸⣿⣿⣿⡇⠀⢸⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡄
                ⢸⣿⣿⣿⡇⠀⢸⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡇
                ⢸⣿⣿⣿⡇⠀⢸⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡿⠀
                ⢸⣿⣿⣿⡇⠀⢸⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⠁⠀
                ⢸⣿⣿⣿⡇⠀⢸⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⠁⠀⠀
                ⢸⣿⣿⣿⡇⠀⢸⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⠃⠀⠀⠀
                ⢸⣿⣿⣿⡇⠀⠈⠻⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡿⠃⠀⠀⠀⠀
                """
                print(joinha)
            else:
                print("Soma incorreta")
                print(f"Soma esperada: {soma}") 
                negativo = """
                ⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣠⣴⡶⠶⣶⣦⣤⣶⣶⣶⣦⣤⠀⠀⠀⠀⠀⠀⠀
                ⠀⠀⠀⠀⠀⠀⠀⢀⣴⡿⠋⢡⣴⣾⠿⠛⠉⠀⠀⠀⠈⢻⣇⠀⠀⠀⠀⠀⠀
                ⠀⠀⣀⣀⣀⣀⣴⡿⠋⠀⠀⠀⠻⣷⣄⣀⣤⣶⠿⠿⠿⠿⠿⢿⣶⡀⠀⠀⠀
                ⠀⣸⡟⠛⠛⠛⠋⠀⠀⠀⠀⠀⢴⣾⠿⠛⠉⠀⠀⣀⣤⣄⣀⣀⣽⣇⠀⠀⠀
                ⠀⣿⠃⠀⠀⠀⠀⠀⠀⠀⠀⠀⠈⠻⣷⣤⣴⣾⠿⠛⠉⠉⠉⠉⠛⠻⣿⡆⠀
                ⢸⣿⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠸⣿⣏⠁⠀⠀⣀⣠⣶⣶⣶⣦⣤⣿⡇⠀
                ⢸⣿⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠈⣻⣷⣶⡿⠟⠋⠁⠀⠀⠉⠙⢿⣦⠀
                ⠀⣿⡆⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠙⣿⣄⡀⠀⠀⢀⣠⣤⡀⠀⠀⣿⡇
                ⠀⢹⣷⣤⣤⣤⣀⡀⠀⠀⠀⠀⠀⠀⠀⠀⠈⠙⠻⠿⠿⠟⠛⠉⠉⠀⢀⣿⠇
                ⠀⠀⠉⠉⠉⠉⠛⢿⣦⡀⠀⠀⠀⠀⠀⠀⠀⢀⣀⣀⣀⣀⣀⣤⣴⣶⠟⠁⠀
                ⠀⠀⠀⠀⠀⠀⠀⠀⠹⣷⡄⠀⠀⠀⠀⠀⠀⢸⣿⠛⠛⠛⠋⠉⠁⠀⠀⠀⠀
                ⠀⠀⠀⠀⠀⠀⠀⠀⠀⠘⢿⣦⡀⠀⠀⠀⠀⠀⣿⣇⠀⠀⠀⠀⠀⠀⠀⠀⠀
                ⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠻⣿⣆⠀⠀⠀⠀⠸⣿⡄⠀⠀⠀⠀⠀⠀⠀⠀
                ⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠈⠻⣷⣄⠀⠀⠀⠹⣿⡄⠀⠀⠀⠀⠀⠀⠀
                ⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠈⠻⣷⡄⠀⠀⠸⣿⡀⠀⠀⠀⠀⠀⠀
                ⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢻⣇⠀⠀⠀⣿⡇⠀⠀⠀⠀⠀⠀
                ⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠘⣿⠀⢀⣼⡿⠁⠀⠀⠀⠀⠀⠀
                ⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢿⣿⠿⠛⠁⠀⠀⠀⠀⠀⠀⠀
                """
                print(negativo)


        # Encerra comunicação
        print("-------------------------")
        print("Comunicação encerrada")
        print("-------------------------")
        com1.disable()

    except Exception as erro:
        print("ops! :-\\")
        print(erro)
        com1.disable()

if __name__ == "__main__":
    main()