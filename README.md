# Fusion Core

---

## What is Fusion Core?

This is a WIP application meant to optimize an SC2 build order.
By supplying a target unit composition, Fusion Core will find the fastest possible solution.

## Goals with this project

The goal of this project will be to make getting into Starcraft 2 easier.
The minutiae of every little thing to do within the first 2-3 minutes of the game can have
extremely detrimental effects on your gameplay, and figuring out optimal solutions is beyond
what most players are interested in accomplishing.

While you can look up whatever the current, popular build order is on Spawning Tool, this
takes the fun of trying your own ideas out of the game. Fusion Core aims to enable creative,
strategy-driven builds without having to lose 500 times in order to figure out how to remove
inefficiencies.

## Methods

We will be loosely emulating the game environment using data collected on all important variables
(such as worker count, saturation, tech tree, and abilities).

There are a couple ways this can be approached.

#1) Brute Force
At every game tick, we can attempt all possible game actions by asking the GameState object.
While this won't explore EVERY possible permutation because of in-game limits, it will likely be taxing on performance.
The goal will be to approach the target unit composition as fast as possible.

#2) Income Focus
At every game tick, we can attempt all possible actions that accomplish the target unit composition, while not
letting the production of workers stop until a certain amount. This will decrease the range of possibilities to test.
