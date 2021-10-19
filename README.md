# MDP-Planning-Implementation
This repository contains the implementation of the MDP planning methods and an Anti-Tic-Toe Game based on the methods.

# Problem Statement
Please head over to the [assignment webpage](https://www.cse.iitb.ac.in/~shivaram/teaching/cs747-a2021/pa-2/programming-assignment-2.html) on the instructor's website.

# Usage
### Task1:

The classes and policy calculation functions related to the task are implemented in the file `submission/planner.py`. The file `planner.py` takes two arguments:
* ```--mdp```: path to the file describing the MDP
* ```--algorithm```: any one out of Value Iteration `vi`, Linear Programming `lp` and Howard Policy Iteration `hpi`. The default is set to `hpi`.

The program evaluated the salues of the states and the optimal actions for the states and prints them on stdout. Example command to run the program:
```
submission $ python3 planner.py --mdp ../pa2_base/data/mdp/continuing-mdp-10-5.txt --algorithm vi
```

### Task2:

In this task, as mentioned in the assignment, we generate an optimal policy for our player who plays against a predefined policy in an Anti-Tic-Tac-Toe game. Each of the two players have some valid states i.e. the states where they can take actions at. These states are stored in the two statefiles present at `pa2_base/data/attt/states`

We require to run three files for the task:
* `encoder.py` - takes arguments `--policy` which is the opponent's policy file, `--states` which is our player's valid states file
* `planner.py` - as described above
* `decoder.py` - takes arguemnts `--value-policy` which is the value-policy file generated using the planner script, `--states` which is our player's valid states file, `--player-id` which is our player's id i.e. 1 or 2
