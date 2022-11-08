import numpy as np
from kivy.app import App
from kivy.uix.screenmanager import ScreenManager,Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.graphics import Color,Rectangle,Ellipse
from kivy.clock import Clock
from kivy.lang.builder import Builder
import consts 
Patterns = consts.Templates()

                        #telas de menu
class Gerenciador(ScreenManager): #classe que gerencia as paginas do aplicatico
    pass
class MainMenu(Screen): #pagina que explica sobre automato celular e leva para os dois projetos
    pass
class GameOfLife(Screen): # pagina que explica sobre os ditos jogos da vida e leva para os dois tipos que simulamos
    pass
class Sandpile(Screen): #pagina que descreve o sandpile e configura a simulacao
    pass

                        # parte dos quadrados
class SquareLife(Screen): #pagina onde tudo do jogo da vida dos quadrados acontece
    def __init__(self, **kw):
        super().__init__(**kw)
        self.add_widget(SquareMenu())
    def DrawSimulation(self,cells):
        layout = BoxLayout(orientation='vertical')
        layout.add_widget(InSimulationOptions())        
        layout.add_widget(SquareLifeSimulation(cells))
        self.remove_widget(self.children[0])
        self.add_widget(layout)
    def DrawTemplatesmenu(self):
        self.remove_widget(self.children[0])
        self.add_widget(SquareTemplates())
        
class SquareMenu(BoxLayout): # widget que contem o menu do jogo da vida dos quadrados
    def GenClearWorld(self):
        size = (self.ids.SizeSquare.text).split(',')
        sizex = int(size[0])
        sizey = int(size[1])
        cellsmatrix = np.zeros((sizey,sizex))
        self.parent.DrawSimulation(cellsmatrix)
    def GenTemplate(self):
        self.parent.DrawTemplatesmenu()
        
class SquareTemplates(BoxLayout): # widget com estruturas interessantes dos quadrados
    def RunTemplate(self,nome):
        if nome == 'Spacefiller_1':
            cells = Patterns.Spacefiller_1()
            self.parent.DrawSimulation(cells)
        if nome == 'Dart':
            cells = Patterns.Dart()
            self.parent.DrawSimulation(cells)
        if nome == 'Gosper_glider_gun':
            cells = Patterns.Gosper_glider_gun()
            self.parent.DrawSimulation(cells)
        if nome == 'Octagon_4':
            cells = Patterns.Octagon_4()
            self.parent.DrawSimulation(cells)
        if nome == 'Blinker_puffer_1':
            cells = Patterns.Blinker_puffer_1()
            self.parent.DrawSimulation(cells)

class SquareLifeSimulation(BoxLayout): # widget de simulacao(recebe uma matriz com as celulas)
    def __init__(self,cells, **kwargs):
        super().__init__(**kwargs)
        self.CellsMatrix = cells
        self.Cells = []
        for row in np.ndindex(cells.shape[0]):
            cellcol = []
            for col in np.ndindex(cells.shape[1]):
                cellcol.append([])
            self.Cells.append(cellcol)
        with self.canvas:
            Color(rgb=(1,0,0))
            self.Grid = Rectangle(pos=(self.pos),size=(self.size))
        self.DrawCells()
        self.bind(pos=self.UpdateSizes)
        self.bind(size=self.UpdateSizes)

    def UpdateSizes(self, *args): # arruma o tamanho da simulacao quando a tela muda de resolucao.
        self.cellsizex = self.size[0]/len(self.Cells[0])
        self.cellsizey = self.size[1]/len(self.Cells)
        self.Grid.pos = self.pos
        self.Grid.size = self.size
        for row in range(len(self.Cells)):
            for col in range(len(self.Cells[0])):
                self.Cells[row][col][1].pos = (col*self.cellsizex,row*self.cellsizey)
                self.Cells[row][col][1].size = (self.cellsizex-1,self.cellsizey-1)

    def DrawCells(self): #desenha de acordo com a matriz inicial os quadrados com suas cores.
        self.cellsizex = self.size[0]/len(self.Cells[0])
        self.cellsizey = self.size[1]/len(self.Cells)
        for row in range(len(self.Cells)):
            for col in range(len(self.Cells[0])):
                with self.canvas:
                    if self.CellsMatrix[row,col]==1:
                            self.Cells[row][col].append(Color(rgb=(0,0,0)))
                    else:
                            self.Cells[row][col].append(Color(rgb=(1,1,1)))
                    self.Cells[row][col].append(Rectangle(pos=(col*self.cellsizex,row*self.cellsizey),size=(self.cellsizex-1,self.cellsizey-1)))

    def on_touch_down(self, touch): #possibilita desenhar com click do mouse
        if self.collide_point(touch.x,touch.y):
            cellcol = int(touch.pos[0]/self.cellsizex)
            cellrow = int(touch.pos[1]/self.cellsizey)
            self.MouseDraw(cellcol,cellrow)
        return super().on_touch_down(touch)    

    def on_touch_move(self, touch): #possibilita desenhar com movimento do mouse
        if self.collide_point(touch.x,touch.y):
            cellcol = int(touch.pos[0]/self.cellsizex)
            cellrow = int(touch.pos[1]/self.cellsizey)
            if self.pastcell != (cellrow,cellcol):
                self.MouseDraw(cellcol,cellrow)
        return super().on_touch_move(touch)

    def MouseDraw(self,cellcol,cellrow): # desenha e atualiza a matriz das celulas
        if self.CellsMatrix[cellrow,cellcol] == 0:
            self.CellsMatrix[cellrow,cellcol] = 1
            self.Cells[cellrow][cellcol][0].rgb = [0,0,0]
        else:
            self.CellsMatrix[cellrow,cellcol] = 0
            self.Cells[cellrow][cellcol][0].rgb = [1,1,1]
        self.pastcell = (cellrow,cellcol)

    def RunWorld(self,*kw): # roda as geracoes do mundo
        UpdatedWorld = np.zeros(self.CellsMatrix.shape)
        for row,col in np.ndindex(UpdatedWorld.shape):
            if row == 0:
                rowinit = 0
            else: 
                rowinit = row -1
            if col == 0:
                colinit = 0
            else:
                colinit = col -1
            alive =np.sum(self.CellsMatrix[rowinit:row+2,colinit:col+2]) - self.CellsMatrix[row,col]
            if self.CellsMatrix[row,col] == 1 :
                if 2 <= alive <= 3 :
                    UpdatedWorld[row,col]=1
                else:
                    self.Cells[row][col][0].rgb = [1,1,1]
            else:
                if alive == 3 :
                    UpdatedWorld[row,col]=1
                    self.Cells[row][col][0].rgb = [0,0,0]
        self.CellsMatrix = UpdatedWorld

    def ClearWorld(self): # limpa a matriz e a tela
        self.CellsMatrix = np.zeros(self.CellsMatrix.shape)
        for row,col in np.ndindex(self.CellsMatrix.shape):
            self.Cells[row][col][0].rgb = [1,1,1]


class InSimulationOptions(BoxLayout): # menu com algumas opcoes dentro da simulacao( chama o RunWorld e o ClearWorld)
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.running = False
        self.GenSpeed = -1
    def Clear(self):
        self.parent.children[0].ClearWorld()#limpa o tabuleiro
        if self.running:
            self.Generation.cancel()
            self.running = not self.running
            self.GenSpeed = -1  
    def run(self,*kw):
        if not self.running:
            self.Generation = Clock.schedule_interval(self.parent.children[0].RunWorld,30/60)
            self.GenSpeed= 30/60
        else:
            self.Generation.cancel()
            self.GenSpeed = -1
        self.running = not self.running
    def slow(self,*kw):
        if self.GenSpeed > 0 :
            self.Generation.timeout +=5/60
            self.GenSpeed = self.GenSpeed + 5/60
    def speed(self,*kw):
        if self.GenSpeed >= 6/60 :
            self.Generation.timeout -=5/60
            self.GenSpeed = self.GenSpeed - 5/60


        #   parte do hexagono
