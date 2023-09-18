from bts.movement.general import normalise

import agentpy as ap

class Faulty(ap.Agent):
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
        self.opinion = 0.1
        
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


    def update_position(self):
        """
        Updates agent's position using velocity
        """
        self.space.move_by(self, self.vel)