import socket
import select
import struct
import sys

AGENT_HOST = ''                 # Symbolic name meaning all available interfaces
AGENT_PORT = 5042              # Arbitrary non-privileged port
RLGLUE_HOST = 'localhost'     
RLGLUE_PORT = 4096           

agent_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
agent_socket.bind((AGENT_HOST, AGENT_PORT))
agent_socket.listen(1)
agent_conn, agent_addr = agent_socket.accept()
print('Agent connection from'+str(agent_addr))

rlglue_socket =  socket.socket(socket.AF_INET, socket.SOCK_STREAM)
rlglue_socket.connect((RLGLUE_HOST,RLGLUE_PORT))

while 1:
    if select.select([agent_conn],[],[],0)[0]:
        data = agent_conn.recv(8192)
        if not data: break
        state = 'waiting'
        #f.write('<- Agent : '+str(len(data))+'\n')
        rlglue_socket.sendall(data)
        #f.write('RLGlue <- : '+str(len(data))+'\n')
    #else:
    #    f.write('<- Agent : XXX\n')
    if select.select([rlglue_socket],[],[],0)[0]:
        data = rlglue_socket.recv(8192)
        if not data: break
        #f.write('RLGlue -> : '+str(len(data))+'\n')
        #The first int describe the kind of message, see ClientAgent.py
        message_type = struct.unpack("!i",data[:4])[0]
        message_length = struct.unpack("!i",data[4:8])[0] + 8 #Announced length + header length
        while len(data) < message_length:
            #print("Waiting for "+str(message_length)+" got "+str(len(data)))
            data += rlglue_socket.recv(8192)
        #print('RLGlue -> type '+str(message_type)+': '+str(len(data))),
        if message_type == 4:
            #print("We see a agent init message")
            #print('It has a announced length of '+str(message_length)+' and data has a len of '+str(len(data)))
            #print(data[:8])
            #print(data[8:])
            #print(str(struct.unpack("!i",data[8:12])[0]))
            task_spec = data[12:]
            print(task_spec)
        elif message_type == 6:
            #print("We see an agent step message")
            #print("Reward : "),
            #print(str(struct.unpack("!d",data[8:16])[0]))
            #print("Payload : {nbint} ints, {nbdouble} doubles, and {nbchar} chars".format(
            #    nbint = struct.unpack("!i",data[16:20])[0],
            #    nbdouble =  struct.unpack("!i",data[20:24])[0],
            #    nbchar =  struct.unpack("!i",data[24:28])[0]))
            pass
        else:
            #print("We see some other kind of message")
            pass
        agent_conn.sendall(data)
        #f.write('-> Agent : '+str(len(data))+'\n')
    #else:
        #f.write('RLGlue ->: XXX\n')
agent_conn.close()
rlglue_socket.close()