class HexagonLife(Screen):
    def __init__(self, **kw):
        super().__init__(**kw)
        self.add_widget(HexagonMenu())

    def DrawSimulation(self,cells,survives,borns):
        layout = BoxLayout(orientation='vertical')
        layout.add_widget(InSimulationOptions())        
        layout.add_widget(HexagonLifeSimulation(cells,survives,borns))
        self.remove_widget(self.children[0])
        self.add_widget(layout)


class HexagonMenu(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def GenClearWorld(self):
        size = (self.ids.SizeHexagon.text).split(',')
        sizex = int(size[0])
        sizey = int(size[1])
        survivebtns = self.ids.survivebtns.children
        bornbtns = self.ids.bornbtns.children
        SurviveRange = []
        BornRange = []
        for i in range(len(bornbtns)):
            if survivebtns[i].state == 'down':
                SurviveRange.append(int(survivebtns[i].text))
            if bornbtns[i].state == 'down':
                BornRange.append(int(bornbtns[i].text))  
        cellsmatrix = np.zeros((sizey,sizex))
        self.parent.DrawSimulation(cellsmatrix,SurviveRange,BornRange)


class HexagonTemplates(BoxLayout):
    pass
class HexagonLifeSimulation(BoxLayout):
    def __init__(self,cells,survives,borns, **kwargs):
        super().__init__(**kwargs)
        self.CellsMatrix = cells
        self.SurviveRange = survives
        self.BornRange = borns
        self.Cells = []
        for row in np.ndindex(cells.shape[0]):
            cellcol = []
            for col in np.ndindex(cells.shape[1]):
                cellcol.append([])
            self.Cells.append(cellcol)
        with self.canvas:
            Color(rgb=(1,0,0))
            self.Grid = Rectangle(pos=(self.pos),size=(self.size))
        self.DrawCells()
        self.bind(pos=self.UpdateSizes)
        self.bind(size=self.UpdateSizes)

    def UpdateSizes(self, *args): # arruma o tamanho da simulacao quando a tela muda de resolucao.
        self.cellsizex = self.size[0]/(len(self.Cells[0])+0.5) 
        self.cellsizey = self.size[1]/(1+0.75*(len(self.Cells)-1))
        self.Grid.pos = self.pos
        self.Grid.size = self.size
        for row in range(len(self.Cells)):
            for col in range(len(self.Cells[0])):
                if row%2 == 0:
                    posx = col*self.cellsizex
                else:
                    posx =0.5*self.cellsizex*0.934+ col*self.cellsizex
                posy = 0 +0.75*self.cellsizey*row
                self.Cells[row][col][1].pos = (posx,posy)
                self.Cells[row][col][1].size = (self.cellsizex,self.cellsizey*0.868)

    def DrawCells(self): #desenha de acordo com a matriz inicial os quadrados com suas cores.
        self.cellsizex = self.size[0]/(len(self.Cells[0])+0.5)
        self.cellsizey = self.size[1]/(1+0.75*(len(self.Cells)-1))
        for row in range(len(self.Cells)):
            for col in range(len(self.Cells[0])):
                with self.canvas:
                    if self.CellsMatrix[row,col]==1:
                            self.Cells[row][col].append(Color(rgb=(0,0,0)))
                    else:
                            self.Cells[row][col].append(Color(rgb=(1,1,1)))
                    if row%2 == 0:
                        posx = col*self.cellsizex
                    else:
                        posx =0.5*self.cellsizex*0.934+ col*self.cellsizex
                    posy = 0 +0.75*self.cellsizey*row
                    self.Cells[row][col].append(Ellipse(pos=(posx,posy),size=(self.cellsizex,self.cellsizey*0.868),segments=6))

    def on_touch_down(self, touch): #possibilita desenhar com click do mouse
        if self.collide_point(touch.x,touch.y):
            cellrow = int(touch.pos[1]/(self.cellsizey*0.75))
            if cellrow >len(self.Cells)-1:
                cellrow = len(self.Cells)-1
            if cellrow%2 == 0:
                touchposx = touch.pos[0]
                tamanhodalinha = self.cellsizex*len(self.Cells[0])
                if touchposx > tamanhodalinha:
                    touchposx = tamanhodalinha-1
                cellcol = int(touchposx/(self.cellsizex))
            else:
                touchposx = touch.pos[0]-0.5*self.cellsizex*0.934-1
                tamanhodalinha = self.cellsizex*len(self.Cells[0])
                if touchposx < self.size[0]-tamanhodalinha:
                    touchposx = self.size[0]-tamanhodalinha+1
                cellcol = int(touchposx/(self.cellsizex))
            self.MouseDraw(cellcol,cellrow)
        return super().on_touch_down(touch)  

    def on_touch_move(self, touch): #possibilita desenhar com movimento do mouse
        if self.collide_point(touch.x,touch.y):
            cellrow = int(touch.pos[1]/(self.cellsizey*0.75))
            if cellrow >len(self.Cells)-1:
                cellrow = len(self.Cells)-1
            if cellrow%2 == 0:
                touchposx = touch.pos[0]
                tamanhodalinha = self.cellsizex*len(self.Cells[0])
                if touchposx > tamanhodalinha:
                    touchposx = tamanhodalinha-1
                cellcol = int(touchposx/(self.cellsizex))
            else:
                touchposx = touch.pos[0]-0.5*self.cellsizex*0.934-1
                tamanhodalinha = self.cellsizex*len(self.Cells[0])
                if touchposx < self.size[0]-tamanhodalinha:
                    touchposx = self.size[0]-tamanhodalinha+1
                cellcol = int(touchposx/(self.cellsizex))
            if self.pastcell != (cellrow,cellcol):
                self.MouseDraw(cellcol,cellrow)
        return super().on_touch_move(touch)

    def MouseDraw(self,cellcol,cellrow): # desenha e atualiza a matriz das celulas
        if self.CellsMatrix[cellrow,cellcol] == 0:
            self.CellsMatrix[cellrow,cellcol] = 1
            self.Cells[cellrow][cellcol][0].rgb = [0,0,0]
        else:
            self.CellsMatrix[cellrow,cellcol] = 0
            self.Cells[cellrow][cellcol][0].rgb = [1,1,1]
        self.pastcell = (cellrow,cellcol)
        
    def RunWorld(self,*kw): # roda as geracoes do mundo
        UpdatedWorld = np.zeros(self.CellsMatrix.shape)
        for row,col in np.ndindex(UpdatedWorld.shape):
            if row == 0:
                rowinit = 0
            else: 
                rowinit = row -1
            if col == 0:
                colinitpar = 1
                colinitimpar =0
                faltaimpar = 0
            else:
                colinitpar = col
                colinitimpar = col
                faltaimpar = self.CellsMatrix[row,col-1]
            if col == len(self.CellsMatrix)-1:
                faltapar=0
            else:
                faltapar=self.CellsMatrix[row,col+1]
            if row%2 == 0:
                alive =np.sum(self.CellsMatrix[rowinit:row+2,colinitpar-1:col+1]) - self.CellsMatrix[row,col] +faltapar
            else:
                alive =np.sum(self.CellsMatrix[rowinit:row+2,colinitimpar:col+2]) - self.CellsMatrix[row,col] +faltaimpar
            if self.CellsMatrix[row,col] == 1 :
                if alive in self.SurviveRange :
                    UpdatedWorld[row,col]=1
                else:
                    self.Cells[row][col][0].rgb = [1,1,1]
            else:
                if alive in self.BornRange :
                    UpdatedWorld[row,col]=1
                    self.Cells[row][col][0].rgb = [0,0,0]
        self.CellsMatrix = UpdatedWorld

    def ClearWorld(self): # limpa a matriz e a tela
        self.CellsMatrix = np.zeros(self.CellsMatrix.shape)
        for row,col in np.ndindex(self.CellsMatrix.shape):
            self.Cells[row][col][0].rgb = [1,1,1]


            #parte do sandpile
class Sandpile(Screen):
    # descricao do abelian sandpile
    # configuracoes da simulacao
    # vai para tela com a simulacao
    pass
class SandpileSimulation(Screen):
    pass


                # inicializacao
class CellularAutomata(App):
    def build(self):
        return Builder.load_file('./kvfile/CellularAutomata.kv')
CellularAutomata().run()

