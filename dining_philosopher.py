import time
import logging
import random
import logging
import sphof
from sphof import PhilosopherActor, LeadActor

class MyPhilosopher(PhilosopherActor):
    
    def setup(self):
        self.register_string("chopstick1", "", "rs")
        self.register_string("chopstick2", "", "rs")
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
            if self.get_value("chopstick1") == self.name() and\
                self.get_value("chopstick2") == self.name():
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
        self.register_string("chopstick1", "", "rwe")
        self.register_string("chopstick2", "", "rwe")
        self.register_string("chopstick3", "", "rwe")
        self.register_string("chopstick4", "", "rwe")
        self.register_string("chopstick5", "", "rwe")
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
            self.signal_subscribe(peer, "chopstick1", self.uuid(), "chopstick1")
            self.signal_subscribe(peer, "chopstick2", self.uuid(), "chopstick2")
        if name == "Plato":
            self.signal_subscribe(self.uuid(), "state2", peer, "state")
            self.signal_subscribe(peer, "chopstick1", self.uuid(), "chopstick2")
            self.signal_subscribe(peer, "chopstick2", self.uuid(), "chopstick3")
        if name == "Aristotle":
            self.signal_subscribe(self.uuid(), "state3", peer, "state")
            self.signal_subscribe(peer, "chopstick1", self.uuid(), "chopstick3")
            self.signal_subscribe(peer, "chopstick2", self.uuid(), "chopstick4")
        if name == "Socrates":
            self.signal_subscribe(self.uuid(), "state4", peer, "state")
            self.signal_subscribe(peer, "chopstick1", self.uuid(), "chopstick4")
            self.signal_subscribe(peer, "chopstick2", self.uuid(), "chopstick5")
        if name == "Kant":
            self.signal_subscribe(self.uuid(), "state5", peer, "state")
            self.signal_subscribe(peer, "chopstick1", self.uuid(), "chopstick5")
            self.signal_subscribe(peer, "chopstick2", self.uuid(), "chopstick1")
    
    def on_peer_signaled(self, peer, name, data):
        if name == "Descartes":
            if data[1] == "HUNGRY":
                if not self.get_value("chopstick1") and not self.get_value("chopstick2"):
                    # chopsticks are available
                    self.emit_signal("chopstick1", "Descartes")
                    self.emit_signal("chopstick2", "Descartes")
            if data[1] == "THINKING":
                if self.get_value("chopstick1") == "Descartes" and\
                        self.get_value("chopstick1") == "Descartes":
                    # chopsticks are released
                    self.emit_signal("chopstick1", "")
                    self.emit_signal("chopstick2", "")
        if name == "Plato":
            if data[1] == "HUNGRY":
                if not self.get_value("chopstick2") and not self.get_value("chopstick3"):
                    # chopsticks are available
                    self.emit_signal("chopstick2", "Plato")
                    self.emit_signal("chopstick3", "Plato")
            if data[1] == "THINKING":
                if self.get_value("chopstick2") == "Plato" and\
                        self.get_value("chopstick3") == "Plato":
                    # chopsticks are released
                    self.emit_signal("chopstick2", "")
                    self.emit_signal("chopstick3", "")       
        if name == "Aristotle":
            if data[1] == "HUNGRY":
                if not self.get_value("chopstick3") and not self.get_value("chopstick4"):
                    # chopsticks are available
                    self.emit_signal("chopstick3", "Aristotle")
                    self.emit_signal("chopstick4", "Aristotle")
            if data[1] == "THINKING":
                if self.get_value("chopstick3") == "Aristotle" and\
                        self.get_value("chopstick4") == "Aristotle":
                    # chopsticks are released
                    self.emit_signal("chopstick3", "")
                    self.emit_signal("chopstick4", "")
        if name == "Socrates":
            if data[1] == "HUNGRY":
                if not self.get_value("chopstick4") and not self.get_value("chopstick5"):
                    # chopsticks are available
                    self.emit_signal("chopstick4", "Socrates")
                    self.emit_signal("chopstick5", "Socrates")
            if data[1] == "THINKING":
                if self.get_value("chopstick4") == "Socrates" and\
                        self.get_value("chopstick5") == "Socrates":
                    # chopsticks are released
                    self.emit_signal("chopstick4", "")
                    self.emit_signal("chopstick5", "")
        if name == "Kant":
            if data[1] == "HUNGRY":
                if not self.get_value("chopstick5") and not self.get_value("chopstick1"):
                    # chopsticks are available
                    self.emit_signal("chopstick5", "Kant")
                    self.emit_signal("chopstick1", "Kant")
            if data[1] == "THINKING":
                if self.get_value("chopstick5") == "Kant" and\
                        self.get_value("chopstick1") == "Kant":
                    # chopsticks are released
                    self.emit_signal("chopstick5", "")
                    self.emit_signal("chopstick1", "")

    def on_peer_exit(self, peer, name, *args, **kwargs):
        print("EXIT", peer, name)
    
    def update(self):
        # thread 1
        if self.get_value("state1") == "HUNGRY":
            if not self.get_value("chopstick1"):
                self.emit_signal("chopstick1", "Descartes")
            if self.get_value("chopstick1") == "Descartes" and not self.get_value("chopstick2"):
                self.emit_signal("chopstick2", "Descartes")

        # thread 2
        if self.get_value("state2") == "HUNGRY":
            if not self.get_value("chopstick2"):
                self.emit_signal("chopstick2", "Plato")
            if self.get_value("chopstick2") == "Plato" and not self.get_value("chopstick3"):
                self.emit_signal("chopstick3", "Plato")
        # thread 3
        if self.get_value("state3") == "HUNGRY":
            if not self.get_value("chopstick3"):
                self.emit_signal("chopstick3", "Aristotle")
            if self.get_value("chopstick3") == "Aristotle" and not self.get_value("chopstick4"):
                self.emit_signal("chopstick4", "Aristotle")
        # thread 4
        if self.get_value("state4") == "HUNGRY":
            if not self.get_value("chopstick4"):
                self.emit_signal("chopstick4", "Socrates")
            if self.get_value("chopstick4") == "Socrates" and not self.get_value("chopstick5"):
                self.emit_signal("chopstick5", "Socrates")
        # thread 5
        if self.get_value("state5") == "HUNGRY":
            if not self.get_value("chopstick5"):
                self.emit_signal("chopstick5", "Kant")
            if self.get_value("chopstick5") == "Kant" and not self.get_value("chopstick1"):
                self.emit_signal("chopstick1", "Kant")


if __name__ == "__main__":
    logger = logging.getLogger("zocp")
    logger.setLevel(logging.WARNING)
    logger.addHandler(logging.StreamHandler())
    logger.propagate = False
    w = Waiter("Waiter")
    w.run()
