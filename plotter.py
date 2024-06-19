import json
import matplotlib.pyplot as plt
from evaluation_Functions import  *

file_path_flow_numbers="test_res\\n64_test_total_flows_LR02_LLR07_date1906.json"
with open(file_path_flow_numbers, 'r') as file:
    full_results = json.load(file)

x_values = full_results["x_values"]
results=full_results["mean_res"]
name_list = ("BvN-sys","RR-sys","COMP-sys")
marker_list = ('D','^','o')
color_list =( '#2ca02c','#ff7f0e', '#1f77b4')
for i, row in enumerate(np.transpose(results)):
    plt.plot(x_values,1/row, label=f'{name_list[i]}', marker=marker_list[i],
             linestyle='-', linewidth=2,color= color_list[i])

plt.xscale('log')
# Add labels and title
plt.xlabel('X-axis')
plt.ylabel('Y-axis')
#plt.title('Curves from Matrix Rows')
plt.legend()
plt.show()