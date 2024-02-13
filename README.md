# CP-Sim

THINGS YOU (ME) WILL FORGET 

H1 = White -> opinion closer to 1
H2 = Black -> opinion closer to 0

Opinion = Value representing an agent's belief in the correct hypothesis

SProdOp
Opinion is continuous, but bounded between 0.05 and 0.95, if the result of pooling or evidential updating produces a number outside of these bounds, it is changed back to the closest bound. i.e. an agent who pools with neighbours resulting in an opinion of 0.01 would change it's opinion to 0.05

BBots
Opinion is discrete, can either be 0.05, 0.5, or 0.95:
0.05 - Agent is decided on H2
0.5 - Agent is undecided
0.95 - Agent is decided on H1

DMMD
Opinion is discrete, can either be 0.05 or 0.95:
0.05 - Agent is decided on H2
0.95 - Agent is decided on H1

Belief = An opinion which is above 0.9 or below 0.1, which then corresponds to an agent being confident in either of the two states

For example, an agent in SProdOp with an opinion of 0.91 can be said to have a belief in H1.