import hashlib


class merkleNode:
    def __init__(self, data, left, right) -> None:
        self.data = data
        self.left = left
        self.right = right


class merkleTree:
    def __init__(self) -> None:
        self.merkleRoot = None

    def create(self, transactions) -> None:
        leafNodes = []
        for transaction in transactions:
            leafNode = merkleNode(transaction.getTransactionHash(), None, None)
            leafNodes.append(leafNode)
        self.merkleRoot = self.buildTree(leafNodes)
        return self.merkleRoot

    def buildTree(self, nodes):
        size = len(nodes)

        if (size == 1):
            return nodes[0]
        if (size % 2):
            nodes.append(nodes[size-1])

        newNodes = []
        i = 0
        while (i < size):
            node = merkleNode(hashlib.sha256((
                str(nodes[i].data) + str(nodes[i+1].data)).encode('utf-8')).hexdigest(), nodes[i], nodes[i+1])
            newNodes.append(node)
            i += 2
        return self.buildTree(newNodes)
