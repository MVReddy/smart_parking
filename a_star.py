#################################################################
#
# Monterrey Institute of Technology and Higher Education
# Master in Computer Sciences
#
# Final Project: Spart Parking using A-Star Algorithm for path finding
#
# Course:   Intelligent Systems
# Lecturer: Dr. Gildardo Sanchez 
#
# Team Members: Jose Ramon Obeso
#               Obed Nehemias Munoz Reynoso
#           
#################################################################

from json_loader import loader

class Node():

    def __init__(self, type, h):
        self.type = type
        self.h = h 
        self.neighbors = []
       
    def add_neighbor(self,neighbor):
        neighbor.parent = self 
        self.neighbors.append(neighbor)
    
    def add_section_neighbor(self, neighbor):
        self.neighbors.append(neighbor)

class AStar():

    def __init__(self, filename):
        self.build_graph(filename)
     
    def build_graph(self, filename):
        paths = loader.json_to_dict(filename)

        self.graph = Node("start", paths["destinations"])
        
        for section in paths["sections"]:
            section_neighbor = Node("section", section["destinations"])
            section_neighbor.name = section["name"] 
            section_neighbor.path_from_start = section["path_from_start"]  
            self.graph.add_neighbor(section_neighbor)
            for slot in section["slots"]:
                slot_neighbor = Node("slot", slot["destinations"])
                slot_neighbor.id = slot["id"]
                slot_neighbor.path_from_section_start = slot["path_from_section_start"] 
                slot_neighbor.status = slot["status"]
                slot_neighbor.type = slot["type"]
                section_neighbor.add_neighbor(slot_neighbor)           

            for section in paths["sections"]:
                if section["near_sections"]:                    
                    for current_section in self.graph.neighbors:
                        if current_section.name == section["name"]:
                            current_section.near_sections = section["near_sections"]
                            for near_section in current_section.near_sections:
                                for dest_section in self.graph.neighbors:
                                    for key in near_section:
                                        if dest_section.name == key: 
                                            current_section.add_section_neighbor(dest_section)
    def rebuild_graph(self, slot):
        for section in self.graph.neighbors:
            if slot.parent.name == section.name:
                section.neighbors.remove(slot) 

    def a_star(self,start,goal):
      
        closed_set = []
        open_set = [start]
        came_from = [] 

        g_score = 0
        f_score = g_score + self.get_h(start,goal)

        while open_set:
              current = self.get_lowest_f(open_set, goal)
              print current.type
              if current.type == "slot":
                 return [self.reconstruct_path(current, goal), current]
               
              open_set.remove(current)
              closed_set.append(current)
              
              for neighbor in current.neighbors:
                  if neighbor in closed_set:
                      continue
                  tentative_g_score = self.get_g(current) + self.distance_between(current, neighbor) 
                  if neighbor not in open_set or tentative_g_score < self.get_g(neighbor):

                     neighbor.came_from = current
                     neighbor.g = tentative_g_score
                     neighbor.f = neighbor.g + self.get_h(neighbor,goal) 
                     if neighbor not in open_set:
                         open_set.append(neighbor)   
        return None

    def get_lowest_f(self, open_set, goal):
        lowest = None
        for node in open_set:
            if not lowest:
                lowest = node 
            else:
                if self.get_f(node,goal) < self.get_f(lowest, goal):
                    lowest = node
        return lowest
    
    def get_g(self,node):
       try: 
           return node.g
       except AttributeError:
           pass    
       if node.type == "start": 
           g = 0
       elif node.type == "section":
           g = len(node.path_from_start) * 5       
       elif node.type == "slot":
           g = len(node.parent.path_from_start) * 5 + (node.path_from_section_start - 1) * 5
       return g
         
    def get_h(self,node, goal):
        
        for destination in node.h:
            if destination["name"] == goal:
                return destination["distance"]
   
    def get_f(self,node,goal):
        try:
            return node.f
        except AttributeError:
            pass 
        return get_g(node) + get_h(node,goal) 

    def reconstruct_path(self,node, goal):
        try:
            node.came_from
        except AttributeError:
            return []
        path = [] 
        while True:

            if node.type == "slot":
                path = node.path_from_section_start + path
                node = node.parent
            elif node.type == "section":
                try:
                    path = node.came_from.near_sections[goal] + path
                    node = node.came_from
                except AttributeError:
                    print 
                    path = node.path_from_start + path  
                    node = node.parent
            elif node.type == "start":
                path.reverse()
                return path 



    def distance_between(self, current, neighbor):
        if current.type == "section" and neighbor.type == "slot":
            return (len(neighbor.path_from_section_start) - 1) * 5
        elif current.type == "section" and neighbor.type == "section":
            
            return len(current.near_sections[0][neighbor.name]) * 5   
        else:
           return 0 
