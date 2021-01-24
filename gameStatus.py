class GameStatus():
    def __init__(self):
        self.boardPosition = [[0 for col in range(19)] for row in range(19)]
        self.__posX = [28, 59, 90, 120, 150, 180, 210, 240, 270, 300, 330, 360, 390, 420, 450, 480, 510, 540, 570]
        self.__posY = [53, 84, 115, 145, 175, 205, 235, 265, 295, 325, 355, 385, 415, 445, 475, 505, 535, 565, 695]  

    # def isConnect6(self, board, color):
        # for y in range(19):
        #     for x in range(19):
        #         try:
        #             if board[y][x] is color and board[y + 1][x] is color :
        #         else:

    def checkBoard(self, posX, posY, color):
        if self.boardPosition[posY][posX] is not 0:
            return (-1, -1)

        self.boardPosition[posY][posX] = color
        
        return (self.__posX[posX] - 23, self.__posY[posY] - 50)
    # def 두 개의 돌을 놓았는 지