import json
import matplotlib.pyplot as plt
from evaluation_Functions import *


def plot_figure_four_a(data_file_path):
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
    plt.xlabel('X-axis')
    plt.ylabel('Y-axis')
    #plt.title('Curves from Matrix Rows')
    plt.legend()
    plt.show()


def plot_figure_four_b(data_file_path):
    file_path_flow_numbers = data_file_path
    with open(file_path_flow_numbers, 'r') as file:
        full_results = json.load(file)
    bvn_res=list(full_results["BvN_dist_mean"]/np.max(full_results["BvN_dist_mean"]))
    x_values = full_results["parameters"]["List_of_tested_vals"]
    results = [full_results["max_mean"], full_results["var_dist_mean"],
               full_results["sparsity_mean"], bvn_res]

    name_list = ("Max", "VarDist", "Sparsity", "BVN length")
    marker_list = ('o', '^', 'D', 's')
    color_list = ('#1f77b4', '#ff7f0e',  '#2ca02c','#d62728')
    for i, row in enumerate(results):
        plt.plot(x_values, row, label=f'{name_list[i]}', marker=marker_list[i],
                 linestyle='-', linewidth=2, color=color_list[i])

    plt.xscale('log')
    # Add labels and title
    plt.xlabel('X-axis')
    plt.ylabel('Y-axis')
    #plt.title('Curves from Matrix Rows')
    plt.legend()
    plt.show()

def plot_figure_four_c(data_file_path):
    # TODO: this
    return None
def plot_figure_five_six(data_file_path,x_title):
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

    # Add labels and title
    plt.xlabel(x_title)
    plt.ylabel('Y-axis')
    plt.ylim([0, 1])
    #plt.title('Curves from Matrix Rows')
    plt.legend()
    plt.show()


file_path_flow_numbers = "test_res\\test_flow_number_LR02_LLR07_n64.json"

file_path_sparse_large_load = "test_res/test_large_flow_load_LRR07_FN64_n64.json"
file_path_dense_large_load = "test_res/test_large_flow_load_LRR07_FN3000_n64.json"

file_path_sparse_large_ratio = "test_res\\test_large_flow_ratio_LR02_FN64_n64.json"
file_path_dense_large_ratio = "test_res\\test_large_flow_ratio_LR02_FN3000_n64.json"

#plot_figure_four_a(file_path_flow_numbers)
plot_figure_four_b(file_path_flow_numbers)

plot_figure_five_six(file_path_sparse_large_load,"Large Flow Load(c)")
plot_figure_five_six(file_path_dense_large_load,"Large Flow Load(c)")
plot_figure_five_six(file_path_sparse_large_ratio,"Large Flow Ratio(c)")
plot_figure_five_six(file_path_dense_large_ratio,"Large Flow Ratio(c)")
# plot_figure_five_six(file_path_sparse_large_ratio)
# plot_figure_five_six(file_path_dense_large_ratio)

