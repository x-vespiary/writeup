import socket
import networkx as nx
import parse
import sys

from matching.games import StableMarriage

sys.setrecursionlimit(10000)


def solve(inputs):
    cur = 0

    (N, index) = parse.parse("{:d} {:d}", inputs[cur])
    cur += 1
    college_preferences = {}
    student_preferences = {}
    names = []
    for i in range(N):
        xs = list(map(int, inputs[cur].split(" ")))
        cur += 1
        college_preferences[i] = xs
    for i in range(N):
        xs = list(map(int, inputs[cur].split(" ")))
        cur += 1
        student_preferences[i] = xs
    for i in range(N):
        names.append(inputs[cur])
        cur += 1
    game = StableMarriage.create_from_dictionaries(
        student_preferences, college_preferences
    )
    t = game.solve()
    ks = list(t.keys())
    vs = list(t.values())
    pairs = {}
    for i in range(N):
        pairs[vs[i].name] = ks[i].name
    return names[pairs[index]]


client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(("algo.hsctf.com", 4002))
client.settimeout(1)

while True:
    text = ""
    while True:
        try:
            s = client.recv(4096).decode("utf-8")
            if len(s) == 0:
                break
            text += s
        except socket.timeout:
            break

    if len(text) == 0:
        break
    else:
        print(text)

        lines = list(filter(
            lambda line: line.split(" ")[0].isdecimal() or len(line.split(" ")) == 2,
            text.splitlines()
        ))

        if len(lines) > 0:
            cost = solve(lines)

            print("> {}".format(cost))
            client.send("{}\n".format(cost).encode('utf-8'))
