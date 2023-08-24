import agentpy as ap
import numpy as np

from bts.movement import flocking

""""""""""""""""""""
""" Set up model """ 
""""""""""""""""""""

class Agent(ap.Agent):
    """ 
    Class which defines agents and specifies their behaviour in the model
    """

    """"""""""""
    """ INIT """
    """"""""""""

    def setup(self):
        """
        Set up agents
        """
        self.vel = self.model.nprandom.random(self.p.ndim) - 0.5

    def setup_pos(self, space):
        """
        Set up agents initial position in the space
        """
        self.space = space
        self.neighbors = space.neighbors
        self.pos = space.positions[self]

    """"""""""""""""""""""""
    """ HELPER FUNCTIONS """
    """"""""""""""""""""""""

    
    """"""""""""""""""
    """  MOVEMENT  """
    """"""""""""""""""

    def update_velocity(self):
        """
        Update agent's velocity
        """
        self.vel = flocking.update_vel(self)


    def update_position(self):
        """
        Updates agent's position using velocity
        """
        self.space.move_by(self, self.vel)

    """"""""""""""""""
    """  OPINION   """
    """"""""""""""""""

    def update_opinion(self):
        """
        Update opinion of agent
        """

class Model(ap.Model):
    """
    Class which defines the model, specifies what happens at each time step in the model,
    and records data from what goes on in the model. This can then be used for 
    visualisation and analysis.
    """

    """"""""""""""""""""""""
    """ HELPER FUNCTIONS """
    """"""""""""""""""""""""

    def init_space(self):
        """
        Initialise space
        """
        self.space = ap.Space(self, shape=[self.p.size]*self.p.ndim)


    def add_agents(self):
        """
        Add agents to space
        """
        self.agents = ap.AgentList(self, self.p.population, Agent)
        self.space.add_agents(self.agents, random=True)
        self.agents.setup_pos(self.space)

    def record_positions(self):
        """
        Record positions of agents
        """
        # Record agents positions
        pos = self.space.positions.values() # Get agent's positions
        pos = np.array(tuple(pos)).T
        self.record("pos", pos)

    """"""""""""""""""""""""
    """  KEY FUNCTIONS   """
    """"""""""""""""""""""""

    def setup(self):
        """ 
        Initialise the space of the model and the agents in it. 
        This is called once at the beginning of the model
        """
        self.init_space()
        self.add_agents()

    def step(self):
        """ 
        Put anything in here you want each agent to do at each step (e.g. update position)
        """
        self.agents.update_velocity()
        self.agents.update_position()


    def update(self):
        """
        Called at each step but for the model as a whole rather than for each agent.
        Put here any data you want to record or checks to terminate the simulation.
        """
        self.record_positions()
    
    def end(self):
        """ 
        Called at the end of the simulation.
        Put here any metrics you want to save at the end of the model 
        """

""""""""""""""""""
""" Run model """ 
""""""""""""""""""

def run_sim(Model, parameters):
    """ 
    Run a single simulation and collect results
    """
    # Run model and collect results
    model = Model(parameters)
    simulation = model.run()
    results = simulation.variables.Model
    return model, results

def run_exp(model, parameters, runs):
    """
    Run many simulations and collect results for each
    """
    # Get 10 different random seeds 
    sample = ap.Sample(parameters, runs)
    # Run experiment and gather results
    exp = ap.Experiment(model, sample, record=True)
    results = exp.run(-1)
    return results