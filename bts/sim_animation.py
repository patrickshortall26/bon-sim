from typing import Any
from matplotlib import animation
import matplotlib.pyplot as plt


class UpdateAgents:
    def __init__(self, ax, model, results):
        self.results = results
        self.ax = ax
        self.agents, = self.ax.plot([], [], 'o', markersize=3)
        self.ax.set_xlim(0, model.p.size)
        self.ax.set_ylim(0, model.p.size)
        self.ax.tick_params(left = False, right = False , labelleft = False ,
                labelbottom = False, bottom = False)
    
    def __call__(self, frame):
        xpos = self.results['pos'][frame][0]
        ypos = self.results['pos'][frame][1]
        self.agents.set_data(xpos, ypos)
        return self.agents,
        

def animate(model, results):
    fig, ax = plt.subplots(figsize=(7,7))
    ua = UpdateAgents(ax, model, results)
    # Get the animation
    anim = animation.FuncAnimation(fig, ua, frames=len(results.index), blit=True, interval=20, repeat=True)
    plt.show()
    return anim