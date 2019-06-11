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

### Q-Learning

### States

## Evaluation:

### Quantitative Evaluation

![](Indiana-JonesWR.png)

### Qualitative Evaluation

## References:
