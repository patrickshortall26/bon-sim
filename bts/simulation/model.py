import agentpy as ap
import numpy as np
import itertools

from bts.movement import flocking, random_walk
from bts.opinion_updating import pooling, dmmd, bayes_bots

from bts.simulation.agent import Agent

MOVEMENT_TYPES = {'flocking' : flocking, 'random_walk' : random_walk}
OPINION_UPDATING_STRATEGIES = {'pooling' : pooling, 'bbots' : bayes_bots, 'dmmd' : dmmd}

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
    """ HELPER METHODS """
    """"""""""""""""""""""""    
    def init_space(self):
        self.search_space = self.create_search_space()
        self.space = ap.Space(self, shape=[self.p.size]*self.p.ndim)

    def create_search_space(self):
        search_space = np.zeros((self.p.size, self.p.size))
        # Amount of boxes needed is space*fill ratio
        nunsafe_spots = int(self.p.size*self.p.fill_ratio)
        # Generate a list of all the possible areas an unsafe spot could be in
        ij_poss_unsafe_spots = [list(range(0,self.p.size,self.p.size//10)), list(range(0,self.p.size,self.p.size//10))]
        poss_unsafe_spots = list(itertools.product(*ij_poss_unsafe_spots))
        # Add in unsafe spots and remove the index from the possible list until all the unsafe spots have been placed
        for _ in range(nunsafe_spots):
            indexes = self.random.choice(poss_unsafe_spots)
            search_space[indexes[0]:indexes[0]+self.p.size//10, indexes[1]:indexes[1]+self.p.size//10] = 1
            poss_unsafe_spots.remove(indexes)
        return search_space

    def add_agents(self):
        self.agents = ap.AgentList(self, self.p.healthy_population+self.p.faulty_population, Agent)
        self.space.add_agents(self.agents, random=True)
        self.agents.setup_pos(self.space)

    def define_subsets(self):
        """
        Define subsets of agents based on if they're healthy, faulty, or granuloma
        """
        self.healthy_agents = self.agents.select(self.agents.type == "Healthy")
        self.faulty_agents = self.agents.select(self.agents.type == "Faulty")
        self.non_granuloma_agents = self.healthy_agents + self.faulty_agents
        self.granuloma_agents = self.agents.select(self.agents.type == "Granuloma")

    def check_consensus(self):
        """
        Check if agents have reached consensus for either option
        """
        opinion_array = np.array(self.healthy_agents.opinion)
        nconsensus_one = np.count_nonzero(opinion_array <= 0.1)
        nconsensus_two = np.count_nonzero(opinion_array >= 0.9)
        if nconsensus_one >= 0.9*len(self.healthy_agents):
            self.stop()
        if nconsensus_two >= 0.9*len(self.healthy_agents):
            self.stop()

    def record_positions(self):
        """
        Record positions of agents
        """
        pos = self.space.positions.values()
        pos = np.array(tuple(pos)).T
        self.record("pos", pos)

    def record_opinions(self):
        """
        Record opinions of agents
        """
        opinions = np.array(self.agents.opinion, dtype=np.float32)
        self.record("opinions", tuple(opinions))

    def record_agent_list_sizes(self):
        h_agents_num = len(self.healthy_agents.select(self.healthy_agents < 0.1))

    """"""""""""""""""""""""
    """  KEY METHODS   """
    """"""""""""""""""""""""
    """ The four methods Agentpy uses to run the model """

    def setup(self):
        """ 
        Initialise the space of the model and the agents in it. 
        This is called once at the beginning of the model
        """
        self.movement_type = MOVEMENT_TYPES[self.p.movement_type]
        self.opinion_updating_strategy = OPINION_UPDATING_STRATEGIES[self.p.opinion_updating_strategy]
        self.init_space()
        self.add_agents()
        self.define_subsets()

    def step(self):
        """ 
        Put anything in here you want each agent to do at each step (e.g. update position)
        """
        self.healthy_agents.faulty_check()
        self.define_subsets()
        self.healthy_agents.update_opinion()
        self.non_granuloma_agents.update_velocity()
        self.granuloma_agents.update_tracking_velocity()
        self.agents.update_position()

    def update(self):
        """
        Put here any data you want to record or checks to terminate the simulation.
        """
        self.record_positions()
        self.record_opinions()
        self.check_consensus()
    
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
    model = Model(parameters)
    simulation = model.run()
    results = simulation.variables.Model
    return model, results

def run_exp(model, parameters, nruns):
    """
    Run many simulations and collect results for each
    """
    sample = ap.Sample(parameters, nruns)
    exp = ap.Experiment(model, sample, record=True)
    results = exp.run(-1)
    return results