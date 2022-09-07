import pygame
from pygame.locals import *
import sys #talvez so o exit
import random #talvez só o randint
import time #parece util para testes de velocidade 
import numpy as np #ajuda a trabalhar com matriz
import consts

# gera o tema seja com efeitos ou não:
class game:
    def __init__(self):
        #criando a tela do jogo
        pygame.init()
        # pygame.mixer.init() se for colocar som
        self.tela = pygame.display.set_mode((consts.LARGURA, consts.ALTURA))
        pygame.display.set_caption('game of life')
        self.relogio = pygame.time.Clock()
        self.esta_rodando = True
    def load_theme(self,tema):
        self.Grid = tema[0]
        self.Alive = tema[1]
        self.Dead = tema[2]
    def gen_clear_world(self,size):
        self.cell_size = int(consts.ALTURA / size)
        clear_world = np.zeros((size,size))
        return clear_world
    def gen_preset_world(self,preset):
        self.cell_size = preset.cellsize
        preset_world = preset
        return preset_world
    def update_world(self,world):
        updated_world = np.zeros(world.shape)
        for row, col in np.ndindex(world.shape):
            if row == 0:
                rowinit = 0
            else:
                rowinit = row - 1
            if col == 0:
                colinit = 0
            else:
                colinit = col - 1
            alive = np.sum(world[rowinit:row+2,colinit:col+2]) - world[row,col]
            if world[row,col] == 1 :
                if 2 <= alive <= 3 :
                    updated_world[row,col] = 1
            else:
                if alive == 3 :
                    updated_world[row,col] = 1
        return updated_world
    def draw_in_world(self,world):
        if pygame.mouse.get_pressed()[0]:
            pos = pygame.mouse.get_pos()
            if world[pos[1]//self.cell_size,pos[0]//self.cell_size] == 1:
                world[pos[1]//self.cell_size,pos[0]//self.cell_size] = 0
            else:
                world[pos[1]//self.cell_size,pos[0]//self.cell_size] = 1
        return world
    def draw_world(self,world):
        self.tela.fill(self.Grid)
        for row , col in np.ndindex(world.shape):
            if world[row,col] == 1:
                pygame.draw.rect(self.tela,self.Alive,(col*self.cell_size,row*self.cell_size,self.cell_size-1,self.cell_size-1))
            else:
                pygame.draw.rect(self.tela,self.Dead,(col*self.cell_size,row*self.cell_size,self.cell_size-1,self.cell_size-1))
        pygame.display.flip()
       
# menu principal:
    # texto explicando comandos basicos do jogo
    #botao que define se vai ser gerado em branco com tamanho escolhido ou com predefinicoes:
    # tem como escolher o tamanho do mundo com input
    # leva para o menu de predefinicoes
    # leva para o menu de temas
    # leva para uma pagina que fala sobre o jogo e explica as regras



# def main_menu(state):
#     MainMenu = state
#     while MainMenu == True:
#         tela.fill((255,0,0))
#         for event in pygame.event.get():
#             if event.type == QUIT:
#                 pygame.quit()
#                 sys.exit()
#         if pygame.mouse.get_pressed()[0]:
#             MainMenu = False
#             mundo =gerar_mundo_limpo()
#             no_mundo(True,mundo)
#         pygame.display.update()
        
#     return

g = game()
running = False
world = g.gen_clear_world(10)
g.load_theme(consts.TRADICIONAL)
world[0,0]=1

while True:
    # fecha o jogo
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
        if event.type == KEYUP:
            if event.key == K_SPACE:
                running = not running
    g.draw_world(world)
    world = g.draw_in_world(world)
    g.draw_world(world)
    if running :
        world = g.update_world(world)
        time.sleep(0.1)
    g.draw_world(world)
    
            
    
    
    pygame.display.update()

