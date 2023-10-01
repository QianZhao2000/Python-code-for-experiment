import pandas as pd
import matplotlib.pyplot as plt
import networkx as nx

# Add bidirectional relationship
def add_double_edge(digraph: nx.DiGraph, node1, node2, info=None, relation='relation'):
    digraph.add_edge(node1, node2)
    digraph.add_edge(node2, node1)
    digraph[node2][node1][relation] = info
    digraph[node1][node2][relation] = info

# Add a one-way relationship
def add_edge(digraph: nx.DiGraph, node1, node2, info=None, relation='relation'):
    digraph.add_edge(node1, node2)
    digraph[node1][node2][relation] = info

def get_edges_relation(digraph: nx.DiGraph,relation="relation"):
    result = []
    for one in digraph.edges(data=True):  
        # ('B745103-074211-3645', 'Reproductive system and breast disorders', {'relation': 'had'})
        result.append(one[2][relation])
    return set(result)


def get_relation_edges(digraph: nx.DiGraph,info=None,relation="relation"):
    result = []
    for one in digraph.edges(data=True):
        if (one[2][relation] == info):
            result.append((one[0],one[1]))
    return set(result)


def add_node_attribute(digraph: nx.DiGraph,nodelist,info=None):
    digraph.add_nodes_from(nodelist,attribute=info)


def get_nodes_attribute(digraph: nx.DiGraph):
    result=[]
    for one in digraph.nodes(data=True):
        result.append(one[1]["attribute"])
    return set(result)


def get_attribute_nodes(digraph: nx.DiGraph,info=None):
    result=[]
    for one in digraph.nodes(data=True):
        if(one[1]["attribute"]==info):
            result.append(one[0])
    return set(result)



def get_relation_nodes(digraph: nx.DiGraph,node,info,relation="relation"):
    pnodelist=[]
    web=digraph[node]
    for one in web:
        if web[one][relation]==info:
            pnodelist.append(one)
    return pnodelist




### 1. Build knowledge graph

G = nx.DiGraph()


ae = pd.read_csv('AE.csv')
dm = pd.read_csv('DM.csv')

ae = ae.head(10)
dm = dm.head(5)

# Add nodes and their attributes
add_node_attribute(G, list(ae['STUDYID']), 'Study Identifier')
add_node_attribute(G, list(ae['USUBJID']), 'Unique Subject Identifier')
# add_node_attribute(G, list(ae['AEBODSYS']), 'Body System or Organ Class')
# add_node_attribute(G, list(ae['AEOUT']), 'Outcome of Adverse Event')
# add_node_attribute(G, list(ae['AESEV']), 'Severity/Intensity')
add_node_attribute(G, ['age', 'country'], 'Demographics')

# Add edges
for idx, row in ae.iterrows():
    add_edge(G, row['USUBJID'], row['STUDYID'], 'belongs to')
    # add_edge(G, row['USUBJID'], row['AEBODSYS'], 'had')
    # add_edge(G, row['USUBJID'], row['AEOUT'], 'outcome')
    # add_edge(G, row['USUBJID'], row['AESEV'], 'severity')

for idx, row in dm.iterrows():
    add_double_edge(G, row['USUBJID'], 'age', row['AGE'])
    add_double_edge(G, row['USUBJID'], 'country', row['COUNTRY'])

nx.draw(G, with_labels=True, node_color='r', font_size=10, pos = nx.spring_layout(G))
plt.show()

print("***************Nodes Attributes***************")
#print("All nodes attribues:", get_nodes_attribute(G))
#print("All nodes whose attribute is Study Identifier:", get_attribute_nodes(G, "Study Identifier"))
#print("All nodes whose attribute is Unique Subject Identifier:", get_attribute_nodes(G, "Unique Subject Identifier"))
#print("All nodes whose attribute is Demographics:", get_attribute_nodes(G, 'Demographics'))
print("All nodes information:", G.nodes(data=True),"\n\n")


print("***************Edges Attributes***************")
#print("All edges attributes:", get_edges_relation(G))
#print("All edges whose attribute is USA:", get_relation_edges(G, "USA"))
print("All edges information:", G.edges(data=True), "\n\n")


print("***************Knowledge Base Question Answering***************")
print("The age of the person whose USUBJID is B745103-074211-3645 is:", G['B745103-074211-3645']['age']['relation'])
print("The country of the person whose USUBJID is B745103-074211-3239 is:", G['B745103-074211-3239']['country']['relation'])




key = get_relation_nodes(G, 'age', 26)
print("People whose age is 26?", get_relation_nodes(G, 'age', 26))
print("probability:", 1/len(key))