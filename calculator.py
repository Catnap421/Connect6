import copy
import random
import pprint
import logging
import os

logger = logging.getLogger()
logger.setLevel(logging.INFO)

formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')

if os.path.isfile('my.log'):    
    os.remove('my.log')

file_handler = logging.FileHandler('my.log')
file_handler.setFormatter(formatter)
logger.addHandler(file_handler)

class Calculator():
    def __init__(self, color, gameStatus):
        self.weightBoard = [[0 for col in range(19)] for row in range(19)]
        self.color = color
        self.gameStatus = gameStatus

    def run(self, remain):
        nextPointPos = self.calculateNextPosbyPoint()
        self.calculateWeightBoard(nextPointPos, self.color, remain, self.gameStatus.board)
        nextPos = self.calculateNextPosByWeight(nextPointPos)
        x,y = nextPos[random.randrange(len(nextPos))]
        print("by Weight:", x, y)
        return x, y

    def calculateNextPosbyPoint(self):
        nextPos = []
        maxWeight = 1

        for y in range(19):
            for x in range(19):
                weight = self.gameStatus.pointBoard[y][x]
                if weight == maxWeight:
                    nextPos.append([x, y])

        return nextPos

    def calculateNextPosByWeight(self, nextPointPos):
        nextPos = []
        maxWeight = 1

        for y in range(19):
            for x in range(19):
                weight = self.weightBoard[y][x]
                if weight > maxWeight :
                    maxWeight = weight
                    nextPos = [[x, y]]
                elif weight == maxWeight:
                    nextPos.append([x, y])

        if nextPos == []:
            nextPos = [nextPointPos[random.randrange(len(nextPointPos))]]
        return nextPos

    def calculateWeightBoard(self, nextPos, color, remain, board):   
        self.weightBoard = [[0 for col in range(19)] for row in range(19)] 

        for pos in nextPos:
            x = pos[0]
            y = pos[1]
            weight = 0
            tempBoard = copy.deepcopy(board)
            tempBoard[y][x] = 3 - color
            logger.info(f'{x}, {y}')
            weight += self.slideHorizontally(x, y, 6, 3 - color, remain, tempBoard)
            weight += self.slideVertically(x, y, 6, 3 - color, remain, tempBoard)
            weight += self.slideDiagonally1(x, y, 6, 3 - color, remain, tempBoard)
            weight += self.slideDiagonally2(x, y, 6, 3 - color, remain, tempBoard)

            tempBoard[y][x] = color
            weight += self.slideHorizontally(x, y, 6, color, remain, tempBoard)
            weight += self.slideVertically(x, y, 6, color, remain, tempBoard)
            weight += self.slideDiagonally1(x, y, 6, color, remain, tempBoard)
            weight += self.slideDiagonally2(x, y, 6, color, remain, tempBoard)

            self.weightBoard[y][x] = weight

        #pprint.pprint(self.weightBoard)
        return 

    def calculateWeight(self, color, remain, countN):
        """
        1. 내 돌이 6개가 되는 경우(6) : 1000000
        2. 상대가 6개가 완성 되는 경우(5, 6) : 400000
        3. 내가 공격을 완성하는 경우(4, 5) : 40000
        4. 상대가 공격을 완성하는 경우(3, 4) : 10000 / 5000
        5. 내가 공격 빌드업(2, 3): 300 / 1000

        """
        if color == self.color:
            if remain == 1: 
                weight = countN['count6'] * 1000000 \
                    + countN['count5'] * 40000 + countN['count4'] * 40000 \
                        + countN['count3'] * 300 \
                            + countN['count2'] * 100 
            else: # 내 첫 차례
                weight = countN['count6'] * 1000000 + countN['count5'] * 1000000 \
                    + countN['count4'] * 40000 + countN['count3'] * 40000 \
                        + countN['count2'] * 300 
        else :
            weight = countN['count6'] * 400000 + countN['count5'] * 200000 \
                + countN['count4'] * 10000 \
                    + countN['count3'] * 5000 \
                        + countN['count2'] * 400 

        return weight
        
    def slideHorizontally(self, x, y, n, color, remain, board):
        # n : window size
        minX, maxX = max(0, x - 5), min(18, x + 5)

        space = 0 # 그 사이에 빈 칸이 있냐 없냐에 따라 가중치를 다르게 (1 이나 2이냐는 남은 기회에 따라 중요도가 달라짐)

        window = []

        countN = {
            "count6" : 0, "count5" : 0, "count4" : 0, "count3" : 0, "count2" : 0
        }

        for x in range(minX, maxX + 1):
            self.calculateCount(window, countN, n, board[y][x], color)

        return self.calculateWeight(color, remain, countN)

    def slideVertically(self, x, y, n, color, remain, board):
        minY, maxY = max(0, y - 5), min(18, y + 5)


        space = 0 

        window = []

        countN = {
            "count6" : 0, "count5" : 0, "count4" : 0, "count3" : 0, "count2" : 0
        }

        for y in range(minY, maxY + 1):
            self.calculateCount(window, countN, n, board[y][x], color)

        return self.calculateWeight(color, remain, countN)
   
    def slideDiagonally1(self, x, y, n, color, remain, board):
        minX, minY, maxX, maxY = x, y, x, y

        i = 0
        while minX > 0 and minY > 0 and i <= 5:
            minX, minY = x - i, y - i
            i += 1

        i = 0
        while maxX < 18 and maxY < 18 and i <= 5:
            maxX, maxY = x + i, y + i
            i += 1

        space = 0 

        window = []

        countN = {
            "count6" : 0, "count5" : 0, "count4" : 0, "count3" : 0, "count2" : 0
        }

        slideLength = min(maxX - minX + 1, maxY - minY + 1)
        for i in range(slideLength):
            self.calculateCount(window, countN, n, board[minY + i][minX + i], color)
        return self.calculateWeight(color, remain, countN)

    def slideDiagonally2(self, x, y, n, color, remain, board):
        minX, minY, maxX, maxY = x, y, x, y

        i = 0
        while minX > 0 and maxY < 18 and i <= 5:
            minX, maxY = x - i, y + i
            i += 1

        i = 0
        while maxX < 18 and maxY > 0 and i <= 5:
            maxX, minY = x + i, y - i
            i += 1

        space = 0 

        window = []

        countN = {
            "count6" : 0, "count5" : 0, "count4" : 0, "count3" : 0, "count2" : 0
        }

        slideLength = min(maxX - minX + 1, maxY - minY + 1)

        for i in range(slideLength):
            self.calculateCount(window, countN, n, board[minY + i][maxX - i], color)

        return self.calculateWeight(color, remain, countN)

    def calculateCount(self, window, countN, n, value, color):
        opponentColor = 3 - color

        currentColor = value

        if len(window) == n:
            window.pop(0)
        window.append(currentColor)

        if len(window) != n:
            return

        count = 0

        try: 
            for stone in window:
                logger.info(f'{color}, {stone}, {window}')

                if stone == opponentColor:
                    raise Exception('상대돌 발견')
                elif stone == color:
                    count += 1
            countN['count' + str(count)] += 1
        except Exception:
          
            return
    
    def __init_window(self):
        window = []

        return window
