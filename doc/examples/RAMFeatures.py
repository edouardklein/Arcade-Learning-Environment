from FeatureAgent import *
from rlglue.types import Observation, Action
import numpy
numpy_int_type = numpy.dtype('int32').newbyteorder('>')

class RAMFeatures(FeatureAgent):
    def __init__(self):
        super().__init__()
        self.binary_masks = [pow(2,i) for i in range(0,7)]

    def init_to_agent(self, task_spec):
        '''Our new task_spec string discards the screen info and only keeps the RAM, and ask only for the action from the first player'''
        #Old task_spec is : VERSION RL-Glue-3.0 PROBLEMTYPE episodic DISCOUNTFACTOR 1 OBSERVATIONS INTS (128 0 255)(33600 0 127) ACTIONS INTS (0 17)(18 35) REWARDS (UNSPEC UNSPEC) EXTRA Name: Arcade Learning Environment
        return "VERSION RL-Glue-3.0 PROBLEMTYPE episodic DISCOUNTFACTOR 1 OBSERVATIONS INTS (1024 0 1) ACTIONS INTS (0 17) REWARDS (UNSPEC UNSPEC) EXTRA Name: Arcade Learning Environment, Asterix game, RAM features"

    def start_to_agent(self, observation):
        return self.new_observation(observation)

    def step_to_agent(self, reward, observation):
        return reward, self.new_observation(observation)

    def new_observation(self, observation):
        #The 1024 bits of RAM of the Atari are passed as 1024 ints
        answer = Observation(1024,0,0)
        answer.intArray = numpy.zeros(1024,dtype=numpy_int_type)
        for i in range(0,1024):
            answer.intArray[i] = observation[i/8] & self.binary_masks[i%8]
        return answer
        
    def step_from_agent(self, action):
        answer = Action(2,0,0)
        answer.intArray = [action.intArray[0], 18]
        return answer

if __name__=="__main__":
    agent = RAMFeatures()
    agent.loop()

