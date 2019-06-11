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

![](Indiana-JonesWR.png)
y = 5 [0.647, 0.703, 0.722, 0.716, 0.741, 0.728, 0.732, 0.726, 0.729, 0.73] 3 arrows not adjacent
y = 17 [0.647, 0.743, 0.775, 0.761, 0.789, 0.781, 0.781, 0.778, 0.778, 0.778] 2 arrows not adjacent
y = 29 [0.667, 0.703, 0.735, 0.741, 0.733, 0.738, 0.738, 0.733, 0.734, 0.722] 3 arrows adjacent
y = 41 [0.843, 0.891, 0.901, 0.91, 0.904, 0.887, 0.889, 0.888, 0.887, 0.892] 1 arrow
y = 53 [0.549, 0.624, 0.636, 0.652, 0.685, 0.691, 0.689, 0.678, 0.687, 0.692] 4 arrows all adjcent
y = 65 [0.588, 0.574, 0.609, 0.632, 0.637, 0.631, 0.618, 0.628, 0.63, 0.622] 4 arrows all adjacent

### Qualitative Evaluation

### Overall Goals Reached
dodge multiple arrows coming from dispensers at randomized positions/one of our goals is to allow the agent to get hit instead of restarting the mission, and incorporating that information into our rewards system

## References:
