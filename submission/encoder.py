import numpy as np
import argparse

# adding command line arguments
parser = argparse.ArgumentParser()
parser.add_argument("--policy", required=True)
parser.add_argument("--states", required=True)


def isTerminal(s):
    s = list(s)
    # 1 won, column
    for c in ['1', '2']:
        f = True
        for i in range(3):
            f = True
            for j in range(i, 9, 3):
                f = f and s[j] == c
            if f:
                return int(c)

        # 1 won, rows
        f = True
        for i in range(0, 9, 3):
            f = True
            for j in range(i, i+3):
                f = f and s[j] == c
            if f:
                return int(c)
        # 1 won, diag
        f = True
        for i in range(3):
            f = f and s[4*i] == c
        if f:
            return int(c)

        f = True
        for i in range(2, 8, 2):
            f = f and s[i] == c
        if f:
            return int(c)

    for c in s:
        if c == '0':
            return -1

    return 0


def nextState(s, a, pl):
    if s[a] != '0':
        return '-1'
    else:
        st = list(s)
        st[a] = pl
        return ''.join(st)


if __name__ == "__main__":
    args = parser.parse_args()

    policyfile = args.policy
    statefile = args.states

    states = []
    with open(statefile) as f:
        states = f.read().splitlines()

    numStates = len(states)
    numActions = 9

    state_to_index = {}
    cnt = 0
    for s in states:
        state_to_index[s] = cnt
        cnt += 1

    end_state = numStates
    opp = None
    opponent_dic = {}
    lines = []
    with open(policyfile) as f:
        lines = f.read().splitlines()

    opp = int(lines[0].split()[0])
    for line in lines[1:]:
        lst = line.split()
        opponent_dic[lst[0]] = [float(p) for p in lst[1:]]

    print("numStates", numStates+1)
    print("numActions", numActions)
    print("end", end_state)

    player = 3 - opp

    for s in range(len(states)):
        for a in range(9):
            next = nextState(states[s], a, str(player))
            if next != '-1':
                win = isTerminal(next)
                if win == opp:
                    print("transition", s, a, end_state, 1, 1)
                elif win == player or win == 0:
                    print("transition", s, a, end_state, 0, 1)
                else:
                    end_win = 0
                    end_lose = 0
                    for _a in range(9):
                        pl_next = nextState(next, _a, str(opp))
                        if pl_next != '-1':
                            _win = isTerminal(pl_next)
                            if _win == opp:
                                end_win += opponent_dic[next][_a]
                                # print("transition", s, a, end_state,
                                #       1, opponent_dic[next][_a])
                            elif _win == player or _win == 0:
                                end_lose += opponent_dic[next][_a]
                                # print("transition", s, a, end_state,
                                #       0, opponent_dic[next][_a])
                            else:
                                print("transition", s, a, state_to_index[pl_next],
                                      0, opponent_dic[next][_a])

                    if end_win > 0:
                        print("transition", s, a, end_state,
                              1, end_win)
                    if end_lose > 0:
                        print("transition", s, a, end_state,
                              0, end_lose)
    print("mdptype episodic")
    print("discount 1")
