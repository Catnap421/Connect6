class CoordinateConverter(): 
    def __init__(self): 
        self.__posX = [28, 59, 90, 120, 150, 180, 210, 240, 270, 300, 330, 360, 390, 420, 450, 480, 510, 540, 570]
        self.__posY = [53, 84, 115, 145, 175, 205, 235, 265, 295, 325, 355, 385, 415, 445, 475, 505, 535, 565, 695]  
        # imagePosition        

    def ConvertBoardToImage(self, boardPosX, boardPosY):
        return (self.__posX[boardPosX] - 23, self.__posY[boardPosY] - 50)

    def ConvertImageToBoard(self, imagePosX, imagePosY):
        boardPosX = ((imagePosX - 28 - 15) // 30) + 1
        boardPosY = ((imagePosY - 53 - 15) // 30) + 1
        return (boardPosX, boardPosY) # board 좌표