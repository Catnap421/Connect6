from coordinateConverter import *

class GameStatus():
    # Class constants
    INF = float("inf")  # infinity
    NEG_INF = - float("inf")  # -infinity

    def __init__(self):
        self.board = [[0 for col in range(19)] for row in range(19)]
        self.pointBoard = [[0 for col in range(19)] for row in range(19)]
        self.turn = [1, 1] # 1 : black 2: white
        self.count = 0
        self.start = False
    
    def isStart(self):
        return self.start

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
                    if board[y][18 - x] is color and board[y + 1][18 - (x + 1)] is color and board[y + 2][18 - (x + 2)] is color \
                        and board[y + 3][18 - (x + 3)] is color and board[y + 4][18 - (x + 4)] is color and board[y + 5][18 - (x + 5)] is color:    
                        return (color, True)
                except IndexError:
                    continue

        return (color, False)

    def isExist(self, boardX, boardY):
        return True if self.board[boardY][boardX] == 0 else False

    def checkBoard(self, boardX, boardY, color):
        if not self.isExist(boardX, boardY):
            return [None, None]

        self.count += 1
        self.board[boardY][boardX] = color

        self.pointBoard[boardY][boardX] = 0

        idx = 1
        if self.count > 8:
            idx = 2
            
        for y in range(boardY - idx, boardY + idx + 1):
            for x in range(boardX - idx, boardX + idx + 1):
                try: 
                    if self.board[y][x] == 0:
                        self.pointBoard[y][x] = 1
                except IndexError:
                    continue

        return CoordinateConverter.ConvertBoardToImage(boardX, boardY)

    # def 두 개의 돌을 놓았는 지
    def setTurn(self):
        self.turn[1] += 1
        if self.turn[1] == 2:
            self.turn = [3 - self.turn[0], 0]

    def getTurn(self):
        return self.turn[0]

  