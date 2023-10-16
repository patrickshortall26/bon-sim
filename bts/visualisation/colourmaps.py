from matplotlib.colors import LinearSegmentedColormap
import numpy as np

COLOUR_1 = np.array((222, 0, 222))/255
COLOUR_2 = np.array((247, 154, 5))/255
COLOUR_3 = np.array((3, 207, 252))/255

colors = [tuple(COLOUR_1), tuple(COLOUR_2), tuple(COLOUR_3)]
cmap_name = 'yp_cmap'
# Create the colormap
YP_CMAP = LinearSegmentedColormap.from_list(cmap_name, colors, N=100)