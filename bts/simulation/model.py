import agentpy as ap
import numpy as np

from bts.movement import flocking, random_walk
from bts.opinion_updating import pooling

from bts.simulation.agents.healthy import Healthy
from bts.simulation.agents.faulty import Faulty

MOVEMENT_TYPES = {'flocking' : flocking, 'random_walk' : random_walk}
OPINION_UPDATING_STRATEGIES = {'pooling' : pooling}

""""""""""""""""""""
""" Set up model """ 
""""""""""""""""""""

class Model(ap.Model):
    """
    Class which defines the model, specifies what happens at each time step in the model,
    and records data from what goes on in the model. This can then be used for 
    visualisation and analysis.
    """

    """"""""""""""""""""""""
    """ HELPER FUNCTIONS """
    """"""""""""""""""""""""
    def create_search_space(self, min_size=20, max_size=40):
        """
        Create an array of zeros (safe areas) and ones (unsafe areas)
        Min and max size are the minimum and maximunm side lengths of the unsafe areas
        """
        search_space = np.zeros((self.p.size, self.p.size))
        for _ in range(int(self.p.size/10)):
            # Generate unsafe spot
            unsafe_spot = np.ones([self.random.randint(min_size,max_size)]*self.p.ndim)
            # Pick a random index to put the unsafe spot
            x_spot_index = self.random.randint(0,self.p.size-(1+unsafe_spot.shape[0]))
            y_spot_index = self.random.randint(0,self.p.size-(1+unsafe_spot.shape[0]))
            search_space[y_spot_index:y_spot_index+unsafe_spot.shape[0], x_spot_index:x_spot_index+unsafe_spot.shape[0]] = unsafe_spot
        return search_space


    def init_space(self):
        """
        Initialise space
        """
        self.search_space = self.create_search_space()
        self.space = ap.Space(self, shape=[self.p.size]*self.p.ndim)

    def add_healthy_agents(self):
        """
        Add agents to space
        """
        self.healthy_agents = ap.AgentList(self, self.p.healthy_population, Healthy)
        self.space.add_agents(self.healthy_agents, random=True)
        self.healthy_agents.setup_pos(self.space)

    def add_faulty_agents(self):
        """
        Add agents to space
        """
        self.faulty_agents = ap.AgentList(self, self.p.faulty_population, Faulty)
        self.space.add_agents(self.faulty_agents, random=True)
        self.faulty_agents.setup_pos(self.space)

    def add_agents(self):
        self.add_healthy_agents()
        self.add_faulty_agents()
        self.agents = self.healthy_agents + self.faulty_agents

    def record_positions(self):
        """
        Record positions of agents
        """
        # Record agents positions
        pos = self.space.positions.values() # Get agent's positions
        pos = np.array(tuple(pos)).T
        self.record("pos", pos)

    def record_opinions(self):
        """
        Record opinions of agents
        """
        opinions = np.array(self.agents.opinion, dtype=np.float32)
        self.record("opinions", tuple(opinions))

    """"""""""""""""""""""""
    """  KEY FUNCTIONS   """
    """"""""""""""""""""""""

    def setup(self):
        """ 
        Initialise the space of the model and the agents in it. 
        This is called once at the beginning of the model
        """
        self.movement_type = MOVEMENT_TYPES[self.p.movement_type]
        self.opinion_updating_strategy = OPINION_UPDATING_STRATEGIES[self.p.opinion_updating_strategy]
        self.init_space()
        self.add_agents()

    def step(self):
        """ 
        Put anything in here you want each agent to do at each step (e.g. update position)
        """
        self.agents.update_velocity()
        self.agents.update_position()
        self.healthy_agents.update_opinion()


    def update(self):
        """
        Called at each step but for the model as a whole rather than for each agent.
        Put here any data you want to record or checks to terminate the simulation.
        """
        self.record_positions()
        self.record_opinions()
    
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