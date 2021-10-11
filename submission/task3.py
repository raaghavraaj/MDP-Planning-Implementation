import numpy as np
import os

path1 = "../pa2_base/data/attt/states/states_file_p1.txt"
path2 = "../pa2_base/data/attt/states/states_file_p2.txt"

# print(os.getcwd())
np.random.seed(0)
states1 = []
numStates1 = 0
with open(path1) as f1:
    lines = f1.read().splitlines()
    numStates1 = len(lines)
    states1 = lines

states2 = []
numStates2 = 0
with open(path2) as f2:
    lines = f2.read().splitlines()
    numStates2 = len(lines)
    states2 = lines


def get(s):
    for i in range(9):
        if s[i] == '0':
            return i


def initialise(path, states):
    f = open(path, 'w')
    f.write("1\n")
    for s in states:
        f.write(s)
        l = -1
        for i in range(9):
            if s[i] == '0':
                l = i
                break
        for i in range(9):
            if i == l:
                f.write(" 1")
            else:
                f.write(" 0")
        f.write("\n")


initialise('initial_policy.txt', states1)
player1_policy = None
with open('initial_policy.txt') as f:
    player1_policy = [[0]*9]*numStates1
    lines = f.read().splitlines()[1:]
    for i in range(len(lines)):
        probs = lines[i].split()[1:]
        for j in range(9):
            player1_policy[i][j] = int(probs[j])

player2_policy = [[0 for i in range(9)] for j in range(numStates2)]
# print(len(player2_policy))
# print(len(player2_policy[0]))
cnt = 0
while True:
    if cnt % 2 == 0:
        with open("policy1.txt", "w") as f:
            f.write("1\n")
            for i in range(len(states1)):
                # print(player1_policy[i])
                st = states1[i] + ' ' + ' '.join([str(x)
                                                  for x in player1_policy[i]]) + '\n'
                f.write(st)

        os.system(
            "python3 encoder.py --policy policy1.txt --states {} > mdpfile".format(path2))

        os.system("python3 planner.py --mdp mdpfile > vpfile")

        os.system(
            "python3 decoder.py --value-policy vpfile --states {} --player-id 2 > policyfile".format(path2))

        with open("policyfile") as f:
            new_player2_policy = [[0]*9]*numStates2
            lines = f.read().splitlines()[1:]
            for i in range(len(lines)):
                probs = lines[i].split()[1:]
                for j in range(9):
                    new_player2_policy[i][j] = int(probs[j])

        print(cnt)
        print("Old Player 2 Policy")
        print(player2_policy)
        print("new player 2 policy")
        print(new_player2_policy)

        f = True
        for i in range(numStates2):
            for j in range(9):
                f = f and new_player2_policy[i][j] == player2_policy[i][j]
        if f:
            print("converged on  count {}".format(cnt+1))
            break
        player2_policy = new_player2_policy
    else:
        with open("policy2.txt", "w") as f:
            f.write("2\n")
            for i in range(len(states2)):
                st = states2[i] + ' ' + ' '.join([str(x)
                                                  for x in player2_policy[i]]) + '\n'
                f.write(st)

        os.system(
            "python3 encoder.py --policy policy2.txt --states {} > mdpfile".format(path1))

        os.system("python3 planner.py --mdp mdpfile > vpfile")

        os.system(
            "python3 decoder.py --value-policy vpfile --states {} --player-id 1 > policyfile".format(path1))

        with open("policyfile") as f:
            new_player1_policy = [[0]*9]*numStates1
            lines = f.read().splitlines()[1:]
            for i in range(len(lines)):
                probs = lines[i].split()[1:]
                for j in range(9):
                    new_player1_policy[i][j] = int(probs[j])

        print(cnt)
        print("Old Player 1 Policy")
        print(player1_policy)
        print("new player 1 policy")
        print(new_player1_policy)
        f = True
        for i in range(numStates1):
            for j in range(9):
                f = f and new_player1_policy[i][j] == player1_policy[i][j]
        if f:
            print("converged on  count {}".format(cnt+1))
            break
        player1_policy = new_player1_policy

    cnt += 1
