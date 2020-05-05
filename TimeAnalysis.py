from NodeSimulation import Node
import time
import matplotlib.pyplot as plt

NUM_SIMULATIONS = 10

manufacturer2 = Node(10, 40)
wholesaler2 = Node(50, 65)
manufacturer2.register_node(wholesaler2)

times = []
transaction_cnt = []
for j in range(NUM_SIMULATIONS):
    for i in range(100 * j):
        if (i % 2):
            manufacturer2.transaction("send", "wholesaler1", 4)
        else:
            wholesaler2.transaction("send", "retailer1", 4)
    t1 = time.time()
    manufacturer2.mine()
    wholesaler2.mine()
    t2 = time.time()
    times.append(t2-t1)
    transaction_cnt.append(100*j)

plt.plot(transaction_cnt, times)
plt.xlabel('Number of Transactions') 
plt.ylabel('Mining time')  
plt.title('Graph Of Mining time vs No of Transactions') 
plt.show()