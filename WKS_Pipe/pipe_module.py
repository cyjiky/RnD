import numpy as np
from typing import List, Dict, Literal
import requests


class Pipe:
    """
    Compute pipe parameters via Hyperbolic function

    Parameters
    ----------
    longest_dim : float
        Diameter of widest diameter of the pipe (left or right borders, in our specific case)
    shortest_dim : float
        Diameter of narrowest diameter of the pipe (center of pipe, in our specific case)
    pipe_length : float
        Length of pipe
    X_shift : float
        Pipe shift by OX
    Y_shift : float
        Pipe shift by OY
    step : float
        Function step
    """

    def __init__(
        self,
        longest_dim: float = 127.537,
        shortest_dim: float = 125,
        pipe_length: float = 750,
        X_shift: float = 0,
        Y_shift: float = 0,
    ) -> None:

        self._b = np.float64(shortest_dim)

        self.length = pipe_length

        self.X_new = X_shift
        self.Y_new = -Y_shift
        self.true_p = (pipe_length / 2, longest_dim)

        self._a = np.sqrt(
            (self.true_p[0] ** 2) / (((self.true_p[1] ** 2) / self._b**2) - 1)
        )

    def calculate_points_Y(
        self, step: float
    ) -> List[Dict[Literal["X", "Y", "Step"], float]]:

        X = np.linspace(0, self.length, num=int(self.length / step))
        Y = self._b * np.sqrt(1 + ((X - self.length / 2) ** 2 / self._a**2))

        res = []

        for x, y in zip(X, Y):
            cords = {}
            cords["X"] = float(x - self.X_new)
            cords["Y"] = float(y - self.Y_new)
            # cords["Step"] = step

            res.append(cords)

        return res


pipe = Pipe(longest_dim=625.001, shortest_dim=615.025, pipe_length=880)

""" number of steps """
Y_sample = pipe.calculate_points_Y(step=int(880 / 177))
print(np.array(Y_sample)[:, np.newaxis])


""" step size """
# Y_sample = pipe.calculate_points_Y(step=0.224)
# for n in Y_sample:
#     print(n)


url = "http://127.0.0.1:8000/[your endpoint URI]"

try:
    response = requests.post(url, json=Y_sample)
    print(f"Status: {response.status_code}")
    print(f"Answer: {response.json()}")
except requests.exceptions.RequestException as e:
    print(f"Oh noooo: {e}")
