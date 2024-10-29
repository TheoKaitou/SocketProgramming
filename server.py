import socket
import threading
import queue


type=socket.SOCK_DGRAM
server = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)


server_ip = socket.gethostbyname(socket.gethostname())
port = int(input("Masukkan Server Port: "))

server.bind((server_ip, port))
serveraddress =  (server_ip, port)

username = []
password = []
chatroom = []
class Chatroom:
    def __init__(self, chatName, chatPass, chatParticipants):
        self.chatName = chatName
        self.chatPass = chatPass
        self.chatParticipants = chatParticipants
invalidmessage = "Input yang diberikan Tidak Valid."

def Receive(sock):
    while True:
        try:
            data,addr = sock.recvfrom(1024)
            data.put = ((data, addr))
        except:
            pass

def ClientReceive():
    while True:
        while not data.empty():
            data, addr = data.get()
            decodedata = data.decode()
            client = addr

            decodedata = decodedata.split(",")
            command = decodedata[0]
            information = decodedata[1]

            if command == decodedata:
                match command:
                    case "1":
                        register(client, information)
                    case "2":
                          server.sendto(invalidmessage, client)
            else:
                 server.sendto(invalidmessage.encode(), client)



def login(client, information):
    information = information.split(";")
    logged_in = False        
    log_user = information[0]
    log_pass = information[1]

    if log_user in username:
        index = username.index(log_user)
        if log_pass == password[index]:
            logged_in = True

    if logged_in:
        server.sendto('Berhasil Login'.encode(), client)
    else: 
       server.sendto('username atau password salah!'.encode(), client)

def register(client, information):
    information = information.split(";")
    reguser = information[0]
    regpass = information[1]
    if reguser in username:
        server.sendto("Username telah terdaftar, Silahkan masukkan username lain.".encode(), client)
    else:
        username.append(reguser)
        password.append(regpass)
        server.sendto(f"{reguser} berhasil didaftarkan.".encode() client)

def create(client, information):
    information = information.split
    chatname = information[0]
    chatpassword = information[1]

    if chatname in chatroom:
        server.sendto(invalidmessage.encode(), client)
    else:
        chatroom.append(Chatroom(chatname, chatpassword, []))
        server.sendto(f'Chatroom {chatname} berhasil dibuat'.encode(), client)