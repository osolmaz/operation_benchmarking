from operation_pricing.operations import diophantine
import pandas as pd
import matplotlib.pyplot as plt
from scipy.optimize import least_squares
import numpy as np

df = pd.read_csv("data_sha1.csv")

timevar_list = df["time_vars"].to_list()

timevar_list = [eval(i) for i in timevar_list]

n_timevars = len(timevar_list[0])

timevar_keys = []


for i in range(n_timevars):
    new_col = [j[i] for j in timevar_list]
    key = "time_var_%d"%i

    timevar_keys.append(key)

    df[key] = pd.DataFrame(new_col)


df["mean_time"] = df["elapsed_time"]/df["n_exec"]


def positive_part(x):
    return np.array([max(i, 0.) for i in x])

def negative_part(x):
    return np.array([max(-i, 0.) for i in x])


def f(x):
    m, n = x

    residual = m*df["time_var_0"]+n-df["mean_time"]

    pos = positive_part(residual)
    neg = negative_part(residual)

    # import ipdb; ipdb.set_trace()
    result = pos - 10*neg


    return result


result = least_squares(f, [1,1])

m, n = result.x

X = np.linspace(df["time_var_0"].min(), df["time_var_0"].max(), 1000)
Y = m*X + n


plt.scatter(df["time_var_0"], df["mean_time"], marker="x")
plt.plot(X, Y, color="red", label="fit")
plt.grid()
plt.legend()
plt.show()
