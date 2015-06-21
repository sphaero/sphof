import time
import logging
import random
import logging
import sphof
from sphof import Actor

class Philosopher(Actor):
    
    def __init__(self, *args, **kwargs):
        super(Philosopher, self).__init__(*args, **kwargs)
        self.topics = []                      # food for thought
        self.setup()
        self.start()
        
        # run this actor in a thread
        self.thread = threading.Thread(target=self.run)
        self.thread.daemon = True
        self.thread.start()
    
    def setup(self):
        self.register_string("fork1", "", "rs")
        self.register_string("fork2", "", "rs")
        self.register_string("state", "HUNGRY", "re")

    def update(self):
        if self.get_value("state") == "HUNGRY":
            return
        elif self.get_value("state") == "EATING":
            self.eat()
            if len(self.topics) > 100:
                self.emit_signal("state", "THINKING")
                print("{0}:Hmmmmm... let me think...{1}".format(self.name(), len(self.topics)))
        else:
            if len(self.topics) == 0:
                self.emit_signal("state", "HUNGRY")
                print("{0}:I need foooooood...{1}".format(self.name(), len(self.topics)))
            else:
                enlightenment = self.think()
                if enlightenment:
                    print("{0}:Eureka:{1}".format(self.name(), enlightenment))

    def think(self):
        topic = self._get_text()            # get a text
        if topic:
            rnd = random.random()           # estimate quality
            if rnd > 0.99:                 # if it is good
                return topic                # return the thought
            else:
                return None                 # else return nothing
        else:
            print("{0}:Out of topics, need food for thought".format(self.name()))
            
    def eat(self):
        self.topics.append("Blablabla{0}".format(len(self.topics)))
        #time.sleep(0.1)                 # crunch
        
    def on_peer_signaled(self, peer, name, data):
        #print("PHIL SIGNAL:", name, data)
        if name == "TableServant":
            if self.get_value("fork1") == self.name() and\
                self.get_value("fork2") == self.name():
                    print("{0}:Jay food, eating....{1}".format(self.name(), len(self.topics)))
                    if self.get_value("state") != "EATING":
                        self.emit_signal("state", "EATING")
            else:
                if self.get_value("state") == "EATING":
                    self.emit_signal("state", "THINKING")
                               
                
                
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
                if not self.get_value("fork1") and not self.get_value("fork2"):
                    # forks are available
                    self.emit_signal("fork1", "Thread1")
                    self.emit_signal("fork2", "Thread1")
            if data[1] == "THINKING":
                if self.get_value("fork1") == "Thread1" and\
                        self.get_value("fork1") == "Thread1":
                    # forks are released
                    self.emit_signal("fork1", "")
                    self.emit_signal("fork2", "")
        if name == "Thread2":
            if data[1] == "HUNGRY":
                if not self.get_value("fork2") and not self.get_value("fork3"):
                    # forks are available
                    self.emit_signal("fork2", "Thread2")
                    self.emit_signal("fork3", "Thread2")
            if data[1] == "THINKING":
                if self.get_value("fork2") == "Thread2" and\
                        self.get_value("fork3") == "Thread2":
                    # forks are released
                    self.emit_signal("fork2", "")
                    self.emit_signal("fork3", "")       
        if name == "Thread3":
            if data[1] == "HUNGRY":
                if not self.get_value("fork3") and not self.get_value("fork4"):
                    # forks are available
                    self.emit_signal("fork3", "Thread3")
                    self.emit_signal("fork4", "Thread3")
            if data[1] == "THINKING":
                if self.get_value("fork3") == "Thread3" and\
                        self.get_value("fork4") == "Thread3":
                    # forks are released
                    self.emit_signal("fork3", "")
                    self.emit_signal("fork4", "")
        if name == "Thread4":
            if data[1] == "HUNGRY":
                if not self.get_value("fork4") and not self.get_value("fork5"):
                    # forks are available
                    self.emit_signal("fork4", "Thread4")
                    self.emit_signal("fork5", "Thread4")
            if data[1] == "THINKING":
                if self.get_value("fork4") == "Thread4" and\
                        self.get_value("fork5") == "Thread4":
                    # forks are released
                    self.emit_signal("fork4", "")
                    self.emit_signal("fork5", "")
        if name == "Thread5":
            if data[1] == "HUNGRY":
                if not self.get_value("fork5") and not self.get_value("fork1"):
                    # forks are available
                    self.emit_signal("fork5", "Thread5")
                    self.emit_signal("fork1", "Thread5")
            if data[1] == "THINKING":
                if self.get_value("fork5") == "Thread5" and\
                        self.get_value("fork1") == "Thread5":
                    # forks are released
                    self.emit_signal("fork5", "")
                    self.emit_signal("fork1", "")

    def on_peer_exit(self, peer, name, *args, **kwargs):
        print("EXIT", peer, name)
    
    def update(self):
        # thread 1
        if self.get_value("state1") == "HUNGRY":
            if not self.get_value("fork1"):
                self.emit_signal("fork1", "Thread1")
            if self.get_value("fork1") == "Thread1" and not self.get_value("fork2"):
                self.emit_signal("fork2", "Thread1")

        # thread 2
        if self.get_value("state2") == "HUNGRY":
            if not self.get_value("fork2"):
                self.emit_signal("fork2", "Thread2")
            if self.get_value("fork2") == "Thread2" and not self.get_value("fork3"):
                self.emit_signal("fork3", "Thread2")
        # thread 3
        if self.get_value("state3") == "HUNGRY":
            if not self.get_value("fork3"):
                self.emit_signal("fork3", "Thread3")
            if self.get_value("fork3") == "Thread3" and not self.get_value("fork4"):
                self.emit_signal("fork4", "Thread3")
        # thread 4
        if self.get_value("state4") == "HUNGRY":
            if not self.get_value("fork4"):
                self.emit_signal("fork4", "Thread4")
            if self.get_value("fork4") == "Thread4" and not self.get_value("fork5"):
                self.emit_signal("fork5", "Thread4")
        # thread 5
        if self.get_value("state5") == "HUNGRY":
            if not self.get_value("fork5"):
                self.emit_signal("fork5", "Thread5")
            if self.get_value("fork5") == "Thread5" and not self.get_value("fork1"):
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
