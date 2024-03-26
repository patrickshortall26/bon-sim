from bts.movement.general import normalise

import agentpy as ap
import numpy as np

def get_true_positive(init_tp, tracking_time, mu):
    """
    Get the true positive rate for a given time having tracked
    """
    true_positive = (init_tp + mu*tracking_time)/(1 + mu*tracking_time)
    return true_positive

def get_false_positive(init_fp, tracking_time, mu):
    """
    Get the true positive rate for a given time having tracked
    """
    false_positive = 1 - ((1 - init_fp + mu*tracking_time)/(1 + mu*tracking_time))
    return false_positive


class Agent(ap.Agent):
    """ 
    Class which defines agents and specifies their behaviour in the model
    """

    """"""""""""
    """ INIT """
    """"""""""""
    def pooling_setup(self):
        """
        Set up agents to pool
        """
        if self.p.healthy_population > 0:
            self.opinion = 0.5
            self.type = "Healthy"
            self.p.healthy_population -= 1
        else:
            self.opinion = 0.05
            self.type = "Faulty"
    
    def dmmd_setup(self):
        """
        Set up agents to follow DMMD strategy
        """
        if self.p.healthy_population > 0:
            if self.p.healthy_population % 2 == 0:
                self.opinion = 0.05
            else:
                self.opinion = 0.95
            self.type = "Healthy"
            self.p.healthy_population -= 1
            self.state = "exploration"
            self.observations = [0, 0]
            self.explore_time = int(self.model.nprandom.exponential(self.p.tau_exploration)) + 1
            self.time_in_state = 0
            self.option_quality = 0
        else:
            self.opinion = 0.05
            self.type = "Faulty"
            self.state = "dissemination"

    def bbots_setup(self):
        """
        Set up agents to pool
        """
        if self.p.healthy_population > 0:
            self.opinion = 0.5
            self.type = "Healthy"
            self.p.healthy_population -= 1
            self.observations = [0, 0]
            self.last_observation = 0.5
            self.time_since_observation = 0
        else:
            self.opinion = 0.05
            self.type = "Faulty"


    def setup(self):
        """
        Set up agents
        """
        setups = {"pooling" : self.pooling_setup, "dmmd" : self.dmmd_setup, 'bbots' : self.bbots_setup}
        self.vel = self.p.speed*normalise(self.model.nprandom.random(self.p.ndim) - 0.5)
        self.time_straight = 0
        self.time_before_turn = int(self.model.nprandom.exponential(self.p.time_period))
        setups[self.p.opinion_updating_strategy]()
            
        
    def setup_pos(self, space):
        """
        Set up agents initial position in the space
        """
        self.space = space
        self.neighbors = space.neighbors
        self.pos = space.positions[self]
    
    """"""""""""""""""
    """  MOVEMENT  """
    """"""""""""""""""
    def avoid_borders(self):
        for dim in range(self.p.ndim):
            if self.pos[dim] < int(self.p.size/20):
                self.vel[dim] += self.p.speed*0.5
            if self.pos[dim] > self.p.size - int(self.p.size/20):
                self.vel[dim] -= self.p.speed*0.5
        self.vel = normalise(self.vel)

    def update_velocity(self):
        """
        Update agent's velocity
        """
        self.vel = self.model.movement_type.update_vel(self)
        self.avoid_borders()
        self.vel *= self.p.speed

    def update_tracking_velocity(self):
        """
        Granuloma agents update their tracking velocity
        """
        # Get faulty agent to be tracked
        faulty_agent = self.model.agents.select(self.model.agents.id == self.tracking_id)[0]
        self.vel = faulty_agent.pos - self.pos
        # Avoid borders and normalise speed
        self.avoid_borders()
        self.vel *= self.p.speed

    def update_position(self):
        """
        Updates agent's position using velocity
        """
        self.space.move_by(self, self.vel)

    """"""""""""""""""
    """  OPINION   """
    """"""""""""""""""
    def update_tracking_time(self):
        self.tracking_time += 1


    def double_faulty_check(self):
        """
        Double check that the faulty agent you're tracking is faulty 
        """
        if self.tracking_time % self.p.double_check_rate == 0:
            # Check the actual status of the agent
            actual_status = self.model.agents.select(self.model.agents.id == self.tracking_id)[0].type
            if actual_status == "Healthy":
                if self.model.random.random() <= (1-get_false_positive(self.p.false_positive, self.tracking_time, self.p.mu)):
                    self.type = "Healthy"
                    self.tracking_id = None
                    self.tracking_time = 0
                    self.vel = -self.vel
            else:
                if self.model.random.random() <= (1-get_true_positive(self.p.true_positive, self.tracking_time, self.p.mu)):
                    self.type = "Healthy"
                    self.tracking_id = None
                    self.tracking_time = 0
                    self.vel = -self.vel

    def faulty_check(self):
        """
        Check for faulty agents in the vicinity
        """
        if self.model.t != 0:
            if self.model.t % self.p.faulty_search_rate == 0:
                nbs = self.neighbors(self, distance=self.p.detection_radius)
                if "Granuloma" not in nbs.type and len(nbs) > 0:
                    for nb in nbs:
                        if self.model.random.random() <= self.p.false_positive and nb.type == "Healthy":
                            self.type = "Granuloma"
                            self.tracking_id = nb.id
                            self.tracking_time = 1
                        if nb.type == "Faulty":
                            if self.model.random.random() <= self.p.true_positive:
                                self.type = "Granuloma"
                                self.tracking_id = nb.id
                                self.tracking_time = 1

    def non_dupe(self):
        """ Check there's not another granuloma agent tracking same 'faulty' agent """
        #for 

    def update_opinion(self):
        """
        Update opinion of agent
        """
        self = self.model.opinion_updating_strategy.update_opinion(self) 