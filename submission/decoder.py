import argparse

# adding command line arguments
parser = argparse.ArgumentParser()
parser.add_argument("--value-policy", required=True)
parser.add_argument("--states", required=True)
parser.add_argument("--player-id", required=True, type=int)

if __name__ == "__main__":
    args = parser.parse_args()

    value_policy = args.value_policy
    statefile = args.states
    player = args.player_id

    print(player)

    states = []
    with open(statefile) as f:
        states = f.read().splitlines()

    actions = []
    with open(value_policy) as f:
        actions = [int(line.split()[1]) for line in f.read().splitlines()]

    for i in range(len(states)):
        lst = ['0']*9
        lst[actions[i]] = '1'
        print(states[i], ' '.join(lst))
