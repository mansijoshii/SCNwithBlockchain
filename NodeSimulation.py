from Blockchain import Blockchain
from Blockchain import Block
import copy

class Node:
    def __init__(self):
        self.number_of_goods = 0
        self.blockchain = Blockchain()
        self.peers = []
        self.blockchain.create_genesis_block()

    def transaction(self, type_of_transaction, type_of_place, count):
        self.blockchain.add_new_transaction(type_of_transaction, type_of_place, count)

    def mine(self):
        self.blockchain.mine_and_announce(self.peers)
        
    def register_node(self, other_node):
        other_node.blockchain = copy.deepcopy(self.blockchain)
        for peer in self.peers:
            other_node.peers.append(peer)
        other_node.peers.append(self)
        self.peers.append(other_node)
        

    def display_chain(self):
        self.blockchain.display_chain()


#Creating a node and adding its transactions to the blockchain
manufacture = Node()
manufacture.transaction("send", "warehouse", 4)
manufacture.transaction("send", "warehouse", 5)
manufacture.mine()
#manufacture.display_chain()

#Registering another node with the pre-existing blockchain
retailer = Node()
manufacture.register_node(retailer)
#retailer.display_chain()

#Mining and announcing the transaction to node's peers
retailer.transaction("recieve", "warehouse", 23)
retailer.mine()
#retailer.display_chain()
#manufacture.display_chain()

retailer.transaction("recieve", "warehouse", 344)
retailer.mine()
#manufacture.display_chain()

wholesaler = Node()
retailer.register_node(wholesaler)
wholesaler.display_chain()
