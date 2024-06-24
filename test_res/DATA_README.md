#  Structure of experiment result jason
This file describes the structure and each field in the the json files in this folder
* ### `parameters`: List of parameters used in the test, which includes:
* ####          `n`: Number of nodes\ network size
* ####          `rd`: Demand aware reconfiguration time
* ####         ` r`: Transmission rate
* ####        `large_ratio`: The ratio of the number of large flows of all flows
* ####        `large_load_ratio`: The ratio of the load of large flows
* ####          `number_of_tests`: The number of tests which were run
* ####         `List_of_tested_vals`: The tested values. This could represent the flow number, large flow load or large flow ratio
* ####        `test_name`: Which test was used to create this data set
* ### `full_result`: This is raw DCT result for our three systems. The list has a list for each of our 'number_of_tests' tetes, where each sublist has the same form as "mean_res". (Not used)

````
In the following fields each element in position "i" is equivalent to an experiment with List_of_tested_vals[i]
 in terms of tested parameter. And each result is the mean of "number_of_tests" results.
````




* ### `mean_res`: The mean DCT results for our three systems in the tuple (_"BvN-sys"_, _"RR-sys"_, _"COMP-sys"_).
* ### `bvn_dis_mean`: The number of elements in the BvN decomposition (Not used)
* ### `sparsity_mean`: The sparsity of the tested traffic matrix
* ### `max_mean`: The maximal value of the tested traffic matrix
* ### `var_mean`: The variation distance value of the tested traffic matrix
* ### `piv_res_mean`: A tuple where each element represents the division of the pivot algorithm in terms of the number of permutations sent to da-sys or rr-sys where (da, rr) (Not used)
* ### `da_load_mean`: The total fraction of the load sent towards da-sys by the pivot algorithm

## Partial Example
```json
{
"parameters":  {
        "List_of_tested_vals": [4,8,16,32],
        "large_load_ratio": 0.7,
        "large_ratio": 0.2,
        "n": 64,
        "number_of_tests": 28,
        "r": 10000000000,
        "rd": 0.01,
        "test_name": "flow_number"
}
}
```
#### Here we see that the experiment tested flow numbers, with 4 different options.