my_seq = [2, 1, 3, 2, 1, 3, 0, 7, 3, 5, 0, 1, 4, 2, 1, 0]
# my_seq = [0, 7, 2, 1, 8, 0, 1, 3]

tree = []


def create_tree(tree, seq, depth):
    if depth <= 0:
        tree.append(seq.pop())
        tree.append(seq.pop())
        return
    tree.append([])
    tree.append([])
    depth -= 1
    for i in tree:
        create_tree(i, seq, depth)


create_tree(tree, my_seq, 3)
print(tree)


# tree = [[0,1],[1,0]]
pos=0
bestNode = None
bestValue = 0

def recurse(node):
    global bestNode
    global bestValue
    if is_leaf(node):
        v = node[pos]
        if v > bestValue:
            bestValue = v
            bestNode = node
        return
    for child in node:
        recurse(child)
    return bestNode

def is_leaf(node):
    t = [i for i in node if type(i) == int]
    res = any(t)
    return res

shit = [recurse(tree[0]), recurse(tree[1])]
ind = max(shit, key=lambda x: x[pos])
bestMove= [tree[0], tree[1]][shit.index(ind)]

print(bestMove)
