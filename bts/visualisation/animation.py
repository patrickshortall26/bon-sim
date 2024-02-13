from matplotlib import animation
from bts.visualisation.colourmaps import YP_CMAP, COLOUR_1, COLOUR_2, COLOUR_3
import matplotlib.patches as patches
import matplotlib.pyplot as plt
import numpy as np

cHEALTHY_UNDECIDED = 'black'
cHEALTHY_H1 = 'blue'
cHEALTHY_H2 = 'orange'
cFAULTY = 'red'
cTRACKING = 'green'

class UpdateAgents:
    def __init__(self, ax, model, results):
        self.model = model
        self.results = results
        self.ax = ax
        # Simulation

        self.ax[0].imshow(model.search_space, cmap='binary', vmin=0, vmax=5)

        self.healthy_undecided_agents = self.ax[0].scatter([], [], s=20, c=cHEALTHY_UNDECIDED)
        self.healthy_h1_agents = self.ax[0].scatter([], [], s=20, c=cHEALTHY_H1)
        self.healthy_h2_agents = self.ax[0].scatter([], [], s=20, c=cHEALTHY_H2)
        self.faulty_agents = self.ax[0].scatter([], [], s=20, c=cFAULTY)
        self.tracking_agents = self.ax[0].scatter([], [], s=20, c=cTRACKING)


        self.ax[0].set_xlim(0, model.p.size)
        self.ax[0].set_ylim(0, model.p.size)
        self.ax[0].tick_params(left = False, right = False , labelleft = False ,
                labelbottom = False, bottom = False)
        
        # Results
        self.ax[1].text(0.5, 0.9, "Stats", fontsize=26, ha="center") 
        self.time = self.ax[1].text(0.5, 0.85, f"t = {0}", fontsize="large", ha="center")

        self.ax[1].add_patch(patches.Rectangle((0.2, 0.75), 0.05, 0.025, linewidth=1, edgecolor=cHEALTHY_H1, facecolor=cHEALTHY_H1))
        self.decided1text =  self.ax[1].text(0.3, 0.75, f"Decided 1: {0}", fontsize="x-large")

        self.ax[1].add_patch(patches.Rectangle((0.2, 0.7), 0.05, 0.025, linewidth=1, edgecolor=cHEALTHY_H2, facecolor=cHEALTHY_H2))
        self.decided2text =  self.ax[1].text(0.3, 0.7, f"Decided 2: {0}", fontsize="x-large")

        self.ax[1].tick_params(left = False, right = False , labelleft = False ,
                labelbottom = False, bottom = False)
    
    def __call__(self, frame):
        # Simulation

        if self.results['nH1'][frame] + self.results['nH2'][frame] != self.results['nHealthy'][frame]:
            xpos = self.results['healthy_undecided_pos'][frame][0]
            ypos = self.results['healthy_undecided_pos'][frame][1]
            self.healthy_undecided_agents.set_offsets(np.stack((xpos, ypos), axis=1))

        if self.results['nH1'][frame] > 0:
            xpos = self.results['healthy_h1_pos'][frame][0]
            ypos = self.results['healthy_h1_pos'][frame][1]
            self.healthy_h1_agents.set_offsets(np.stack((xpos, ypos), axis=1))

        if self.results['nH2'][frame] > 0:
            xpos = self.results['healthy_h2_pos'][frame][0]
            ypos = self.results['healthy_h2_pos'][frame][1]
            self.healthy_h2_agents.set_offsets(np.stack((xpos, ypos), axis=1))

        if self.results['nFaulty'][frame] > 0:
            xpos = self.results['faulty_pos'][frame][0]
            ypos = self.results['faulty_pos'][frame][1]
            self.faulty_agents.set_offsets(np.stack((xpos, ypos), axis=1))

        if self.results['nTracking'][frame] > 0:
            xpos = self.results['tracking_pos'][frame][0]
            ypos = self.results['tracking_pos'][frame][1]
            self.tracking_agents.set_offsets(np.stack((xpos, ypos), axis=1))

        # Results
        self.time.set_text(f"t = {frame}")
        self.decided1text.set_text(f"Decided 1: {self.results['nH1'][frame]}")
        self.decided2text.set_text(f"Decided 2: {self.results['nH2'][frame]}")

        return self.healthy_h1_agents, self.healthy_undecided_agents, self.faulty_agents, self.healthy_h2_agents, self.tracking_agents, self.time, self.decided1text, self.decided2text,
        

def animate(model, results):
    fig, ax = plt.subplots(1,2,figsize=(12,7), width_ratios=[5, 2], dpi=75)
    fig.canvas.manager.set_window_title('Simulation')
    ua = UpdateAgents(ax, model, results)
    # Get the animation
    anim = animation.FuncAnimation(fig, ua, frames=len(results.index), blit=True, interval=20, repeat=True)
    plt.show()
    return anim