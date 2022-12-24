from typing import BinaryIO
from datetime import datetime
import socket
import pickle
import time
import hashlib


def makePkt(seqnum,data):
        packet = [seqnum, data]
        # packet.append(getHash(packet))
        return packet

def makeACK(expectedseqnum):
    packet = [expectedseqnum]
    # packet.append(getHash(packet))
    return packet

def makebreakingpkt(nextSeq,expectedseqnum):
    packet = [nextSeq,expectedseqnum]
    # packet.append(getHash(packet))
    return packet

def gbn_server(iface:str, port:int, fp:BinaryIO) -> None:
    host = iface
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
    nextSeqnum = 0
    bytearr = bytearray() 
    while True:
        packet, Addr = ServerSocket.recvfrom(2096)
        pkt = pickle.loads(packet)
        # print("packet",pkt[0])
        if pkt[0] == nextSeqnum:
            if len(pkt[1]) == 0:
                break
            bytearr.extend(pkt[1])
            # print(bytearr)
            nextSeqnum +=1
            pack = makeACK(nextSeqnum)
            message = pickle.dumps(pack,protocol=pickle.DEFAULT_PROTOCOL)
            ServerSocket.sendto(message,Addr)
        else:
            # print("in else")
            # print(nextSeqnum)
            pack = makeACK(nextSeqnum)
            message = pickle.dumps(pack,protocol=pickle.DEFAULT_PROTOCOL)
            ServerSocket.sendto(message,Addr)
    # print(bytearr)
    fp.write(bytearr)
    fp.close()
            
def gbn_client(host:str, port:int, fp:BinaryIO) -> None:
    windowSize = 3
    temp_array = []
    data = fp.read(1024)
    w = 0
    while data:
        temp_array.append(data)
        w += 1
        data = fp.read(1024)
    temp_array.append( bytes())
    # print(type(temp_array[0]))
    # print(len(temp_array))

    client_socket =socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)
    response = socket.getaddrinfo(host,port,family=socket.AF_UNSPEC,proto = socket.IPPROTO_UDP)
    ip_address = ""
    for i in response:
        if i[0] == socket.AddressFamily.AF_INET:
            ip_address = i[4][0]
        break
    Addr =(ip_address,port)
    print("Hello, I am a client")
    base = 0
    nextSeqnum = 0
    # counter = 0
    abc = False
    # count = 0 
    Startdatetimeout = datetime.utcnow() - datetime(1970, 1, 1)
    secondsTimeOut =(Startdatetimeout.total_seconds())
    StartmillisecondsTimeOut = round(secondsTimeOut*1000)
    while True:
        if abc:
            break
        for i in range(base, min((base + windowSize),len(temp_array))):
            # if base + windowSize > 117:
            #     print(base+windowSize)
            sndpkt = makePkt(nextSeqnum, temp_array[i])
            # send packet
            message = pickle.dumps(sndpkt,protocol=pickle.DEFAULT_PROTOCOL)
            client_socket.sendto(message,Addr)
            nextSeqnum += 1
            # if temp_array[i] == bytes():
                # print("in ifffff")
                # abc = True
        client_socket.settimeout(0.06)

        try:
            counter = 0
            while counter < windowSize :
                # print("in try")
                # print("receiving")
                packet, serverAddress = client_socket.recvfrom(4096)
                rcvpkt = pickle.loads(packet)
                base = rcvpkt[0]
                nextSeqnum = base
                counter += 1
                # print("waiting")

            # print("nextSeqnum",nextSeqnum)
            # print("window size",windowSize)
            # print("base",base)
            if counter == windowSize:
                windowSize += 1
        except:
            # count += 1
            # if count > 30:
            #     break
            # print("in except")
            if windowSize > 1:
                windowSize -= 1
            Enddatetimeout = datetime.utcnow() - datetime(1970, 1, 1)
            EndsecondsTimeOut =(Enddatetimeout.total_seconds())
            EndmillisecondsTimeOut = round(EndsecondsTimeOut*1000)
            # print(EndmillisecondsTimeOut- StartmillisecondsTimeOut)
            if EndmillisecondsTimeOut- StartmillisecondsTimeOut > 2750:
                break
            # print("windowsize in except",windowSize)
            # abc = False
            # continue
            
    fp.close()
    client_socket.close()

        
    
    






    