Philosopher Actor classes
-------------------------

The Philosopher Actor classes provide classes with methods for the 
Dining Philosophers Problem from test 2. 

PhilosopherActor class
######################
.. autoclass:: sphof.PhilosopherActor
    :member-order: groupwise
    :members: setup, update, draw, think, eat, register_string, emit_signal, signal_subscribe, on_peer_enter
    :show-inheritance:

LonePhilosopherActor class
##########################
.. autoclass:: sphof.LonePhilosopherActor
    :members: setup, update, draw, think, eat
    :show-inheritance:
