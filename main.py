#!/usr/bin/env python3
from umich_sim.sim_config import ConfigPool, Config, WizardConfig
import hydra
from hydra.conf import ConfigStore
from omegaconf import OmegaConf


@hydra.main(version_base=None, config_path="conf", config_name="config")
def game_loop(config: Config) -> None:
    pygame.init()
    pygame.font.init()
    world = None

    cs = ConfigStore.instance()
    try:
        client = carla.Client(config.server_addr, config.carla_port)
        client.set_timeout(2.0)

        display = pygame.display.set_mode(config.client_resolution,
                                          pygame.HWSURFACE | pygame.DOUBLEBUF)

        hud = HUD(args.width, args.height)
        world = World(client.get_world(), hud, config.car_filter)
        controller = Controller.get_instance()

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
    test()
    exit(0)

    log_level = logging.DEBUG if args.debug else logging.INFO
    logging.basicConfig(format='%(levelname)s: %(message)s', level=log_level)

    logging.info('listening to server %s:%s', args.host, args.port)

    print(__doc__)

    try:
        game_loop(args)
    except KeyboardInterrupt:
        print('\nCancelled by user. Bye!')
