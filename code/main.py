# ==============================================================================
# MODULES
# ==============================================================================
import MalmoPython                                      # Malmo
import logging                                          # world debug prints
import time                                                     # sleep for a few ticks every trial

import world                                            # world manipulation/observation functions
from dodger import Dodger                       # dodger ai

# ==============================================================================
# GLOBAL VARS
# ==============================================================================
# log to file / terminal
#logging.basicConfig(filename="log.txt", level=logging.DEBUG)
logging.basicConfig(level=logging.DEBUG)
#logging.getLogger().disabled = True

# external file info
mission_xml = "mission1c.xml"

# ai info
health = 20
T = 20
# ==============================================================================
# MAIN
# ==============================================================================
def main():
        # get agent_host
        agent_host = MalmoPython.AgentHost()
        world.handle_args(agent_host)
        T = 20
        # create ai
        dodger = Dodger(agent_host)
        
        # continuously repeat trials
        num_reps = 30000
        for rep in range(num_reps):
                health = T          
                # death/first run: (re)start mission
                
                if health < 20 or rep == 0:
                        T = 20
                        logging.info("(re)starting mission")
                        agent_host.sendCommand("quit")
                        world.start_mission(agent_host, mission_xml)
                        time.sleep(0.5)
                        world.refresh(agent_host, dodger)

                # mission in progress
                else:
                        T = dodger.run() # <20 = arrow hit, 100 = found treasure
                        time.sleep(0.01)
                        
        time.sleep(1)

if __name__ == '__main__':
        main()

