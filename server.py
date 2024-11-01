import socket
import threading
import queue


type=socket.SOCK_DGRAM
server = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

server_ip = str(input("Masukkan Server IP: "))
port = int(input("Masukkan Server Port: "))
server.bind((server_ip, port))
serveraddress =  (server_ip, port)
print(serveraddress)

username = []
password = []
chatroom = []
activeuser = []
class Chatroom:
    def __init__(self, chatName, chatPass, chatParticipants):
        self.chatName = chatName
        self.chatPass = chatPass
        self.chatParticipants = chatParticipants
invalidmessage = "Input yang diberikan Tidak Valid."

datas = queue.Queue()

def Receive():
    while True:
        try:
            data, addr = server.recvfrom(1024)
            datas.put((data, addr))
        except:
            pass

def ClientReceive():
    while True:
        while not datas.empty():
            data, addr = datas.get()
            decodedata = data.decode()
            client = addr

            decodedata = decodedata.split(";")
            command = decodedata[0]
            information = decodedata[:1]

            print(f"{client} : {decodedata[1]}")

            if command == decodedata:
                match command:
                    case "1":
                        register(client, information)
                    case "2":
                        login(client, information)
                    case "3":
                        create(client, information)
                    case "4":
                        join(client, information)
                    case "5":
                        logout(client, information)
                    case "6":
                        leave(client, information)
                    case "7":
                        sendchat(client, information)
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
        server.sendto("2!1!Berhasil Login".encode(), client)
        activeuser.append(log_user)
    else: 
       server.sendto("2;0;username atau password salah!".encode(), client)

def register(client, information):
    information = information.split(",")
    reguser = information[0]
    regpass = information[1]
    if reguser in username:
        server.sendto("2;1;Username telah terdaftar, Silahkan masukkan username lain.".encode(), client)
    else:
        username.append(reguser)
        password.append(regpass)
        server.sendto(f"{reguser} berhasil didaftarkan.".encode(), client)

def logout(client, information):
    information = information.split(";")
    logoutuser = information[1]
    if logoutuser in activeuser:
        server.sendto("5;1;Berhasil Keluar dari aplikasi RUDAL_CHAT".encode(), client)
        activeuser.remove(logoutuser)
        for Chatroom in chatroom:
            if logoutuser in Chatroom.chatParticipant:
                Chatroom.chatParticipants.remove(client)
    else:
        server.sendto("5;0;Anda tidak pernah melakukan login.")

def create(client, information):
    information = information.split
    chatname = information[0]
    chatpassword = information[1]

    global chatroom
    for Chatroom in chatroom:
        if chatroom.chatname == chatname:
            server.sendto(invalidmessage.encode(), client)
        else:
            chatroom.append(Chatroom(chatname, chatpassword, []))
            server.sendto(f"3;1;Chatroom {chatname} berhasil dibuat".encode(), client)

def join(client, information):
    information = information.split
    chatname = information[0]
    chatpassword = information[1]

    global chatroom
    for Chatroom in chatroom:
        if Chatroom.chatName == chatname:
            if Chatroom.chatPass == chatpassword:
                Chatroom.chatParticipants.append(client)
                server.sendto(f"4;1;Selamat anda telah bergabung di groupchat {chatname}".encode(), client)
            else:
                server.sendto("4;0;Password Salah Silahkan lakukan lagi!".encode(), client)
        else:
            server.sendto("4;0;Chatroom tidak ditemukan".encode(), client)

def leave(client, information):
    information = information.split
    chatname = information[1]

    for Chatroom in chatroom:
        if Chatroom.chatName == chatname:
            Chatroom.chatParticipants.remove(client)
            server.sendto(f"6;1;Anda berhasil keluar dari groupchat {chatname}".encode(), client)
        else:
            server.sendto("6;0;Anda tidak bergabung dalam chatroom!".encode(), client())

def sendchat(client, information):

    message = information.split(",")[1]
    clientUsername = information.split(",")[2]
    chatname = information.split(",")[3]
    global chatrooms
    for chatroom in chatrooms:
        if chatroom.chatName == chatname:
            for participant in chatroom.chatParticipants:
                server.sendto({message},{clientUsername},{chatname}.encode(), participant)


clients = set()

receive_thread = threading.Thread(target=Receive)
receive_thread.start()

sending_thread = threading.Thread(target=ClientReceive)
sending_thread.start()