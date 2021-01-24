class GameStatus():
    def __init__(self):
        self.board = [[0 for col in range(19)] for row in range(19)]
        self.__posX = [28, 59, 90, 120, 150, 180, 210, 240, 270, 300, 330, 360, 390, 420, 450, 480, 510, 540, 570]
        self.__posY = [53, 84, 115, 145, 175, 205, 235, 265, 295, 325, 355, 385, 415, 445, 475, 505, 535, 565, 695]  

    def isConnect6(self, color):
        board = self.board
        for y in range(19):
            for x in range(19):
                try:
                    if board[y][x] is color and board[y + 1][x] is color and board[y + 2][x] is color \
                        and board[y + 3][x] is color and board[y + 4][x] is color and board[y + 5][x] is color:
                        return (color, True)
                    if board[y][x] is color and board[y][x + 1] is color and board[y][x + 2] is color \
                        and board[y][x + 3] is color and board[y][x + 4] is color and board[y][x + 5] is color:
                        return (color, True)
                    if board[y][x] is color and board[y + 1][x + 1] is color and board[y + 2][x + 2] is color \
                        and board[y + 3][x + 3] is color and board[y + 4][x + 4] is color and board[y + 5][x + 5] is color:
                        return (color, True)
                    if board[y][18 - x] is color and board[y + 1][18 - x + 1] is color and board[y + 2][18 - x + 2] is color \
                        and board[y + 3][18 - x + 3] is color and board[y + 4][18 - x + 4] is color and board[y + 5][18 - x + 5] is color:    
                        return (color, True)
                except IndexError:
                    continue
        print('아직')
        return (color, False)
                
    def checkBoard(self, posX, posY, color):
        if self.board[posY][posX] is not 0:
            return (-1, -1)

        self.board[posY][posX] = color
        
        return (self.__posX[posX] - 23, self.__posY[posY] - 50)
    # def 두 개의 돌을 놓았는 지