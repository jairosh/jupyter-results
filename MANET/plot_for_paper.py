#!/usr/bin/env python3
import pandas as pd
import matplotlib.pyplot as plt
from mpl_toolkits.axes_grid1 import AxesGrid

colourWheel = ['#329932',
               '#ff6961',
               'b',
               '#6a3d9a',
               '#fb9a99',
               '#e31a1c',
               '#fdbf6f',
               '#ff7f00',
               '#cab2d6',
               '#6a3d9a',
               '#ffff99',
               '#b15928',
               '#67001f',
               '#b2182b',
               '#d6604d',
               '#f4a582',
               '#fddbc7',
               '#f7f7f7',
               '#d1e5f0',
               '#92c5de',
               '#4393c3',
               '#2166ac',
               '#053061']
dashesStyles = [[3, 1],
                [1000, 1],
                [2, 1, 10, 1],
                [4, 1, 1, 1, 1, 1]]

# Load the results
df = pd.read_csv('results.csv')

# Filter out the unnecesary data
# Fix the buffer size to 50MB
df = df[df.buffer_size == 50]
# Discard results for 800 and 1000
df = df[df.nodes <= 600]

points = df.groupby(by=['router', 'nodes', 'message_interval']).mean()
error = df.groupby(by=['router', 'nodes', 'message_interval']).sem() * 1.96

data = points[['delivery_prob', 'latency_avg', 'overhead_ratio', 'speed_avg']].join(error[['delivery_prob', 'latency_avg', 'overhead_ratio', 'speed_avg']], rsuffix='_err')

# fig, ax = plt.subplots(ncols=4)
fig, axes = plt.subplots(nrows=1, ncols=4, sharey=True)
nodes = [100, 200, 400, 600]
nodes.reverse()
x = ['5,25', '25,35', '35,60', '60, 120']
styles = ['b.-', 'r+--', 'g^-.', 'yv:', 'ks-', 'c*:']
routers = ['BFGMP', 'SprayAndWait', 'Epidemic', 'Prophet', 'Seer']
plt.setp(axes, xticks=[0, 1, 2, 3], xticklabels=x)
fig.text(0.5, 0.04, 'Message creation interval (s)', ha='center')
fig.text(0.04, 0.5, 'Packet Delivery Ratio', va='center', rotation='vertical')
for subp in range(4):
    n = nodes.pop()
    axes[subp].set_title('n={}'.format(n))
    for idx, router in enumerate(routers):
        y = data.loc[router, n].reindex(x)
        axes[subp].plot([0, 1, 2, 3], y['delivery_prob'].as_matrix(), styles[idx])

plt.legend(routers)
plt.draw()
plt.show()
