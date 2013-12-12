import socket
import select
import struct
import sys
import numpy
numpy_int_type = numpy.dtype('int32').newbyteorder('i')
numpy_float_type = numpy.dtype('float64').newbyteorder('i')
from rlglue.types import Observation

class FeatureAgent():
    def __init__(self):
        AGENT_HOST = '' # Symbolic name meaning all available interfaces
        AGENT_PORT = 5042 # Arbitrary non-privileged port
        RLGLUE_HOST = 'localhost'     
        RLGLUE_PORT = 4096           
        agent_socket = socket.socket(socket.AF_INET,
                                          socket.SOCK_STREAM)
        agent_socket.bind((AGENT_HOST, AGENT_PORT))
        agent_socket.listen(1)
        self.agent_conn, agent_addr = agent_socket.accept()
        print('Agent connection from'+str(agent_addr))
        self.rlglue_socket =  socket.socket(socket.AF_INET,
                                            socket.SOCK_STREAM)
        self.rlglue_socket.connect((RLGLUE_HOST,RLGLUE_PORT))

    def parse_step_message(self, data):
        reward = struct.unpack("!d",data[8:16])[0]
        nbint = struct.unpack("!i",data[16:20])[0]
        nbdouble =  struct.unpack("!i",data[20:24])[0]
        nbchar =  struct.unpack("!i",data[24:28])[0]
        observation = Observation(nbint, nbdouble, nbchar)
        if nbint > 0:
            observation.intArray = numpy.frombuffer(data,
                                                    dtype=numpy_int_type,
                                                    count=nbint,
                                                    offset=28)
        if nbdouble > 0:
            observation.doubleArray = numpy.frombuffer(data,
                                                dtype=numpy_float_type,
                                                count=nbdouble,
                                                offset=28+nbint*4)
        if nbchar > 0:
            observation.charArray = numpy.frombuffer(data,
                                            dtype='S1',
                                            count=nbchar,
                                            offset=28+nbint*4+nbdouble*8)
        return reward, observation
        
    def loop(self):
        while 1:
            if select.select([self.agent_conn],[],[],0)[0]:
                data = self.agent_conn.recv(8192)
                if not data: break
                self.rlglue_socket.sendall(data)
            if select.select([self.rlglue_socket],[],[],0)[0]:
                data = self.rlglue_socket.recv(8192)
                if not data: break
                message_type = struct.unpack("!i",data[:4])[0]
                message_length = struct.unpack("!i",data[4:8])[0] + 8 
                while len(data) < message_length:
                    data += self.rlglue_socket.recv(8192)
                if message_type == 4: #4 <-> agent_init
                    task_spec = data[12:] #12 bytes for the two int header of the message and the int header of the string
                    new_task_spec = self.init_to_agent(task_spec)
                    #TODO: Construire dans data le "nouveau" message
                    print(new_task_spec)
                elif message_type == 6: #6 <-> agent_step
                    reward, observation = self.parse_step_message(data)
                    new_reward, new_observation = self.step_to_agent(
                        reward,
                        observation)
                    #TODO: Construire le nouveau message dans data
                self.agent_conn.sendall(data)
        self.agent_conn.close()
        self.rlglue_socket.close()


    def init_to_agent(self, task_spec):
        return task_spec

    def step_to_agent(self, reward, observation):
        return reward, observation
    

if __name__=="__main__":
    agent = FeatureAgent()
    agent.loop()
        
