class CoordinateConverter(): 
    def __init__(self): 

        self.arrayPosition = [[0 for col in range(19)] for row in range(19)]
        self.__posX = [28, 59, 90, 120, 150, 180, 210, 240, 270, 300, 330, 360, 390, 420, 450, 480, 510, 540, 570]
        self.__posY = [53, 84, 115, 145, 175, 205, 235, 265, 295, 325, 355, 385, 415, 445, 475, 505, 535, 565, 695]  
        # imagePosition        

    def ConvertArrayToImage(self, arrayPosX, arrayPosY):
        return (self.__posX[arrayPosX] - 23, self.__posY[arrayPosY] - 50)

    def ConvertImageToArray(self, imagePosX, imagePosY):
        # 기준 28 <= x <= 570, 53 <= y <= 595
        arrayPosX = ((imagePosX - 28 - 15) // 30) + 1
        arrayPosY = ((imagePosY - 53 - 15) // 30) + 1
        if self.arrayPosition[arrayPosY][arrayPosX] == 1:
            return (False, False)

        self.arrayPosition[arrayPosY][arrayPosX] = 1
        
        
        return (self.__posX[arrayPosX] - 23, self.__posY[arrayPosY] - 50) # background 좌표