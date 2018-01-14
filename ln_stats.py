from lnd_rpc import LNDRPC
from time import sleep, gmtime, strftime
import json
import re
from math import log

l = LNDRPC()

# get graph
g = l.describe_graph()

total_capacity = 0
for e in g.edges:
    total_capacity += e.capacity

channels = len(g.edges)
nodes = len(g.nodes)

# check aliases for uniqueness
aliases = {}
for n in g.nodes:
    if n.alias not in aliases:
        aliases[n.alias] = 1
    else:
        aliases[n.alias] += 1

node_ids = {}
for n in g.nodes:
    # use alias if unique, otherwise pub_key
    if aliases[n.alias] == 1:
        node_ids[n.pub_key] = n.alias.rstrip(' \t\r\n\0')
    else:
        node_ids[n.pub_key] = n.pub_key

j_nodes = []
for n in g.nodes:
    j_nodes.append({"id": node_ids[n.pub_key], "group":n.color})

j_edges = []
for e in g.edges:
    j_edges.append({"source": node_ids[e.node1_pub],
                    "target": node_ids[e.node2_pub],
                    "value": int(50/log(e.capacity))})

json_out = {"nodes": j_nodes, "links": j_edges}
print json.dumps(json_out)

f = open('data.json', 'w')
f.write(json.dumps({'nodes': nodes, 'channels': channels, 'generated': strftime("%Y-%m-%d %H:%M:%S", gmtime())}))
f.close()
