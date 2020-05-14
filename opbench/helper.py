import pandas as pd
import numpy as np

from opbench.config import TIME_SCALE


def parse_benchmark_result(
    csv_file_path, remove_outlier_sigma_count=5, row_limit=None, used_arg_indices=None
):
    df = pd.read_csv(csv_file_path, nrows=row_limit)
    input_arr = df["args"].to_list()
    input_arr = [eval(i) for i in input_arr]
    input_arr = np.array(input_arr)

    runtime_arr = (df["total_elapsed_time"] / df["n_exec"]).to_numpy()

    if input_arr.dtype is not np.float64:
        input_arr = input_arr.astype(np.float64)

    if runtime_arr.dtype is not np.float64:
        runtime_arr = runtime_arr.astype(np.float64)

    if remove_outlier_sigma_count != None:
        input_arr_new = []
        runtime_arr_new = []

        mean = np.mean(runtime_arr)
        std = np.std(runtime_arr)

        for i, j in zip(input_arr, runtime_arr):
            if abs(j - mean) <= remove_outlier_sigma_count * std:
                input_arr_new.append(i)
                runtime_arr_new.append(j)

        input_arr = np.array(input_arr_new)
        runtime_arr = np.array(runtime_arr_new)

    # if row_limit != None:
    #     if len(runtime_arr) > row_limit:
    #         input_arr = input_arr[:row_limit, :]
    #         runtime_arr = runtime_arr[:row_limit]

    runtime_arr = runtime_arr / TIME_SCALE

    if used_arg_indices is not None:
        input_arr = input_arr[:, used_arg_indices]

    return input_arr, runtime_arr