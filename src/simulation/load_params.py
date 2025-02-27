import pandas as pd

from src.config import BLD
from src.simulation import params_scenarios


def load_params(scenario):
    """Return params fitting to the given scenario.

    Note that many scenarios must be implemented through `load_simulation_inputs`.

    Args:
        scenario (str): name of the function that exists in
            src/simulation/params_scenarios.py.

    Returns:
        params (pandas.DataFrame): params adjusted to the scenario.

    """
    params = pd.read_pickle(BLD / "params.pkl")

    scenario_func = getattr(params_scenarios, scenario)
    params = scenario_func(params)

    assert params["value"].notnull().all()
    return params
