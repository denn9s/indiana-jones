# ==============================================================================
# MODULES
# ==============================================================================
import MalmoPython                  # Malmo
import logging                      # world debug prints
import time                         # sleep for a few ticks every trial
import random                       # random chance to choose actions
import world                        # world observation
import sys                          # max int tau
from collections import deque       # states/actions/rewards history

# ==============================================================================
# AI class
# ==============================================================================
class Dodger(object):
    def __init__(self, agent_host, alpha=0.3, gamma=1, n=1):
        self.alpha = alpha              # learning rate
        self.gamma = gamma              # value decay rate
        self.n = n                      # number of back steps to update
        self.epsilon = 0.2              # chance of taking a random action
        self.q_table = {}
        self.agent_host = agent_host    
        self.ep_running = False
        self.ep_finish = False
    
    def update_q_table(self, tau, S, A, R, T):
        curr_s, curr_a, curr_r = S.popleft(), A.popleft(), R.popleft()
        G = sum([self.gamma ** i * R[i] for i in range(len(S))])
        if tau + self.n < T:
            G += self.gamma ** self.n * self.q_table[S[-1]][A[-1]]

        old_q = self.q_table[curr_s][curr_a]
        self.q_table[curr_s][curr_a] = old_q + self.alpha * (G - old_q)


    def get_curr_feedback(self):
        #TODO: what defines our reward?
        return 0
        
    def calculate_reward(self):
        #TODO: what defines our reward?
        return 0

    def choose_action(self, curr_state, possible_actions):
        # new state
        if curr_state not in self.q_table.keys():
            self.q_table[curr_state] = {"move 1":0, "move 0":0}
        
        # chance to choose a random action
        if random.random() < self.epsilon:
            rand_action_i = random.randint(0, len(possible_actions) - 1)
            return "move 1"
            #return possible_actions[rand_action_i]
        
        # epsilon greedy policy
        states = dict(self.q_table[curr_state].items())
        best_value = max(states.values())
        best_actions = []
        for action in possible_actions:
            if self.q_table[curr_state][action] == best_value:
                best_actions.append(action)
        
        # no best action should never occur... just in case though  
        if len(best_actions) == 0:
            rand_action_i = random.randint(0, len(possible_actions) - 1)
            return possible_actions[rand_action_i]
            
        rand_action_i = random.randint(0, len(best_actions) - 1)
        
        #return best_actions[rand_action_i]
               
        
        return "move 0"

    def get_curr_state(self,obs):
        # TODO: what defines our state?
        #print ("I am at " + str(world.get_curr_pos(obs)["z"] + 316.5)) ## move 1 makes z += 1
        
        pos = world.get_arrow_pos(obs)
        myPos = world.get_curr_pos(obs)
        if len(pos) == 0:
            return tuple((myPos["z"], None))
        for i in pos.keys():
            #print(round(world.get_arrow_pos(obs)[i]["x"]))
            return tuple((myPos["z"], round(world.get_arrow_pos(obs)[i]["x"])))

                
    def was_hit(self,obs):
        # returns current hp of the agent
        
        if (obs["Life"] != 20):
            return True
        return False


    def run(self):
        S, A, R = deque(), deque(), deque()
        running = True
        while running:
            obs = world.get_world_observations(self.agent_host)
            
            
            # TODO: do things with obs... use/make helper functions in world.py
            
            if self.ep_running == True:
                
                # get current state and the best action from it
                s0 = self.get_curr_state(obs)
                possible_actions = ["move 1", "move 0"]
                a = self.choose_action(s0, possible_actions)
                
                # add state/action/reward to history
                S.append(s0)
                A.append(a)
                R.append(0)
                
                T = sys.maxsize
                for t in range(sys.maxsize):
                    obs = world.get_world_observations(self.agent_host)
                   
                    if (obs["Life"] < 20):
                        return obs["Life"] # EXITS MISSION HERE AND IS A FAIL
                        # EXIT AND RESTART MISSION!!!!
                    if (world.get_curr_pos(obs)["z"] == -308.5):
                        return 100 #EXITS MISSION HERE AND IS A WIN
                    # TODO: same as above todo
                    
                    if t < T:
                        if self.ep_finish == True:
                            # end state and get final reward
                            T = t + 1
                            state.append(None)
                            reward = self.calculate_reward()
                            R.append(reward)
                            self.ep_finish = False
                        else:
                            # act
                            # TODO: how to move a perfect 1 square? DONE CAN MOVE PERFECT SQUARE - ETHAN
                            self.agent_host.sendCommand(A[-1])
                            time.sleep(0.25)
                            print(A[-1])
                            #self.agent_host.sendCommand("move 0")
                            
                            # get reward
                            #time.sleep(???) wait a bit and get feedback?
                            reward = self.get_curr_feedback()
                            R.append(reward)
                
                            # get current state and the best action from it
                            s0 = self.get_curr_state(obs)
                            possible_actions = ["move 1", "move 0"]
                            a = self.choose_action(s0, possible_actions)
        
                            # add state/action to history
                            S.append(s0)
                            A.append(a)
                        
                        # TODO: wtf is this
                        tau = t - self.n + 1
                        if tau >= 0:
                            self.update_q_table(tau, S, A, R, T)
                        if tau == T - 1:
                            while len(S) > 1:
                                tau = tau + 1
                            self.update_q_table(tau, S, A, R, T)
                            running = False
                            break
        return
