#
# Copyright (C) 2008, Brian Tanner
#
# http://rl-glue-ext.googlecode.com/
#
# Licensed under the Apache License, Version 2.0 (the "License"
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#

import sys

import rlglue.RLGlue as RLGlue

whichEpisode = 0


def runEpisode(stepLimit):
    global whichEpisode
    terminal = RLGlue.RL_episode(stepLimit)
    totalSteps = RLGlue.RL_num_steps()
    totalReward = RLGlue.RL_return()

    print "Episode " + str(whichEpisode) + "\t " + str(totalSteps) + " steps \t" + str(totalReward) + " total reward\t " + str(terminal) + " natural end"
    with open('Expert.log', 'a') as f:
        f.write("Episode " + str(whichEpisode) + "\t " + str(totalSteps) + " steps \t" +
                str(totalReward) + " total reward\t " + str(terminal) + " natural end\n")

    whichEpisode = whichEpisode + 1

# Main Program starts here

print "\n\nExperiment starting up!"
taskSpec = RLGlue.RL_init()
print "RL_init called, the environment sent task spec: " + taskSpec

print "\n\n---------Learning phase, 5000 learning episodes----------"
for i in range(0, 5000):
    runEpisode(3600)
    if i % 100 == 0:
        RLGlue.RL_agent_message("save "+str(whichEpisode))
        
print "\n\n---------Testing phase, 10 learning episodes----------"
RLGlue.RL_agent_message("Evaluation")
for i in range(0,10):
    runEpisode(3600)

RLGlue.RL_cleanup()
