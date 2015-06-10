import time
import logging
import random
import tkinter
import threading
from PIL import Image, ImageDraw, ImageTk
from zocp import ZOCP
import logging

class Philosopher(ZOCP):
    
    def __init__(self, *args, **kwargs):
        super(Philosopher, self).__init__(*args, **kwargs)
        self.topics = []                      # food for thought
        self.register_string("fork1", "", "rs")
        self.register_string("fork2", "", "rs")
        self.register_string("state", "HUNGRY", "re")
        self.start()
        
        # run this actor in a thread
        self.thread = threading.Thread(target=self.run)
        self.thread.daemon = True
        self.thread.start()
    
    def update(self):
        if self.capability["state"]["value"] == "HUNGRY":
            #print("{0}:I need foooooood...{1}".format(self.name(), len(self.topics)))
            if self.capability["fork1"]["value"] == self.name() and\
                self.capability["fork2"]["value"] == self.name():
                    print("{0}:Jay food, eating....{1}".format(self.name(), len(self.topics)))
                    if self.capability["state"]["value"] != "EATING":
                        self.emit_signal("state", "EATING")
        elif self.capability["state"]["value"] == "EATING":
            self.eat()
            if len(self.topics) > 100:
                self.emit_signal("state", "THINKING")
        else:
            if len(self.topics) == 0:
                self.emit_signal("state", "HUNGRY")
            else:
                enlightenment = self.think()
                if enlightenment:
                    print("Eureka:", enlightenment, len(self.topics))

    def think(self):
        topic = self._get_text()            # get a text
        if topic:
            rnd = random.random()           # estimate quality
            if rnd > 0.9999:                # if it is good
                return topic                # return the thought
            else:
                return None                 # else return nothing
        else:
            print("Out of topics, need food for thought")
            
    def eat(self):
        self.topics.append("Blablabla{0}".format(len(self.topics)))
        #time.sleep(0.1)                 # crunch
        
    def on_peer_signaled(self, peer, name, data):
        #print("PHIL SIGNAL:", name, data)
        if name == "TableServant":
            if self.capability["fork1"]["value"] == self.name() and\
                self.capability["fork2"]["value"] == self.name():
                    print("WE CAN EAT")
                    if self.capability["state"]["value"] != "EATING":
                        self.emit_signal("state", "EATING")
            else:
                if self.capability["state"]["value"] == "EATING":
                    self.emit_signal("state", "THINKING")
                print("{0}:Hmmmmm... let me think...{1}".format(self.name(), len(self.topics)))           
                
                
    def on_peer_subscribed(self, peer, name, data):
        if name == "TableServant":
            self.emit_signal("state", "HUNGRY")

    def run(self):
        self._running = True
        t = time.time()
        try:
            reap_at = time.time() + 1/12.
            while self._running:
                timeout = reap_at - time.time()
                if timeout < 0:
                    timeout = 0
                self.run_once(timeout * 1000)
                # set next interval
                reap_at = time.time() + 1/12.
 
                #self._pre_update()
                self.update()
                #self._post_update()
 
                # stats
                #if t + 1 < time.time():
                #    print("{0}: fps: {1}".format(self.name(), 1/((time.time() - t)/self._count)))
                #    t = time.time()
                #    self._count = 0
        except KeyboardInterrupt as e:
            print("Exception: Philosopher:{0}".format(e))
        finally:
            self._running = False
            self.stop()        

    def _get_text(self):
        try:
            return self.topics.pop()
        except IndexError:
            return None


