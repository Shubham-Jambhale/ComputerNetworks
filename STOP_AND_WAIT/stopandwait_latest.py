
'''
from typing import BinaryIO
import struct
import hashlib
import socket
import pickle

snd_state = 0      
rcv_state = 0

def stopandwait_server(iface:str, port:int, fp:BinaryIO) -> None:
    host =iface
    #using this global receive state to store which receive state is going on curretly
    global rcv_state
    #creating a server socket
    ServerSocket = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)
    #checking getaddr info for server address
    response = socket.getaddrinfo(host,port,family=socket.AF_UNSPEC,proto = socket.IPPROTO_UDP)
    ip_address = ""
    for i in response:
        if i[0] == socket.AddressFamily.AF_INET:
            ip_address = i[4][0]
        break
    ServerSocket.bind((ip_address, port))
    print("Hello, I am a server")
    while True:
        #receiving data from client
        data,Addr = ServerSocket.recvfrom(2056)
        #using pickle to unpack the data
        packet = pickle.loads(data)
        #breaking conditions
        if not packet["data"] or len(packet["data"]) == 0:
            break
        dicti = {}
        #if correct packet received the sending the ack
        if packet["type_id"] == 12:
            #checking if correct sequence number is received
            if packet["snd_state"] == 0:
                type_id = 11
                dicti["type_id"] = type_id
                dicti["snd_state"] = packet["snd_state"]
                #creating the requierd ack header to send the ack
                ACK = pickle.dumps(dicti,protocol=pickle.DEFAULT_PROTOCOL)
                ServerSocket.sendto(ACK,Addr)
                #after sending the ack changing the receive state for next packet
                if rcv_state == 1: 
                    rcv_state = 0
                else:
                    rcv_state = 1
                
                # writing the data to the file as correct data is received
                if not packet["data"] or len(packet["data"]) == 0:
                    break
                else:
                    fp.write(packet["data"])
            else:
                type_id = 11
                dicti["type_id"] = type_id
                dicti["snd_state"] = packet["snd_state"]
                ACK = pickel.dumps(dicti,protocol=pickle.DEFAULT_PROTOCOL)
                ServerSocket.sendto(ACK,Addr)
        else:
            continue
    fp.close()

def stopandwait_client(host:str, port:int, fp:BinaryIO) -> None:
    #storing the global sequence number in this variable
    global snd_state
    #type_id tells us ack or nack
    type_id = 12

    #creating a client socket
    client_socket =socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)
    # getaddr info handling 
    response = socket.getaddrinfo(host,port,family=socket.AF_UNSPEC,proto = socket.IPPROTO_UDP)
    ip_address = ""
    for i in response:
        if i[0] == socket.AddressFamily.AF_INET:
            ip_address = i[4][0]
        break
    Addr =(ip_address,port)
    print("Hello, I am a client")
    data = fp.read(256)
    #reading data from file and storing it into dictionary
    dicti = {"type_id":type_id,"snd_state":snd_state,"data":data}
    #packing the data using pickle and sending the data to the server
    packet = pickle.dumps(dicti,protocol=pickle.DEFAULT_PROTOCOL)
    while data:
        client_socket.sendto(packet,Addr)
        #setting the roundtrip time for timeout for 50ms
        client_socket.settimeout(0.5)
        #try to receive ack in the given tiem period 
        try :
            recv,addr = client_socket.recvfrom(1024)
        #resend the package if timeout
        except socket.timeout:
            continue
        #once the ack is received send the next package so stopping the timer
        client_socket.settimeout(None)
        #unpacking the ack
        rec_pack = pickle.loads(recv)
        #checking if correct ack
        if  rec_pack["type_id"]== 11:
                #everything seems correct so reading the next data and sending the data
            data = fp.read(256)
            type_id = 12
            dicti_1 = {}
            dicti_1["type_id"] = type_id
            dicti_1["snd_state"] = 0
            dicti_1["data"] = data
            #packing and sending the data
            packet = pickle.dumps(dicti_1,protocol=pickle.DEFAULT_PROTOCOL)
        else:
            continue 
    #sendig the last byte as empty array to indicate server that whole data is sent.
    dicti_2 = {"type_id":type_id, "snd_state":0, "data":bytes()}
    packet = pickle.dumps(dicti_2,protocol=pickle.DEFAULT_PROTOCOL)
    client_socket.sendto(packet,Addr) 
    fp.close()


'''

from typing import BinaryIO
import struct
import hashlib
import socket
import pickle

snd_state = 0      
rcv_state = 0

