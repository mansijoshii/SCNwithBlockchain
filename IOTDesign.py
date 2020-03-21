import threading
import random
from time import sleep

class good:
    def __init__ (self, id):
        self.good_id = id


class Manufacturer:
    def __init__(self):
        self.num_goods = 0
    def produce(self):
        self.num_goods+=1
        good_produced = good(self.num_goods)
        print("Manufacturer produced good "+ str(good_produced.good_id))
        return good_produced

class Wholesaler:
    def __init__(self):
        self.curr_goods = 0
    def receive(self, good_received):
        self.curr_goods+=1
        print("Wholesaler received good " + str(good_received.good_id))
    def send(self, good_sent):
        self.curr_goods-=1
        print("Wholesaler sent good " + str(good_sent.good_id))


class Retailer:
    def __init__(self):
        self.stock_goods = 0
    def receive(self, good_received):
        self.stock_goods+=1
        print("Retailer received good " + str(good_received.good_id))


man = Manufacturer()
who = Wholesaler()
ret = Retailer()

def manufacture():
    for i in range(5):
        new_good = man.produce()
        stock_of_goods.append(new_good)
        t = random.randint(1,5)
        sleep(t/100)

def begin_chain ():
    cnt_completed = 0
    while (cnt_completed != 5):
        if (len(stock_of_goods) != 0):
            new_good = stock_of_goods.pop(0)
            who.receive(new_good)
            t = random.randint(1,5)
            sleep(t/100)
            who.send(new_good)
            t = random.randint(1,5)
            sleep(t/100)
            ret.receive(new_good)
            cnt_completed += 1

t1 = threading.Thread(target=manufacture)
t2 = threading.Thread(target=begin_chain)
t1.start()
t2.start()
t1.join()
t2.join()
print("Ended")

