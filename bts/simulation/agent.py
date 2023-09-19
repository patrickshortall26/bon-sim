from bts.movement.general import normalise

import agentpy as ap
import numpy as np

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
        self.vel = self.p.speed*normalise(self.model.nprandom.random(self.p.ndim) - 0.5)
        if self.p.healthy_population > 0:
            self.opinion = np.float64(self.model.random.random())
            self.type = "Healthy"
            self.p.healthy_population -= 1
        else:
            self.opinion = 0.1
            self.type = "Faulty"

        
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
            if self.pos[dim] < 30:
                self.vel[dim] += self.p.speed*0.5
            if self.pos[dim] > self.p.size - 30:
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
        faulty_agent = self.model.faulty_agents.select(self.model.faulty_agents.id == self.tracking_id)[0]
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
    def faulty_check(self):
        """
        Check for faulty agents in the vicinity
        """
        if self.model.random.random() <= self.p.faulty_search_rate:
            nbs = self.neighbors(self, distance=self.p.detection_radius)
            if "Granuloma" not in nbs.type and len(nbs) > 0:
                for nb in nbs:
                    if nb.type == "Faulty":
                        if self.model.random.random() <= self.p.detection_rate:
                            self.type = "Granuloma"
                            self.tracking_id = nb.id

    def update_opinion(self):
        """
        Update opinion of agent
        """
        self = self.model.opinion_updating_strategy.update_opinion(self) 