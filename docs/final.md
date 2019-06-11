---
layout: default
title: Final Report
---


## Video:

## Project Summary:

This overall goal of this project was to have our agent be able to traverse through a walkway to reach a treasure chest at the end. Along the way, however, there will be randomly placed dispensers that shoot arrows perpendicular to the walkway. Our agent, Indiana Jones, should use reinforcement learning in order to learn how to dodge these arrows to reach the treasure.

Our agent will have a walkway that is 10 units long, with the treasure chest (goal) being at the end of the walkway. On the left of the agent, there will be randomly placed dispensers that fire at different intervals. These will be placed 6 units away from the walkway. There will be multiple variations of dispenser positions, as shown in the diagram below. We will have, at minimum, one dispenser, and a maximum of four dispensers. Although the agent *may* be able to randomly move through the walkway with one dispenser, the hardest challenges will be the three staggered dispensers and four adjacent dispensers.

| ![](finalreportoverview.png) |
|:--:| 
| *Figure 1: Environment Overview* |

Because of the difficulty of traversing through multiple arrows being fired, we needed a reinforcement learning algorithm in order to teach our agent when to move and when to stop. If, instead, we used a hard-coded method of avoiding the arrows, there would be the issue of the agent requiring very specific dispenser timings to cross, which would not be ideal. For example, we could design the agent to run across the walkway when all dispensers fire at once, but that would take a significant amount of waiting. To counteract this, we decided the best course of action would be a Q-learning algorithm, a reinforcement learning algorithm that integrates Q-tables.

## Approaches:
baseline and proposed approach

### Q-Learning
Explain exactly what it is and how it works (epsilon,alpha,etc)

advantages and disadvantages

include pseudocode and equations


### States

## Evaluation:

### Quantitative Evaluation

| ![](Indiana-JonesWR.png) |
|:--:|
| *@@@@@@@@@UPDATE THIS AT THE END@@@@@@@@@@@ *Figure X: Agent Win Rates* |

The above image shows the overall winrates of our agent across different environments. The raw data is shown here. The difference between the average winrate of the first 50 runs and the last 50 runs are also below. 
y = 5 [0.647, 0.703, 0.722, 0.716, 0.741, 0.728, 0.732, 0.726, 0.729, 0.73] 3 Arrows not Adjacent, Difference = 0.083, 8.3%

y = 17 [0.647, 0.743, 0.775, 0.761, 0.789, 0.781, 0.781, 0.778, 0.778, 0.778] 2 Arrows not Adjacent, Difference = 0.131, 13.1%

y = 29 [0.667, 0.703, 0.735, 0.741, 0.733, 0.738, 0.738, 0.733, 0.734, 0.722] 3 Arrows Adjacent, Difference = 0.055, 5.5%

y = 41 [0.843, 0.891, 0.901, 0.91, 0.904, 0.887, 0.889, 0.888, 0.887, 0.892] 1 Arrow, Difference = 0.049, 4.9%

y = 53 [0.549, 0.624, 0.636, 0.652, 0.685, 0.691, 0.689, 0.678, 0.687, 0.692] 4 Arrows Adjacent, Difference = 0.143, 14.3%

To reiterate, the y is used to determine which environment was used in the data collection. Each element of the list are the numbers used in the graph. Factors that we hypothesized to affect the overall winrate of each iteration were amount of arrow dispensers, location of arrow dispensers, and whether they were adjacent or not.

#### Amount of Arrow Dispensers





### Qualitative Evaluation

### Overall Goals Reached
dodge multiple arrows coming from dispensers at randomized positions/one of our goals is to allow the agent to get hit instead of restarting the mission, and incorporating that information into our rewards system

## References:
