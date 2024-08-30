import struct
import numpy as np
from enlace import *
import time

serialName = "/dev/cu.usbmodem2101"  # Mudar conforme Sistema operacional e porta usada
#serialName = "COM7"  

def main():
    try:
        print("Iniciou o main")
        com1 = enlace(serialName)
        com1.enable()
        print("Abriu a comunicação")
        
        print("esperando 1 byte de sacrifício")
        rxBuffer, nRx = com1.getData(1)
        com1.rx.clearBuffer()
        time.sleep(.1)
        
        numeros_recebidos = []
        print("Okaaay lets go 🏎️ 🏁")
        time.sleep(2)
        print("a espera acabou 🕰️")
        
        start_time = time.time()  # Inicia o contador de tempo
        timeout = 3 # Timeout de 3 segundos para indicar o fim da transmissão

        while True:
            # Verifica se há bytes disponíveis para leitura
            if com1.rx.getBufferLen() >= 4:  # Se há 4 ou mais bytes disponíveis no buffer
                rxBuffer, nRx = com1.getData(4)
                if nRx > 0:
                    numero = np.frombuffer(rxBuffer, dtype=np.float32)[0]
                    print(f"Mensagem recebida: {numero}")
                    numeros_recebidos.append(numero)
                    print("número armazenado")
                    print("números recebidos:", numeros_recebidos)
                    
                    start_time = time.time()  # Reinicia o contador após receber dados
            else:
                # Verifica se passou o tempo limite sem receber dados
                if time.time() - start_time > timeout:
                    print("Timeout: mais de 3 segundos sem receber dados. Fim da transmissão. 🛑")
                # Calculo da soma dos números recebidos
                    soma = 0
                    for numero in numeros_recebidos:
                        soma += numero
                    print(f"Soma dos números recebidos: {soma} 🤓")
                    # Envia a soma dos números recebidos
                    print("Enviando soma 🤔")
                    time.sleep(0.5)
                    com1.sendData(np.float32(soma))
                    print("Soma enviada ✅")
                    time.sleep(0.5)
                    break

    except Exception as erro:
        print("ops! :-\\")
        print(erro)

    finally:
        print("-------------------------")
        print("🛑 Comunicação encerrada 🛑")
        print("-------------------------")
        com1.disable()

if __name__ == "__main__":
    main()