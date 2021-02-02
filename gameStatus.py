from coordinateConverter import *

class GameStatus():
    # Class constants
    INF = float("inf")  # infinity
    NEG_INF = - float("inf")  # -infinity

    def __init__(self):
        self.board = [[0 for col in range(19)] for row in range(19)]
        self.turn = [1, 1] # 1 : black 2: white

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
                
    def checkBoard(self, boardPosX, boardPosY, color):
        if self.board[boardPosY][boardPosX] is not 0:
            return (-1, -1)
        self.board[boardPosY][boardPosX] = color

        return CoordinateConverter.ConvertBoardToImage(boardPosX, boardPosY)

    # def 두 개의 돌을 놓았는 지
    def setTurn(self):
        self.turn[1] += 1
        if self.turn[1] == 2:
            self.turn = [3 - self.turn[0], 0]

    def getTurn(self):
        return self.turn[0]

  