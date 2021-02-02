# AI 코드 작성
"""
의사 코드

<미니맥스>



<알파 베타>

function alphabeta(node, depth, α, β, maximizingPlayer)
    if depth = 0 or node is a terminal node
        return the heuristic value of node
    if maximizingPlayer
        for each child of node
            α := max(α, alphabeta(child, depth - 1, α, β, FALSE))
            if β ≤ α
                break (* β cut-off *)
        return α
    else
        for each child of node
            β := min(β, alphabeta(child, depth - 1, α, β, TRUE))
            if β ≤ α
                break (* α cut-off *)
        return β

"""
""" 6개로 슬라이딩 윈도우 처럼 확인해서 4개 혹은 5개면 필히 두어야함"""
class Calculator():
    def __init__(self, color):
        self.weightBoard = [[0 for col in range(19)] for row in range(19)]
        self.color = color

    def calculateNextPos(self):
        nextPos = []
        maxWeight = 1

        for y in range(19):
            for x in range(19):
                weight = weightBoard[y][x]

                if weight > maxWeight :
                    maxWeight = weight
                    nextPos = [[x, y]]
                elif weight == maxWeight:
                    nextPos.append([x, y])

        return nextPos
    
    # def minimax(self, node, depth, color):
    #     # bestValue = [x, y, value]\
    #     if depth == 0:
    #         return (x, y, value)
    #     if maximizingPlayer
    #         bestValue := -∞
    #         for each child of node
    #             val := minimax(child, depth - 1, FALSE))
    #             bestValue := max(bestValue, val);
    #         return bestValue
    #     else
    #         bestValue := +∞
    #         for each child of node
    #             val := minimax(child, depth - 1, TRUE))
    #             bestValue := min(bestValue, val);
    #         return bestValue

    # 슬라이딩 윈도우처럼 6개의 윈도우 안에 몇 개의 돌이 있냐에 따라 가중치를 계산하자
    def initWeightBoard(self, board, pos):
        # 여기서 돌아야 할 예상 후보군을 먼저 선정 
        # pos : (x, y) 상대가 둔 돌의 위치
        posX = pos[0]
        posY = pos[1]
        minX = max(0, posX - 2)
        maxX = min(18, posX + 2)
        minY = max(0, posY - 2)
        maxY = min(18, posY + 2)

        for y in range(minY, maxY + 1):
            for x in range(minX, maxX + 1):
                if board[y][x] == 0:
                    self.weightBoard[y][x] = 1


    def calculateWeight(self, depth, color, remain, board):
        nextPos = self.calculateNextPos()
        
        for pos in nextPos:
            x = pos[0]
            y = pos[1]
            weight = 0
            weight += slideHorizontally(x, y, 6, color, remain, board)
            weight += slideVertically(x, y, 6, color, remain, board)
            weight += slideDiagonally1(x, y, 6, color, remain, board)
            weight += slideDiagonally2(x, y, 6, color, remain, board)

            weightBoard[y][x] = weight
        return weight

    def slideHorizontally(self, x, y, n, color, remain, board):
        # n : window size
        # 만약 해당 위치에 돌을 둔다면
        board[y][x] = color
        minX = max(0, x - 5)
        maxX = min(18, x + 5)

        count = 0
        space = 0 # 그 사이에 빈 칸이 있냐 없냐에 따라 가중치를 다르게 (1 이나 2이냐는 남은 기회에 따라 중요도가 달라짐)

        window = []
        # init window
        for i in range(n):
            window.append(board[y][minX + i])

        countN = {
            "count6" : 0
            "count5" : 0,
            "count4" : 0,
            "count3" : 0,
            "count2" : 0,
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
                countN['count' + count] += 1
            except Exception:
                continue

        if remain == 1: 
            weight = countN['count6'] * 10000 + countN['count5'] * 100 + countN['count4'] * 100 + countN['count3'] * 50 + countN['count2'] * 40
        else:
            weight = countN['count6'] * 10000 + countN['count5'] * 10000 + countN['count4'] * 100 + countN['count3'] * 100 + countN['count2'] * 40
        return weight

    def slideVertically(self, x, y, n, color, remain, board):
        board[y][x] = color
        minY = max(0, y - 5)
        maxY = min(18, Y + 5)

        count = 0
        space = 0 

        window = []

        for i in range(n):
            window.append(board[minY + i][x])

        countN = {
            "count6" : 0
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
                countN['count' + count] += 1
            except Exception:
                continue

        if remain == 1: 
            weight = countN['count6'] * 10000 + countN['count5'] * 100 + countN['count4'] * 100 + countN['count3'] * 50 + countN['count2'] * 40
        else:
            weight = countN['count6'] * 10000 + countN['count5'] * 10000 + countN['count4'] * 100 + countN['count3'] * 100 + countN['count2'] * 40
        return weight
    
    def slideDiagonally1(self, x, y, n, color, remain, board):
        board[y][x] = color
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
            "count6" : 0
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
                countN['count' + count] += 1
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
        board[y][x] = color
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
            "count6" : 0
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
                countN['count' + count] += 1
            except Exception:
                continue
            except IndexError:
                continue


        if remain == 1: 
            weight = countN['count6'] * 10000 + countN['count5'] * 100 + countN['count4'] * 100 + countN['count3'] * 50 + countN['count2'] * 40
        else:
            weight = countN['count6'] * 10000 + countN['count5'] * 10000 + countN['count4'] * 100 + countN['count3'] * 100 + countN['count2'] * 40
        return weight
    
    def __init_window(self):
        window = []

        return window