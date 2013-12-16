from FeatureAgent import *
from rlglue.types import Observation, Action

class RAMFeatures(FeatureAgent):
    def __init__(self):
        super().__init__()

    def init_to_agent(self, task_spec):
        '''Our new task_spec string discards the screen info and only keeps the RAM, and ask only for the action from the first player'''
        #Old task_spec is : VERSION RL-Glue-3.0 PROBLEMTYPE episodic DISCOUNTFACTOR 1 OBSERVATIONS INTS (128 0 255)(33600 0 127) ACTIONS INTS (0 17)(18 35) REWARDS (UNSPEC UNSPEC) EXTRA Name: Arcade Learning Environment
        return "VERSION RL-Glue-3.0 PROBLEMTYPE episodic DISCOUNTFACTOR 1 OBSERVATIONS INTS (128 0 255) ACTIONS INTS (0 17) REWARDS (UNSPEC UNSPEC) EXTRA Name: Arcade Learning Environment, Asterix game, RAM features"

    def start_to_agent(self, observation):
        return self.new_observation(observation)

    def step_to_agent(self, reward, observation):
        return reward, self.new_observation(observation)

    def new_observation(self, observation):
        answer = Observation(128,0,0)
        answer.intArray = observation.intArray[:128]
        return answer
        
    def step_from_agent(self, action):
        answer = Action(2,0,0)
        answer.intArray = [action.intArray[0], 18]
        return answer

if __name__=="__main__":
    agent = RAMFeatures()
    agent.loop()

