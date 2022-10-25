#!/usr/bin/env python3
import hydra
from hydra.conf import ConfigStore
from omegaconf import OmegaConf
import pygame
import carla
import logging
from umich_sim.sim_backend.carla_modules import HUD, World
from umich_sim.sim_config import ConfigPool, Config, WizardConfig
from umich_sim.wizard import Wizard


@hydra.main(version_base=None, config_path="conf", config_name="config")
def game_loop(config: Config) -> None:
    ConfigPool.load_config(config)

    log_level = logging.DEBUG if config.debug else logging.INFO
    logging.basicConfig(format='%(levelname)s: %(message)s', level=log_level)

    logging.info('listening to server %s:%s', config.server_addr,
                 config.carla_port)
    pygame.init()
    pygame.font.init()
    world = None

    try:
        client = carla.Client(config.server_addr, config.carla_port)
        client.set_timeout(2.0)

        display = pygame.display.set_mode(config.client_resolution,
                                          pygame.HWSURFACE | pygame.DOUBLEBUF)

        hud = HUD(*config.client_resolution)
        world: World = World(client, hud, config.car_filter)
        controller: Wizard = Wizard.get_instance()

        clock = pygame.time.Clock()
        controller.run(clock, display)

    finally:
        print('\nCancelled by user. Bye!')
        if world is not None:
            world.destroy()
        pygame.quit()


@hydra.main(version_base=None, config_path="conf", config_name="config")
def test(cfg: Config) -> None:
    print(OmegaConf.to_yaml(cfg))


if __name__ == "__main__":
    cs = ConfigStore.instance()
    cs.store(group="wizard", name="base_wizard", node=WizardConfig)
    cs.store(name="base_config", node=Config)
    # test()
    try:
        game_loop()
    except KeyboardInterrupt:
        print('\nCancelled by user. Bye!')
