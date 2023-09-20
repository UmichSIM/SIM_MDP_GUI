#!/usr/bin/env python3
"""
Welcome to CARLA manual control with steering wheel Logitech G29.
To drive start by preshing the brake pedal.
Change your wheel_config.ini according to your steering wheel.
To find out the values of your steering wheel use jstest-gtk in Ubuntu.
"""
import pygame
import os
import carla
import datetime
import math
import csv
import time
import threading
from threading import Thread
from .module_helper import get_actor_display_name

class FadingText(object):

    def __init__(self, font, dim, pos):
        self.font = font
        self.dim = dim
        self.pos = pos
        self.seconds_left = 0
        self.surface = pygame.Surface(self.dim)

    def set_text(self, text, color=(255, 255, 255), seconds=2.0):
        text_texture = self.font.render(text, True, color)
        self.surface = pygame.Surface(self.dim)
        self.seconds_left = seconds
        self.surface.fill((0, 0, 0, 0))
        self.surface.blit(text_texture, (10, 11))

    def tick(self, _, clock):
        delta_seconds = 1e-3 * clock.get_time()
        self.seconds_left = max(0.0, self.seconds_left - delta_seconds)
        self.surface.set_alpha(500.0 * self.seconds_left)

    def render(self, display):
        display.blit(self.surface, self.pos)


class HelpText(object):

    def __init__(self, font, width, height):
        lines = __doc__.split('\n')
        self.font = font
        self.dim = (680, len(lines) * 22 + 12)
        self.pos = (0.5 * width - 0.5 * self.dim[0],
                    0.5 * height - 0.5 * self.dim[1])
        self.seconds_left = 0
        self.surface = pygame.Surface(self.dim)
        self.surface.fill((0, 0, 0, 0))
        for n, line in enumerate(lines):
            text_texture = self.font.render(line, True, (255, 255, 255))
            self.surface.blit(text_texture, (22, n * 22))
            self._render = False
        self.surface.set_alpha(220)

    def toggle(self):
        self._render = not self._render

    def render(self, display):
        if self._render:
            display.blit(self.surface, self.pos)


