import socket
import networkx as nx
import parse


def solve(inputs):
    i = 0

    (N, M, K, L) = parse.parse("{:d} {:d} {:d} {:d}", inputs[i])
    i += 1

    G = nx.DiGraph()

    for _ in range(M):
        (U, V, I, F) = parse.parse("{:d} {:d} {:d} {:d}", inputs[i])
        i += 1
        G.add_edge(U, V, weight=I, capacity=F)

    for _ in range(K):
        (U, P) = parse.parse("{:d} {:d}", inputs[i])
        i += 1
        G.add_edge("s", U, weight=0, capacity=P)

    flow = 0
    for _ in range(L):
        (U, C) = parse.parse("{:d} {:d}", inputs[i])
        i += 1
        G.add_edge(U, "t", weight=0, capacity=C)
        flow += C

    G.add_node("s", demand=-flow)
    G.add_node("t", demand=flow)

    return nx.min_cost_flow_cost(G)


client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(("algo.hsctf.com", 4001))
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
            lambda line: line.split(" ")[0].isdecimal(),
            text.splitlines()
        ))

        if len(lines) > 0:
            cost = solve(lines)

            print("> {}".format(cost))
            client.send("{}\n".format(cost).encode('utf-8'))
