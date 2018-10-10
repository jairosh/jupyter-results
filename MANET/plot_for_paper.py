#!/usr/bin/env python3
import argparse
import itertools
import pandas as pd
import matplotlib.pyplot as plt
# from mpl_toolkits.axes_grid1 import AxesGrid
from matplotlib.lines import Line2D

# Black + the default color cycler
COLOR_WHEEL = ['black'] + ['C{}'.format(color) for color in range(10)]
DASHES = [[3, 1],
          [1000, 1],
          [2, 1, 10, 1],
          [4, 1, 1, 1, 1, 1]]
MARKERS = ['.', '+', '^', 'v', '<', '>', 's']
STYLES = list(zip(COLOR_WHEEL, itertools.cycle(MARKERS),
                  itertools.cycle(DASHES)))


def export_legend(labels, outputfile='legend.pgf'):
    """Exports the legend of a certain matplotlib figure into the specified file

    Args:
        legend (matplotlib.legend): The legend object
        outputfile (str, optional): The destination file
    """
    handles = []
    # Create a proxy artist to exract the legend
    fig = plt.figure()
    for index in range(len(labels)):
        style = STYLES[index]
        handles.append(Line2D([], [], color=style[0], marker=style[1],
                              dashes=style[2], fillstyle='none'))
    legend = plt.legend(handles, labels, loc=3, ncol=int(len(labels) / 2) + 1,
                        framealpha=0, frameon=False)
    fig.canvas.draw()
    # fig.patch.set_visible(False)
    plt.gca().axis('off')
    bbox = legend.get_window_extent().transformed(fig.dpi_scale_trans.inverted())
    fig.savefig(outputfile, dpi="figure", bbox_inches=bbox)


def plot_split_dataframe(dataframe, metric, ylabel, outputfile, title=True, size=(6.7, 2)):
    """Plots a dataframe with outliers into two split plots

    Args:
        dataframe (pandas.DataFrame): Description
        metric (str): Description
        ylabel (str): Description
        outputfile (str): Description
        legend (bool, optional): Description
        title (bool, optional): Description
        size (tuple, optional): Description
    """
    plt.style.use('seaborn-deep')
    x_labels = ['[5,25]', '[25,35]', '[35,60]', '[60,120]']
    x_values = ['5,25', '25,35', '35,60', '60, 120']

    # Variables in plot
    columns = [100, 200, 400]
    columns.reverse()
    ncols = len(columns)
    routers = ['Proposed', 'Spray n\' Wait', 'Epidemic', 'PRoPHET', 'SeeR',
               'MaxPROP', 'Epidemic with Oracle']
    x_ticks = [0, 1, 2, 3]

    fig, axes = plt.subplots(nrows=2, ncols=ncols, figsize=size)
    plt.setp(axes[1], xticks=x_ticks, xticklabels=x_labels)
    fig.text(0.44, -0.25, 'Message creation interval (s)', ha='center')
    fig.text(0.01, 0.5, ylabel, va='center', rotation='vertical')

    # Iterate through the subplot and plot in each one
    for subplot in range(ncols):
        network_size = columns.pop()
        if title:
            axes[0, subplot].set_title('n={}'.format(network_size))
        for index, router in enumerate(routers):
            y_data = dataframe.loc[router, network_size].reindex(x_values)
            style = STYLES[index]
            axes[1, subplot].plot(x_ticks, y_data[metric].as_matrix(),
                                  color=style[0], marker=style[1],
                                  dashes=style[2], linewidth=1,
                                  fillstyle='none')
            axes[0, subplot].plot(x_ticks, y_data[metric].as_matrix(),
                                  color=style[0], marker=style[1],
                                  dashes=style[2], linewidth=1,
                                  fillstyle='none')
            axes[1, subplot].set_ylim(0, 700)
            axes[0, subplot].set_ylim(2000, 2500)
            # hide the spines between ax and ax2
            axes[1, subplot].spines['top'].set_visible(False)
            axes[0, subplot].spines['bottom'].set_visible(False)
            axes[0, subplot].xaxis.tick_top()
            axes[0, subplot].tick_params(labeltop='off')  # don't put tick labels at the top
            axes[1, subplot].xaxis.tick_bottom()

            d = .015  # how big to make the diagonal lines in axes coordinates
            # arguments to pass to plot, just so we don't keep repeating them
            kwargs = dict(transform=axes[0, subplot].transAxes, color='k', clip_on=False)
            axes[0, subplot].plot((-d, +d), (-d, +d), **kwargs)        # top-left diagonal
            axes[0, subplot].plot((1 - d, 1 + d), (-d, +d), **kwargs)  # top-right diagonal

            kwargs.update(transform=axes[1, subplot].transAxes)  # switch to the bottom axes
            axes[1, subplot].plot((-d, +d), (1 - d, 1 + d), **kwargs)  # bottom-left diagonal
            axes[1, subplot].plot((1 - d, 1 + d), (1 - d, 1 + d), **kwargs)  # bottom-right diagonal

    plt.subplots_adjust(left=0.1, right=0.9, top=0.9, bottom=0.1, wspace=0.2)
    # Rotate all the ticks in x axis
    for ax in fig.axes:
        plt.sca(ax)
        plt.xticks(rotation=90)
    plt.draw()
    plt.savefig(outputfile, bbox_inches='tight')


