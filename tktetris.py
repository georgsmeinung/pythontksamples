"""
Tetris Clone
------------
Modified version to use Tk
"""
from tkinter import *
from datetime import *
from random import *
from ctypes import windll
from tkinter import font as tkfont

#setting for avoinding blurred GUI in Windows 11
#with high DPI
#https://stackoverflow.com/questions/41315873/attempting-to-resolve-blurred-tkinter-text-scaling-on-windows-10-high-dpi-disp
windll.shcore.SetProcessDpiAwareness(1)

BOARD_WIDTH = 10
BOARD_HEIGHT = 20
TILE_SIZE = 50
TILE_MARGIN = 2
REFRESH_INTERVAL = 100
LEVEL_ACCELERATION = 10

#Logic init
board = list()
level = 1
piecesMax = 7
currentPace = 400
fallingPiece = oldPiece = canvas = window = None
oldCol = oldRow = 0
points = 0

pieceColor = {
    0: "black", #Color for Empty cell
    1: "yellow", #Color for the "O", square or "Smashboy" piece 
    2: "deep sky blue", #Color for the "I", stick or "Hero" piece
    3: "red3", #Color for the "Z", dog left or "Cleveland Z" piece
    4: "chartreuse2", #Color for the "S", dog right or "Rhode Island Z" piece
    5: "purple3", #Color for the "T" or "Teewee" piece
    6: "DarkOrange2", #Color for the "L", periscope left or "Orange Ricky" piece
    7: "blue" #Color for the "J", periscope right or "Blue Ricky" piece 
}

pieceMap = {
    #The "O" or square piece
    1: [
        [1,1],
        [1,1]],
    #The "I" of stick piece
    2: [
        [2],
        [2],
        [2],
        [2]],
    #The "Z", dog looking left or "Cleveland Z" piece
    3: [
        [0,3,3],
        [3,3,0]],
    #The "S", dog looking right or "Rhode Island Z" piece
    4: [
        [4,4,0],
        [0,4,4]],
    #The "T" or "Teewee" piece
    5: [
        [5,5,5],
        [0,5,0]],
    #The "L", periscope looking left or "Orange Ricky" piece
    6: [
        [0,6],
        [0,6],
        [6,6]],
    #The "J", periscope looking right or "Blue Ricky" piece
    7: [
        [7,0],
        [7,0],
        [7,7]]
}

def initGame():
    seed(None)


def initBoard():
    global board 
    board = [[0 for j in range(BOARD_WIDTH)] for i in range(BOARD_HEIGHT)]


def matrixWidth(piece):
    return len(piece[0])


def matrixHeight(piece):
    return len(piece)

"""
def showPiece(text,piece):
    height = matrixHeight(piece)
    width = matrixWidth(piece)

    print(text)
    print("    ",end="")
    for j in range(width):
        print("[{}]".format(j),end="")
    print(end="\n")
    for i in range(height):
        print("[{}]".format(i),end=" ")
        for j in range(width):
            print(" {} ".format(piece[i][j]),end="")
        print(end="\n")
"""

def drawWindow():
    global window, status, canvas, points, level, fallingPiece, currentPace, clockcount, fallingCol, fallingRow

    clockcount = 0
    fallingCol = fallingRow = 0
    
    status = Canvas (
        master = window,
        bg = "white",
        height = TILE_SIZE,
        width = canvasWidth
    )
    status.pack()
    canvas = Canvas (
        master = window,
        bg = "black",
        height = canvasHeight,
        width = canvasWidth
    ) 
    canvas.pack()


