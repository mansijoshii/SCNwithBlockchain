from NodeSimulation import Node
import time
import matplotlib.pyplot as plt

NUM_SIMULATIONS = 10

manufacturer1 = Node(10, 25)
wholesaler1 = Node(25, 76)
retailer1 = Node(56, 89)

# Registering Peers
manufacturer1.register_node(wholesaler1)
manufacturer1.register_node(retailer1)

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
        if (cnt % 3 == 0):
            manufacturer1.transaction("send", "wholesaler1", 4)

        elif (cnt % 3 == 1):
            wholesaler1.transaction("send", "retailer1", 4)
 
        else:
            retailer1.transaction("receive", "wholesaler1", 4)
      
        cnt += 1
    t3 = t2-t1
    transaction_cnt.append(cnt)
    transaction_time.append(t3)
    transaction_tps.append(cnt/t3)
    manufacturer1.mine()
    # time.sleep(2)
    
tps = sum(transaction_cnt)/sum(transaction_time)

print("Average throughput over " + str(NUM_SIMULATIONS) + " simulations is " + 
    str(tps) + " transactions per second")

plt.plot(transaction_cnt, transaction_tps)
plt.xlabel('Number of Transactions') 
plt.ylabel('TPS')  
plt.title('Analysis of throughput') 
plt.show()

