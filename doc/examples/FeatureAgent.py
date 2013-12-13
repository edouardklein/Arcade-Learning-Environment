import socket
import select
import struct
import sys
import numpy
numpy_int_type = numpy.dtype('int32').newbyteorder('i')
numpy_float_type = numpy.dtype('float64').newbyteorder('i')
from rlglue.types import Observation
from Network import *

class NetworkWithBind(Network):
    def __init__(self):
        super().__init__()
        AGENT_HOST = '' # Symbolic name meaning all available interfaces
        AGENT_PORT = 5042 # Arbitrary non-privileged port
        agent_socket = socket.socket(socket.AF_INET,
                                          socket.SOCK_STREAM)
        agent_socket.bind((AGENT_HOST, AGENT_PORT))
        agent_socket.listen(1)
        self.agent_conn, agent_addr = agent_socket.accept()
        print('Agent connection from'+str(agent_addr))

    def send_to_agent(self):
        self.agent_conn.sendall(self.sendBuffer.getvalue())

    def recv_from_agent(self):
        return self.recv_from_source(self.agent_conn)

    def close(self):
        super().close()
        self.agent_conn.close()
        
class FeatureAgent():
    def __init__(self):
        self.network = NetworkWithBind()
        self.network.connect();

    def parse_step_message(self):
        reward = self.network.getDouble()
        observation = self.network.getObservation()
        return reward, observation
        
    def loop(self):
        while 1:
            if select.select([self.network.agent_conn],[],[],0)[0]:
                message_type, message_length = self.network.recv_from_agent()
                if message_type == 5 or message_type == 6: #start or step
                    action = self.network.getAction()
                    new_action = self.step_from_agent(action)
                    #TODO construire le message
                    self.network.recvBuffer.seek(0)
                    self.network.sendBuffer = self.network.recvBuffer
                else:
                    self.network.recvBuffer.seek(0)
                    self.network.sendBuffer = self.network.recvBuffer
                self.network.send()
                self.network.clearSendBuffer()
            if select.select([self.network.sock],[],[],0)[0]:
                message_type,message_length = self.network.recv()
                if message_type == 4: #4 <-> agent_init
                    task_spec = self.network.getString()
                    new_task_spec = self.init_to_agent(task_spec)
                    #TODO: Construire dans data le "nouveau" message
                    print(new_task_spec)
                    self.network.recvBuffer.seek(0)
                    self.network.sendBuffer = self.network.recvBuffer
                elif message_type == 5: #5 <-> agent_start
                    observation = self.network.getObservation()
                    new_observation = self.start_to_agent(observation)
                    #TODO construire le nouveau message
                    self.network.recvBuffer.seek(0)
                    self.network.sendBuffer = self.network.recvBuffer
                elif message_type == 6: #6 <-> agent_step
                    reward, observation = self.parse_step_message()
                    new_reward, new_observation = self.step_to_agent(
                        reward,
                        observation)
                    #TODO: Construire le nouveau message dans data
                    self.network.recvBuffer.seek(0)
                    self.network.sendBuffer = self.network.recvBuffer
                else:
                    self.network.recvBuffer.seek(0)
                    self.network.sendBuffer = self.network.recvBuffer
                self.network.send_to_agent()
                self.network.clearSendBuffer()
        self.network.close()


    def init_to_agent(self, task_spec):
        return task_spec

    def start_to_agent(self, observation):
        return observation
        
    def step_to_agent(self, reward, observation):
        return reward, observation
    
    def step_from_agent(self, action):
        return action
        
if __name__=="__main__":
    agent = FeatureAgent()
    agent.loop()
        
