import socket
import threading
import sys

# Set up UDP socket

server = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

# Konfigurasi server
server_ip = str(input("Masukkan Server IP: "))
port = int(input("Masukkan Server Port: "))
username = str
isinroom = False
roomlist = []
temproom = str

def receive_messages():
    while True:
        try:
            # Menerima pesan dari server
            message, _ = server.recvfrom(1024)
            decodedmessage = message.decoded()
            information = decodedmessage.split(";")
            if information[0] == 1:
                registerresponse(information)
            elif information[0] == 2:
                loginresponse(information)
            elif information[0] == 3:
                createchatresponse(information)
            elif information[0] == 4:
                joinresponse(information)
            elif information[0] == 5:
                logoutresponse(information)
            elif information[0] == 6:
                leaveresponse(information)
            else:
                print(information[2].decode())
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

def register():
    usr = str(input("Masukkan Username yang ingin anda Gunakan: "))
    password = str(input("Masukkan password yang ingin anda gunakan: "))
    server.sendto(f"1,{usr};{password}".encode(), server_ip)

def registerresponse(information):
    userinfo = information[2].split(";")
    usr = userinfo [0]
    if information[1] == 1:
        print(f"User {usr} telah berhasil didaftarkan, silahkan login.")
    else:
        print(f"Pendaftaran Gagal, silahkan coba lagi.")

def login():
    usr = str(input("username: "))
    password = str(input("password: "))
    server.sendto(f"2,{usr};{password}".encode(), (server_ip, port))

def loginresponse(information):
    userinfo = information[2].split(";")
    usr = userinfo[0]
    global username
    if information[1] == 1:
        print(f"Selamat datang di RUDAL_CHAT {usr}")
        username = usr
    else:
        print("Login Gagal, perhatikan username dan password anda")

def createchat():
    chatname = str(input("Masukkan name dari groupchat yang ingin anda buat: "))
    chatpass = str(input("Masukkan password dari groupchat yang ingin anda buat: "))
    server.sendto(f"3;{chatname},{chatpass}".encode(), (server_ip, port))

def createchatresponse(information):
    if information[1] == 1:
        print(information[2])
        global isinroom
        isinroom = True
    else:
        print(information[2])

def join():
    chatname = str(input("Masukkan name dari groupchat yang ingin anda buat: "))
    chatpass = str(input("Masukkan password dari groupchat yang ingin anda buat: "))
    global temproom
    temproom = chatname
    server.sendto(f"4;{chatname},{chatpass}".encode(), (server_ip, port))

def joinresponse(information):
    if information[1] == 0:
        print(information[2])
    else:
        print(information[2])
        global isinroom
        isinroom = True
        roomlist.append(temproom)

def logout(user):
    server.sendto(f"5;{user}")

def logoutresponse(information):
    if information[1] == 0:
        print(information[2])
    else:
        print(information[2])
        global isinroom
        global username
        isinroom = False
        username = ""

def leave():
    chatname = str(input("Masukkan nama groupchat yang anda ingin keluar: "))
    global temproom
    temproom = chatname
    chatpass = str(input("Masukkan password groupchat untuk validasi: "))
    server.sendto(f"6;{chatname},{chatpass}".encode(), (server, port))

def leaveresponse(information):
    if information[1] == 0:
        print(information[2])
    else:
        print(information[2])
        roomlist.remove(temproom)
        if len(roomlist) == 0:
            global isinroom
            isinroom = False

def sendchat():
    message = (str(input("Masukkan pesan anda: ")))
    server.sendto(f"6;{message}".encode(), (server_ip, port))


receive_thread = threading.Thread(target=receive_messages)
receive_thread.start()

sending_thread = threading.Thread(target=send_messages)
sending_thread.start()
