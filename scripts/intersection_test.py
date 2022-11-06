#!/usr/bin/env python3

from umich_sim.sim_backend.experiments import IntersectionExperiment
from umich_sim.sim_backend.helpers import VehicleType
import hydra
from hydra.conf import ConfigStore
from omegaconf import OmegaConf
from umich_sim.sim_config import ConfigPool, Config, WizardConfig

# Sample configuration dictionary
# Notes: the vehicle with ID 0 must always be the ego vehicle,
# the vehicle's ID's must increase in consecutive order, otherwise later vehicles will be left out,
# the value of spawn_point corresponds with the spawn_point numbers found in the MapExplorationExperiment,
# spawn_offset shifts the spawn point forward or backward by x meters
configuration_dictionary = {
    "debug": True,
    "number_of_vehicles": 5,

    # Ego vehicle that simply goes straight through each intersection
    0: {
        "type": VehicleType.EGO_FULL_MANUAL,
        "spawn_point": 188,
        "spawn_offset": 0.0,
        "sections": {
            0: 'straight',
            1: 'straight',
            2: 'straight',
            3: 'straight'
        }
    },

    # Initial lead vehicle that turns right at the second intersection
    1: {
        "type": VehicleType.LEAD,
        "spawn_point": 188,
        "spawn_offset": 10.0,
        "sections": {
            0: 'straight',
            1: 'right'
        }
    },

    # Vehicle that turns right at initial intersection
    2: {
        "type": VehicleType.GENERIC,
        "spawn_point": 59,
        "spawn_offset": 0.0,
        "sections": {
            0: 'right'
        }
    },

    # Vehicle that turns right at the second intersection
    3: {
        "type": VehicleType.GENERIC,
        "spawn_point": 253,
        "spawn_offset": 0.0,
        "sections": {
            1: 'right'
        }
    },

    # Vehicle that turns left at the third intersection
    4: {
        "type": VehicleType.GENERIC,
        "spawn_point": 277,
        "spawn_offset": 0.0,
        "sections": {
            2: 'left',
            3: 'left'  # Current this is left due to some weirdness with Carla lanes, it actually goes straight
        }
    }
}



@hydra.main(version_base=None, config_path="conf", config_name="config")
def main(config: Config) -> None:
    config.gui_mode = True
    ConfigPool.load_config(config)

    # Create a new Experiment and initialize the server
    experiment = IntersectionExperiment(True)
    experiment.init()

    # Set up the experiment
    experiment.initialize_experiment(configuration_dictionary)

    # Start the main simulation loop
    try:
        experiment.run_experiment()
    finally:
        experiment.clean_up_experiment()


if __name__ == "__main__":
    cs = ConfigStore.instance()
    cs.store(group="wizard", name="base_wizard", node=WizardConfig)
    cs.store(name="base_config", node=Config)
    main()
