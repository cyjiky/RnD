import numpy as np
from typing import List, Dict, Literal, Tuple

from pipe_exceptions import Exceptions


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

    @staticmethod
    def _calculate_new_a_b(
        shortest_dim: float, true_point_X: float, true_point_Y: float
    ) -> Tuple[float, float]:
        """Returns a and b respectively"""
        b = shortest_dim / 2

        # TODO: Add constraits for root term, it can't be less than 0
        a = np.sqrt((true_point_X**2) / ((((true_point_Y / 2) ** 2) / b**2) - 1))

        return a, b

    def _update_a_b(self) -> None:
        self._a, self._b = self._calculate_new_a_b(
            shortest_dim=self._shortest_dim,
            true_point_X=self._length / 2,
            true_point_Y=self._longest_dim,
        )

    def __init__(
        self,
        longest_dim: float = 127.537,
        shortest_dim: float = 125,
        pipe_length: float = 750,
        X_new: float = 0,
        Y_new: float = 0,
    ) -> None:

        Exceptions.validate_pipe_dimensions(
            longest_dim=longest_dim, shortest_dim=shortest_dim, pipe_length=pipe_length
        )
        Exceptions.validate_X_Y_new(X_new=X_new, Y_new=Y_new)

        self._shortest_dim = shortest_dim
        self._longest_dim = longest_dim
        self._length = pipe_length

        self._X_new = X_new
        self._Y_new = -Y_new

        self._update_a_b()

    @property
    def length(self) -> float:
        return self._length

    @length.setter
    def length(self, value: float) -> None:
        Exceptions.validate_pipe_dimensions(pipe_length=value)

        self._length = value
        self._update_a_b()

    @property
    def longest_dim(self) -> float:
        return self._longest_dim

    @longest_dim.setter
    def longest_dim(self, value: float) -> None:
        Exceptions.validate_pipe_dimensions(
            longest_dim=value, shortest_dim=self._shortest_dim
        )

        self._longest_dim = value
        self._update_a_b()

    @property
    def shortest_dim(self) -> float:
        return self._shortest_dim

    @shortest_dim.setter
    def shortest_dim(self, value: float) -> None:
        Exceptions.validate_pipe_dimensions(
            shortest_dim=value, longest_dim=self._longest_dim
        )

        self._shortest_dim = value
        self._update_a_b()

    @property
    def X_new(self) -> float:
        return self._X_new

    @X_new.setter
    def X_new(self, value: float) -> None:
        Exceptions.validate_X_Y_new(X_new=value)
        self._X_new = value

    @property
    def Y_new(self) -> float:
        return self._Y_new

    @Y_new.setter
    def Y_new(self, value: float) -> None:
        Exceptions.validate_X_Y_new(Y_new=value)
        self._Y_new = -value

    # a and b must be protected from outside changing
    @property
    def a(self) -> float:
        return self._a

    @property
    def b(self) -> float:
        return self._b

    def calculate_points_Y(
        self, step: float
    ) -> List[Dict[Literal["X", "Y", "Step"], float]]:

        Exceptions.validate_step(step=step, pipe_length=self._length)

        # self.length+step to include last X coordinates
        X = np.arange(start=0, stop=self._length + step, step=step)
        Y = self._b * np.sqrt(1 + ((X - self._length / 2) ** 2 / self._a**2))
        Y *= 2  # To take diameter

        res = []

        for x, y in zip(X, Y):
            if x > self._length:
                continue

            Exceptions.validate_ans(X=x, Y=y, Step=step)

            cords = {}
            cords["X"] = float(x - self.X_new)
            cords["Y"] = float(y - self.Y_new)

            res.append(cords)

        return res


if __name__ == "__main__":
    """Usage example"""

    try:
        pipe = Pipe(longest_dim=30, shortest_dim=40, pipe_length=100)
    except ValueError as e:
        print(f"Catched ValueError: {e}")

    pipe = Pipe(longest_dim=50, shortest_dim=10, pipe_length=10)

    cords = pipe.calculate_points_Y(0.1)
    print(f"Computed {len(cords)} values")
    print(cords[:10])
    print("...")
    print(cords[len(cords) - 10 :])


# url = "http://127.0.0.1:8000/[your endpoint URI]"

# try:
#     response = requests.post(url, json=Y_sample)
#     response.raise_for_status()
#     print(f"Answer: {response.json()}")
# except requests.exceptions.RequestException as e:
#     print(f"Oh noooo: {e}")
