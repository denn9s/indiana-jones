---
layout: default
title:  Status
---

# {{ page.title }}

## Video Summary


## Summary
Our overall goal was to have our agent be able to dodge various enemy projectiles, such as skeleton arrows or blaze fireballs in order to reach a chest. However, we wanted to modify our environment to be slightly more controlled, so we decided to have our agent dodge arrows fired from dispensers. We wanted our progress to have a solid, simple foundation, so we designed our agent to dodge a single incoming arrow from a dispenser. As of now, our agent is designed to solely move forwards and backwards in order to dodge incoming arrows from the sides. We incorporated reinforcement learning by utilizing q-tables, Q-learning, to allow the agent to dodge the projectiles and reach the goal.

## Approach
Our main approach to reaching our goal is to have our agent bounded by the sides in order to lower the amount of states. The agent is also spawned in the same spawn point, with the goal being 9 blocks down the straight path. We also kept the dispenser at the same position, aimed at the middle of the agent's path. The dispenser will be positioned 6 units away from the pathway of the agent.

![](indianajones-overview.png)

We decided that Q-learning was the best approach to developing our agent's movements. As a whole, it seemed that Q-learning would be the best approach due to the fact that we could break down our environment into easily-defined states and rewards. Restraining our agent to a straight pathway also helped in reducing the size of the Q-table.

## Evaluation

### Quantitative Evaluation
Our main criteria for the quantitative evalution of our agent is how far the agent got before he was hit by an arrow. However, due to the nature of our current one arrow implementation, this evaluation in our current state is not that useful as the agent either is hit by the arrow, or passes the arrow tile and retrieves the treasure. Instead we decided to look at whether the agent decided to "move 0" or wait in response to the arrow's placement through the use of q-learning with rewards, or if the agent was lucky and randomly passed the arrow tile. Our agent had gone through numerous iterations of different reward settings in order to determine what was the sweet spot for the best performance.

Our group had also used a random runs where the agent randomly chooses to wait or walk to compare our results with the q-table. We wanted to see if the win rates of the random runs were similar to our q-table so judge if the optimal reward setting was applied or required adjusting. We created another scoring method that had the agent stop before the arrow and then moving based on the arrow position. This allowed us to see the win-rate in a controlled setting to limit other potential factors that may have affected the run, mainly being random chance. This "hard coded" run allowed us to eliminate the time variable it took to get to the treasure after clearing the arrow tile if we wanted to include time as part of the evalutaion. 

TODO: add the diagram in main.py and talk about the winrate!!!@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@


### Qualitative Evaluation
The main method we can use to evaluate our agent's actions is by watching how it performs against the arrow over time. We should mainly be watching how the agent walks across the walkway, noting whether or not it is stopping/going randomly. Ideally, we would view a good result as non-random movement after a decent amount of episodes, while a bad result would be completely random movement (reaching the goal by pure luck).


## Remaining Goals and Challenges
Currently, our agent is constrained to a dodging a single arrow in an extremely short path. We would like for our agent to be able to dodge multiple arrows coming from dispensers at randomized positions. With that being said, we would like to have the agent's path to the goal be longer. 
Some challenges that we were facing are continuting to optimize our reward settings as the increase in winrate between our regular runs and random runs is moderate currently due to our one arrow setup, however once we incorporate mulitple dispensers, we would have to adjust the reward as it would be a more important factor in the success rate of our agent.

## Resources Used
