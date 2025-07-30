from cmu_graphics import *

def onAppStart(app):
    app.width = 400
    app.height = 600

    #Road Properties 
    app.roadWidth = 300 
    app.roadX = (app.width- app.roadWidth) //2

    #Animation for road lines
    app.roadLineOffset = 0

    #Player
    app.playerImageUrl = 'https://tinyurl.com/4xemdrhk'
    app.playerSize = 60
    app.playerY = app.height - 100
    app.playerLane = 1

    #Lane Center Positions
    laneWidth = app.roadWidth // 3
    app.lanePositions = [
        app.roadX + laneWidth//2,    #Left Lane
        app.roadX + laneWidth + laneWidth //2,    #Center Lane
        app.roadX + 2 * laneWidth + laneWidth//2   #Right Lane
    ]

def redrawAll(app): 
    drawBackground(app)
    drawRoad(app)
    drawPlayer(app)

def drawBackground(app): 
    drawRect(0, 0, app.width, app.height, fill = 'lightblue' ) #Sky Background
    #ask TAs about clouds tomorrow

def drawRoad(app): 
    drawRect(app.roadX, 0, app.roadWidth, app.height, fill = 'darkGrey') #Main Road
    
    drawRect(app.roadX - 10, 0, 10, app.height, fill = 'grey') #Road Edge
    drawRect(app.roadX + app.roadWidth, 0, 10, app.height, fill = 'grey') #Road Edge

    laneWidth = app.roadWidth // 3

    drawRect(app.roadX + laneWidth -2, 0, 4, app.height, fill = 'white') #Left Lane Divider
    drawRect(app.roadX + 2 * laneWidth -2, 0, 4, app.height, fill = 'white' ) #Right Lane Divider
    
    drawMovingLaneLines(app)

def drawMovingLaneLines(app):
    laneWidth = app.roadWidth // 3

    leftCenter = app.roadX + laneWidth //2
    middleCenter = app.roadX + laneWidth + laneWidth // 2
    rightCenter = app.roadX + 2 * laneWidth + laneWidth // 2

    dashLength = 30
    dashGap = 20

    y = app.roadLineOffset 

    while y < app.height: 
        if y + dashLength > 0:
            drawRect(leftCenter - 2, y, 4, dashLength, fill = 'yellow')
            drawRect(middleCenter - 2, y, 4, dashLength, fill = 'yellow') #fixed YAYYY
            drawRect(rightCenter - 2, y, 4, dashLength, fill = 'yellow')
        y += dashLength + dashGap

def drawPlayer(app): 
    #Player Position
    playerX = app.lanePositions[app.playerLane]
    playerY = app.playerY 

    #Draw Player
    if app.playerImageUrl != "": 
        drawImage(app.playerImageUrl, playerX-app.playerSize//2, 
                  playerY - app.playerSize//2, width = app.playerSize, 
                  height = app.playerSize)
    else: 
        drawRect(playerX - app.playerSize//2, playerY - app.playerSize//2, 
                app.playerSize, app.playerSize, fill='red', border='darkRed', borderWidth=2)
        drawLabel('PLAYER', playerX, playerY, fill='white', size=10, bold=True)

def onStep(app): 
    app.roadLineOffset += 3

    if app.roadLineOffset > 50: 
        app.roadLineOffset = 0
runApp()