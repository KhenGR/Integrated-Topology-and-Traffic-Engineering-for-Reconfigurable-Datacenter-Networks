import json
import os
import matplotlib.pyplot as plt
import matplotlib.lines as mlines
from src.evaluation_Functions import *

# This will print headlines in the figures if true
PAPER_MODE = True


# #some simple functions used to plot  a theortic figure
# def dct_da_cont(v, rc):
#     """The DCT of the DA system in v permutations and rc reconfiguration"""
#     return 1 + v * rc


def plot_figure_flow_numbers_thru(data_file_path, fig_path=None):
    """
    This plots figure
    :param data_file_path:
    :param fig_path:
    :return:
    """
    file_path_flow_numbers = data_file_path
    with open(file_path_flow_numbers, 'r') as file:
        full_results = json.load(file)

    x_values = full_results["parameters"]["List_of_tested_vals"]
    results = full_results["mean_res"]
    name_list = ("BvN-sys", "RR-sys", "COMP-sys")
    marker_list = ('D', '^', 'o')
    color_list = ('#2ca02c', '#ff7f0e', '#1f77b4')
    for i, row in enumerate(np.transpose(results)):
        plt.plot(x_values, 1 / row, label=f'{name_list[i]}', marker=marker_list[i],
                 linestyle='-', linewidth=2, color=color_list[i])

    plt.xscale('log')
    # Add labels and title
    plt.xlabel(r'Total flows ($n_{f}$)')
    plt.ylabel('Throughput')
    if PAPER_MODE is True:
        plt.title('Figure 4(a)')
    plt.legend()
    if fig_path is not None:
        full_fig_path = os.path.join(fig_path, "figure_flow_numbers_thru.png")
        plt.savefig(full_fig_path)
    plt.show()


def plot_figure_four_flow_numbers_matrix_measure(data_file_path, fig_path=None):
    with open(data_file_path, 'r') as file:
        full_results = json.load(file)
    bvn_res = list(full_results["BvN_dist_mean"] / np.max(full_results["BvN_dist_mean"]))
    x_values = full_results["parameters"]["List_of_tested_vals"]
    results = [full_results["max_mean"], full_results["var_dist_mean"],
               full_results["sparsity_mean"], bvn_res]

    name_list = ("Max", "VarDist", "Sparsity", "BVN length")
    marker_list = ('o', '^', 'D', 's')
    color_list = ('#1f77b4', '#ff7f0e', '#2ca02c', '#d62728')
    for i, row in enumerate(results):
        plt.plot(x_values, row, label=f'{name_list[i]}', marker=marker_list[i],
                 linestyle='-', linewidth=2, color=color_list[i])

    plt.xscale('log')
    # Add labels and title
    plt.xlabel(r'Total flows ($n_{f}$)')
    plt.ylabel('Matrix Measure')
    if PAPER_MODE is True:
        plt.title('Figure 4(b)')
    plt.legend()
    if fig_path is not None:
        full_fig_path = os.path.join(fig_path, "figure_flow_numbers_matrix_measure.png")
        plt.savefig(full_fig_path)
    plt.show()


def plot_figure_pivot_load(data_file_path, fig_path=None):
    with open(data_file_path, 'r') as file:
        full_results = json.load(file)
    x_values = full_results["parameters"]["List_of_tested_vals"]
    results = full_results["da_load_mean"]
    results = [results, results]
    # total_cof_list=full_results["BvN_dist_mean"]
    # results =np.array(results)/np.array(total_cof_list)
    # results = [1-np.array(i)/j for i,j , in zip(results,total_cof_list)]
    name_list = (r"$m^{RR}$", r"$m^{DA}$")
    marker_list = ('', '^', 'D', 's')
    color_list = ('#ff7f0e', 'skyblue', '#2ca02c', '#d62728')
    for i, row in enumerate(results):
        plt.plot(x_values, row, label=f'{name_list[i]}', marker=marker_list[i],
                 linestyle='-', linewidth=2, color=color_list[i])
    # Set the x-axis in this plot to be logarithmic
    plt.xscale('log')
    # Add labels and title
    plt.xlabel(r'Total flows ($n_{f}$)')
    plt.ylabel('Demand Fraction')
    if PAPER_MODE is True:
        plt.title('Figure 4(c)')
    plt.ylim([0, 1])
    plt.fill_between(x_values, results[0], 1, where=(np.array(x_values) >= 0), interpolate=True, color='skyblue',
                     alpha=0.4)
    plt.fill_between(x_values, results[1], where=(np.array(x_values) >= 0), interpolate=True, color='#ff7f0e',
                     alpha=0.2)
    red_square = mlines.Line2D([], [], color=('#ff7f0e', 0.2), marker='s', linestyle='None',
                               markersize=9, label=name_list[0])
    blue_square = mlines.Line2D([], [], color=('skyblue', 0.4), marker='s', linestyle='None',
                                markersize=9, label=name_list[1])
    plt.legend(handles=[red_square, blue_square])
    if fig_path is not None:
        full_fig_path = os.path.join(fig_path, "figure_pivot_load.png")
        plt.savefig(full_fig_path)
    plt.show()


def plot_figures_large_load_ratio_change(data_file_path, x_title: str, fig_path=None):
    with open(data_file_path, 'r') as file:
        full_results = json.load(file)

    x_values = full_results["parameters"]["List_of_tested_vals"]
    results = full_results["mean_res"]
    name_list = ("BvN-sys", "RR-sys", "COMP-sys")
    marker_list = ('D', '^', 'o')
    color_list = ('#2ca02c', '#ff7f0e', '#1f77b4')
    for i, row in enumerate(np.transpose(results)):
        plt.plot(x_values, 1 / row, label=f'{name_list[i]}', marker=marker_list[i],
                 linestyle='-', linewidth=2, color=color_list[i])
    # Add labels and title
    plt.xlabel(x_title)
    plt.ylabel('Throughput')
    plt.ylim([0.18, 1])
    test_name = full_results["parameters"]["test_name"]
    if PAPER_MODE is True:
        if test_name != "large_flow_load":
            plt.title("Figure 6")
        else:
            plt.title("Figure 5")
    plt.legend()
    if 'FN64' in data_file_path:
        sparse_type = 'sparse'
    else:
        sparse_type = 'dense'
    if fig_path is not None:
        full_fig_path = os.path.join(fig_path, f"figure_{test_name}_load_type_{sparse_type}.png")
        plt.savefig(full_fig_path)
    plt.show()

