
class dodger(object):
	def __init__(self, alpha=0.3, gamma=1, n=1):
		self.epsilon = 0.2,		# chance of taking a random action
		self.q_table = {},		# N tiles * M hazard positions * O hazards
		self.n = n,				# number of back steps to update
		self.alpha = alpha,		# learning rate
		self.gamma = gamma		# value decay rate

	def run():
		return