def plot_dataframe(dataframe, metric, ylabel, outputfile, legend=True,
                   title=True, size=(6.7, 2)):
    # Visualization options
    # Styles: seaborn-notebook, seaborn-muted, seaborn-darkgrid,
    #         Solarize_Light2, _classic_test, ggplot, classic,
    #         seaborn, seaborn-bright, seaborn-whitegrid, seaborn-paper,
    #         grayscale, seaborn-talk, seaborn-white, seaborn-poster,
    #         fivethirtyeight, seaborn-deep, seaborn-dark-palette, bmh,
    #         fast, seaborn-pastel, seaborn-dark, seaborn-colorblind,
    #         seaborn-ticks, dark_background
    #  ggplot bmh
    plt.style.use('seaborn-deep')
    x_labels = ['[5,25]', '[25,35]', '[35,60]', '[60,120]']
    x_values = ['5,25', '25,35', '35,60', '60, 120']

    # Variables in plot
    columns = [100, 200, 400]
    columns.reverse()
    ncols = len(columns)
    routers = ['Proposed', 'Spray n\' Wait', 'Epidemic', 'PRoPHET', 'SeeR',
               'MaxPROP', 'Epidemic with Oracle']
    x_ticks = [0, 1, 2, 3]

    fig, axes = plt.subplots(nrows=1, ncols=ncols, sharey=True,
                             figsize=(6.7, 2))
    plt.setp(axes, xticks=x_ticks, xticklabels=x_labels)
    fig.text(0.44, -0.10, 'Message creation interval (s)', ha='center')
    fig.text(0.01, 0.5, ylabel, va='center', rotation='vertical')

    # Iterate through the subplot and plot in each one
    for subplot in range(ncols):
        network_size = columns.pop()
        if title:
            axes[subplot].set_title('n={}'.format(network_size))
        for index, router in enumerate(routers):
            y_data = dataframe.loc[router, network_size].reindex(x_values)
            style = STYLES[index]
            axes[subplot].plot(x_ticks, y_data[metric].as_matrix(),
                               color=style[0], marker=style[1],
                               dashes=style[2], linewidth=1,
                               fillstyle='none')

    if legend:
        # axes[2].legend(routers, ncol=int(len(routers) / 2) + 1,
        #               loc='lower center', bbox_to_anchor=(-0.7, -0.7))
        export_legend(routers)
        # export_legend(plt.legend(routers, ncol=int(len(routers) / 2) + 1,
        #                         loc='lower center',
        #                         bbox_to_anchor=(-0.7, -0.7)))

    # Set limits
    # plt.ylim((0, 1))
    plt.subplots_adjust(left=0.1, right=0.9, top=0.9, bottom=0.1, wspace=0.2)
    # Rotate all the ticks in x axis
    #for ax in fig.axes:
    #    plt.sca(ax)
    #    plt.xticks(rotation=90)
    plt.draw()
    plt.savefig(outputfile, bbox_inches='tight')


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
    #plot_metrics(data, variables, ['PDR', 'Latency (s)', 'Overhead Ratio'], 'test.pgf')
    plot_dataframe(data, 'latency_avg', 'Latency (s)', 'latency.pgf', legend=False)
    plot_dataframe(data, 'delivery_prob', 'Packet Delivery Ratio', 'pdr.pgf', legend=False, title=False)    
    plot_dataframe(data, 'overhead_ratio', 'Overhead Ratio', 'or.pgf', legend=False, title=False)
    plot_dataframe(data, 'overhead_ratio', '22222', 'test.pgf', title=False)
    plot_split_dataframe(data, 'overhead_ratio', 'Overhead Ratio', 'overhead.pgf')



if __name__ == '__main__':
    main()