class HUD(object):
    """
    Singleton class HUD for gui controls
    """
    __instance = None
    last_update_time = time.time()
    data_collect_interval = 0.03
    data_thread = None
    vehicle = None
    display = None
    time_list = []
    speed_list = []
    
    # Temp for display testing
    # Define colors
    BLACK = (0, 0, 0)
    WHITE = (255, 255, 255)
    RED = (255, 0, 0)

    # Define the window size
    WINDOW_WIDTH = 800
    WINDOW_HEIGHT = 600
    
    # Initialize pygame
    x = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]
    #y = [1, -1, -2, -3, -4, -5, -6, -7, -8, -9]
    y = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]

    def __init__(self, width, height):
        self.dim = (width, height)
        font = pygame.font.Font(pygame.font.get_default_font(), 20)
        font_name = 'courier' if os.name == 'nt' else 'mono'
        fonts = [x for x in pygame.font.get_fonts() if font_name in x]
        default_font = 'ubuntumono'
        mono = default_font if default_font in fonts else fonts[0]
        mono = pygame.font.match_font(mono)
        self._font_mono = pygame.font.Font(mono, 12 if os.name == 'nt' else 14)
        self._notifications = FadingText(font, (width, 40), (0, height - 40))
        self.help: HelpText = HelpText(pygame.font.Font(mono, 24), width,
                                       height)
        self.server_fps = 0
        self.frame = 0
        self.simulation_time = 0
        self._show_info = True
        self._info_text = []
        self._server_clock = pygame.time.Clock()
        if HUD.__instance is None:
            HUD.__instance = self
        else:
            raise Exception("Error: Reinitialization of HUD")
        
        self.data_thread = Thread(target=self.data_collection)
        self.data_thread.start()

    @staticmethod
    def get_instance():
        if HUD.__instance is None:
            raise Exception("Error: Class HUD not initialized")
        return HUD.__instance

    def on_world_tick(self, timestamp):
        self._server_clock.tick()
        self.server_fps = self._server_clock.get_fps()
        self.frame = timestamp.frame
        self.simulation_time = timestamp.elapsed_seconds

    def tick(self, clock):
        from . import World, EgoVehicle
        world: World = World.get_instance()
        self._notifications.tick(world, clock)
        if not self._show_info:
            return
        self.vehicle: EgoVehicle = EgoVehicle.get_instance()
        t = self.vehicle.get_transform()
        v = self.vehicle.get_velocity()
        c = self.vehicle.get_control()
        heading = 'N' if abs(t.rotation.yaw) < 89.5 else ''
        heading += 'S' if abs(t.rotation.yaw) > 90.5 else ''
        heading += 'E' if 179.5 > t.rotation.yaw > 0.5 else ''
        heading += 'W' if -0.5 > t.rotation.yaw > -179.5 else ''
        colhist = world.collision_sensor.get_collision_history()
        collision = [colhist[x + self.frame - 200] for x in range(0, 200)]
        max_col = max(1.0, max(collision))
        collision = [x / max_col for x in collision]
        vehicles = world.world.get_actors().filter('vehicle.*')

        self._info_text = [
            'Driver: % 20s' % self.vehicle.get_driver_name(),
            'Server:  % 16.0f FPS' % self.server_fps,
            'Client:  % 16.0f FPS' % clock.get_fps(),
            '',
            'Vehicle: % 20s' %
            get_actor_display_name(world.vehicle.carla_vehicle, truncate=20),
            #'Map:     % 20s' % world.map.name,
            'Simulation time: % 12s' %
            datetime.timedelta(seconds=int(self.simulation_time)),
            '',
            'Speed:   % 15.0f km/h' %
            (3.6 * math.sqrt(v.x**2 + v.y**2 + v.z**2)),
            u'Heading:% 16.0f\N{DEGREE SIGN} % 2s' % (t.rotation.yaw, heading),
            'Accelero: (%5.1f,%5.1f,%5.1f)' %
            (world.imu_sensor.accelerometer),  #new
            'Location:% 20s' % ('(% 5.1f, % 5.1f)' %
                                (t.location.x, t.location.y)),
            'GNSS:% 24s' % ('(% 2.6f, % 3.6f)' %
                            (world.gnss_sensor.lat, world.gnss_sensor.lon)),
            'Height:  % 18.0f m' % t.location.z,
            ''
        ]
        # f = open("../../../arduino_projects/import_txt_test/accels.txt", "a")
        # f.write(str(round((3.6 * math.sqrt(v.x**2 + v.y**2 + v.z**2)) % 255, 2)))
        # # f.write(str(round(world.imu_sensor.accelerometer[0], 2)))
        # f.write('\n')
        # f.close()

        if isinstance(c, carla.VehicleControl):
            self._info_text += [('Throttle:', c.throttle, 0.0, 1.0),
                                ('Steer:', c.steer, -1.0, 1.0),
                                ('Brake:', c.brake, 0.0, 1.0),
                                ('Reverse:', c.reverse),
                                ('Hand brake:', c.hand_brake),
                                ('Manual:', c.manual_gear_shift),
                                'Gear:        %s' % {
                                    -1: 'R',
                                    0: 'N'
                                }.get(c.gear, c.gear)]
        self._info_text += [
            '', 'Collision:', collision, '',
            'Number of vehicles: % 8d' % len(vehicles)
        ]
        if len(vehicles) > 1:
            self._info_text += ['Nearby vehicles:']
            distance = lambda l: math.sqrt((l.x - t.location.x)**2 +
                                           (l.y - t.location.y)**2 +
                                           (l.z - t.location.z)**2)
            vehicles = [(distance(x.get_location()), x) for x in vehicles
                        if x.id != self.vehicle.carla_vehicle.id]
            for d, self.vehicle in sorted(vehicles):
                if d > 200.0:
                    break
                vehicle_type = get_actor_display_name(self.vehicle, truncate=22)
                self._info_text.append('% 4dm %s' % (d, vehicle_type))

    def toggle_info(self):
        self._show_info = not self._show_info

    def notification(self, text, seconds=2.0):
        self._notifications.set_text(text, seconds=seconds)

    def error(self, text):
        self._notifications.set_text('Error: %s' % text, (255, 0, 0))

    def render(self, display):
        if self._show_info:
            info_surface = pygame.Surface((220, self.dim[1]))
            info_surface.set_alpha(100)
            self.display = display
            self.display.blit(info_surface, (0, 0))
            v_offset = 4
            bar_h_offset = 100
            bar_width = 106
            for item in self._info_text:
                if v_offset + 18 > self.dim[1]:
                    break
                if isinstance(item, list):
                    if len(item) > 1:
                        points = [(x + 8, v_offset + 8 + (1.0 - y) * 30)
                                  for x, y in enumerate(item)]
                        pygame.draw.lines(self.display, (255, 136, 0), False,
                                          points, 2)
                    item = None
                    v_offset += 18
                elif isinstance(item, tuple):
                    if isinstance(item[1], bool):
                        rect = pygame.Rect((bar_h_offset, v_offset + 8),
                                           (6, 6))
                        pygame.draw.rect(self.display, (255, 255, 255), rect,
                                         0 if item[1] else 1)
                    else:
                        rect_border = pygame.Rect((bar_h_offset, v_offset + 8),
                                                  (bar_width, 6))
                        pygame.draw.rect(self.display, (255, 255, 255), rect_border,
                                         1)
                        f = (item[1] - item[2]) / (item[3] - item[2])
                        if item[2] < 0.0:
                            rect = pygame.Rect((bar_h_offset + f *
                                                (bar_width - 6), v_offset + 8),
                                               (6, 6))
                        else:
                            rect = pygame.Rect((bar_h_offset, v_offset + 8),
                                               (f * bar_width, 6))
                        pygame.draw.rect(self.display, (255, 255, 255), rect)
                    item = item[0]
                if item:  # At this point has to be a str.
                    surface = self._font_mono.render(item, True,
                                                     (255, 255, 255))
                    self.display.blit(surface, (8, v_offset))
                v_offset += 18
                
                
                self.drawGraph(self.time_list, self.speed_list, self.time_list[-1], 120, self.time_list[0], (50, 700), 20, 100, self.display)
        self._notifications.render(self.display)
        self.help.render(self.display)

    def drawGraph(self, x, y, xmax, ymax, xmin, graph_inter_in, tick_length_in, graph_len_in, screen):
        
        # Set up the window
        #screen = pygame.display.set_mode((self.WINDOW_WIDTH, self.WINDOW_HEIGHT))
        #pygame.display.set_caption("Graph")
        
        # Define the function to convert x and y values to screen coordinates
        def convert_coordinates(x_value, y_value, graphIntersect, xtick_val, ytick_val, tick_length):
            xnew = ((x_value - xmin)/xtick_val) * tick_length + graphIntersect[0]
            #print(x_value/xtick_val)
            ynew = graphIntersect[1] - (y_value/ytick_val) * tick_length
            return(xnew,ynew)
            
        def drawTicks(graphIntersect, graphLength, tickLength, xtickVal, ytickVal):
            buffer = tickLength
            tickSize = 10 #height
            for i in range(int(graphLength/tickLength)):
                tick_pos = (graphIntersect[0] + buffer*i, graphIntersect[1])
                pygame.draw.line(screen, self.WHITE, (tick_pos[0], tick_pos[1]+tickSize), (tick_pos[0], tick_pos[1]-tickSize))
                num_text = str(round(i*xtickVal+xmin,2))
                num_surface = pygame.font.SysFont(None, 10).render(num_text, True, self.WHITE)
                num_pos = (tick_pos[0]-num_surface.get_width()//2, tick_pos[1]+tickSize+5)
                screen.blit(num_surface, num_pos)
                
                tick_pos = (graphIntersect[0], graphIntersect[1] - buffer*i)
                pygame.draw.line(screen, self.WHITE, (tick_pos[0]-tickSize, tick_pos[1]), (tick_pos[0]+tickSize, tick_pos[1]))
                num_text = str(round(i*ytickVal,2))
                num_surface = pygame.font.SysFont(None, 20).render(num_text, True, self.WHITE)
                num_pos = (tick_pos[0]-tickSize-5-num_surface.get_width(), tick_pos[1]-num_surface.get_height()//2)
                screen.blit(num_surface, num_pos)
                
        # Define the main loop
        done = False
            # Handle events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                done = True
        
        # Draw the x and y axes
        tickLength = tick_length_in
        maxX = xmax
        maxY = ymax
        
        graphIntersect = graph_inter_in
        graphLength = graph_len_in
        
        xtickVal = (maxX-xmin)/(graphLength/tickLength-1)
        
        if xtickVal == 0:
            xtickVal = 0.0001
        
        ytickVal = maxY/(graphLength/tickLength-1)
        
        if ytickVal == 0:
            ytickVal = 0.0001
        
        pygame.draw.line(screen, self.WHITE, graphIntersect, (graphIntersect[0]+graphLength, graphIntersect[1]))
        pygame.draw.line(screen, self.WHITE, graphIntersect, (graphIntersect[0], graphIntersect[1]-graphLength))
        
        drawTicks(graphIntersect, graphLength, tickLength, xtickVal, ytickVal)
        #print(convert_coordinates(60, 60, graphIntersect, xtickVal, ytickVal, tickLength))
        # Draw the x and y values as points
        for i in range(len(x)-1):
            convertedCords = convert_coordinates(x[i], y[i], graphIntersect, xtickVal, ytickVal, tickLength)
            nextCords = convert_coordinates(x[i+1], y[i+1], graphIntersect, xtickVal, ytickVal, tickLength)
            #print(convert_coordinates(x[i], y[i], graphIntersect, xtickVal, ytickVal, tickLength))
            # pygame.draw.circle(screen, RED, convertedCords, 5)
            
            pygame.draw.line(screen, self.WHITE, convertedCords, nextCords , 2)
            pygame.display.flip()


    def data_collection(self):
        """Collect Data."""
        elm_num = int(10000 / self.data_collect_interval)
        startTime = time.time()
        
        with open(f'umich_sim/data_output/data.csv', 'a', newline='') as f:
            print("[INFO] Initial Ouput")
            w = csv.writer(f)
            
            timestamp = time.time()
            value = datetime.datetime.fromtimestamp(timestamp)
            date_str = value.strftime('%Y-%m-%d %H:%M:%S')
            
            w.writerow([])
            w.writerow([f"DATE: {date_str}"])
            w.writerow(["Timestamp", "Time (s)", "Ego Position X (m)", "Ego Position Y (m)", "Speed (km/h)", "Steering Wheel Angle", "Throttle Angle", "Brake Angle"])
            
        
        while True: 
            time.sleep(0.1)

            if time.time() - self.last_update_time >= self.data_collect_interval:
                self.last_update_time = time.time()
                if self.vehicle is not None:
                    t = self.vehicle.get_transform()
                    v = self.vehicle.get_velocity()
                    c = self.vehicle.get_control()
                    
                    timestamp = self.last_update_time
                    value = datetime.datetime.fromtimestamp(timestamp)
                    date_str = value.strftime('%Y-%m-%d %H:%M:%S.%f')[:-3]
                    speed = math.sqrt(v.x**2 + v.y**2 + v.z**2) * 10
                    steeringAngle = ((c.steer * -1) + 1) * 90
                    
                    if len(self.time_list) >= elm_num:
                        self.time_list.pop()
                    self.time_list.append(timestamp - startTime)
                    
                    if len(self.speed_list) >= elm_num:
                        self.speed_list.pop()
                    self.speed_list.append(speed)
                    
                    assert(len(self.speed_list) == len(self.time_list))
                    
                    

                    with open(f'umich_sim/data_output/data.csv', 'a', newline='') as f:
                        w = csv.writer(f)
                        w.writerow([date_str, str(timestamp) , t.location.x, t.location.y, speed, steeringAngle, c.throttle, c.brake])