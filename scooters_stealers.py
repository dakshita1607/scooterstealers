from cmu_graphics import *
import random

def onAppStart(app):
    app.width = 400
    app.height = 600

    #Road Properties 
    app.roadWidth = 300 
    app.roadX = (app.width- app.roadWidth) //2

    #Animation for road lines
    app.roadLineOffset = 0

    #Player
    app.playerImageUrl = 'https://us-east.storage.cloudconvert.com/tasks/4b4ff701-4128-481e-92e3-c43673fe7467/image-removebg-preview%20%281%29%202.png?X-Amz-Algorithm=AWS4-HMAC-SHA256&X-Amz-Content-Sha256=UNSIGNED-PAYLOAD&X-Amz-Credential=cloudconvert-production%2F20250730%2Fva%2Fs3%2Faws4_request&X-Amz-Date=20250730T044221Z&X-Amz-Expires=86400&X-Amz-Signature=5bb70c0ea557d8814bddac0c11927da6088e43063febc6c76c6f90e0375668cf&X-Amz-SignedHeaders=host&response-content-disposition=inline%3B%20filename%3D%22image-removebg-preview%20%281%29%202.png%22&response-content-type=image%2Fpng&x-id=GetObject'
    app.playerSize = 70
    app.playerY = app.height - 100
    app.playerLane = 1

    #Lane Center Positions
    laneWidth = app.roadWidth // 3
    app.lanePositions = [
        app.roadX + laneWidth//2,    #Left Lane
        app.roadX + laneWidth + laneWidth //2,    #Center Lane
        app.roadX + 2 * laneWidth + laneWidth//2   #Right Lane
    ]

    #Coins 

    app.coins = []
    app.coinSize = 25
    app.coinSpeed = 4
    app.coinSpawnTimer = 0
    app.coinSpawndx = 60
    app.score = 0 

def redrawAll(app): 
    drawBackground(app)
    drawRoad(app)
    drawPlayer(app)
    drawCoins(app)
    drawScore(app)

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
    else: #fail safe in case my image doesnt work
        drawRect(playerX - app.playerSize//2, playerY - app.playerSize//2, 
                app.playerSize, app.playerSize, fill='red', border='darkRed', borderWidth=2)
        drawLabel('PLAYER', playerX, playerY, fill='white', size=10, bold=True)

def drawCoins(app):
    for coin in app.coins: 
        drawCircle(coin['x'], coin['y'], app.coinSize//2, fill = 'gold', border = 'orange', borderWidth = 2) #Hopefully this is cute when my code FINALLY WORKS OMGGG AHHH

def onKeyPress(app, key): 
    if key == 'a' or key == 'left': 
        if app.playerLane > 0: 
            app.playerLane -= 1
    
    elif key == 'd' or key == 'right': 
        if app.playerLane < 2: 
            app.playerLane += 1

def onStep(app): 
    app.roadLineOffset += 3

    if app.roadLineOffset > 50: 
        app.roadLineOffset = 0

    #Coin Spawn
    if app.coinSpawnTimer >= app.coinSpawndx: 
        spawnCoin(app)
        app.coinSpawnTimer = 0

    updateCoins(app)
    checkCoinCollision(app)


def drawScore(app): 
    drawLabel(f'Score: {app.score}', 50, 30, fill='black', size = 20, bold = True)

def spawnCoin(app): 
    lane = random.randint(0,2) #Choose a lane for coin randomly
    coin = {
        'x': app.lanePositions[lane],
        'y': -app.coinSize, #Start above screen
        'lane': lane
    }
    app.coins.append(coin)

def updateCoins(app): 
    for coin in app.coins: 
        coin['y'] += app.coinSpeed #Move coins down the screen
    
    app.coins = [coin for coin in app.coins if coin['y'] < app.height + app.coinSize]

def checkCoinCollision(app): 
    playerX = app.lanePositions[app.playerLane]
    playerY = app.playerY 

    coinsToRemove = []

    i = 0 
    while i < len(app.coins): 
        coin = app.coins[i]
        if coin['lane'] == app.playerLane:
            distance = ((playerX-coin['x'])**2 + (playerY-coin['y']**2)**0.5)
            if distance < (app.playerSize + app.coinSize) // 2: 
                app.coins.pop(i)
                app.score += 10
            else:
                i += 1
        else:
            i += 1

runApp()