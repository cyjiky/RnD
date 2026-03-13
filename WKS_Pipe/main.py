from pipe_module import Pipe
from pipe_exceptions import ConfigException
import json
from typing import Dict, Any
import os


class MissingValue:
    """Custom object that used in missing JSON key cases"""

    pass


def _check_numeric_type(value: Any) -> bool:
    return isinstance(value, (int, float)) and value is not False and value is not True


def validate_pipe_config(pipe_config: Dict) -> None:
    """
    raise: ConfigException (inherits from Exception) on validation failure
    """

    longest_diameter = pipe_config.get("longest_diameter", MissingValue)
    shortest_diameter = pipe_config.get("shortest_diameter", MissingValue)
    pipe_length = pipe_config.get("pipe_length", MissingValue)

    if longest_diameter is MissingValue:
        raise ConfigException(
            "'longest_diameter' is missing in 'pipe_config' (conf.json file)"
        )
    elif shortest_diameter is MissingValue:
        raise ConfigException(
            "'shortest_diameter' is missing in 'pipe_config' (conf.json file)"
        )
    elif pipe_length is MissingValue:
        raise ConfigException(
            "'pipe_length' is missing in 'pipe_config' (conf.json file)"
        )

    conf_keys = {
        "longest_diameter": longest_diameter,
        "shortest_diameter": shortest_diameter,
        "pipe_length": pipe_length,
    }

    if not all(_check_numeric_type(conf_key) for conf_key in conf_keys.values()):
        raise ConfigException(
            "Some keys in 'pipe_config' have invalid value types, only int or float allowed (conf.json file)"
        )


def validate_compute_config(compute_config: Dict) -> None:
    """
    raise: ConfigException (inherits from Exception) on validation failure
    """

    step_value = compute_config.get("step_value", MissingValue)

    if step_value is MissingValue:
        raise ConfigException(
            "'step_value' is missing in 'compute_config' (conf.json file)"
        )

    if not _check_numeric_type(step_value):
        raise ConfigException(
            f"'step_value' key in 'compute_config' has invalid value type, only int and float allowed (conf.json file)"
        )


if __name__ == "__main__":
    config_path = os.path.join("conf", "pipe_config.json")

    config = None

    try:
        with open(config_path, "r") as file:
            config = json.load(file)
    except FileNotFoundError:
        raise ConfigException("'conf/pipe_config.json' is not found, create it first")

    if not config or not isinstance(config, dict):
        raise ConfigException("Invalid of malformed json config provided")

    pipe_config = config.get("pipe_config", None)
    compute_config = config.get("compute_config", None)

    if pipe_config is None or compute_config is None:
        raise ConfigException(
            f"'{"pipe_config" if not pipe_config else "compute_config"}' key is missing in conf.json"
        )

    validate_pipe_config(pipe_config)
    validate_compute_config(compute_config)

    pipe = Pipe(
        longest_dim=pipe_config["longest_diameter"],
        shortest_dim=pipe_config["shortest_diameter"],
        pipe_length=pipe_config["pipe_length"],
    )

    computations = pipe.calculate_points_Y(step=compute_config["step_value"])
    result_path = os.path.join("results", "cords_results.json")

    if not os.path.isdir("results"):
        os.mkdir("results")

    with open(result_path, "w") as f:
        json.dump(computations, f, indent=4)
