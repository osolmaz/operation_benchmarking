import os
import logging

from operation_benchmarking.plotting import plot_argumentless_operation
from operation_benchmarking.helper import parse_benchmark_result
from operation_benchmarking.operations.host_functions import *

import matplotlib.pyplot as plt

logging.basicConfig(level=logging.INFO)


DEGREE_OF_CONFIDENCE = 0.99
ROW_LIMIT = 10_000
DATA_DIR = "host-function-metrics"
PLOT_DIR = "out"


operations = [
    # Constant operations
    AddAssociatedKeyOperation(),
    AddOperation(),
    CreatePurseOperation(),
    GetArgSizeOperation(),
    GetBalanceOperation(),
    GetBlocktimeOperation(),
    GetCallerOperation(),
    GetMainPurseOperation(),
    GetPhaseOperation(),
    GetSystemContractOperation(),
    IsValidUrefOperation(),
    ReadValueOperation(),
    RemoveAssociatedKeyOperation(),
    RevertOperation(),
    SetActionThresholdOperation(),
    TransferFromPurseToAccountOperation(),
    TransferFromPurseToPurseOperation(),
    TransferToAccountOperation(),
    UpdateAssociatedKeyOperation(),
    # Linear operations
    AddLocalOperation(),
    CallContractOperation(),
    GetArgOperation(),
    GetKeyOperation(),
    HasKeyOperation(),
    LoadNamedKeysOperation(),
    NewUrefOperation(),
    PrintOperation(),
    PutKeyOperation(),
    ReadHostBufferOperation(),
    ReadValueLocalOperation(),
    RemoveKeyOperation(),
    RetOperation(),
    WriteOperation(),
]

# operations = [GetArgOperation()]


if not os.path.exists(PLOT_DIR):
    os.makedirs(PLOT_DIR)

# op1 = AddLocalOperation()
# op1_param = op1.fit_parameters(
#     "host-function-metrics/add_local.csv", 0.99, bounds=((0, 0), (np.inf, np.inf))
# )
# op1.plot_model_performance(
#     op1_param, "host-function-metrics/add_local.csv", "data_op1.jpg",
# )

for op in operations:
    logging.info("Fitting model for operation: " + op.get_name())
    data_file_path = os.path.join(DATA_DIR, op.get_name() + ".csv")
    plot_path = os.path.join(PLOT_DIR, op.get_name() + ".jpg")

    n_param = op.get_n_model_param()
    bounds = [[0 for i in range(n_param)], [np.inf for i in range(n_param)]]

    op_param = op.fit_parameters(
        data_file_path, DEGREE_OF_CONFIDENCE, row_limit=ROW_LIMIT, bounds=bounds,
    )

    op.plot_model_performance(
        op_param, data_file_path, plot_path, row_limit=ROW_LIMIT,
    )

    input_arr, runtime_arr = parse_benchmark_result(data_file_path, row_limit=ROW_LIMIT)

    # import ipdb; ipdb.set_trace()
    # plt.figure()
    # plt.scatter(input_arr[:,0], runtime_arr, marker='x')
    # plt.grid()
    # # plt.hist(runtime_arr)
    # plt.show()