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
        # Each tile is ten by ten, so 100 tiles in the space, number of black tiles is that times the fill ratio
        num_tiles = 20 # Num tiles in each direction
        nunsafe_spots = int((num_tiles**2)*self.p.fill_ratio)
        tile_side_length = self.p.size//num_tiles
        # Generate a list of all the possible areas an unsafe spot could be in
        ij_poss_unsafe_spots = [list(range(0,self.p.size,tile_side_length)), list(range(0,self.p.size,tile_side_length))]
        poss_unsafe_spots = list(itertools.product(*ij_poss_unsafe_spots))
        # Add in unsafe spots and remove the index from the possible list until all the unsafe spots have been placed
        for _ in range(nunsafe_spots):
            
            indexes = self.random.choice(poss_unsafe_spots)
            search_space[indexes[0]:indexes[0]+tile_side_length, indexes[1]:indexes[1]+tile_side_length] = 1
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
        nconsensus_one = np.count_nonzero(opinion_array >= 0.9)
        nconsensus_two = np.count_nonzero(opinion_array <= 0.1)
        if nconsensus_one >= 0.9*len(self.healthy_agents):
            self.correct_decision = not bool(round(self.p.fill_ratio))
            self.stop()
        if nconsensus_two >= 0.9*len(self.healthy_agents):
            self.correct_decision = bool(round(self.p.fill_ratio))
            self.stop()

    def record_positions(self):
        """
        Record positions of agents
        """
        # Setup agent lists for h1, h2, and undecided
        healthy_h1 = self.healthy_agents.select(self.healthy_agents.opinion >= 0.9)
        healthy_h2 = self.healthy_agents.select(self.healthy_agents.opinion <= 0.1)
        healthy_undecided = self.healthy_agents.select(self.healthy_agents.opinion > 0.1 and self.healthy_agents.opinion < 0.9)

        # Get positions of healthy agents
        healthy_h1_pos = np.array(tuple(   healthy_h1.pos  )).T
        healthy_h2_pos = np.array(tuple(   healthy_h2.pos   )).T
        healthy_undecided_pos = np.array(tuple(   healthy_undecided.pos    )).T

        # Get positions of faulty and tracking agents
        faulty_pos = np.array(tuple(   self.faulty_agents.pos   )).T
        tracking_pos = np.array(tuple(   self.granuloma_agents.pos   )).T

        # Record all the positions 
        self.record("healthy_h1_pos", healthy_h1_pos)
        self.record("healthy_h2_pos", healthy_h2_pos)
        self.record("healthy_undecided_pos", healthy_undecided_pos)
        self.record("faulty_pos", faulty_pos)
        self.record("tracking_pos", tracking_pos)

    def record_numbers(self):
        """
        Record the following three numbers:
        - Number of healthy agents
        - Number of faulty agents
        - Number of tracking agents
        - Number of healthy agents with belief in H1
        - Number of healthy agents with belief in H2
        """
        # First three
        self.record("nHealthy", len(self.healthy_agents))
        self.record("nFaulty", len(self.faulty_agents))
        self.record("nTracking", len(self.granuloma_agents))
        # Last two
        opinion_array = np.array(self.healthy_agents.opinion)
        nconsensus_one = np.count_nonzero(opinion_array >= 0.9)
        nconsensus_two = np.count_nonzero(opinion_array <= 0.1)
        self.record("nH1", nconsensus_one)
        self.record("nH2", nconsensus_two)


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
        self.correct_decision = False
        self.observations = [0,0]

    def step(self):
        """ 
        Put anything in here you want each agent to do at each step (e.g. update position)
        """
        self.granuloma_agents.double_faulty_check()
        self.healthy_agents.faulty_check()
        self.define_subsets()
        self.healthy_agents.update_opinion()
        self.non_granuloma_agents.update_velocity()
        self.granuloma_agents.update_tracking_velocity()
        self.granuloma_agents.update_tracking_time()
        self.agents.update_position()

    def update(self):
        """
        Put here any data you want to record or checks to terminate the simulation.
        """
        if self.p.record_positions:
            self.record_positions()
            self.record_numbers()
        self.check_consensus()
    
    def end(self):
        """ 
        Called at the end of the simulation.
        Put here any metrics you want to save at the end of the model 
        """
        self.report("Correct decision?", self.correct_decision)
        self.report("Time to consensus", self.t)

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
    sample = ap.Sample(parameters, nruns, method='linspace',  randomize=False)
    exp = ap.Experiment(model, sample, record=True, randomize=False)
    results = exp.run(-1, verbose=10)
    return results