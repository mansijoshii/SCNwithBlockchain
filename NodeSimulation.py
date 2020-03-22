from Blockchain import Blockchain
from Blockchain import Block


class Node:
    def __init__(self):
        self.number_of_goods = 0
        self.blockchain = Blockchain()
        self.peers = []
        self.blockchain.create_genesis_block()

    def transaction(self, type_of_transaction, type_of_place, count):
        self.blockchain.add_new_transaction(type_of_transaction, type_of_place, count)

    def mine(self):
        self.blockchain.mine()
        self.blockchain.display_chain()


manufacture = Node()
manufacture.transaction("send", "warehouse", 4)
manufacture.transaction("send", "warehouse", 5)
manufacture.mine()

