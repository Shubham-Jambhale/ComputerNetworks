import socket

from _thread import *
import threading
import os

# print_lock = threading.Lock()

def threaded(conn,address) -> None:
    while conn:
        data = conn.recv(256).decode('utf-8')
        print("got message from ",address)
        if data == 'Hello' or data == 'hello':
            res = 'world'
        elif data == 'exit':
            res = "ok"
            conn.send(res.encode('utf-8'))
            conn.close()
            os._exit(1)
        elif data == "goodbye":
            res = "farewell"
            conn.send(res.encode('utf-8'))
            conn.close()
            break
        else:
            res = data
        conn.send(res.encode('utf-8'))

def chat_server(iface:str, port:int, use_udp:bool) -> None:
    host = iface
    if use_udp:
        UDPServerSocket = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)
        UDPServerSocket.bind((host, port))
        print("Hello, I am server")
        while 1:
            message, addr = UDPServerSocket.recvfrom(256)
            data = message.decode('utf-8')
            print("got message from ",addr)
            if data == 'Hello' or data == 'hello':
                res = 'world'
            elif data == 'exit':
                res = "ok"
                UDPServerSocket.sendto(res.encode('utf-8'),addr)
                break
            elif data == "goodbye":
                res = "farewell"
                UDPServerSocket.sendto(res.encode('utf-8'),addr)
            else:
                res = data
            UDPServerSocket.sendto(res.encode('utf-8'),addr)

    else:
        server_socket = socket.socket()
        server_socket.bind((host,port)) 
        server_socket.listen()
        count = 0
        print("Hello, I am Server")
        while True:
            conn, address = server_socket.accept()
            print("connection",count, "from ", str(address))
            # print_lock.acquire()
            processThread = threading.Thread(target=threaded, args=(conn,address))
            processThread.start()
            count += 1
        

def chat_client(host:str, port:int, use_udp:bool) -> None:
   
    if use_udp:
        client_socket =socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)
        Addr =(socket.gethostbyname(host),port)
        print("Hello, I am a client")
        while 1:
            msg =input()
            client_socket.sendto(msg.encode('utf-8'),Addr)
            data,addr = client_socket.recvfrom(256)
            print(data.decode('utf-8'))
            if msg == "exit":
                break
            if msg == "goodbye": 
                break
    else:
        client_socket =socket.socket()
        client_socket.connect((host, port))
        print("Hello, I am a client")
        while True:
            message = input()
            client_socket.send(message.encode('utf-8'))
            data = client_socket.recv(1024).decode('utf-8')
            print(data)
            if message == "exit":
                break
            if message == "goodbye":
                break

        client_socket.close()