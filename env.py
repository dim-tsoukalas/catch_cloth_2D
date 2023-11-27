import os
import pygame
import sys
import time
import pickle

import numpy

######################################################################################################
################################                             #########################################
################################       Class Screen          #########################################
################################                             #########################################
######################################################################################################
class Screen():
    def __init__(self, width, height):
        pygame.init()

        self.width = width
        self.height = height

        # Initialize Screen variables
        self.screen = pygame.display.set_mode((width, height))
        pygame.display.set_caption("Cloth Simulation")

        self.cloth = Cloth(width, height)
        self.hand = Hand(width,height)

        # Normalize the closh position height --LOWEST POINT--
        self.extend_cloth_height = 180

        self.episode = 0
        # Get cloth x, y from real cloth moving
        self.cloth_x, self.cloth_y = self._get_cloth_dimensions_from_files(self.extend_cloth_height, self.episode)
        self.count_cloth_movements = 0

        # Initialize Episode parameters
        # These parameters are used to keep the hand moving during the loop
        self.pressedDown = False
        self.pressedUp = False

        # reset cloth and hand possitions
        self.cloth.pos = [self.cloth_x[0], self.cloth_y[0]]
        self.hand.pos = [self.width // 2, self.height - self.hand.size]


    ##########################
    #####   def reset()  #####
    ##########################

    def reset(self):
        self.pressedDown = False
        self.pressedUp = False
        self.timer = 0

        self.episode +=1 
        # reset cloth and hand possitions
        self.cloth_x, self.cloth_y = self._get_cloth_dimensions_from_files(self.extend_cloth_height, self.episode)
        self.cloth.pos = [self.cloth_x[0], self.cloth_y[0]]
        self.count_cloth_movements = 0
        self.hand.pos = [424, self.height - self.hand.size]
    
    ##########################
    ######   def step()  #####
    ##########################
    def step(self, action):

        state = []
        done = False
        reward = 0

        # Get the previous state if exists,
        # else get the same state

        if self.count_cloth_movements == 0:
            previous_cloth_cords = [0,0]
        else:
            previous_cloth_cords =[self.cloth_x[self.count_cloth_movements-1], self.cloth_y[self.count_cloth_movements-1]]

        # Just the pygame initializations
        clock = pygame.time.Clock()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
                
        ## These statements control the movement of the hand ##
        # If action[0] is 1 go UP
        if action[0] == 1 or self.pressedUp:
            self.pressedUp = True
            self.pressedDown = False
            if self.hand.pos[1] > 364-self.extend_cloth_height:
                self.hand.pos[1] -= self.hand.speed
            else:
                self.pressedUp = False
                self.pressedDown = False

        # If action[0] is 0 go DOWN
        if action[0] == 0 or self.pressedDown:
            self.pressedDown = True
            self.pressedUp = False
            if self.hand.pos[1] < self.height - self.hand.size:
                self.hand.pos[1] += self.hand.speed
            else:
                self.pressedDown = False
                self.pressedUp = False

        # For every step the cloth position changes
        self.cloth.pos[0] = self.cloth_x[self.count_cloth_movements]
        self.cloth.pos[1] = self.cloth_y[self.count_cloth_movements]

        
        # Initialize the catching cloth checking (Just to be more organized)
        cloth_catched = (
            self.cloth.pos[0] < self.hand.pos[0] < self.cloth.pos[0] + self.cloth.size and
            self.cloth.pos[1] < self.hand.pos[1] < self.cloth.pos[1] + self.cloth.size
            )
    
        state = [[previous_cloth_cords], self.cloth.pos, self.hand.pos]
        
        # Get reward if close the fingers at right time
        if action[1] == 1:
            if cloth_catched:
                reward = 100
                done = True
                return state, reward, done
            else:
                reward = -100
                return state, reward, done

        reward-=1
        

        # this parameter used to change the cloth movement for every step
        self.count_cloth_movements+=1                    

        # Refresh screen for animations
        self.screen.fill((255, 255, 255))
        self.cloth.draw(self.screen)
        self.hand.draw(self.screen)
        pygame.display.flip()
        clock.tick(60)

        return state, reward, done
        
    ########################################################################
    #####   def _get_cloth_dimensions_from_files(extend_cloth_height)  #####
    ########################################################################
    def _get_cloth_dimensions_from_files(self, extend_cloth_height, episode):

        # Positions_X
        if episode == 0:
            x_filename = 'positions_x/positions_x.txt'
            y_filename = 'positions_y/positions_y.txt'
        else:
            x_filename = f'positions_x_{episode}.txt'
            y_filename = f'positions_y_{episode}.txt'

        with open(x_filename, 'rb') as f:
            x = pickle.load(f)

        with open(y_filename, 'rb') as f:
            y = pickle.load(f)
            ar = numpy.array(y)
        y=ar-extend_cloth_height
        return x, y


######################################################################################################
################################                             #########################################
################################         Class Cloth         #########################################
################################                             #########################################
######################################################################################################

class Cloth:
    def __init__(self, width, height):
        self.size = 50
        self.color = (255, 0, 0)
        self.pos = 0,0
        self.speed = 3

    def draw(self, screen):
        pygame.draw.rect(screen, self.color, (self.pos[0], self.pos[1], self.size, self.size))
        
######################################################################################################
################################                             #########################################
################################         Class Hand          #########################################
################################                             #########################################
######################################################################################################
class Hand:
    def __init__(self, width, height):
        self.size = 50
        self.color = (0, 0, 255)
        self.pos = [width // 2, height - self.size]
        self.speed = 5.3

    def draw(self, screen):
        pygame.draw.polygon(screen, self.color, [
                (self.pos[0], self.pos[1]),
                (self.pos[0] - self.size // 2, self.pos[1] + self.size),
                (self.pos[0] + self.size // 2, self.pos[1] + self.size)
            ])