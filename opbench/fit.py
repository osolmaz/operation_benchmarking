import numpy as np

from math import ceil
from scipy.optimize import least_squares, fmin, fsolve


def modify_residual(x, alpha):
    return max(x, 0) - alpha * max(-x, 0)


modify_residual_vectorized = np.vectorize(modify_residual)


def fit(operation, input_arr, runtime_arr, degree_of_confidence, x0=None, bounds=None):
    input_size = len(input_arr)

    runtime_model = operation.get_runtime_model()
    n_param = operation.get_n_model_param()
    n_input = operation.get_model_input_size()

    if input_arr.dtype is not np.float64:
        input_arr = input_arr.astype(np.float64)

    if runtime_arr.dtype is not np.float64:
        runtime_arr = runtime_arr.astype(np.float64)

    if not x0:
        x0 = np.ones(n_param, dtype=np.float64)

    def f(param):
        residual = runtime_model(param, input_arr)
        residual = residual - runtime_arr
        return residual

    if bounds:
        result = least_squares(f, x0, bounds=bounds, method="dogbox")
    else:
        result = least_squares(f, x0, method="dogbox")

    param = result.x

    model_result = runtime_model(param, input_arr)
    difference = runtime_arr - model_result

    constant = fit_constant(difference, degree_of_confidence)

    param[operation.get_constant_term_idx()] += constant

    return param


def fit_constant(runtime_arr, degree_of_confidence):
    assert 0 <= degree_of_confidence <= 1

    if len(runtime_arr) < 10:
        raise Exception("Data series too small for fitting")
    sorted_ = np.sort(runtime_arr)

    idx = ceil((len(runtime_arr) - 1) * degree_of_confidence)

    if idx == len(runtime_arr) - 1:
        return sorted_[-1]

    lower_bound = sorted_[idx]
    upper_bound = sorted_[idx + 1]

    lower_weight = np.mean(sorted_[: idx + 1])
    upper_weight = np.mean(sorted_[idx + 1 :])

    result = lower_bound + (upper_bound - lower_bound) * lower_weight / (
        lower_weight + upper_weight
    )

    # print(runtime_arr.shape, runtime_arr[-10:])
    # print(idx, result, degree_of_confidence)

    return result
