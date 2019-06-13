# ==============================================================================
# MODULES
# ==============================================================================
import MalmoPython					# Malmo
import logging						# world debug prints
import time							# sleep for a few ticks every trial
import sys							# sys arguments
import json							# read world observations
import os							# get full path to mission xml
import random                       # teleport to random dungeon
# ==============================================================================
# AGENT/MISSION FUNCTIONS
# ==============================================================================
def handle_args(agent_host):
	"""	parse system arguments
		args:	malmo agent host	(created beforehand in an outer scope)
	"""
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

def update_mission_xml(mission_xml):
	"""	update the hard-coded mission world path for the user that runs this
		args:	mission filename	(in mc-dodge-bot-master/mission/)
		return:	mission xml path	(the full path to the mission xml)
	"""
	# get full path to master directory
	logging.info("attempting to update mission xml")
	master_dir = os.path.dirname(os.getcwd())
	
	# get full path to mission directory
	os.chdir(master_dir)
	if "mission" not in os.listdir():
		logging.error("no mission directory")
		exit(1)
	mission_dir = master_dir + os.sep + "mission"
	
	# get full path to mission xml
	os.chdir(mission_dir)
	if mission_xml not in os.listdir():
		logging.error("no mission found")
		exit(1)
	mission_xml_path = mission_dir + os.sep + mission_xml

	# get full path to world directory
	os.chdir(master_dir)
	if "world" not in os.listdir():
		logging.error("no world directory")
		exit(1)
	world_dir = master_dir + os.sep + "world"

	# get original line from mission xml to replace
	original_line = None
	logging.info("opening: " + mission_xml_path)
	with open(mission_xml_path, 'r+') as f:
		for line in f.readlines():
			if "FileWorldGenerator" in line:
				original_line = line
				break
	if original_line == None:	
		logging.error("no configuration to load a file from world directory")
		exit(1)
	
	# edit line to include new path to world directory
	left, original_mid, right = original_line.split('"')
	mid_right = original_mid.split("world")[1]
	mid_right = os.sep + mid_right[1:len(mid_right)-1] + os.sep
	updated_line = left + '"' + world_dir + mid_right + '"' + right
	
	# update xml file
	filedata = None
	with open(mission_xml_path, 'r') as f:
		filedata = f.read()
	filedata = filedata.replace(original_line, updated_line)
	with open(mission_xml_path, 'w') as f:
		f.write(filedata)
	logging.info("successfully updated mission xml")
	
	return mission_xml_path

def start_mission(agent_host, mission_xml_path):
	"""	open, read, and start the mission obtained from an xml file
		args:	malmo agent host	(created beforehand in an outer scope)
				mission xml path	(from world.update_mission_xml(...))
	"""
	# get contents of a provided mission xml filepath
	logging.info("opening mission xml")
	with open(mission_xml_path, 'r') as f:
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
def get_observations(agent_host):
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

def get_curr_life(obs):
	"""	get agent's floating point health values
		args:	world observation	
		return: agent health		(float)
	"""	
	if not "Life" in obs:
		logging.error("cannot get life")
		exit(1)
	return obs["Life"]

def get_curr_pos(obs):
	"""	get agent's floating point x-y-z positions
		args:	world observation	(use world.get_observations(...))
		return:	agent's position	(dict of dimension:float positions)
	"""	
	if not "XPos" in obs:
		logging.error("cannot get current position")
		return None
	return {"x":obs[u'XPos'], "y":obs[u'YPos'], "z":obs[u'ZPos']}

def get_arrow_pos(obs):
	"""	get all moving arrows's rounded x position, if any
		args:	world observation	(use world.get_observations(...))
		return:	arrow x positions	(dict of z-position:x-position)
	"""	
	arrow_pos = {}
	arrow_l, arrow_r = obs[u"XPos"]+4.2, obs[u"XPos"]-4.2
	for entity in obs["entities"]:
		if entity["name"] == "Arrow" and entity["motionX"] < -0.1 and \
		   entity["x"] < arrow_l and entity["x"] > arrow_r:
				arrow_pos[int(entity["z"]-1)] = round(entity["x"])
	return arrow_pos

def get_dispenser_pos(agent_host, obs, start_pos):
	"""	get all dispenser's floating point x-y-z positions
		args:	malmo agent host 	(created beforehand in an outer scope)
				world observation	(use world.get_observations(...))
				starting position	(which the view begins from)  
		return:	dispenser positions	(list of x-y-z tuples)
	"""	
	# list of 5 blocks left, 1 block above, and 10 blocks forward from start_pos
	view_left = obs.get(u"view_left", 0)
	dispensers = []
	for i in range(len(view_left)):
		if view_left[i] == "dispenser":
			x, y, z = start_pos["x"], start_pos["y"], start_pos["z"]
			dispensers.append((x + 5.5, y + 1, z + i - 0.5))
	return dispensers

def refill_dispensers(agent_host, dispensers, num_slots = 1):
	"""	refill a list of dispensers with 64 arrows
		args:	malmo agent host 	(created beforehand in an outer scope)
				dispenser positions	(use world.get_dispenser_pos(...))
				num_slots			(number of slots in dispenser to refill)  
		return:	
	"""	
	c1 = "chat /replaceitem block "
	c2 = " slot.container."
	c3 = " minecraft:arrow 64"
	for x, y, z in dispensers:
		xyz = str(int(x)) + " " + str(int(y)) + " " + str(int(z))
		for slot in range(num_slots):
			agent_host.sendCommand(c1 + xyz + c2 + str(slot) + c3)


def soft_refresh(agent_host, dodger):
	"""	teleport agent back to it's starting position and refill dispensers
		args:	malmo agent host 	(created beforehand in an outer scope)
				dodger ai			(created beforehand in an outer scope) 
	"""	
	# world.refresh(...) not called beforehand
	if dodger.start_pos == None or dodger.dispenser_pos == None:
		logging.error("world.soft_refresh(...) before world.refresh(...)")
		exit(1)
	
	# kill mobs
	agent_host.sendCommand("chat /kill @e[type=!minecraft:player]")
	
	# teleport to a new start_pos
	possible_y = [5, 17, 29, 41, 53, 65]
	y = possible_y[0] #random.choice(possible_y)
	x,z = dodger.start_pos["x"], dodger.start_pos["z"]
	xyz = str(x) + " " + str(y) + " " + str(z)
	agent_host.sendCommand("tp " + xyz)
	time.sleep(1)
	
	# get initial observations
	obs = get_observations(agent_host)
	start_pos = get_curr_pos(obs)
	life = get_curr_life(obs)
	
	# refill dispensers
	dispensers = get_dispenser_pos(agent_host, obs, start_pos)
	refill_dispensers(agent_host, dispensers)
	time.sleep(2)
	logging.info("successfully soft refreshed world")

def refresh(agent_host, dodger):
	"""	set agent's starting position and life, and fill dispensers with arrows
		args:	malmo agent host 	(created beforehand in an outer scope)
				dodger ai			(created beforehand in an outer scope) 
	"""	
	# kill mobs
	agent_host.sendCommand("chat /kill @e[type=!minecraft:player]")
	
	# get initial observations
	obs = get_observations(agent_host)
	start_pos = get_curr_pos(obs)
	life = get_curr_life(obs)
	
	# refill dispensers
	dispensers = get_dispenser_pos(agent_host, obs, start_pos)
	refill_dispensers(agent_host, dispensers)

	# set dodger's starting position and life
	dodger.start_pos = start_pos
	dodger.dispenser_pos = dispensers
	dodger.life = life
