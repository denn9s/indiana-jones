import MalmoPython
import logging
import os
import json
import sys
import math
import time
import random

# log to file/terminal
#logging.basicConfig(filename="log.txt", level=logging.DEBUG)
logging.basicConfig(level=logging.DEBUG)

# external file info
mission_xml = "mission.xml"

# ai info
health = 10

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
	with open(mission_xml, 'r') as f:
		mission_file = f.read()
		mission = MalmoPython.MissionSpec(mission_file, True)
		logging.info("successfully obtained mission")
		
	# set up camera POV and recording
	mission.setViewpoint(0)
	mission_record = MalmoPython.MissionRecordSpec()
	
	# attempt to start mission
	num_tries = 3
	for attempt in range(num_tries):
		try:
			agent_host.startMission(mission, mission_record)
			logging.info("successfully attempted to started mission")
			break
		except RuntimeError as e:
			if attempt == num_tries - 1:
				logging.error("could not start mission: ", e)
				exit(1)
			else:
				time.sleep(2)
				
	# update world state (keep a timer to exit out)
	time_out_max = 50
	time_out = 0
	world_state = agent_host.getWorldState()
	while not world_state.has_mission_begun:
		time_out += 1
		if time_out % 10 == 0:
			logging.info("waiting for mission to begin")
		time.sleep(0.1)
		if time_out >= time_out_max:
			logging.error("could not update world state")
			exit(1)
	world_state = agent_host.getWorldState()
	logging.info("successfully obtained world state")
	
def set_world_observations(agent_host, ep_waiting):
	world_state = agent_host.getWorldState()
	if world_state.number_of_observations_since_last_state > 0:
		msg = world_state.observations[-1].text
		ob = json.loads(msg)
		
		# get current position
		curr_pos = [0, 0, 0]
		if "XPos" in ob:
			curr_pos[0] = int(ob[u'XPos'])
		if "YPos" in ob:
			curr_pos[1] = int(ob[u'YPos'])
		if "ZPos" in ob:
			curr_pos[2] = int(ob[u'ZPos'])
		logging.info("curr_pos: ", curr_pos)


		
if __name__ == '__main__':
	# get agent_host
	agent_host = MalmoPython.AgentHost()
	handle_args(agent_host)
	
	num_reps = 30000
	for rep in range(num_reps):
	
		# death/first run: (re)start mission
		if health <= 0 or rep == 0:
			logging.info("(re)starting mission")
			agent_host.sendCommand("quit")
			start_mission(agent_host, mission_xml)

		# mission in progress
		else:
			logging.info("mission in progress...")
			set_world_observations(agent_host, True)
			time.sleep(0.5)
		time.sleep(1)
	
	