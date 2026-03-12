class Exceptions:
    # TODO 

    """ 
    Example:
    def const(
        self, 
        longest_dim,
        shortest_dim,
        pipe_length,
        Step, 
    ): 
        pass 
    """

    def validate_pipe_dimensions(
        longest_dim: float | None = None,
        shortest_dim: float | None = None,
        pipe_length: float | None = None
    ) -> None:
        """checking physical parameters \n\n If some argument is None, skipping that check"""

        if longest_dim != None and longest_dim <= 0:
            raise ValueError("The maximum diameter exists only in the range (0; +infty)")

        if shortest_dim != None and shortest_dim <= 0:
            raise ValueError("The minimum diameter can only exist in the range (0; +infty)")

        if pipe_length != None and pipe_length <= 0:
            raise ValueError("The pipe length can only exist in the range (0; +infty)")

        if longest_dim != None and shortest_dim != None and longest_dim <= shortest_dim:
            raise ValueError("The minimum diameter must be strictly less than the maximum")


    def validate_step(step: float, pipe_length: float) -> None:
        """step check"""

        if step <= 0:
            raise ValueError("The step must be greater than zero")
        if step > pipe_length:
            raise ValueError("Шаг не может быть больше длины самой трубы")


    def validate_X_Y_new(X_new: float | None = None, Y_new: float | None = None) -> None:
        """Checking X_new and Y_new, which are standing for shifting the figure"""

        if X_new != None and X_new < 0:
            raise ValueError("Error: False value 'X_new' must be in range [0; +infty)")

        if Y_new != None and Y_new < 0:
            raise ValueError("Error: False value 'Y_new' must be in range [0; +infty)")


    def validate_ans(X: float, Y: float, Step: float) -> None:
        """Checking the final answers"""

        if X is None:
            raise ValueError("Unknown values ​​of 'X' ")

        if Y is None:
            raise ValueError("Unknown 'Y' values ")

        # ---- TODO
        if X < 0:
            raise ValueError("Error: False value 'X' ")

        if Y < 0:
            raise ValueError("Error: False value 'Y' ")

        if Step < 0:
            raise ValueError("Incorrect step value")


if __name__ == "__main__":
    """Usage example"""