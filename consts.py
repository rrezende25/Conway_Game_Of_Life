import numpy as np
worldsize= (100,100)
class Templates():
    def Spacefiller_1(self):
        listatexto = [
        '.....O.O',
        '....O..O',
        '...OO',
        '..O',
        '.OOOO',
        'O....O',
        'O..O',
        'O..O',
        '.O.........OOO...OOO',
        '..OOOO.O..O..O...O..O',
        '...O...O.....O...O',
        '....O........O...O',
        '....O.O......O...O',
        '.',
        '...OOO.....OOO...OOO',
        '...OO.......O.....O',
        '...OOO......OOOOOOO',
        '...........O.......O',
        '....O.O...OOOOOOOOOOO',
        '...O..O..O............OO',
        '...O.....OOOOOOOOOOOO...O',
        '...O...O.............O...O',
        '....O...OOOOOOOOOOOO.....O',
        '.....OO............O..O..O',
        '........OOOOOOOOOOO...O.O',
        '.........O.......O',
        '..........OOOOOOO......OOO',
        '..........O.....O.......OO',
        '.........OOO...OOO.....OOO',
        '.',
        '...........O...O......O.O',
        '...........O...O........O',
        '...........O...O.....O...O',
        '........O..O...O..O..O.OOOO',
        '.........OOO...OOO.........O',
        '.........................O..O',
        '.........................O..O',
        '.......................O....O',
        '........................OOOO',
        '..........................O',
        '........................OO',
        '.....................O..O',
        '.....................O.O'
        ]
        size =(43,29)
        idealpos =(int((worldsize[0]-size[0])/2),int((worldsize[1]-size[1])/2))
        matrizerada = np.zeros(size)
        for i in range(len(listatexto)):
            for j in range(len(listatexto[i])):
                if listatexto[i][j] == 'O':
                    matrizerada[i,j] = 1
        pattern = self.AumentaOTamanho(matrizerada,idealpos)
        return pattern
    def Dart(self):
        listatexto = [
        ".......O",
        "......O.O",
        ".....O...O",
        "......OOO",
        ".",
        "....OO...OO",
        "..O...O.O...O",
        ".OO...O.O...OO",
        "O.....O.O.....O",
        ".O.OO.O.O.OO.O"
        ]
        size =(10,15)
        idealpos =(worldsize[0]-12,int((worldsize[1]-size[1])/2))
        matrizerada = np.zeros(size)
        for i in range(len(listatexto)):
            for j in range(len(listatexto[i])):
                if listatexto[i][j] == 'O':
                    matrizerada[i,j] = 1
        pattern = self.AumentaOTamanho(matrizerada,idealpos)
        return pattern
    def Gosper_glider_gun(self):
        listatexto = [
        "........................O",
        "......................O.O",
        "............OO......OO............OO",
        "...........O...O....OO............OO",
        "OO........O.....O...OO",
        "OO........O...O.OO....O.O",
        "..........O.....O.......O",
        "...........O...O",
        "............OO"
        ]
        size =(9,36)
        idealpos =(5,5)
        matrizerada = np.zeros(size)
        for i in range(len(listatexto)):
            for j in range(len(listatexto[i])):
                if listatexto[i][j] == 'O':
                    matrizerada[i,j] = 1
        pattern = self.AumentaOTamanho(matrizerada,idealpos)
        return pattern
    def Octagon_4(self):
        listatexto = [
        ".......OO.......",
        ".......OO.......",
        "................",
        "......OOOO......",
        ".....O....O.....",
        "....O......O....",
        "...O........O...",
        "OO.O........O.OO",
        "OO.O........O.OO",
        "...O........O...",
        "....O......O....",
        ".....O....O.....",
        "......OOOO......",
        "................",
        ".......OO.......",
        ".......OO......."
        ]
        size =(16,16)
        idealpos =(int((worldsize[0]-size[0])/2),int((worldsize[1]-size[1])/2))
        matrizerada = np.zeros(size)
        for i in range(len(listatexto)):
            for j in range(len(listatexto[i])):
                if listatexto[i][j] == 'O':
                    matrizerada[i,j] = 1
        pattern = self.AumentaOTamanho(matrizerada,idealpos)
        return pattern
    def Blinker_puffer_1(self):
        listatexto = [
        "...O",
        ".O...O",
        "O",
        "O....O",
        "OOOOO",
        ".",
        ".",
        ".",
        ".OO",
        "OO.OOO",
        ".OOOO",
        "..OO",
        ".",
        ".....OO",
        "...O....O",
        "..O",
        "..O.....O",
        "..OOOOOO"
        ]
        size =(18,9)
        idealpos =(int((worldsize[0]-size[0])/2),worldsize[1]-15)
        matrizerada = np.zeros(size)
        for i in range(len(listatexto)):
            for j in range(len(listatexto[i])):
                if listatexto[i][j] == 'O':
                    matrizerada[i,j] = 1
        pattern = self.AumentaOTamanho(matrizerada,idealpos)
        return pattern
    def AumentaOTamanho(self,pattern,pos):
        ClearWorld = np.zeros(worldsize)
        for row,col in np.ndindex(pattern.shape):
            print(pos[0],row, pos[1],col)
            ClearWorld[pos[0]+row, pos[1]+col]=pattern[row,col]
        return ClearWorld



