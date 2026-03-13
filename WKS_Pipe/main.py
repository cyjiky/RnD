from pipe_module import Pipe
from pipe_exceptions import ConfigException
import json
from typing import Dict, Any
import os
import requests

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

def validate_export_config(export_config: Dict) -> None:
    """
    raise: ConfigException (inherits from Exception) on validation failure
    """

    export_json_locally = export_config.get("export_json_local", MissingValue)
    export_sheets_cloud = export_config.get("export_sheets_cloud", MissingValue)

    if export_json_locally is MissingValue:
        raise ConfigException(
            "'export_json_locally' is missing in 'export_config' (conf.json file)"
        )
    elif export_sheets_cloud is MissingValue:
        raise ConfigException(
            "'export_sheets_cloud' is missing in 'export_config' (conf.json file)"
        )
    
    if not isinstance(export_json_locally, bool):
        raise ConfigException(
            "'export_json_locally' has invalid value type, only boolean allowed (conf.json file)"
        )
    elif not isinstance(export_sheets_cloud, bool):
        raise ConfigException(
            "'export_sheets_cloud' has invalid value type, only boolean allowed (conf.json file)"
        )

    if export_json_locally is False and export_sheets_cloud is False:
        raise ConfigException(
            "Not a single export option selected! Set to 'true' at least one in 'export_config' (conf.json file)"
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
    export_config = config.get("export_config", None)

    if not all([pipe_config, compute_config, export_config]):
        raise ConfigException(
            f"'{"pipe_config" if not pipe_config else "compute_config" if compute_config else "export_config"}' key is missing in conf.json"
        )

    validate_pipe_config(pipe_config)
    validate_compute_config(compute_config)
    validate_export_config(export_config)

    pipe = Pipe(
        longest_dim=pipe_config["longest_diameter"],
        shortest_dim=pipe_config["shortest_diameter"],
        pipe_length=pipe_config["pipe_length"],
    )

    computations = pipe.calculate_points_Y(step=compute_config["step_value"])

    if export_config["export_json_local"] is True:
        result_path = os.path.join("results", "cords_results.json")

        if not os.path.isdir("results"):
            os.mkdir("results")

        with open(result_path, "w") as f:
            json.dump(computations, f, indent=4)

    if export_config["export_sheets_cloud"] is True:
        from sheets_export.dtos import Coordinates

        url = "http://127.0.0.1:8000/coordinates"

        # Example 
        # url = "http://127.0.0.1:8000/[your endpoint URI]"

        mapped_serializable_dto = [
            Coordinates(
                X=cord["X"],
                Y=cord["Y"],
                Step=cord.get("Step", None) # Could be None
            ).model_dump() for cord in computations
        ]

        try:
            response = requests.post(url, json=mapped_serializable_dto)
            response.raise_for_status()
            print(f"Response: {response.json()}")
        except requests.exceptions.RequestException as e:
            print(f"Cloud sheets export failed: {e}")