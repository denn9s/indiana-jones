# ==============================================================================
# MODULES
# ==============================================================================
import MalmoPython					# Malmo
import logging						# world debug prints
import time							# sleep for a few ticks every trial
import sys							# sys arguments
import json							# read world observations

# ==============================================================================
# AGENT/MISSION FUNCTIONS
# ==============================================================================
def handle_args(agent_host):
	# ideally run with no arguments
	try:
		agent_host.parse(sys.argv)
	except RuntimeError as e:
		logging.error("ERROR:", e)
		logging.info(agent_host.getUsage())
		exit(1)
	if agent_host.receivedArgument("help"):
		print(agent_host.getUsage())
		exit(0)
	if agent_host.receivedArgument("test"):
		exit(0)

def start_mission(agent_host, mission_xml):
	# get contents of a provided mission xml filepath
	logging.info("opening mission xml")
	with open(mission_xml, 'r') as f:
		mission_file = f.read()
		mission = MalmoPython.MissionSpec(mission_file, True)
		logging.info("successfully opened mission xml")

	# set up camera POV and recording
	mission.setViewpoint(0)
	mission_record = MalmoPython.MissionRecordSpec()
		
	# attempt to start a mission:
	num_tries = 3
	logging.info("attempting to start mission")
	for attempt in range(num_tries):
		try:
			agent_host.startMission(mission, mission_record)
			logging.info("successfully attempted to started mission")
			break
		except RuntimeError as e:
			if attempt == num_tries - 1:
				logging.error("could not start mission")
				exit(1)
			else:
				logging.info("retrying...")
				time.sleep(2)
	
	# update world state
	logging.info("waiting for mission to start")
	world_state = agent_host.getWorldState()
	while not world_state.has_mission_begun:
		time.sleep(0.1)
		world_state = agent_host.getWorldState()
	logging.info("successfully updated world state")

# ==============================================================================
# WORLD MANIPULATION/OBSERVATION FUNCTIONS
# ==============================================================================
def get_dispensers(agent_host):
	# get the x-y-z coordinates of all dispensers in view
	world_state = agent_host.getWorldState()
	if world_state.number_of_observations_since_last_state > 0:
		msg = world_state.observations[-1].text
		obs = json.loads(msg)
		view_left = obs.get(u'view_left', 0)
		dispensers = []
		for i in range(len(view_left)):
			if view_left[i] == "dispenser":
				coord = (obs[u'XPos']+4.5, obs[u'YPos']+1, obs[u'ZPos']+i-0.5)
				dispensers.append(coord)
		return dispensers
	else:
		logging.error("cannot view dispensers")
		exit(1)

def refill_arrows(agent_host, dispensers):
	c1 = "/replaceitem block "
	c2 = "slot.container."
	c3 = " minecraft:arrow 64"
	for x, y, z in dispensers:
		xyz = str(int(x)) + " " + str(int(y)) + " " + str(int(z))
		for slot in range(4):
			agent_host.sendCommand(c1 + xyz + c2 + str(slot) + c3)

def refresh(agent_host, dodger):
	# refill dispensers
	dispensers = get_dispensers(agent_host)
	refill_arrows(agent_host, dispensers)

	# set new episode
	dodger.ep_running = True
	dodger.ep_finish = False
	
def get_curr_pos(obs):
	# get a dict of curent x-y-z positions
	return {"x":obs[u'XPos'], "y":obs[u'YPos'], "z":obs[u'ZPos']}

def get_curr_hp(obs):
        # returns current hp of the agent
        return obs["Life"]
        
def get_arrow_pos(obs):
	# get a dict of arrow positions by their z-positions
	arrows = {}
	arrow_l, arrow_r = obs["XPos"]+4.2, obs["XPos"]-2.4
	for entity in obs["entities"]:
		if entity["name"] == "Arrow" and entity["motionX"] < -0.01 and \
		   entity["x"] < arrow_l and entity["x"] > arrow_r:
				arrows[int(entity["z"])] = entity
	return arrows

def get_world_observations(agent_host):
	"""	get world observations from the agent's most recent world state
		args:	malmo agent host	(created beforehand in an outer scope)
		return: world observation	(dict of info:value)
	"""
	world_state = agent_host.peekWorldState()
	while True:
	
		# valid world state: get observations
		if world_state.number_of_observations_since_last_state > 0:
			msg = world_state.observations[-1].text
			obs = json.loads(msg)  

			# check for any errors
			for err in world_state.errors:
				logging.error(err)
			if "entities" not in obs:
				logging.error("no entities in the world")
				exit(1)
			
			return obs
		
		# invalid world state: get another one asap
		else:
			world_state = agent_host.getWorldState()
