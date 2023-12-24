# type ignore in numpy because of ruamel.yaml
import numpy as np  # type: ignore
import pandas as pd
import scipy.stats as stats
from prefect import task


@task
def sim_df(size, seed: int | None = None) -> pd.DataFrame:
    y = stats.norm.rvs(loc=10, scale=2, size=size, random_state=seed)
    m = np.array([1, 2, 4])
    a = np.array([0.75, 0.85, 0.95])
    # create a symmetric matrix size * size
    # matrix created using multiplication of inverse of a vector is always
    # symmetric and positive definite
    c = np.dot(a[:, None], a[None, :])
    x = stats.multivariate_normal.rvs(
        mean=m, cov=c, size=size, random_state=seed
    )
    d = np.concatenate((y[:, None], x), axis=1)
    return pd.DataFrame(data=d, columns=["y", "x1", "x2", "x3"])
