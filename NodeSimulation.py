from Blockchain import Blockchain
from Blockchain import Block
import copy
import time
import matplotlib.pyplot as plt 

NUM_SIMULATIONS = 10

class Node:
    def __init__(self, xcoord, ycoord):
        self.number_of_goods = 0
        self.blockchain = Blockchain()
        self.peers = []
        self.blockchain.create_genesis_block()
        self.xcoord = xcoord
        self.ycoord = ycoord

    def produce (self, count_of_goods):
        self.number_of_goods += count_of_goods
    
    def transaction(self, type_of_transaction, type_of_person, count_of_goods):
        self.blockchain.add_new_transaction(type_of_transaction, type_of_person, count_of_goods)
        if (type_of_transaction == "send"):
            self.number_of_goods -= count_of_goods
        if (type_of_transaction == "receive"):
            self.number_of_goods += count_of_goods

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


# Creating SCN nodes and specifying their location
manufacturer1 = Node(10, 25)
manufacturer2 = Node(12, 22)

wholesaler1 = Node(25, 76)
wholesaler2 = Node(30, 65)
wholesaler3 = Node(27, 70)

retailer1 = Node(56, 89)
retailer2 = Node(43, 89)

attacker = Node(11, 23)

# Registering Peers
manufacturer1.register_node(manufacturer2)
manufacturer1.register_node(wholesaler1)
manufacturer1.register_node(wholesaler2)
manufacturer1.register_node(wholesaler3)
manufacturer1.register_node(retailer1)
manufacturer1.register_node(retailer2)

# Performing transactions, Mining and Announcing to Peers
# manufacturer1.produce(20)
# manufacturer2.produce(30)
# manufacturer1.transaction("send", "wholesaler2", 4)
# manufacturer1.mine()
# manufacturer2.transaction("send", "wholesaler3", 5)
# manufacturer2.mine()
# print(manufacturer2.number_of_goods)
# manufacturer1.display_chain()

# Measuring Performance
transaction_cnt = []
transaction_time = []
transaction_tps = []
for i in range(NUM_SIMULATIONS):
    print("Running Simulation " + str(i+1))
    cnt = 0
    t1 = time.time()
    t2 = 0
    while 1:
        t2 = time.time()
        if (t2 - t1 >= 0.01 * (i+1)):
            break
        if (cnt % 2 == 0):
            manufacturer1.transaction("send", "wholesaler1", 4)
        elif (cnt % 2 == 1):
            wholesaler1.transaction("send", "retailer1", 4)
        cnt += 1
    t3 = t2-t1
    transaction_cnt.append(cnt)
    transaction_time.append(t3)
    transaction_tps.append(cnt/t3)
    time.sleep(2)

tps = sum(transaction_cnt)/sum(transaction_time)

print("Average throughput over " + str(NUM_SIMULATIONS) + " simulations is " + 
    str(tps) + " transactions per second")

plt.plot(transaction_cnt, transaction_tps)

plt.xlabel('Number of Transactions') 
plt.ylabel('TPS')  
plt.title('Analysis of throughput') 
plt.show() 