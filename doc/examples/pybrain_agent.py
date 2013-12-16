from rlglue.agent import AgentLoader as AgentLoader
from pybrain.rl.learners.valuebased import ActionValueNetwork
from pybrain.rl.agents import LearningAgent
from pybrain.rl.learners import NFQ
from pybrain.tools.rlgluebridge import RlglueAgentAdapter
import pickle


class myAdapter(RlglueAgentAdapter):
    def __init__(self, klass, *args, **kwargs):
        super(myAdapter, self).__init__(klass, *args, **kwargs)
        
    def agent_message(self, message):
        if message == 'Evaluation':
            self.agent._setLearning(False)
            print('Evaluation')
            return 'No more exploration'
        elif message[:4] == 'save':
            try:
                name = '_'+message[5:]
            except:
                name = ''
            print("Saving in file : "+'pybrain_agent'+name+'.pickle')
            with open('pybrain_agent'+name+'.pickle', 'w') as f:
                pickle.dump(learner, f)
            return 'saved'
        else:
            return 'Message not understood'

if __name__ == "__main__":
    controller = ActionValueNetwork(1024, 18)
    try:
        with open('pybrain_agent.pickle', 'r') as f:
            print("Reading value from file")
            learner = pickle.load(f)
    except IOError:
        print("Starting with fresh value")
        learner = NFQ()
    agent = myAdapter(LearningAgent, controller, learner)
    AgentLoader.loadAgent(agent)
    with open('pybrain_agent.pickle', 'w') as f:
        pickle.dump(learner, f)
