import numpy as np
import argparse
import pulp as lp

# adding command line arguments
parser = argparse.ArgumentParser()
parser.add_argument("--mdp", required=True,
                    help="path to the input MDP file")
parser.add_argument("--algorithm", default="vi",
                    help="either vi, hpi or lp algorithm")

np.random.seed(0)


def checkPrecision(a, b, lim):
    sub = np.abs(a - b)
    if np.any(sub >= lim):
        return False
    else:
        return True


def valueIteration(T, gamma, mdpType, endStates):
    n, k = len(T), len(T[0])  # numStates, numActions

    V_star = np.zeros(n, dtype=float)
    pi_star = np.zeros(n)

    while True:
        V_temp = np.zeros(n)
        for s in range(n):
            V_temp[s] = max([sum([p*(r + gamma*V_star[s_prime])
                            for (s_prime, p, r) in T[s][a]]) for a in range(k)])
        if checkPrecision(V_temp, V_star, 1e-9):
            break
        V_star = V_temp.copy()

    Q_star = [[sum([p*(r + gamma*V_star[s_prime]) for (s_prime, p, r) in T[s][a]])
               for a in range(k)] for s in range(n)]
    pi_star = np.argmax(Q_star, axis=-1)

    if mdpType:
        for s in endStates:
            V_star[s] = 0

    return V_star, pi_star


def howardPI(T, gamma, mdpType, endStates):
    n, k = len(T), len(T[0])  # numStates, numActions

    V_star = np.zeros(n)
    pi_star = np.random.choice(np.arange(k), n)
    while True:
        # calculating V using Bellman Equations
        A = np.zeros((n, n))
        B = np.zeros(n)
        for s in range(n):
            for (s_prime, p, r) in T[s][pi_star[s]]:
                A[s][s_prime] = p
                B[s] += p*r
        A = gamma * A - np.eye(n)
        B = -1 * B

        if mdpType:
            A = np.delete(A, endStates, 0)
            A = np.delete(A, endStates, 1)
            B = np.delete(B, endStates, 0)

        V_star = np.linalg.solve(A, B)
        V = np.zeros(n)
        write = 0
        for i in range(n):
            if i not in endStates:
                V[i] = V_star[write]
                write += 1
        V_star = V

        # computing Q_star and new policy values to check
        Q_star = [[sum([p*(r + gamma*V_star[s_prime]) for (s_prime, p, r) in T[s][a]])
                   for a in range(k)] for s in range(n)]
        pi = np.argmax(Q_star, axis=1)
        if np.all(pi == pi_star):
            break
        pi_star = pi

    return V_star, pi_star


def linearProgramming(T, gamma, mdpType, endStates):
    n, k = len(T), len(T[0])  # numStates, numActions

    problem = lp.LpProblem("mdp", lp.LpMinimize)
    vars = [lp.LpVariable("V"+str(s)) for s in range(n)]

    problem += sum(vars)

    for s in range(n):
        if s in endStates:
            problem += vars[s] == 0
            continue

        for a in range(k):
            temp = sum([p*(r + gamma*vars[s_prime])
                        for (s_prime, p, r) in T[s][a]])
            problem += vars[s] >= temp

    problem.solve(lp.PULP_CBC_CMD(msg=0))

    V_star = [var.varValue for var in vars]
    Q_star = [[sum([p*(r + gamma*V_star[s_prime]) for (s_prime, p, r) in T[s][a]])
               for a in range(k)] for s in range(n)]
    pi_star = np.argmax(Q_star, axis=-1)

    if mdpType:
        for s in endStates:
            V_star[s] = 0

    return V_star, pi_star


class MDP:
    def __init__(self, path):

        with open(path) as f:
            lines = f.read().splitlines()
            self.numStates = int(lines[0].split()[1])
            self.numActions = int(lines[1].split()[1])
            self.endStates = [int(s) for s in lines[2].split()[1:]]

            # transition and reward matrix, N x A x N
            self.T = [[list() for j in range(self.numActions)]
                      for i in range(self.numStates)]
            self.mdpType = None  # 0 continuing, 1 episodic
            self.gamma = None

            for l in lines[3:]:
                d = l.split()
                if d[0] == "transition":
                    s = int(d[1])
                    a = int(d[2])
                    s_prime = int(d[3])
                    r = float(d[4])
                    p = float(d[5])
                    self.T[s][a].append((s_prime, p, r))

                elif d[0] == "mdptype":
                    if d[1] == "continuing":
                        self.mdpType = 0
                    else:
                        self.mdpType = 1

                elif d[0] == "discount":
                    self.gamma = float(d[1])

    def runAlgo(self, algorithm):
        if algorithm == "vi":
            return valueIteration(self.T, self.gamma, self.mdpType, self.endStates)

        elif algorithm == "hpi":
            return howardPI(self.T, self.gamma, self.mdpType, self.endStates)

        else:
            return linearProgramming(self.T, self.gamma, self.mdpType, self.endStates)


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
