import numpy as np
from typing import List, Dict, Literal, Tuple
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

    @staticmethod
    def _calculate_new_a_b(shortest_dim: float, true_point_X: float, true_point_Y: float) -> Tuple[float, float]:
        """Returns a and b respectively"""
        b = shortest_dim
        a = np.sqrt(
            (true_point_X ** 2) / (((true_point_Y ** 2) / b ** 2) - 1)
        )

        return a, b
    
    def _update_a_b(self) -> None:
        self._a, self._b = self._calculate_new_a_b(
            shortest_dim=self._shortest_dim,
            true_point_X=self._length / 2,
            true_point_Y=self._longest_dim
        )

    def __init__(
        self,
        longest_dim: float = 127.537,
        shortest_dim: float = 125,
        pipe_length: float = 750,
        X_shift: float = 0,
        Y_shift: float = 0,
    ) -> None:
        
        self._shortest_dim = shortest_dim
        self._longest_dim = longest_dim
        self._length = pipe_length

        self._X_new = X_shift
        self._Y_new = -Y_shift

        self._update_a_b()

    @property
    def length(self) -> float:
        return self._length
    
    @length.setter
    def length(self, value: float) -> None:
        # TODO: Constraits for lengt

        self._length = value
        self._update_a_b()


    @property
    def longest_dim(self) -> float:
        return self._longest_dim
    
    @longest_dim.setter
    def longest_dim(self, value: float) -> None:
        # TODO: Constraits for longest diameter

        self._longest_dim = value
        self._update_a_b()

    @property
    def shortest_dim(self) -> float:
        return self._shortest_dim
    
    @shortest_dim.setter
    def shortest_dim(self, value: float) -> None:
        ## TODO: Constraits for shortest diameter

        self._shortest_dim = value
        self._update_a_b()

    @property
    def X_new(self) -> float:
        return self._X_new
    
    @X_new.setter
    def X_new(self, value: float) -> None:
        ## TODO: Constraits for X_new

        self._X_new = value

    @property
    def Y_new(self) -> float:
        return self._Y_new
    
    @Y_new.setter
    def Y_new(self, value: float) -> None:
        ## TODO: Constraits for Y_new

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


if __name__ == "__main__":
    """Usage example"""