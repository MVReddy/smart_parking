"""

"""

__author__ = 'Obed N Munoz'
import pygame
import json_loader
from json_loader import loader
from a_star import AStar
import sys
import time
import json
import random
import argparse

def main(args):

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

    # Loading Paths (complete paths to all sections and from section start to parking slots)     
    filename = "maps/paths.json"
    path = []
    paths = loader.json_to_dict(filename)
    a_star = AStar(filename)
#    print a_star

    #initialize json loader, build tileset list, load player graphic
    initial = json_loader.Initialize(screen, TESTING, map_file, player_image_file, paths, 80)

    # initialize position of player when game first starts
    initial_position = (-4574,-4837)  
    map = json_loader.Map(initial, initial_position)
    map.move(initial_position[0], initial_position[1])
    #map.move_to_tile([146,153])

    # handle events such as keyboard / touchscreen presses
    event = json_loader.Event(initial)
    clock = pygame.time.Clock()

    # Generating pathfile 
    if args.generate_path:
        pathfile = open("path"+ str(random.randint(1,100)), 'w')
        new_path = []

    sections = paths["sections"]
    section = sections[0]

    slot = -1    
    new_car = 0
    [x,y] = [0,0]


    students = 10
#    path =  a_star.a_star(a_star.graph,"Caseta Policia")[0]
    

    while True:
        event.update()
    
        if event.direction == "start" and not path:
            #new_car = random.randint(1,10)  
            map.player.change_car_image("img/car_24px_"+str(students)+".png")
            astar =  a_star.a_star(a_star.graph,"Caseta Policia")
            path = astar[0]
            a_star.rebuild_graph(astar[1])
            #slot += 1
            #path = [x for x in section["path_from_start"]]
            #path +=  section["slots"][slot]["path_from_section_start"]
            #path.reverse()   
       
        if path:
            move = path.pop()
            map.move_to_tile(move)
            time.sleep(.1)
            event.direction = "car_moving"
            if not path:
                map.change_tile(move, 3, students-1)
                map.player.change_car_image("img/direction_24px.png")
                event.direction = "stop"  
                students = students - 1
        map.update(event.direction)
        
        event.direction = "stop"  

        # Path file helper
        if args.generate_path:
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
 
    main(args) 
