import copy
import random

class Calculator():
    def __init__(self, color, gameStatus):
        self.weightBoard = [[0 for col in range(19)] for row in range(19)]
        self.color = color
        self.gameStatus = gameStatus

    def run(self, remain):
        nextPointPos = self.calculateNextPosbyPoint()
        self.calculateWeight(nextPointPos, self.color, remain, self.gameStatus.board)
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

    def calculateWeight(self, nextPos, color, remain, board):   
        self.weightBoard = [[0 for col in range(19)] for row in range(19)] 

        print(board)

        for pos in nextPos:
            x = pos[0]
            y = pos[1]
            weight = 0
            tempBoard = copy.deepcopy(board)
            tempBoard[y][x] = color
            weight += self.slideHorizontally(x, y, 6, color, remain, tempBoard)
            print(weight)
            weight += self.slideVertically(x, y, 6, color, remain, tempBoard)
            print(weight)
            weight += self.slideDiagonally1(x, y, 6, color, remain, tempBoard)
            print(weight)
            weight += self.slideDiagonally2(x, y, 6, color, remain, tempBoard)
            print(weight)
            weight += self.slideOpponentHorizontally(x, y, 6, 3 - color, remain, tempBoard)
            print(weight)
            weight += self.slideOpponentVertically(x, y, 6, 3 - color, remain, tempBoard)
            print(weight)
            weight += self.slideOpponentDiagonally1(x, y, 6, 3 - color, remain, tempBoard)
            print(weight)
            weight += self.slideOpponentDiagonally2(x, y, 6, 3 - color, remain, tempBoard)
            print(weight)
            self.weightBoard[y][x] = weight
 
        return 

    def slideHorizontally(self, x, y, n, color, remain, board):
        # n : window size
        # 만약 해당 위치에 돌을 둔다면
        minX = max(0, x - 5)
        maxX = min(18, x + 5)

        count = 0
        space = 0 # 그 사이에 빈 칸이 있냐 없냐에 따라 가중치를 다르게 (1 이나 2이냐는 남은 기회에 따라 중요도가 달라짐)

        window = []
        # init window
        for i in range(n):
            window.append(board[y][minX + i])

        countN = {
            "count6" : 0,
            "count5" : 0,
            "count4" : 0,
            "count3" : 0,
            "count2" : 0,
            "count1" : 0
        }


        for x in range(minX, maxX + 1):
            currentColor = board[y][x]
            if currentColor == 3 - color: # 다른 색상이면
                window = []
            if len(window) == n:
                window.pop(0)
            window.append(currentColor)
            try:
                count = 0
                for stone in window:
                    if stone == 3 - color:
                        raise Exception('상대돌 발견')
                    elif stone == color:
                        count += 1
                countN['count' + str(count)] += 1
            except Exception:
                continue

        if remain == 1: 
            weight = countN['count6'] * 10000 + countN['count5'] * 100 + countN['count4'] * 100 + countN['count3'] * 50 + countN['count2'] * 40 
        else:
            weight = countN['count6'] * 10000 + countN['count5'] * 10000 + countN['count4'] * 100 + countN['count3'] * 100 + countN['count2'] * 40 
        return weight

    def slideVertically(self, x, y, n, color, remain, board):
        minY = max(0, y - 5)
        maxY = min(18, y + 5)

        count = 0
        space = 0 

        window = []

        for i in range(n):
            window.append(board[minY + i][x])

        countN = {
            "count6" : 0,
            "count5" : 0,
            "count4" : 0,
            "count3" : 0,
            "count2" : 0,
        }


        for y in range(minY, maxY + 1):
            currentColor = board[y][x]
            if currentColor == 3 - color: 
                window = []
            if len(window) == n:
                window.pop(0)
            window.append(currentColor)
            try:
                count = 0
                for stone in window:
                    if stone == 3 - color:
                        raise Exception('상대돌 발견')
                    elif stone == color:
                        count += 1
                countN['count' + str(count)] += 1
            except Exception:
                continue

        if remain == 1: 
            weight = countN['count6'] * 10000 + countN['count5'] * 100 + countN['count4'] * 100 + countN['count3'] * 50 + countN['count2'] * 40
        else:
            weight = countN['count6'] * 10000 + countN['count5'] * 10000 + countN['count4'] * 100 + countN['count3'] * 100 + countN['count2'] * 40
        return weight
    
    def slideDiagonally1(self, x, y, n, color, remain, board):
        minX = max(0, x - 5)
        maxX = min(18, x + 5)
        minY = max(0, y - 5)
        maxY = min(18, y + 5)

        count = 0
        space = 0 

        window = []

        for i in range(n):
            window.append(board[minY + i][minX + i])

        countN = {
            "count6" : 0,
            "count5" : 0,
            "count4" : 0,
            "count3" : 0,
            "count2" : 0,
        }

        for i in range(2 * n - 1):
            try: 
                currentColor = board[minY + i][minX + i]
                if currentColor == 3 - color: 
                    window = []
                if len(window) == n:
                    window.pop(0)
                window.append(currentColor)

                count = 0
                for stone in window:
                    if stone == 3 - color:
                        raise Exception('상대돌 발견')
                    elif stone == color:
                        count += 1
                countN['count' + str(count)] += 1
            except Exception:
                continue
            except IndexError:
                continue


        if remain == 1: 
            weight = countN['count6'] * 10000 + countN['count5'] * 100 + countN['count4'] * 100 + countN['count3'] * 50 + countN['count2'] * 40
        else:
            weight = countN['count6'] * 10000 + countN['count5'] * 10000 + countN['count4'] * 100 + countN['count3'] * 100 + countN['count2'] * 40
        return weight

    def slideDiagonally2(self, x, y, n, color, remain, board):
        minX = max(0, x - 5)
        maxX = min(18, x + 5)
        minY = max(0, y - 5)
        maxY = min(18, y + 5)

        count = 0
        space = 0 

        window = []

        for i in range(n):
            window.append(board[minY + i][maxX - i])

        countN = {
            "count6" : 0,
            "count5" : 0,
            "count4" : 0,
            "count3" : 0,
            "count2" : 0,
        }

        for i in range(2 * n - 1):
            try: 
                currentColor = board[minY + i][maxX - i]
                if currentColor == 3 - color: 
                    window = []
                if len(window) == n:
                    window.pop(0)
                window.append(currentColor)

                count = 0
                for stone in window:
                    if stone == 3 - color:
                        raise Exception('상대돌 발견')
                    elif stone == color:
                        count += 1
                countN['count' + str(count)] += 1
            except Exception:
                continue
            except IndexError:
                continue


        if remain == 1: 
            weight = countN['count6'] * 10000 + countN['count5'] * 100 + countN['count4'] * 100 + countN['count3'] * 50 + countN['count2'] * 40
        else:
            weight = countN['count6'] * 10000 + countN['count5'] * 10000 + countN['count4'] * 100 + countN['count3'] * 100 + countN['count2'] * 40
        return weight
    
    def slideOpponentHorizontally(self, x, y, n, color, remain, board):
        # n : window size
        # 만약 해당 위치에 돌을 둔다면
        minX = max(0, x - 5)
        maxX = min(18, x + 5)

        count = 0
        space = 0 # 그 사이에 빈 칸이 있냐 없냐에 따라 가중치를 다르게 (1 이나 2이냐는 남은 기회에 따라 중요도가 달라짐)

        window = []
        # init window
        for i in range(n):
            window.append(board[y][minX + i])

        countN = {
            "count6" : 0,
            "count5" : 0,
            "count4" : 0,
            "count3" : 0,
            "count2" : 0,
            "count1" : 0
        }


        for x in range(minX, maxX + 1):
            currentColor = board[y][x]
            if currentColor == 3 - color: # 다른 색상이면
                window = []
            if len(window) == n:
                window.pop(0)
            window.append(currentColor)
            try:
                count = 0
                for stone in window:
                    if stone == 3 - color:
                        raise Exception('상대돌 발견')
                    elif stone == color:
                        count += 1
                countN['count' + str(count)] += 1
            except Exception:
                continue


        weight = countN['count6'] * 100000 + countN['count5'] * 100000 + countN['count4'] * 1000 + countN['count3'] * 1000 + countN['count2'] * 400 
        return weight

    def slideOpponentVertically(self, x, y, n, color, remain, board):
        minY = max(0, y - 5)
        maxY = min(18, y + 5)

        count = 0
        space = 0 

        window = []

        for i in range(n):
            window.append(board[minY + i][x])

        countN = {
            "count6" : 0,
            "count5" : 0,
            "count4" : 0,
            "count3" : 0,
            "count2" : 0,
        }


        for y in range(minY, maxY + 1):
            currentColor = board[y][x]
            if currentColor == 3 - color: 
                window = []
            if len(window) == n:
                window.pop(0)
            window.append(currentColor)
            try:
                count = 0
                for stone in window:
                    if stone == 3 - color:
                        raise Exception('상대돌 발견')
                    elif stone == color:
                        count += 1
                countN['count' + str(count)] += 1
            except Exception:
                continue

        weight = countN['count6'] * 100000 + countN['count5'] * 100000 + countN['count4'] * 1000 + countN['count3'] * 1000 + countN['count2'] * 400 

        return weight
    
    def slideOpponentDiagonally1(self, x, y, n, color, remain, board):
        minX = max(0, x - 5)
        maxX = min(18, x + 5)
        minY = max(0, y - 5)
        maxY = min(18, y + 5)

        count = 0
        space = 0 

        window = []

        for i in range(n):
            window.append(board[minY + i][minX + i])

        countN = {
            "count6" : 0,
            "count5" : 0,
            "count4" : 0,
            "count3" : 0,
            "count2" : 0,
        }

        for i in range(2 * n - 1):
            try: 
                currentColor = board[minY + i][minX + i]
                if currentColor == 3 - color: 
                    window = []
                if len(window) == n:
                    window.pop(0)
                window.append(currentColor)

                count = 0
                for stone in window:
                    if stone == 3 - color:
                        raise Exception('상대돌 발견')
                    elif stone == color:
                        count += 1
                countN['count' + str(count)] += 1
            except Exception:
                continue
            except IndexError:
                continue


        weight = countN['count6'] * 100000 + countN['count5'] * 100000 + countN['count4'] * 1000 + countN['count3'] * 1000 + countN['count2'] * 400 
        
        return weight

    def slideOpponentDiagonally2(self, x, y, n, color, remain, board):
        minX = max(0, x - 5)
        maxX = min(18, x + 5)
        minY = max(0, y - 5)
        maxY = min(18, y + 5)

        count = 0
        space = 0 

        window = []

        for i in range(n):
            window.append(board[minY + i][maxX - i])

        countN = {
            "count6" : 0,
            "count5" : 0,
            "count4" : 0,
            "count3" : 0,
            "count2" : 0,
        }

        for i in range(2 * n - 1):
            try: 
                currentColor = board[minY + i][maxX - i]
                if currentColor == 3 - color: 
                    window = []
                if len(window) == n:
                    window.pop(0)
                window.append(currentColor)

                count = 0
                for stone in window:
                    if stone == 3 - color:
                        raise Exception('상대돌 발견')
                    elif stone == color:
                        count += 1
                countN['count' + str(count)] += 1
            except Exception:
                continue
            except IndexError:
                continue
        
        weight = countN['count6'] * 100000 + countN['count5'] * 100000 + countN['count4'] * 1000 + countN['count3'] * 1000 + countN['count2'] * 400 

        return weight
    
    def __init_window(self):
        window = []

        return window
