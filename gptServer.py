import struct
import numpy as np
from enlace import *
import cv2
import os
import time

serialName = "/dev/cu.usbmodem2101"  

def cria_datagrama(num_pacote, total_pacotes, payload):
    head = struct.pack('>III', num_pacote, total_pacotes, len(payload))
    eop = b'\xAA\xBB\xCC'  # Exemplo de EOP
    datagrama = head + payload + eop
    return datagrama

def abre_pacote(datagrama):
    head = datagrama[:12]
    num_pacote, total_pacotes, payload_size = struct.unpack('>III', head)
    payload = datagrama[12:-3]
    return num_pacote, total_pacotes, payload_size, payload

def main():
    try:
        print("Iniciou o main do server 🚀")
        com1 = enlace(serialName)
        com1.enable()
        print("Abriu a comunicação com a porta serial 📡")

        # Espera handshake
        print("Esperando handshake do client 🙄⌛️")
        time.sleep(0.5)
        rxBuffer, _ = com1.getData(15)  # Recebe um datagrama completo (12 head + 0 payload + 3 EOP)

        if rxBuffer[-3:] == b'\xAA\xBB\xCC':  # Verifica o EOP
            print("Handshake recebido 🤝")
            ack = struct.pack('>III', 0, 0, 0) + b'\xAA\xBB\xCC'
            com1.sendData(ack)  # Confirmação do handshake
        else:
            print("❌ Erro no handshake, encerrando comunicação.❌ 😔")
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
            com1.disable()
            return

        arquivo = []

        i = 0
        while True:
            print("Esperando pacote... 📦")
            time.sleep(0.5)

            head, _ = com1.getData(12)

            print(f"Datagrama recebido: {rxBuffer.hex()}")

            num_pacote, total_pacotes, payload_size = struct.unpack('>III', head)
            print(f"Pacote: {num_pacote}, Total de Pacotes: {total_pacotes}, Tamanho do Payload: {payload_size}")

            payload, _ = com1.getData(payload_size)  
            eop, _ = com1.getData(3)
            print(eop)

            if eop == b'\xAA\xBB\xCC' and num_pacote == i + 1:
                arquivo.append(payload)
                print(f"Pacote {num_pacote} de {total_pacotes} recebido com sucesso ✅")
                print("Enviando confirmação... 📨")
                ack = b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x01\xaa\xbb\xcc'
                print(f"ACK: {ack}")
                time.sleep(0.5)
                com1.sendData(ack)
                i += 1
            else:
                print(f"❌Erro no pacote {num_pacote}. Solicitando novamente... 👉👈")
                nack = b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\xaa\xbb\xcc'
                print(f"NACK: {nack}")
                time.sleep(0.5)
                com1.sendData(nack)

            if num_pacote == total_pacotes:
                arquivo = b''.join(arquivo)
                print("Todos os pacotes recebidos com sucesso. 🎉")
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
                diretorio = "./imgs"
                if not os.path.exists(diretorio):
                    os.makedirs(diretorio)
                caminho_arquivo = os.path.join(diretorio, "recebido.jpg")
                
                with open(caminho_arquivo, "wb") as f:
                    f.write(arquivo)
                    print("Arquivo salvo com sucesso 📁📸")
                    
                # Abrir imagem usando OpenCV
                print("Abrindo imagem... 🖼️")
                img = cv2.imread("recebido.jpg")
                cv2.imshow("Imagem Recebida", img)
                cv2.waitKey(0)  # Espera até que qualquer tecla seja pressionada
                cv2.destroyAllWindows()  # Fecha a janela
                break

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