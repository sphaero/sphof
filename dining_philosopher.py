import time
import logging
import random
import logging
import sphof
from sphof import PhilosopherActor, LeadActor

class MyPhilosopher(PhilosopherActor):
    
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

    def on_peer_signaled(self, peer, name, data):
        if name == "Waiter":
            if self.get_value("fork1") == self.name() and\
                self.get_value("fork2") == self.name():
                    print("{0}:Jay food, eating....{1}".format(self.name(), len(self.topics)))
                    if self.get_value("state") != "EATING":
                        self.emit_signal("state", "EATING")
            else:
                if self.get_value("state") == "EATING":
                    self.emit_signal("state", "THINKING")
                               
    def on_peer_subscribed(self, peer, name, data):
        if name == "Waiter":
            # when we discover the Waiter we tell him our state
            self.emit_signal("state", "HUNGRY")


class Waiter(LeadActor):

    def setup(self):
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
        self.add_actor(MyPhilosopher("Descartes"))
        self.add_actor(MyPhilosopher("Plato"))
        self.add_actor(MyPhilosopher("Aristotle"))
        self.add_actor(MyPhilosopher("Socrates"))
        self.add_actor(MyPhilosopher("Kant"))

    def on_peer_enter(self, peer, name, *args, **kwargs):
        if name == "Descartes":
            self.signal_subscribe(self.uuid(), "state1", peer, "state")
            self.signal_subscribe(peer, "fork1", self.uuid(), "fork1")
            self.signal_subscribe(peer, "fork2", self.uuid(), "fork2")
        if name == "Plato":
            self.signal_subscribe(self.uuid(), "state2", peer, "state")
            self.signal_subscribe(peer, "fork1", self.uuid(), "fork2")
            self.signal_subscribe(peer, "fork2", self.uuid(), "fork3")
        if name == "Aristotle":
            self.signal_subscribe(self.uuid(), "state3", peer, "state")
            self.signal_subscribe(peer, "fork1", self.uuid(), "fork3")
            self.signal_subscribe(peer, "fork2", self.uuid(), "fork4")
        if name == "Socrates":
            self.signal_subscribe(self.uuid(), "state4", peer, "state")
            self.signal_subscribe(peer, "fork1", self.uuid(), "fork4")
            self.signal_subscribe(peer, "fork2", self.uuid(), "fork5")
        if name == "Kant":
            self.signal_subscribe(self.uuid(), "state5", peer, "state")
            self.signal_subscribe(peer, "fork1", self.uuid(), "fork5")
            self.signal_subscribe(peer, "fork2", self.uuid(), "fork1")
    
    def on_peer_signaled(self, peer, name, data):
        if name == "Descartes":
            if data[1] == "HUNGRY":
                if not self.get_value("fork1") and not self.get_value("fork2"):
                    # forks are available
                    self.emit_signal("fork1", "Descartes")
                    self.emit_signal("fork2", "Descartes")
            if data[1] == "THINKING":
                if self.get_value("fork1") == "Descartes" and\
                        self.get_value("fork1") == "Descartes":
                    # forks are released
                    self.emit_signal("fork1", "")
                    self.emit_signal("fork2", "")
        if name == "Plato":
            if data[1] == "HUNGRY":
                if not self.get_value("fork2") and not self.get_value("fork3"):
                    # forks are available
                    self.emit_signal("fork2", "Plato")
                    self.emit_signal("fork3", "Plato")
            if data[1] == "THINKING":
                if self.get_value("fork2") == "Plato" and\
                        self.get_value("fork3") == "Plato":
                    # forks are released
                    self.emit_signal("fork2", "")
                    self.emit_signal("fork3", "")       
        if name == "Aristotle":
            if data[1] == "HUNGRY":
                if not self.get_value("fork3") and not self.get_value("fork4"):
                    # forks are available
                    self.emit_signal("fork3", "Aristotle")
                    self.emit_signal("fork4", "Aristotle")
            if data[1] == "THINKING":
                if self.get_value("fork3") == "Aristotle" and\
                        self.get_value("fork4") == "Aristotle":
                    # forks are released
                    self.emit_signal("fork3", "")
                    self.emit_signal("fork4", "")
        if name == "Socrates":
            if data[1] == "HUNGRY":
                if not self.get_value("fork4") and not self.get_value("fork5"):
                    # forks are available
                    self.emit_signal("fork4", "Socrates")
                    self.emit_signal("fork5", "Socrates")
            if data[1] == "THINKING":
                if self.get_value("fork4") == "Socrates" and\
                        self.get_value("fork5") == "Socrates":
                    # forks are released
                    self.emit_signal("fork4", "")
                    self.emit_signal("fork5", "")
        if name == "Kant":
            if data[1] == "HUNGRY":
                if not self.get_value("fork5") and not self.get_value("fork1"):
                    # forks are available
                    self.emit_signal("fork5", "Kant")
                    self.emit_signal("fork1", "Kant")
            if data[1] == "THINKING":
                if self.get_value("fork5") == "Kant" and\
                        self.get_value("fork1") == "Kant":
                    # forks are released
                    self.emit_signal("fork5", "")
                    self.emit_signal("fork1", "")

    def on_peer_exit(self, peer, name, *args, **kwargs):
        print("EXIT", peer, name)
    
    def update(self):
        # thread 1
        if self.get_value("state1") == "HUNGRY":
            if not self.get_value("fork1"):
                self.emit_signal("fork1", "Descartes")
            if self.get_value("fork1") == "Descartes" and not self.get_value("fork2"):
                self.emit_signal("fork2", "Descartes")

        # thread 2
        if self.get_value("state2") == "HUNGRY":
            if not self.get_value("fork2"):
                self.emit_signal("fork2", "Plato")
            if self.get_value("fork2") == "Plato" and not self.get_value("fork3"):
                self.emit_signal("fork3", "Plato")
        # thread 3
        if self.get_value("state3") == "HUNGRY":
            if not self.get_value("fork3"):
                self.emit_signal("fork3", "Aristotle")
            if self.get_value("fork3") == "Aristotle" and not self.get_value("fork4"):
                self.emit_signal("fork4", "Aristotle")
        # thread 4
        if self.get_value("state4") == "HUNGRY":
            if not self.get_value("fork4"):
                self.emit_signal("fork4", "Socrates")
            if self.get_value("fork4") == "Socrates" and not self.get_value("fork5"):
                self.emit_signal("fork5", "Socrates")
        # thread 5
        if self.get_value("state5") == "HUNGRY":
            if not self.get_value("fork5"):
                self.emit_signal("fork5", "Kant")
            if self.get_value("fork5") == "Kant" and not self.get_value("fork1"):
                self.emit_signal("fork1", "Kant")


if __name__ == "__main__":
    logger = logging.getLogger("zocp")
    logger.setLevel(logging.WARNING)
    logger.addHandler(logging.StreamHandler())
    logger.propagate = False
    w = Waiter("Waiter")
    w.run()