def stopandwait_server(iface:str, port:int, fp:BinaryIO) -> None:
    host =iface
    #using this global receive state to store which receive state is going on curretly
    global rcv_state
    #creating a server socket
    ServerSocket = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)
    #checking getaddr info for server address
    response = socket.getaddrinfo(host,port,family=socket.AF_UNSPEC,proto = socket.IPPROTO_UDP)
    ip_address = ""
    for i in response:
        if i[0] == socket.AddressFamily.AF_INET:
            ip_address = i[4][0]
        break
    ServerSocket.bind((ip_address, port))
    print("Hello, I am a server")
    while True:
        #receiving data from client
        data,Addr = ServerSocket.recvfrom(2056)
        #using pickle to unpack the data
        packet = pickle.loads(data)
        #breaking conditions
        if not packet["data"] or len(packet["data"]) == 0:
            break
        dicti = {}
        #if correct packet received the sending the ack
        if packet["type_id"] == 12:
            #checking if correct sequence number is received
            if packet["snd_state"] == rcv_state:
                type_id = 11
                dicti["type_id"] = type_id
                dicti["snd_state"] = packet["snd_state"]
                #creating the requierd ack header to send the ack
                ACK = pickle.dumps(dicti,protocol=pickle.DEFAULT_PROTOCOL)
                ServerSocket.sendto(ACK,Addr)
                #after sending the ack changing the receive state for next packet
                if rcv_state == 1: 
                    rcv_state = 0
                else:
                    rcv_state = 1
                
                # writing the data to the file as correct data is received
                if not packet["data"] or len(packet["data"]) == 0:
                    break
                else:
                    fp.write(packet["data"])
            else:
                type_id = 11
                dicti["type_id"] = type_id
                dicti["snd_state"] = packet["snd_state"]
                ACK = pickel.dumps(dicti,protocol=pickle.DEFAULT_PROTOCOL)
                ServerSocket.sendto(ACK,Addr)
        else:
            continue
    fp.close()

def stopandwait_client(host:str, port:int, fp:BinaryIO) -> None:
    #storing the global sequence number in this variable
    global snd_state
    #type_id tells us ack or nack
    type_id = 12

    #creating a client socket
    client_socket =socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)
    # getaddr info handling 
    response = socket.getaddrinfo(host,port,family=socket.AF_UNSPEC,proto = socket.IPPROTO_UDP)
    ip_address = ""
    for i in response:
        if i[0] == socket.AddressFamily.AF_INET:
            ip_address = i[4][0]
        break
    Addr =(ip_address,port)
    print("Hello, I am a client")
    data = fp.read(1024)
    #reading data from file and storing it into dictionary
    dicti = {"type_id":type_id,"snd_state":snd_state,"data":data}
    #packing the data using pickle and sending the data to the server
    packet = pickle.dumps(dicti,protocol=pickle.DEFAULT_PROTOCOL)
    while data:
        client_socket.sendto(packet,Addr)
        #setting the roundtrip time for timeout for 50ms
        client_socket.settimeout(0.5)
        #try to receive ack in the given tiem period 
        try :
            recv,addr = client_socket.recvfrom(1024)
        #resend the package if timeout
        except socket.timeout:
            continue
        #once the ack is received send the next package so stopping the timer
        client_socket.settimeout(None)
        #unpacking the ack
        rec_pack = pickle.loads(recv)
        #checking if correct ack
        if  rec_pack["type_id"]== 11:
            if rec_pack["snd_state"] == snd_state:  
                #changing states for next msg
                if snd_state == 1:
                    snd_state = 0
                else:
                    snd_state = 1
                #everything seems correct so reading the next data and sending the data
                data = fp.read(256)
                type_id = 12
                dicti_1 = {}
                dicti_1["type_id"] = type_id
                dicti_1["snd_state"] = snd_state
                dicti_1["data"] = data
                #packing and sending the data
                packet = pickle.dumps(dicti_1,protocol=pickle.DEFAULT_PROTOCOL)
            else:
                continue 
    #sendig the last byte as empty array to indicate server that whole data is sent.
    dicti_2 = {"type_id":type_id, "snd_state":snd_state, "data":bytes()}
    packet = pickle.dumps(dicti_2,protocol=pickle.DEFAULT_PROTOCOL)
    client_socket.sendto(packet,Addr) 
    fp.close()



