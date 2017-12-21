from lnd_rpc import LNDRPC
from time import sleep
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
    if aliases[n.alias] == 1:
        node_ids[n.pub_key] = n.alias.rstrip(' \t\r\n\0') # re_pattern.sub('', n.alias)    
    else:
        node_ids[n.pub_key] = n.pub_key

#re_pattern = re.compile(u'[^\u0000-\uD7FF\uE000-\uFFFF]', re.UNICODE)

j_nodes = []
for n in g.nodes:
    # use alias if unique, otherwise pub_key
    #j_nodes.append({"id": node_ids[n.pub_key], "group":1})
    j_nodes.append({"id": n.pub_key, "group":n.color})

j_edges = []
for e in g.edges:
    #j_edges.append({"source": node_ids[e.node1_pub],
    #                "target": node_ids[e.node2_pub],
    j_edges.append({"source": e.node1_pub,
                    "target": e.node2_pub,
                    "value": int(30/log(e.capacity))})

json_out = {"nodes": j_nodes, "links": j_edges}
print json.dumps(json_out)
