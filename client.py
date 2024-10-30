import socket
import threading
import sys

# Set up UDP socket

server = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

# Konfigurasi server
server_ip = str(input("Masukkan Server IP: "))
port = int(input("Masukkan Server Port: "))

serveraddress = (server_ip, port)

def receive_messages():
    while True:
        try:
            # Menerima pesan dari server
            message, _ = server.recvfrom(1024)
            print(message.decode())
        except:
            pass

def send_messages():
    while True:
        try:
            while True:
                # Kirim pesan ke server
                message = input("Kamu: ")
                if message.lower() == 'exit':
                    print("Keluar dari chat room.")
                    sys.exit()
                server.sendto(message.encode(), (server_ip, port))
        finally:
            server.close()

receive_thread = threading.Thread(target=receive_messages)
receive_thread.start()

sending_thread = threading.Thread(target=send_messages)
sending_thread.start()