#this code is done using struct and submitted in the autograder 1st time. it is working fine on
#local machine but failing on the autograder. it is working fine on lunar and solar loss network 
'''
from typing import BinaryIO
import struct
import hashlib
import socket

snd_state = 0      
rcv_state = 0

def __IntChksum(data):
        # The checksum is just a sum of all the bytes.
        if isinstance(data, bytearray):
            total = sum(data)
        elif isinstance(data, bytes):
            if data and isinstance(data[0], bytes):
                # Python 2 bytes (str) index as single-character strings.
                total = sum(map(ord, data))
            else:
                # Python 3 bytes index as numbers (and PY2 empty strings sum() to 0)
                total = sum(data)
        else:
            # Unicode strings (should never see?)
            total = sum(map(ord, data))
        return total & 0xFFFFFFFF 

def stopandwait_server(iface:str, port:int, fp:BinaryIO) -> None:
    host =iface
    global rcv_state
    ServerSocket = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)
    response = socket.getaddrinfo(host,port,family=socket.AF_UNSPEC,proto = socket.IPPROTO_UDP)
    ip_address = ""
    for i in response:
        if i[0] == socket.AddressFamily.AF_INET:
            ip_address = i[4][0]
        break

    ServerSocket.bind((ip_address, port))
    print("Hello, I am server")
    while True:
        data,Addr = ServerSocket.recvfrom(262)
        if not data or data == b'':
            break
        msg = (len(data) - 6)
        # print(msg)
        form = 'BBHH'+ str(msg)+'s'
        # print(form)
        message_format = struct.Struct(form)
        (type_id,sq_num,chk_sum,payload_len,msg) = message_format.unpack(data)
        # print(payload_len)
        # print(sq_num)
        # print(type(type_id))
        # print("rcv_stste",rcv_state)
        if __IntChksum(data) != 0x0:
            type_id = 11
            if rcv_state == 0:
                sq_num = 1
            else:
                sq_num = 0
            message_format2 = struct.Struct('BBHH')
            chk_sum = 0 
            ACK = message_format2.pack(type_id,sq_num,chk_sum,payload_len)
            chk_sum = __IntChksum(ACK)
            ACK = message_format2.pack(type_id,sq_num,chk_sum,payload_len)
            ServerSocket.sendto(ACK,Addr)
            # print('bak bhosdike in intchecksum')
            # break
            continue
        if type_id == 12:
            if sq_num == rcv_state:
                type_id = 11
                chk_sum = 0
                message_format2 = struct.Struct('BBHH')
                ACK = message_format2.pack(type_id,sq_num,chk_sum,payload_len)
                chk_sum = __IntChksum(ACK)
                ACK = message_format2.pack(type_id,sq_num,chk_sum,payload_len)
                ServerSocket.sendto(ACK,Addr)
                #print("rdt_send: Sent one message of size %d" % length_ack)
                if rcv_state == 1: #update the recieve states to avoid duplicacy
                    rcv_state = 0
                else:
                    rcv_state = 1
                print("in recv", rcv_state)
                if not data or data == b'':
                    break
                else:
                    fp.write(msg)
            else:
                type_id = 11
                chk_sum = 0
                message_format2 = struct.Struct('BBHH')
                ACK = message_format2.pack(type_id,sq_num,chk_sum,payload_len)
                chk_sum = __IntChksum(ACK)
                ACK = message_format2.pack(type_id,sq_num,chk_sum,payload_len)
                ServerSocket.sendto(ACK,Addr)
        else:
            # print('bak bhosdike in else')
            # break
            continue

    fp.close()


def stopandwait_client(host:str, port:int, fp:BinaryIO) -> None:
    global snd_state
    chk_sum = 0
    type_id = 12
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
        strct = 'BBHH' + str(len(data)) + 's'
        message_format = struct.Struct(strct)
        payload_len = len(data)
        packet = message_format.pack(type_id,snd_state,chk_sum,payload_len,data)
        chk_sum = __IntChksum(packet)
        # print(chk_sum)
        packet = message_format.pack(type_id,snd_state,chk_sum,payload_len,data)
        while data:
            client_socket.sendto(packet,Addr)
            client_socket.settimeout(0.1)
            try :
                recv,addr = client_socket.recvfrom(262)
            except socket.timeout:
                continue
            client_socket.settimeout(None)
            message_format2 = struct.Struct('BBHH')
            (type_id,sq_num,chck_sum,payload_len) = message_format2.unpack(recv) #unpack the ack packet
            if __IntChksum(recv) != 0x0: # calculate the checksum
                print("rdt_send: Recieved a corrupted packet: Type = DATA, Length = %d" % len(recv))
                continue
            if type_id == 11: # if ack then enter
                # print(sq_num,snd_state)
                print("rdt_send: Recieved the expected ACK")
                # print(sq_num,snd_state)
                if sq_num == snd_state:  # update the global variables to alternate states # this is done to check for duplicacy with previous message
                    if snd_state == 1:
                        snd_state = 0
                    else:
                        snd_state = 1
                    data = f.read(256)
                    type_id = 12
                    strct = 'BBHH' + str(len(data)) + 's'
                    message_format = struct.Struct(strct)
                    payload_len = len(data)
                    chk_sum = 0
                    packet = message_format.pack(type_id,snd_state,chk_sum,payload_len,data)
                    chk_sum = __IntChksum(packet)
                    packet = message_format.pack(type_id,snd_state,chk_sum,payload_len,data)
                else:
                    continue # if state is different, retransmit packet
            
        client_socket.sendto(b'',Addr)
        f.close()
 
'''