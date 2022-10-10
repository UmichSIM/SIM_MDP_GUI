#!/usr/bin/env python3
import argparse
import logging
import pygame
from sim_backend.wizard.drivers import InputDevType
from sim_backend.wizard.controller import Controller
from sim_backend.carla_modules import HUD, World
from sim_backend.wizard import config
import carla


def game_loop(args):
    pygame.init()
    pygame.font.init()
    world = None

    try:
        client = carla.Client(config.server_addr, args.port)
        client.set_timeout(2.0)

        display = pygame.display.set_mode((args.width, args.height),
                                          pygame.HWSURFACE | pygame.DOUBLEBUF)

        hud = HUD(args.width, args.height)
        world = World(client.get_world(), hud, args.filter)
        controller = Controller.get_instance()

        clock = pygame.time.Clock()
        controller.run(clock, display)

    finally:
        print('\nCancelled by user. Bye!')
        if world is not None:
            world.destroy()
        pygame.quit()


def main():
    argparser = argparse.ArgumentParser(
        description='CARLA Manual Control Client')
    argparser.add_argument('-w',
                           '--wizard',
                           action='store_true',
                           help='run in wizard mode')
    argparser.add_argument('-u',
                           '--user',
                           action='store_true',
                           help='run in user mode')
    argparser.add_argument('-v',
                           '--verbose',
                           action='store_true',
                           dest='debug',
                           help='print debug information')
    argparser.add_argument('--host',
                           metavar='H',
                           default='127.0.0.1',
                           help='IP of the host server (default: 127.0.0.1)')
    argparser.add_argument('-d',
                           '--dev',
                           metavar='H',
                           default=config.user_input_event,
                           help='device handler for racing wheel')
    argparser.add_argument('-p',
                           '--port',
                           metavar='P',
                           default=2000,
                           type=int,
                           help='TCP port to listen to (default: 2000)')
    argparser.add_argument('--res',
                           metavar='WIDTHxHEIGHT',
                           default='1280x720',
                           help='window resolution (default: 1280x720)')
    argparser.add_argument('--filter',
                           metavar='PATTERN',
                           default='vehicle.*',
                           help='actor filter (default: "vehicle.*")')
    args = argparser.parse_args()

    config.server_addr = args.host
    config.user_input_event = args.dev
    if args.wizard:
        config.client_mode = InputDevType.WIZARD
    elif args.user:
        config.client_mode = InputDevType.WHEEL

    args.width, args.height = [int(x) for x in args.res.split('x')]

    log_level = logging.DEBUG if args.debug else logging.INFO
    logging.basicConfig(format='%(levelname)s: %(message)s', level=log_level)

    logging.info('listening to server %s:%s', args.host, args.port)

    print(__doc__)

    try:
        game_loop(args)
    except KeyboardInterrupt:
        print('\nCancelled by user. Bye!')


if __name__ == '__main__':
    main()
