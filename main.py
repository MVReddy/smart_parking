"""

"""

__author__ = 'Obed N Munoz'
import pygame
import json_loader
import sys
import time
import json
import random
import argparse

def main(action=""):

    # initialize pygame
    pygame.init()
    # set screen size of phone or desktop window.  Adjust to your phone
    screen = pygame.display.set_mode((1024, 768))
    pygame.display.set_caption("Use keyboard arrow keys or mouse.  Press TEST to toggle overlay")
    

    # game framerate.  Higher number is faster
    FPS = 40

    # change the file names to your player graphic and map file
    player_image_file = "img/direction_24px.png"
    map_file = "maps/mega_map.json"

    # change to False (with capital F) to turn off red squares over
    # collision rectangles
    TESTING = True

    #initialize json loader, build tileset list, load player graphic
    initial = json_loader.Initialize(screen, TESTING, map_file, player_image_file)

    # initialize position of player when game first starts
    initial_position = (-4574,-4837)  
    map = json_loader.Map(initial, initial_position)
    #map.move_to_tile((159,163))
    map.move(initial_position[0], initial_position[1])

    # handle events such as keyboard / touchscreen presses
    event = json_loader.Event(initial)
    clock = pygame.time.Clock()

    [x,y] = [0,0]
    
    # Generating pathfile 

    if action == 'generate_path':
        pathfile = open("path"+ str(random.randint(1,100)), 'w')
        new_path = []

    # Loading Paths
    filename = "maps/paths.json"
    paths = ''
    path = []

    try:
        with open(filename) as paths_file:
            paths = json.loads(paths_file.read())
    except IOError:
        print("Cannot open map file {}".format(filename))
    
    sections = paths["sections"]
    section = sections[1]

    slot = -1    
    new_car = 0

    while True:
        event.update()
    
        if event.direction == "start" and not path:
            new_car = random.randint(1,10)  
            map.player.change_car_image("img/car_24px_"+str(new_car)+".png")
            slot += 1
            path = [x for x in section["path_from_start"]]
            path +=  section["slots"][slot]["path_from_section_start"]
            path.reverse()   
       
        if path:
            move = path.pop()
            map.move_to_tile(move)
            time.sleep(.1)
            event.direction = "car_moving"
            if not path:
                map.change_tile(move, 3, new_car-1)
                map.player.change_car_image("img/direction_24px.png")
                event.direction = "stop"  
        map.update(event.direction)
        
#        if event.direction != "car_moving":
        
        event.direction = "stop"  

        # Path file helper
        if action == "generate_path":
            if x != map.mapx or y != map.mapy:        
                 tile = [map.player.position[0], map.player.position[1]]
                 if tile not in new_path:
                     new_path.append(tile)
                     pathfile.write(str(tile)+",")
            x = map.mapx
            y = map.mapy 
       
  
        map.display(screen)
        clock.tick(FPS)
        pygame.display.update()
        event.update() 
    

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--generate_path", help="Generates path file path<random_number>", action="store_true")
    args = parser.parse_args()
 
    if args.generate_path:
        main("generate_path")
    else:
        main() 
