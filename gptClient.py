import struct
import numpy as np
from enlace import *
import time

serialName = "COM7"  

def cria_datagrama(num_pacote, total_pacotes, payload):
    head = struct.pack('>III', num_pacote, total_pacotes, len(payload))
    eop = b'\xAA\xBB\xCC'
    datagrama = head + payload + eop
    return datagrama

def main():
    try:
        print("Iniciou o main do client 🚀")
        com1 = enlace(serialName)
        com1.enable()
        print("Abriu a comunicação com a porta serial 📡")
        
        # Handshake
        handshake = cria_datagrama(0, 0, b'')
        time.sleep(0.5)
        com1.sendData(handshake)
        print("Handshake enviado 🤝")
        print("Esperando resposta do server 🕒")
        # Espera resposta do server
        timeout = time.time() + 5
        while com1.rx.getIsEmpty():
            if time.time() > timeout:
                escolha = input("Servidor inativo 😡. Tentar novamente? (S/N): ")
                if escolha.upper() == "S":
                    time.sleep(0.5)
                    com1.sendData(handshake)
                    timeout = time.time() + 5
                else:
                    print("Encerrando comunicação 😔")
                    com1.disable()
                    return
        rxBuffer, _ = com1.getData(15)
        print("Handshake recebido 🤝. Iniciando envio dos pacotes 📦.")

        # Lê Imagem a ser enviada
        imageR = "./imgs/image.png"

        txBuffer = open(imageR, 'rb').read()
        txBufferlen = len(txBuffer)
        
        if txBufferlen % 50 == 0:
            total_pacotes = (txBufferlen / 50)
        else:
            total_pacotes = (txBufferlen // 50) + 1
        
        for i in range(total_pacotes):
            
            payload = txBuffer[:50]
            txBuffer = txBuffer[50:]
            pacote = cria_datagrama(i+1, total_pacotes, payload)
            
            while True:
                print(f"Enviando pacote {i+1} de {total_pacotes}")
                time.sleep(0.5)
                com1.sendData(pacote)
                # Espera confirmação do server
                print("Esperando confirmação do server 🕒")
                while com1.rx.getIsEmpty():
                    pass
                rxBuffer, _ = com1.getData(15)
                print(f"Confirmação recebida: {rxBuffer}")
                if rxBuffer[11] == 0x01:
                    print(f"Pacote {i+1} confirmado pelo server ✅")
                    break
                else:
                    print(f"Pacote {i+1} não confirmado pelo server ❌")
                    escolha = input("Reenviar pacote? (S/N): 🥺 👉👈 ")
                    if escolha.upper() == "N":
                        print("Encerrando comunicação 😔")
                        com1.disable()
                        return
                    else:
                        print("Reenviando pacote")
                        time.sleep(0.5)
                        continue

        print("Todos os pacotes foram enviados 🎉🥳")
        superman = """
        ⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢀⣠⠴⣖⣿⣿⣽⣶⣦⣀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
        ⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣠⡾⠋⢿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣦⣄⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
        ⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣿⣷⣀⠀⢩⣫⣿⣿⣿⣿⣿⣿⣿⣿⣿⣷⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
        ⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣿⣿⠈⢳⣸⣿⣿⣿⣿⣿⣿⠿⠛⠉⣿⣿⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
        ⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣿⣿⠀⠀⡙⠻⣿⡿⠀⠀⠀⠀⠀⠀⣿⡇⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
        ⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣤⣿⡿⠀⠀⠉⠛⠛⢁⠀⠀⠀⠀⠀⠀⢻⡇⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
        ⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢸⣯⣽⡇⠈⢻⢷⣶⣦⠝⠀⡰⡶⣶⡿⣗⢸⢻⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
        ⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢹⣻⡄⠀⠀⠀⠁⠘⠀⠀⡇⠀⠈⠀⠀⢸⣿⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
        ⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣿⡇⠀⠀⠀⠀⠀⠀⠀⣻⡆⠀⠀⠀⢸⡾⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
        ⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢸⡇⠀⠀⠀⠀⡀⢉⣉⠉⢁⠀⠀⠀⢸⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
        ⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢸⣷⡄⠀⠀⠀⠀⠀⠉⠝⠉⠀⠀⠀⡾⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
        ⠀⠀⠀⠀⠀⠀⠀⠀⢀⣀⡀⠀⠀⠀⠀⠀⠀⠀⢸⡇⢻⣄⠀⠀⠀⠀⠀⠀⠀⠀⢀⣾⣧⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
        ⠀⠀⠀⠀⠀⣠⠴⠚⠉⠁⠹⡒⢲⡀⠀⠀⠀⢀⣸⠃⠀⠹⣷⡀⠀⠀⠰⠀⠀⢠⡿⠁⣽⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
        ⠀⠀⠀⢰⠞⠁⠀⠀⠀⠀⠀⠙⡄⢳⣤⠴⠒⠋⠀⠀⠀⠀⢌⠻⠷⠶⠾⠿⠿⠿⡇⠀⢹⠳⣤⡀⡼⠓⢢⡜⠉⠓⠒⠦⣤⡄⠀⠀⠀⠀⠀⠀⠀⠀⠀
        ⠀⠀⠀⢸⠀⢘⣦⣀⠀⠀⠀⠀⠘⣆⢳⡀⠀⠀⠀⠀⠀⠀⠈⢧⡀⠀⠀⠀⠀⣰⠃⠀⠈⠀⠀⣸⠁⢀⡞⠁⠀⠀⠀⠀⣀⡇⠀⠀⠀⠀⠀⠀⠀⠀⠀
        ⠀⢀⣠⠾⠚⠋⠀⠈⠙⠦⣀⠀⠀⠘⡆⢻⡄⠀⠀⠀⠀⠀⠀⠀⠳⠀⠀⠀⢰⠃⠀⠀⠀⠀⢰⠃⢠⠞⠀⠀⠀⢀⣤⠞⠛⠳⢤⣀⠀⠀⠀⠀⠀⠀⠀
        ⠚⠋⠀⠀⠀⠀⠀⠀⠀⠀⠈⠛⠛⠛⠛⠉⠉⠉⠉⠉⠉⠉⠉⠉⠉⠉⠉⠉⠉⠉⠙⠛⠛⠛⠛⠛⠛⠛⠛⠛⠒⠛⠀⠀⠀⠀⠀⠈⠛⢦⣄⠀⠀⠀⠀
        ⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢀⣠⣤⣤⣤⣤⣤⣤⣤⣦⣤⣤⣤⣤⣤⣤⣤⣤⣤⣤⣤⣀⣀⣀⣀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠈⠻⣦⡀⠀
        ⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢀⡴⠋⡠⢶⡆⠀⠀⠀⢀⣠⠤⠶⠶⠶⠶⠤⣄⡀⠀⠀⢶⡒⣶⠆⠀⣈⠳⡄⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠈⠻⣆
        ⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣠⠞⢁⡜⢡⠏⠀⠀⢀⡴⠋⠀⠀⠀⠀⠀⠀⠀⠀⠙⢦⣀⣀⣛⣁⣀⡴⠋⢧⠘⣦⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠘
        ⠀⠀⠀⠀⠀⠀⠀⠀⠀⣼⠃⢀⠞⠀⡟⠀⠀⠀⡞⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠈⢣⡈⢷⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
        ⠀⠀⠀⠀⠀⠀⠀⠀⠀⠉⠳⣌⠳⣤⡇⠀⠀⠀⠙⠦⣀⣀⡀⠀⠀⣀⣀⣀⣀⡤⠤⢤⣀⠀⠀⠀⠀⢀⡴⠋⣵⠟⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
        ⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠈⠳⣌⠁⠀⠀⠀⠀⠀⠀⠉⠉⠉⠉⠉⠉⠉⠀⠀⠀⠀⠈⠙⢢⡀⡠⠊⢠⡞⠁⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
        ⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠈⠳⣄⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠉⢀⡴⠉⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
        ⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠈⠱⢄⠀⢶⡤⢄⣀⣀⡤⠤⠴⠶⠶⠤⣄⠀⠀⠀⠀⡴⠋⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
        ⠀⠀⠀⠀⠀⣀⡀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠳⣄⡉⠢⠤⠴⠦⢄⠀⠀⠀⠀⢀⡇⠀⣠⠞⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
        ⠀⠀⢐⣲⣯⡿⠃⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠈⠛⢦⡀⠀⢠⣞⣀⣀⣀⡤⠞⢀⡜⠁⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
        ⠀⠀⠈⠙⠻⣜⣴⡆⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠙⢦⡀⢶⡒⠒⣶⣄⡴⠋⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
        ⠀⠀⠀⠀⠀⠀⠉⠁⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠙⢦⡓⠞⣳⠏⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
        ⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠙⠟⠁⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
        """
        print(superman)
        print("Encerrando comunicação 😔")
        com1.disable()

    except Exception as erro:
        print("ops! :-\\")  
        print(erro)
        com1.disable()

if __name__ == "__main__":
    main()