def drawBoard():
    global board, canvas, status, fallingPiece, currentPace, clockcount

    xpos = 0
    ypos = 0
    height = matrixHeight(board)
    width = matrixWidth(board)
    
    canvas.delete("all")
    status.delete("all")
    
    for j in range(width):
        xpos += TILE_MARGIN
        for i in range(height):
            ypos += TILE_MARGIN
            canvas.create_rectangle(
                xpos, 
                canvasHeight-ypos-TILE_SIZE, 
                xpos+TILE_SIZE, 
                canvasHeight-ypos, 
                fill=pieceColor[board[i][j]]
            )
            ypos += TILE_SIZE+TILE_MARGIN
        else: 
            ypos = 0
            xpos += TILE_SIZE+TILE_MARGIN
    
    status.create_text(10,15,
        text = "Points: "+str(points)+" Level: "+str(level),
        fill = "black",
        anchor = "nw",
        font = tkfont.Font(family="Helvetica", size = 12, weight="bold")
    )     
    status.pack()
    canvas.pack()


def rotatePiece(piece):
    width = matrixWidth(piece)
    height = matrixHeight(piece)
    newPiece = [[0 for j in range(height)] for i in range(width)]

    for j in range(width):
        for i in range(height):
            newPiece[j][height-i-1] = piece[i][j]

    return newPiece


def pickAPiece():
    pick = randint(1,piecesMax)
    piece = pieceMap[pick]
    rotate = maxRotate = 0
    if pick >= 2 and pick <= 5: maxRotate = 1
    if pick >= 6: maxRotate = 2    
    rotate = randint(0,maxRotate)
    for i in range(rotate):
        piece = rotatePiece(piece)

    return piece


def hasRoom(piece,Col,Row):
    Room = True

    pieceHeight = matrixHeight(piece)
    pieceWidth = matrixWidth(piece)

    if (Row-pieceHeight+1 < 0 ): 
        Room = False
        return Room

    boardCut = [[board[Row-i][Col+j] for j in range(pieceWidth)] for i in range(pieceHeight)]

    for i in range(pieceHeight):
        for j in range (pieceWidth):
            if (piece[i][j] != 0): 
                if (boardCut[i][j] !=0 ): 
                    Room = False
    return Room


def placePiece(piece,Col,Row):
    global board, oldCol, oldRow, oldPiece
    placed = True

    if piece==oldPiece and Col==oldCol and Row==oldRow:
        return placed

    if Row != BOARD_HEIGHT-1:
        oldPieceHeight = matrixHeight(oldPiece)
        oldPieceWidth = matrixWidth(oldPiece)

        for i in range(oldPieceHeight) :
            for j in range(oldPieceWidth):
                if oldPiece[i][j] != 0: 
                    board[oldRow-i][oldCol+j] = 0                         

    if (oldRow!=Row) and (not hasRoom(piece,Col,Row)): 
        placed = False
        piece = oldPiece
        Col = oldCol
        Row = oldRow

    pieceHeight = matrixHeight(piece)
    pieceWidth = matrixWidth(piece)

    for i in range(pieceHeight):
        for j in range(pieceWidth):
                if board[Row-i][Col+j] == 0 and piece[i][j] != 0: 
                    board[Row-i][Col+j] = piece[i][j]

    oldCol = Col
    oldRow = Row
    oldPiece = piece
    return placed


def deleteLine(lineNumber):
    global board, points, level, window, currentPace, levelsLbl, pointsLbl, window, canvas

    points += 10
    if points % 100 == 0: 
        level += 1
        currentPace -= LEVEL_ACCELERATION

    for i in range(lineNumber,BOARD_HEIGHT-3):
        for j in range(BOARD_WIDTH):
            board[i][j] = board[i+1][j]
    for j in range(BOARD_WIDTH): board[BOARD_HEIGHT-1][j] = 0


def checkLinesOnBoard():
    global board

    scanComplete = False
    i = 0
    while not scanComplete:
        countNoZeros=0
        for j in range(BOARD_WIDTH):
            if board[i][j] > 0: countNoZeros+=1
        if countNoZeros == 10: deleteLine(i)
        else: i+=1
        if i==BOARD_HEIGHT: scanComplete = True

