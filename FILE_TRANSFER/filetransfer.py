from typing import BinaryIO
import socket

def file_server(iface:str, port:int, use_udp:bool, fp:BinaryIO) -> None:
    host = iface
    if use_udp:
        ServerSocket = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)
        response = socket.getaddrinfo(
        host,
        port,
        family=socket.AF_UNSPEC,
        proto = socket.IPPROTO_UDP
        )
        ip_address = ""
        for i in response:
            if i[0] == socket.AddressFamily.AF_INET:
                ip_address = i[4][0]
            break

        ServerSocket.bind((ip_address, port))
        print("Hello, I am server")
        with open(fp.name, "wb") as f:
            while True:
                data,Addr = ServerSocket.recvfrom(256)  
                if not data:
                    break
                else:
                    f.write(data)
            f.close()
    else:
        server_socket = socket.socket()
        response = socket.getaddrinfo(
        host,
        port,
        family=socket.AF_UNSPEC,
        proto = socket.IPPROTO_TCP
        )
        ip_address = ""
        for i in response:
            if i[0] == socket.AddressFamily.AF_INET:
                ip_address = i[4][0]
            break
        server_socket.bind((ip_address,port)) 
        server_socket.listen()
        print("Hello, I am Server")
        conn, address = server_socket.accept()
        with open(fp.name, "wb") as f:
            while True:
                data = conn.recv(256)  
                if not data:
                    break
                f.write(data)   
            f.close()
        conn.close()


def file_client(host:str, port:int, use_udp:bool, fp:BinaryIO) -> None:
    if use_udp:
        client_socket =socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)
        response = socket.getaddrinfo(
        host,
        port,
        family=socket.AF_UNSPEC,
        proto = socket.IPPROTO_UDP
        )
        ip_address = ""
        for i in response:
            if i[0] == socket.AddressFamily.AF_INET:
                ip_address = i[4][0]
            break
        Addr =(ip_address,port)
        print("Hello, I am a client")
        with open(fp.name, "rb") as f:
            data = f.read(256)
            while data:
                client_socket.sendto(data,Addr)
                data = f.read(256)
            f.close()
    else:
        client_socket =socket.socket()
        response = socket.getaddrinfo(
        host,
        port,
        family=socket.AF_UNSPEC,
        proto = socket.IPPROTO_TCP
        )
        ip_address = ""
        for i in response:
            if i[0] == socket.AddressFamily.AF_INET:
                ip_address = i[4][0]
            break

        client_socket.connect((ip_address, port))
        print("Hello, I am a client")
        with open(fp.name, "rb") as f:
            data = f.read(256)
            while data:
                client_socket.send(data)
                data =f.read(256)
            f.close()
            client_socket.close()

    

