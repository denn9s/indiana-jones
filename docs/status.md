---
layout: default
title:  Status
---

# {{ page.title }}

## Video Summary


## Summary
Our overall goal was to have our agent be able to dodge various enemy projectiles, such as skeleton arrows or blaze fireballs in order to reach a chest. However, we wanted to modify our environment to be a slightly more controlled, so we decided to have our agent dodge arrows fired from dispensers. We wanted our progress to have a solid, simple foundation, so we designed our agent to dodge a single incoming arrow from a dispenser. As of now, our agent is designed to solely move forwards and backwards in order to dodge incoming arrows from the sides.

## Approach
Our main approach to reaching our goal is to have our agent bounded by the sides in order to lower the amount of states. The agent is also spawned in the same spawn point, with the goal being 9 blocks down the straight path. We also kept the dispenser at the same position, aimed at the middle of the agent's path. The dispenser will be positioned 6 units away from the pathway of the agent.

![](indianajones-overview.png)

We decided that Q-learning was the best approach to developing our agent's movements. As a whole, it seemed that Q-learning would be the best approach due to the fact that we could break down our environment into easily-defined states and rewards. Restraining our agent to a straight pathway also helped in reducing the size of the Q-table.

## Evaluation

### Quantitative Evaluation

### Qualitative Evaluation
The main method we can use to evaluate our agent's actions is by watching how it performs against the arrow over time. We should mainly be watching how the agent walks across the walkway, noting whether or not it is stopping/going randomly. Ideally, we would view a good result as non-random movement after a decent amount of episodes, while a bad result would be completely random movement (reaching the goal by pure luck).


## Remaining Goals and Challenges
Currently, our agent is constrained to a dodging a single arrow in an extremely short path. We would like for our agent to be able to dodge multiple arrows coming from dispensers at randomized positions. With that being said, we would like to have the agent's path to the goal be longer.

## Resources Used