def paintGrid():
    global fallingPiece, fallingCol, fallingRow, currentPace, clockcount, oldRow, points, level, window
    refreshInterval = REFRESH_INTERVAL
    
    # Game Logic
    if not fallingPiece:
        checkLinesOnBoard()
        fallingPiece = pickAPiece()
        fallingCol = (BOARD_WIDTH // 2 - len(fallingPiece) // 2)
        fallingRow = BOARD_HEIGHT-1    
        oldRow = fallingRow    
        if not hasRoom(fallingPiece,fallingCol,fallingRow):
            status.delete("all")
            status.create_text(10,15,
                text = "GAME OVER",
                fill = "red",
                anchor = "nw",
                font = tkfont.Font(family="Helvetica", size = 12, weight="bold")
            )
            status.pack()
            return
            
    if not placePiece(fallingPiece,fallingCol,fallingRow): 
        fallingPiece = None
    if clockcount >= currentPace: 
        fallingRow-=1
        clockcount=0
    else: clockcount += refreshInterval
    drawBoard()
    window.after(REFRESH_INTERVAL,paintGrid)


def keyboardEvent(event):
    global clockcount, oldRow, points, level, fallingPiece, currentPace, fallingCol, fallingRow    
    refreshInterval = REFRESH_INTERVAL
            
    keyCode = event.keysym
    
    #Keyevent processing
    if fallingPiece != None: 
        match keyCode:
            case "Left":
                if fallingCol>0: 
                    fallingCol-=1
            case "Right":
                fallingPieceWidth = matrixWidth(fallingPiece)
                if fallingCol<BOARD_WIDTH-fallingPieceWidth: 
                    fallingCol+=1
            case "Up":
                fallingPiece = rotatePiece(fallingPiece)
                fallingPieceWidth = matrixWidth(fallingPiece)
                fallingPieceHeight = matrixHeight(fallingPiece)
                if fallingCol+fallingPieceWidth>BOARD_WIDTH: 
                    fallingCol=BOARD_WIDTH-fallingPieceWidth
                if fallingRow-fallingPieceHeight<0: 
                    fallingRow=fallingPieceHeight        
            case "space":
                while placePiece(fallingPiece,fallingCol,fallingRow): 
                    fallingRow-=1    
                    
    # Game Logic
    if not fallingPiece:
        checkLinesOnBoard()
        fallingPiece = pickAPiece()
        fallingCol = (BOARD_WIDTH // 2 - len(fallingPiece) // 2)
        fallingRow = BOARD_HEIGHT-1    
        oldRow = fallingRow    
        if not hasRoom(fallingPiece,fallingCol,fallingRow):
            status.delete("all")
            status.create_text(10,15,
                text = "GAME OVER",
                fill = "red",
                anchor = "nw",
                font = tkfont.Font(family="Helvetica", size = 12, weight="bold")
            )
            status.pack()
            return
            
    if not placePiece(fallingPiece,fallingCol,fallingRow): 
        fallingPiece = None
    if clockcount >= currentPace: 
        fallingRow-=1
        clockcount=0
    else: clockcount += refreshInterval

if __name__=="__main__":
    #UI init
    canvasWidth = BOARD_WIDTH*(TILE_SIZE+TILE_MARGIN*2)
    canvasHeight = BOARD_HEIGHT*(TILE_SIZE+TILE_MARGIN*2)
    window = Tk()
    window.title("Tetris Clone")
    window.config(
        width = canvasWidth, 
        height = canvasHeight
    )
    pointsLbl = Label()
    levelsLbl = Label()
    window.bind("<Up>",keyboardEvent)
    window.bind("<Left>",keyboardEvent)
    window.bind("<Right>",keyboardEvent)
    window.bind("<Return>",keyboardEvent)
    window.bind("<space>",keyboardEvent)
    
    initGame()
    initBoard()
    drawWindow()

    window.after(REFRESH_INTERVAL,paintGrid)
    window.mainloop()
