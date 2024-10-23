import socket

def runserver():
    type=socket.SOCK_DGRAM
    server = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)


    server_ip = "127.1.1.1"
    port = 8000

    server.bind((server_ip, port))
    server.listen(0)
    print(f"Bersiap menerima rudal dari {server_ip}:{port}")

    client_socket, client_address = server.accept()
    print(f"Rudal diterima dari {client_address[0]}:{client_address[1]}")


    while True:
        request = client_socket.recv(1024)
        request = request.decode("utf-8")

        if request.lower() == "close":
            client_socket.send("closed".encode("utf-8"))
            break
        print(f"diterima: {request}")

        response = "accepted".encode("utf-8")
        client_socket.send(response)
    
    client_socket.close()
    print("Koneksi putus")
    server.close()