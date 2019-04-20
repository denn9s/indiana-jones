---
layout: default
title:  Proposal
---

# {{ page.title }}

## Summary
Our goal is to create a Minecraft bot that can learn to dodge enemy projectiles, such as skeleton arrows or blaze fireballs. The bot should be able to identify that the Minecraft mob will be able to fire a projectile and properly dodge the incoming projectile.

## Algorithm
We will be using reinforcement learning with Q-Learning.

## Evaluation Plan
The projectile-dodging bot's main metric of measurement will primarily be evaulated through the amount of projectiles dodged. The secondary metric will be the distance and position the mob(s) are spawned from the player, due to the fact that it will generally be easier to dodge projectiles when there is more time to react. We expect using a reinforcement learning (Q-Learning) algorithm will increase the amount of projectiles dodged, at minimum, a linear amount.

To authenticate that the bot is functional, our fundamental sanity case is to have mob(s) randomly spawn around the player during each iteration of testing. In the end, our moonshot case will be the player being able to dodge 100% of incoming projectiles from at least one mob.