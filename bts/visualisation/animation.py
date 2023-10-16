from matplotlib import animation
from bts.visualisation.colourmaps import YP_CMAP, COLOUR_1, COLOUR_2, COLOUR_3
import matplotlib.patches as patches
import matplotlib.pyplot as plt
import numpy as np

class UpdateAgents:
    def __init__(self, ax, model, results):
        self.model = model
        self.results = results
        self.ax = ax
        # Simulation
        self.opinions = np.array(self.results['opinions'][0])
        self.ax[0].imshow(model.search_space, cmap='binary', vmin=0, vmax=5)
        self.agents = self.ax[0].scatter([], [], s=20, c=[], cmap=YP_CMAP, vmin=0, vmax=1)
        self.ax[0].set_xlim(0, model.p.size)
        self.ax[0].set_ylim(0, model.p.size)
        self.ax[0].tick_params(left = False, right = False , labelleft = False ,
                labelbottom = False, bottom = False)
        # Results
        self.ax[1].text(0.5, 0.9, "Stats", fontsize=26, ha="center") 
        self.time = self.ax[1].text(0.5, 0.85, f"t = {0}", fontsize="large", ha="center")
        self.ax[1].add_patch(patches.Rectangle((0.2, 0.75), 0.05, 0.025, linewidth=1, edgecolor=COLOUR_1, facecolor=COLOUR_1))
        self.decided1num = np.count_nonzero(self.opinions <= 0.1) - self.model.p.faulty_population
        self.decided1text =  self.ax[1].text(0.3, 0.75, f"Decided 1: {self.decided1num}", fontsize="x-large")
        self.ax[1].add_patch(patches.Rectangle((0.2, 0.7), 0.05, 0.025, linewidth=1, edgecolor=COLOUR_3, facecolor=COLOUR_3))
        self.decided2num = np.count_nonzero(self.opinions >= 0.9)
        self.decided2text =  self.ax[1].text(0.3, 0.7, f"Decided 2: {self.decided2num}", fontsize="x-large")
        self.ax[1].tick_params(left = False, right = False , labelleft = False ,
                labelbottom = False, bottom = False)
    
    def __call__(self, frame):
        # Simulation
        self.opinions = np.array(self.results['opinions'][frame])
        xpos = self.results['pos'][frame][0]
        ypos = self.results['pos'][frame][1]
        self.agents.set_offsets(np.stack((xpos, ypos), axis=1))
        self.agents.set_array(self.opinions)
        # Results
        self.time.set_text(f"t = {frame}")
        self.decided1num = np.count_nonzero(self.opinions <= 0.1) - self.model.p.faulty_population
        self.decided1text.set_text(f"Decided 1: {self.decided1num}")
        self.decided2num = np.count_nonzero(self.opinions >= 0.9)
        self.decided2text.set_text(f"Decided 2: {self.decided2num}")
        return self.agents, self.time, self.decided1text, self.decided2text,
        

def animate(model, results):
    fig, ax = plt.subplots(1,2,figsize=(12,7), width_ratios=[5, 2], dpi=75)
    fig.canvas.manager.set_window_title('Simulation')
    ua = UpdateAgents(ax, model, results)
    # Get the animation
    anim = animation.FuncAnimation(fig, ua, frames=len(results.index), blit=True, interval=20, repeat=False)
    plt.show()
    return anim