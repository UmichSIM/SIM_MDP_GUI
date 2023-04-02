#!/usr/bin/env python3

from umich_sim.sim_backend.experiments import FreewayExperiment
import hydra
from hydra.conf import ConfigStore
from omegaconf import OmegaConf
from umich_sim.sim_config import ConfigPool, Config, WizardConfig, VehicleType
import pygame

# Sample configuration dictionary
# Notes: the vehicle with ID 0 must always be the ego vehicle,
# the vehicle's ID's must increase in consecutive order, otherwise later vehicles will be left out,
# the value of spawn_point corresponds with the spawn_point numbers found in the MapExplorationExperiment,
# spawn_offset shifts the spawn point forward or backward by x meters
# configuration_new = ScenarioConfig(task=Task.FREEWAY)
# configuration_new.freeways.append(
#     Freeway(
#         subject_lane_vehicles=list(
#             Vehicle(
#                 location=0,
#                 gap=0,
#                 model="",
#                 color=(255, 255, 255),
#                 exp_settings=VehicleExpSettingsFreeway(
#                     vehicle_type=VehicleType.EGO_FULL_MANUAL
#                 ),
#             ),
#             Vehicle(
#                 location=1,
#                 gap=5.0,
#                 model="",
#                 color=(0, 0, 0),
#                 speed=50,
#                 exp_settings=VehicleExpSettingsFreeway(
#                     vehicle_type=VehicleType.LEAD, behavior=Behavior.KEEP_SAME_SPEED
#                 ),
#             ),
#         )
#     )
# )
configuration_dictionary = {
    "debug": True,
    "number_of_vehicles": 2,
    # Ego vehicle that simply goes straight through each Freeway section
    0: {
        "type": VehicleType.EGO_FULL_MANUAL,
        "spawn_point": 13,
        "spawn_offset": -10.0,
        "initial_lane_index": 1,
        "sections": {0: "straight"},
    },
    # Initial lead vehicle that turns right at the second intersection
    1: {
        "type": VehicleType.LEAD,
        "spawn_point": 13,
        "spawn_offset": 0.0,
        "initial_lane_index": 1,
        "sections": {0: "straight"},
    },
}


@hydra.main(version_base=None, config_path="conf", config_name="config")
def main(config: Config) -> None:
    config.gui_mode = True
    ConfigPool.load_config(config)

    # Create a new Experiment and initialize the server
    experiment = FreewayExperiment(True)
    # Initialize the Pygame display
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
