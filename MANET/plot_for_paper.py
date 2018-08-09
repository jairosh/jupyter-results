#!/usr/bin/env python3
import argparse
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
# from mpl_toolkits.axes_grid1 import AxesGrid
from matplotlib.lines import Line2D

COLOR_WHEEL = ['#329932',
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
DASHES = [[3, 1],
          [1000, 1],
          [2, 1, 10, 1],
          [4, 1, 1, 1, 1, 1]]


def main():
    """Main function
    """
    parser = argparse.ArgumentParser()
    parser.add_argument('-c', '--csv', help='CSV file to plot results from',
                        type=str, required=True)
    args = parser.parse_args()
    # Load the results
    try:
        dataframe = pd.read_csv(args.csv)
    except Exception as err:
        print('Error processing file ' + repr(err))
        exit(1)

    # Filter out the unnecesary data
    # Fix the buffer size to 50MB
    dataframe = dataframe[dataframe.buffer_size == 150]
    # Discard results for 800 and 1000
    dataframe = dataframe[dataframe.nodes <= 600]

    groups = ['router', 'nodes', 'message_interval']
    points = dataframe.groupby(by=groups).mean()
    error = dataframe.groupby(by=groups).sem() * 1.96

    variables = ['delivery_prob', 'latency_avg', 'overhead_ratio']
    data = points[variables].join(error[variables], rsuffix='_err')

    # Visualization options
    # Styles: seaborn-notebook, seaborn-muted, seaborn-darkgrid,
    #         Solarize_Light2, _classic_test, ggplot, classic,
    #         seaborn, seaborn-bright, seaborn-whitegrid, seaborn-paper,
    #         grayscale, seaborn-talk, seaborn-white, seaborn-poster,
    #         fivethirtyeight, seaborn-deep, seaborn-dark-palette, bmh,
    #         fast, seaborn-pastel, seaborn-dark, seaborn-colorblind,
    #         seaborn-ticks, dark_background
    #  ggplot bmh
    plt.style.use('bmh')
    # Linestyles
    # : (·········)
    # -. (-·-·-·-·)
    # -- (--------)
    # -  (solid line)

    linestyles = ['b.-', 'r+--', 'g^-.', 'yv:', 'kx-', 'cs:', 'm<:']
    x_labels = ['[5,25]', '[25,35]', '[35,60]', '[60,120]']
    x_values = ['5,25', '25,35', '35,60', '60, 120']

    # Variables in plot
    columns = [100, 200, 400]
    columns.reverse()
    ncols = len(columns)
    routers = ['Proposed', 'Spray n\' Wait', 'Epidemic', 'PRoPHET', 'SeeR',
               'MaxPROP', 'Epidemic with Oracle']
    x_ticks = [0, 1, 2, 3]

    fig, axes = plt.subplots(nrows=1, ncols=ncols, sharey=True, figsize=(6.7, 2.25))
    plt.setp(axes, xticks=x_ticks, xticklabels=x_labels)
    fig.text(0.44, -0.2, 'Message creation interval (s)', ha='center')
    fig.text(0.0, 0.5, 'Packet Delivery Ratio', va='center',
             rotation='vertical')

    # Iterate through the subplot and plot in each one
    for subplot in range(ncols):
        network_size = columns.pop()
        axes[subplot].set_title('n={}'.format(network_size))
        for index, router in enumerate(routers):
            y_data = data.loc[router, network_size].reindex(x_values)
            axes[subplot].plot(x_ticks, y_data['delivery_prob'].as_matrix(),
                               linestyles[index], linewidth=1,
                               fillstyle='none')

    axes[2].legend(routers, ncol=int(len(routers) / 2) + 1, loc='lower center',
                   bbox_to_anchor=(-0.7, -0.7))
    plt.ylim((0, 1))
    plt.subplots_adjust(left=0.1, right=0.9, top=0.9, bottom=0.1, wspace=0.2)
    for ax in fig.axes:
        plt.sca(ax)
        plt.xticks(rotation=90)
    plt.draw()
    plt.savefig('test.pgf', bbox_inches='tight')
    plt.show()


if __name__ == '__main__':
    main()