class TableServantActor(ZOCP):

    def __init__(self, *args, **kwargs):
        super(TableServantActor, self).__init__("TableServant", *args, **kwargs)
        self.register_string("fork1", "", "rwe")
        self.register_string("fork2", "", "rwe")
        self.register_string("fork3", "", "rwe")
        self.register_string("fork4", "", "rwe")
        self.register_string("fork5", "", "rwe")
        self.register_string("state1", "", "rws")
        self.register_string("state2", "", "rws")
        self.register_string("state3", "", "rws")
        self.register_string("state4", "", "rws")
        self.register_string("state5", "", "rws")
        self.register_string("request_food", 0, "rws")
        self.start()
        self.philosophers = [
            Philosopher("Thread1"),
            Philosopher("Thread2"),
            Philosopher("Thread3"),
            Philosopher("Thread4"),
            Philosopher("Thread5")
        ]
        self.run()

    def on_peer_enter(self, peer, name, *args, **kwargs):
        print("ENTER", peer, name)
        if name == "Thread1":
            self.signal_subscribe(self.uuid(), "state1", peer, "state")
            self.signal_subscribe(peer, "fork1", self.uuid(), "fork1")
            self.signal_subscribe(peer, "fork2", self.uuid(), "fork2")
        if name == "Thread2":
            self.signal_subscribe(self.uuid(), "state2", peer, "state")
            self.signal_subscribe(peer, "fork1", self.uuid(), "fork2")
            self.signal_subscribe(peer, "fork2", self.uuid(), "fork3")
        if name == "Thread3":
            self.signal_subscribe(self.uuid(), "state3", peer, "state")
            self.signal_subscribe(peer, "fork1", self.uuid(), "fork3")
            self.signal_subscribe(peer, "fork2", self.uuid(), "fork4")
        if name == "Thread4":
            self.signal_subscribe(self.uuid(), "state4", peer, "state")
            self.signal_subscribe(peer, "fork1", self.uuid(), "fork4")
            self.signal_subscribe(peer, "fork2", self.uuid(), "fork5")
        if name == "Thread5":
            self.signal_subscribe(self.uuid(), "state5", peer, "state")
            self.signal_subscribe(peer, "fork1", self.uuid(), "fork5")
            self.signal_subscribe(peer, "fork2", self.uuid(), "fork1")
    
    def on_peer_signaled(self, peer, name, data):
        #print("TABLE SIGNAL:", name, data)
        if name == "Thread1":
            if data[1] == "HUNGRY":
                if not self.capability["fork1"]["value"] and not self.capability["fork2"]["value"]:
                    # forks are available
                    print("TABLE SIGNAL:", self.capability["fork1"])
                    self.emit_signal("fork1", "Thread1")
                    self.emit_signal("fork2", "Thread1")
            if data[1] == "THINKING":
                if self.capability["fork1"]["value"] == "Thread1" and\
                        self.capability["fork1"]["value"] == "Thread1":
                    # forks are released
                    print("TABLE SIGNAL:", self.capability["fork1"])
                    self.emit_signal("fork1", "")
                    self.emit_signal("fork2", "")
        if name == "Thread2":
            if data[1] == "HUNGRY":
                if not self.capability["fork2"]["value"] and not self.capability["fork3"]["value"]:
                    # forks are available
                    self.emit_signal("fork2", "Thread2")
                    self.emit_signal("fork3", "Thread2")
            if data[1] == "THINKING":
                if self.capability["fork2"]["value"] == "Thread2" and\
                        self.capability["fork3"]["value"] == "Thread2":
                    # forks are released
                    print("TABLE SIGNAL:", self.capability["fork1"])
                    self.emit_signal("fork2", "")
                    self.emit_signal("fork3", "")       
        if name == "Thread3":
            if data[1] == "HUNGRY":
                if not self.capability["fork3"]["value"] and not self.capability["fork4"]["value"]:
                    # forks are available
                    self.emit_signal("fork3", "Thread3")
                    self.emit_signal("fork4", "Thread3")
            if data[1] == "THINKING":
                if self.capability["fork3"]["value"] == "Thread3" and\
                        self.capability["fork4"]["value"] == "Thread3":
                    # forks are released
                    print("TABLE SIGNAL:", self.capability["fork1"])
                    self.emit_signal("fork3", "")
                    self.emit_signal("fork4", "")
        if name == "Thread4":
            if data[1] == "HUNGRY":
                if not self.capability["fork4"]["value"] and not self.capability["fork5"]["value"]:
                    # forks are available
                    self.emit_signal("fork4", "Thread4")
                    self.emit_signal("fork5", "Thread4")
            if data[1] == "THINKING":
                if self.capability["fork4"]["value"] == "Thread4" and\
                        self.capability["fork5"]["value"] == "Thread4":
                    # forks are released
                    self.emit_signal("fork4", "")
                    self.emit_signal("fork5", "")
        if name == "Thread5":
            if data[1] == "HUNGRY":
                if not self.capability["fork5"]["value"] and not self.capability["fork1"]["value"]:
                    # forks are available
                    self.emit_signal("fork5", "Thread5")
                    self.emit_signal("fork1", "Thread5")
            if data[1] == "THINKING":
                if self.capability["fork5"]["value"] == "Thread5" and\
                        self.capability["fork1"]["value"] == "Thread5":
                    # forks are released
                    self.emit_signal("fork5", "")
                    self.emit_signal("fork1", "")

    def on_peer_exit(self, peer, name, *args, **kwargs):
        print("EXIT", peer, name)
    
    def update(self):
        # thread 1
        if self.capability["state1"]["value"] == "HUNGRY":
            if not self.capability["fork1"]["value"]:
                self.emit_signal("fork1", "Thread1")
            if self.capability["fork1"]["value"] == "Thread1" and not self.capability["fork2"]["value"]:
                self.emit_signal("fork2", "Thread1")

        # thread 2
        if self.capability["state2"]["value"] == "HUNGRY":
            if not self.capability["fork2"]["value"]:
                self.emit_signal("fork2", "Thread2")
            if self.capability["fork2"]["value"] == "Thread2" and not self.capability["fork3"]["value"]:
                self.emit_signal("fork3", "Thread2")
        # thread 3
        if self.capability["state3"]["value"] == "HUNGRY":
            if not self.capability["fork3"]["value"]:
                self.emit_signal("fork3", "Thread3")
            if self.capability["fork3"]["value"] == "Thread3" and not self.capability["fork4"]["value"]:
                self.emit_signal("fork4", "Thread3")
        # thread 4
        if self.capability["state4"]["value"] == "HUNGRY":
            if not self.capability["fork4"]["value"]:
                self.emit_signal("fork4", "Thread4")
            if self.capability["fork4"]["value"] == "Thread4" and not self.capability["fork5"]["value"]:
                self.emit_signal("fork5", "Thread4")
        # thread 5
        if self.capability["state5"]["value"] == "HUNGRY":
            if not self.capability["fork5"]["value"]:
                self.emit_signal("fork5", "Thread5")
            if self.capability["fork5"]["value"] == "Thread5" and not self.capability["fork1"]["value"]:
                self.emit_signal("fork1", "Thread5")
        
    def stop(self):
        for t in self.philosophers:
            t.stop()
        ZOCP.stop(self)

    def run(self):
        self._running = True
        t = time.time()
        try:
            reap_at = time.time() + 1/120.
            while self._running:
                timeout = reap_at - time.time()
                if timeout < 0:
                    timeout = 0
                self.run_once(timeout * 1000)
                # set next interval
                reap_at = time.time() + 1/120.
 
                #self._pre_update()
                self.update()
                #self._post_update()
 
                # stats
                #if t + 1 < time.time():
                #    print("{0}: fps: {1}".format(self.name(), 1/((time.time() - t)/self._count)))
                #    t = time.time()
                #    self._count = 0
        except KeyboardInterrupt as e:
            print("Exception: TableServant:{0}".format(e))
        finally:
            self._running = False
            self.stop()        

if __name__ == "__main__":
    logger = logging.getLogger("zocp")
    logger.setLevel(logging.INFO)
    logger.addHandler(logging.StreamHandler())
    logger.propagate = False
    ts = TableServantActor()
