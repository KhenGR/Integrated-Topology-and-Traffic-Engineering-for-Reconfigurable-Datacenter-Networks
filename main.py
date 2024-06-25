from src.multi_proc import *
from src.testing_functions import *
from src.plotter import *


def recreate_paper_results():
    """
    Running this function will generate all data needed to recreate the results in the paper
    :return: Nothing. data will be saved in "test_res" dir
    """
    current_dir = os.getcwd()
    test_res_dir_name = os.path.join(current_dir, "test_res")
    # main test
    run_test_of_total_flow_number_change(test_res_dir_name, 0.2, 0.7, number_of_tests=NUMBER_OF_RUNS)
    # #Test large flow load variation
    # #spars
    run_test_of_large_flow_load_change(test_res_dir_name, 0.2, 64, number_of_tests=NUMBER_OF_RUNS)
    # #dense
    run_test_of_large_flow_load_change(test_res_dir_name, 0.2, 3000, number_of_tests=NUMBER_OF_RUNS)
    # # Test large flow load variation
    # # spars
    run_test_of_large_flow_ratio_change(test_res_dir_name, large_load_ratio=0.7, flow_number=64)
    # # dense
    run_test_of_large_flow_ratio_change(test_res_dir_name, large_load_ratio=0.7, flow_number=3000)


if __name__ == '__main__':
    # Run this to recreate paper results
    #recreate_paper_results()

    # Get path to results dir
    file_path_flow_numbers = "test_res\\test_flow_number_LR02_LLR07_n64.json"
    #
    file_path_sparse_large_load = "test_res\\test_large_flow_load_LR02_FN64_n64.json"
    file_path_dense_large_load = "test_res\\test_large_flow_load_LR02_FN3000_n64.json"
    #
    file_path_sparse_large_ratio = "test_res\\test_large_flow_ratio_LLR07_FN64_n64.json"
    file_path_dense_large_ratio = "test_res\\test_large_flow_ratio_LLR07_FN3000_n64.json"

    # Set path to figures directory
    figure_path = os.path.join(os.getcwd(), "figs")
    # Figures 4 a b and c
    plot_figure_four_flow_numbers_matrix_measure(file_path_flow_numbers, figure_path)
    plot_figure_flow_numbers_thru(file_path_flow_numbers, figure_path)
    plot_figure_pivot_load(file_path_flow_numbers, figure_path)
    # Figures 5 a and b
    plot_figures_large_load_ratio_change(file_path_sparse_large_load, "Large Flow Load ($c_{l}$)", figure_path)
    plot_figures_large_load_ratio_change(file_path_dense_large_load, "Large Flow Load ($c_{l}$)", figure_path)
    # Figures 6 a and b
    plot_figures_large_load_ratio_change(file_path_sparse_large_ratio, "Large Flow Ratio ($t_{l}$)", figure_path)
    plot_figures_large_load_ratio_change(file_path_dense_large_ratio, "Large Flow Ratio ($t_{l}$)", figure_path)
