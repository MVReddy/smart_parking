"""

"""

__author__ = 'Obed N Munoz'
import pygame
import json_loader



def main():

    # initialize pygame
    pygame.init()
    # set screen size of phone or desktop window.  Adjust to your phone
    screen = pygame.display.set_mode((1024, 768))
    pygame.display.set_caption("Use keyboard arrow keys or mouse.  Press TEST to toggle overlay")
    

    # game framerate.  Higher number is faster
    FPS = 40

    # change the file names to your player graphic and map file
    player_image_file = "img/boy_32px.png"
    map_file = "maps/mega_map.json"

    # change to False (with capital F) to turn off red squares over
    # collision rectangles
    TESTING = True

    #initialize json loader, build tileset list, load player graphic
    initial = json_loader.Initialize(screen, TESTING, map_file, player_image_file)

    # initialize position of player when game first starts
    initial_position = (-4574,-4837)  
    map = json_loader.Map(initial, initial_position)
    map.move(initial_position[0], initial_position[1])

    # handle events such as keyboard / touchscreen presses
    event = json_loader.Event(initial)
    clock = pygame.time.Clock()

    [x,y] = [0,0]
    while True:
        event.update()
        map.update(event.direction)
        
#        if event.direction == "start":
        event.direction = "stop"  

        # Paths Creation Helpers
        if x != map.mapx or y != map.mapy:        
             print [[map.mapx,map.mapy], "-->", [map.player.position[0]], map.player.position[1]] 
        x = map.mapx
        y = map.mapy 
  
        map.display(screen)
        clock.tick(FPS)
        pygame.display.update()
        event.update()                                                                                  

if __name__ == "__main__":
    main()
