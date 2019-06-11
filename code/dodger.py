# ==============================================================================
# MODULES
# ==============================================================================
import MalmoPython					# Malmo
import logging						# world debug prints
import time							# sleep for a few ticks every trial
import random						# random chance to choose actions
import world						# world observation
import sys							# max int tau
from collections import deque		# states/actions/rewards history

# ==============================================================================
# AI class
# ==============================================================================
class Dodger(object):
	def __init__(self, agent_host, alpha=0.5, gamma=0.7, n=1):
		self.agent_host = agent_host	# init in main
		self.alpha = alpha				# learning rate
		self.gamma = gamma				# value decay rate
		self.n = n						# number of back steps to update
		self.epsilon = 0.2				# chance of taking a random action
		self.q_table = {}				
		self.start_pos = None			# init in world.refresh(...)
		self.dispenser_pos = None		# init in world.refresh(...)
		self.life = 0					# init in world.refresh(...)
		self.sleep_time	= 0.05			# time to sleep after action
		
	# USE FOR 1 ARROW TESTING PURPOSES ONLY
	def print_1arrow_q_table(self, moveable_blocks, possible_arrow_x_pos):
		"""	prints a formatted q-table for an 1 arrow run
			args:	moveable blocks		(blocks the agent can walk on (rows))
					arrow x positions	(possible arrow x positions (columns))
		"""
		# print arrow x positions (x-axis)
		print("\t", end="")
		for x in possible_arrow_x_pos:
			print(x, "\t", end="")
		print()

		# print each moveable block (y-axis), and q-values for each
		for block in moveable_blocks:
			print(str(block) + "\t", end="")
			for x in possible_arrow_x_pos:
			
				# q-value is " - " if state is not in q-table or la
				q_val = " - "
				state = (block, x)
				if state in self.q_table:
				
					# normalize the q-values so they are a ratio of each other
					m = self.q_table[state]["move 1"]
					w = self.q_table[state]["move 0"]
					if m + w != 0: 
						m, w = m/(m+w), w/(m+w)
						
						# overwhelming q-value to move
						if m >= 1 and w <= 0:
							q_val = "move"
							
						# overwhelming q-value to wait
						elif w >= 1 and m <= 0:
							q_val = "wait"
							
						# both normalized move/wait q-values
						else:
							m, w = int(m * 100), int(w * 100)
							q_val = str(m) + "/" + str(w)
							
				print(q_val, "\t", end="")
			print()

	# USE FOR 1 ARROW HARD CODED RUN TESTING PURPOSES ONLY 
	def print_hc_wr_table(self, wait_block, possible_arrow_x_pos, wr_table):
		"""	prints a formatted win-rate table for a hard coded 1 arrow run
			args:	wait block			(block the agent can walk on (rows))
					arrow x positions	(possible arrow x positions (columns))
					win-rate table		(win-rates per possible arrow x pos)
		"""
		# print arrow x positions (x-axis)
		for pos in possible_arrow_x_pos:
			print("\t" + str(pos), end="")
		
		# print wait block (y-axis)
		print("\n" + str(wait_block), end="")
		
		# print win-rate for each arrow x position
		for wr in wr_table:
			print("\t" + str(wr), end="")
		print()
		
	def update_q_table(self, tau, S, A, R, T):
		"""	performs relevant updates for state tau
		
			args:	tau				(integer state index to update)
					states deque	
					actions deque	
					rewards deque	
					term state index
		"""
		# upon terminating state, A is empty
		if len(A) == 0:
			A.append("move 0")
		
		# calculate q value based on the most recent state/action/reward
		curr_s, curr_a, curr_r = S.popleft(), A.popleft(), R.popleft()
		G = sum([self.gamma ** i * R[i] for i in range(len(S))])
		if tau + self.n < T:
			G += self.gamma ** self.n * self.q_table[S[-1]][A[-1]]
		old_q = self.q_table[curr_s][curr_a]
		self.q_table[curr_s][curr_a] = old_q + self.alpha * (G - old_q)

	def get_reward(self, obs, prev_action):
		"""	get reward based on distance, life, action, and arrow avoidance
			args:	world observation	(use world.get_observations(...))
					prev_action			(use self.get_action(...))
			return:	reward value		(float)
					success flag		(True / False / None = still in progress)
		"""
		# reward = distance from start position * the following multipliers
		curr_pos = world.get_curr_pos(obs)
		dist = curr_pos["z"] - self.start_pos["z"]
		cumulative_multiplier = 1
		
		# initialize reward multipliers and success flag
		damaged = -10
		complete = 10
		waited = 0.9
		avoided_arrow = 3
		success = None
		
		# damaged: extremely low reward and success = False
		if self.start_pos["x"] != curr_pos["x"]:
			cumulative_multiplier *= damaged
			success = False

		# complete: extremely high reward and success = True
		view_ahead = obs.get(u"view_ahead", 0)
		if view_ahead[0] == "chest":
			cumulative_multiplier *= complete
			success = True
		
		# waited: scale down reward
		if prev_action == "move 0":
			cumulative_multiplier *= waited
		
		# avoided arrow: scale up reward
		dispenser_z = [dispenser[2] for dispenser in self.dispenser_pos]
		if int(curr_pos["z"])-2 in dispenser_z:
			cumulative_multiplier *= avoided_arrow
		
		return dist * cumulative_multiplier, success

	def get_action(self, curr_state, possible_actions):
		"""	get best action using epsilon greedy policy
			args:	current state		(use self.get_curr_state(obs))
					possible actions	(["move 1", "move 0"])
			return:	action				("move 1" or "move 0")
		"""
		# new state
		# NOTE: maybe make it so agent always moves in a new state?
		if curr_state not in self.q_table:
			#self.q_table[curr_state] = {"move 1":0.01, "move 0":0}
			self.q_table[curr_state] = {}
			for action in possible_actions:
				self.q_table[curr_state][action] = 0
		
		# chance to choose a random action
		# NOTE: maybe random chance to move instead?
		if random.random() < self.epsilon:
			#return "move"	
			rand_action_i = random.randint(0, len(possible_actions) - 1)
			return possible_actions[rand_action_i]
			
		# get the best action based on the greatest q-val(s)
		states = dict(self.q_table[curr_state].items())
		best_value = max(states.values())
		best_actions = []
		for action in possible_actions:
			if self.q_table[curr_state][action] == best_value:
				best_actions.append(action)
		rand_action_i = random.randint(0, len(best_actions) - 1)
		return best_actions[rand_action_i]

	def get_curr_state(self, obs):
		"""	get a simplified, integer-based version of the environment
			args:	world observations	(use world.get_observations(...))
			return:	state 				((curr z, arrow₁ x, arrow₂ x, ...))
		"""
		# get current z-position rounded down
		state = []
		curr_pos = world.get_curr_pos(obs)
		state.append(int(curr_pos["z"]-1))
		
		# get arrow x-positions, ordered by increasing z-positions
		arrow_pos = world.get_arrow_pos(obs)
		for x, y, z in self.dispenser_pos:
			if int(z) in arrow_pos:
				state.append(arrow_pos[int(z)])
			else:
				state.append(None)
		
		# (curr_pos[z], arrow_pos[z₁] = x₁, arrow_pos[z₂] = x₂, ...)
		return tuple(state)
		
	def run(self):
		"""	observations → state → act → reward ↩, and update q table
			return:	total reward		(cumulative int reward value of the run)
					success flag		(True / False)
		"""
		# history of states/actions/rewards
		S, A, R = deque(), deque(), deque()
		
		# either you move or you don't
		possible_actions = ["move 1", "move 0"]
		
		# returns total reward and success flag
		total_reward = 0
		success = None
		
		# initialize terminating state
		term_state = "END"
		self.q_table[term_state] = {}
		for action in possible_actions:
			self.q_table[term_state][action] = 0
		
		# run until damaged
		ep_running = True
		while ep_running:

			# get initial state/action/reward
			obs = world.get_observations(self.agent_host)
			s0 = self.get_curr_state(obs)
			a0 = self.get_action(s0, possible_actions)
			r0 = 0
			S.append(s0)
			A.append(a0)
			R.append(r0)

			# continuously get observations
			T = sys.maxsize
			for t in range(sys.maxsize):
				obs = world.get_observations(self.agent_host)
				
				# death or out of bounds glitching ends the run
				self.life = world.get_curr_life(obs)
				curr_pos = world.get_curr_pos(obs)
				if self.life == 0 or curr_pos["z"] > self.start_pos["z"] + 10:
					success = False
					return total_reward, success
					
				if t < T:
				
					# episode finish: end state and get final reward
					if ep_running == False:
						T = t + 1
						S.append(term_state)
					
					# episode running: act and get state/action/reward
					else:
						# act (move or wait)
						self.agent_host.sendCommand(A[-1])
						time.sleep(self.sleep_time)
						
						# get reward and check if episode is finished 
						r, success = self.get_reward(obs, A[-1])
						R.append(r)
						total_reward += r
						if success != None:
							ep_running = False
							continue
						
						# get state/action
						s = self.get_curr_state(obs)
						a = self.get_action(s, possible_actions)
						S.append(s)
						A.append(a)
				
				# end of episode: update q table
				tau = t - self.n + 1
				if tau >= 0:
					self.update_q_table(tau, S, A, R, T)
				if tau == T - 1:
					while len(S) > 1:
						tau = tau + 1
					self.update_q_table(tau, S, A, R, T)
					break
						
		return total_reward, success

	def hard_coded_run(self, wait_block, arrow_x_pos):
		"""	guarantee move when agent on wait_block and arrow on arrow_x_pos
			return:	success flag		(True / False)
		"""	
		ep_running = True
		while ep_running:

			# get initial state/action/reward
			obs = world.get_observations(self.agent_host)
			curr_pos = world.get_curr_pos(obs)
			self.life = world.get_curr_life(obs)
			s = self.get_curr_state(obs)
			
			# death or out of bounds glitching ends the run
			if self.life == 0 or curr_pos["z"] > self.start_pos["z"] + 10:
				return False
					
			# act
			if s[0] == wait_block:
				if s[1] == arrow_x_pos:
					self.agent_host.sendCommand(A[-1])
					time.sleep(self.sleep_time)
				else:
					self.agent_host.sendCommand("move 0")
			else:
				self.agent_host.sendCommand(A[-1])
				time.sleep(self.sleep_time)
				
			# win/lose condition
			view_ahead = obs.get(u"view_ahead", 0)
			if view_ahead[0] == "chest":
				return True
			elif self.start_pos["x"] != curr_pos["x"]:
				return False
			else:
				reward += 1
			
