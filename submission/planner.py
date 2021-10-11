import numpy as np
import argparse
import pulp as lp

# adding command line arguments
parser = argparse.ArgumentParser()
parser.add_argument("--mdp", required=True,
                    help="path to the input MDP file")
parser.add_argument("--algorithm", default="vi",
                    help="for one of the 7 algorithms")


def get(T, s, a, s_prime):
    if s_prime in T[s][a]:
        return T[s][a][s_prime]
    else:
        return (0, 0)


def checkPrecision(a, b, lim):
    sub = np.abs(a - b)
    if np.any(sub >= lim):
        return False
    else:
        return True


def valueIteration(T, gamma):
    n, k = len(T), len(T[0])  # numStates, numActions

    V_star = np.zeros(n, dtype=float)
    pi_star = np.zeros(n)

    while True:
        V_temp = np.zeros(n)
        for s in range(n):
            V_temp[s] = max([sum([get(T, s, a, s_prime)[0]*(
                get(T, s, a, s_prime)[1] + gamma*V_star[s_prime]) for s_prime in range(n)]) for a in range(k)])
        if checkPrecision(V_temp, V_star, 1e-9):
            break
        V_star = V_temp

    Q_star = [[sum([get(T, s, a, s_prime)[0]*(get(T, s, a, s_prime)[1] + gamma*V_star[s_prime])
                   for s_prime in range(n)]) for a in range(k)] for s in range(n)]
    pi_star = np.argmax(Q_star, axis=-1)

    return V_star, pi_star


def howardPI(T, gamma, mdpType):

    pass


def linearProgramming(T, gamma, mdpType):
    n, k = len(T), len(T[0])  # numStates, numActions

    problem = lp.LpProblem("mdp", lp.LpMinimize)
    vars = [lp.LpVariable("V"+str(s)) for s in range(n)]

    problem += sum(vars)

    for s in range(n):
        for a in range(k):
            temp = sum([get(T, s, a, s_prime)[0]*(get(T, s, a, s_prime)[1] + gamma*vars[s_prime])
                        for s_prime in range(n)])
            problem += vars[s] >= temp

    problem.solve(lp.PULP_CBC_CMD(msg=0))

    V_star = [var.varValue for var in vars]
    Q_star = [[sum([get(T, s, a, s_prime)[0]*(get(T, s, a, s_prime)[1] + gamma*V_star[s_prime])
                   for s_prime in range(n)]) for a in range(k)] for s in range(n)]
    pi_star = np.argmax(Q_star, axis=-1)

    return V_star, pi_star


class MDP:
    def __init__(self, path):

        with open(path) as f:
            lines = f.read().splitlines()
            self.numStates = int(lines[0].split()[1])
            self.numActions = int(lines[1].split()[1])
            self.endStates = [int(s) for s in lines[2].split()[1:]]

            # transition and reward matrix, N x A x N
            self.T = [[dict() for j in range(self.numActions)]
                      for i in range(self.numStates)]
            self.mdpType = None  # 0 continuing, 1 episodic
            self.gamma = None

            # filling up the matrices and initialising mdpType, gamma
            for l in lines[3:]:
                d = l.split()
                if d[0] == "transition":
                    s = int(d[1])
                    a = int(d[2])
                    s_prime = int(d[3])
                    r = float(d[4])
                    p = float(d[5])
                    self.T[s][a][s_prime] = (p, r)

                elif d[0] == "mdptype":
                    if d[1] == "continuing":
                        self.mdpType = 0
                    else:
                        self.mdpType = 1

                elif d[0] == "discount":
                    self.gamma = float(d[1])

    def runAlgo(self, algorithm):
        if algorithm == "vi":
            V_star, pi_star = valueIteration(self.T, self.gamma)

        elif algorithm == "hpi":
            V_star, pi_star = howardPI(
                self.T, self.gamma, self.mdpType)

        else:
            V_star, pi_star = linearProgramming(
                self.T, self.gamma, self.mdpType)

        # print(V_star)
        # print(pi_star)
        return V_star, pi_star


if __name__ == "__main__":
    # parsing the command line arguments
    args = parser.parse_args()

    path = args.mdp
    algorithm = args.algorithm

    # driver instructions
    mdp = MDP(path)
    V_star, pi_star = mdp.runAlgo(algorithm)
    for v, pi in zip(V_star, pi_star):
        print("{:.6f}\t{}".format(v, pi))
