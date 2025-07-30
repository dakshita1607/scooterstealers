from cmu_graphics import *
import random
import math

def onAppStart(app):
    app.width = 400
    app.height = 600

    #Road Properties 
    app.roadWidth = 300 
    app.roadX = (app.width- app.roadWidth) //2

    #Animation for road lines
    app.roadLineOffset = 0

    #Player
    app.playerImageUrl = 'https://us-east.storage.cloudconvert.com/tasks/18bf846c-cc6b-461f-8786-b3e4bf7bd42a/image-removebg-preview%20%281%29.png?X-Amz-Algorithm=AWS4-HMAC-SHA256&X-Amz-Content-Sha256=UNSIGNED-PAYLOAD&X-Amz-Credential=cloudconvert-production%2F20250730%2Fva%2Fs3%2Faws4_request&X-Amz-Date=20250730T060249Z&X-Amz-Expires=86400&X-Amz-Signature=8ee27db53f56377a46fff7b80016265e3c75a97c86a9b9481a8632579f960a0c&X-Amz-SignedHeaders=host&response-content-disposition=inline%3B%20filename%3D%22image-removebg-preview%20%281%29.png%22&response-content-type=image%2Fpng&x-id=GetObject'
    app.playerSize = 70
    app.playerY = app.height - 100
    app.playerLane = 1

    #Obstacle - Molly's Trolleys
    app.obstacleImageUrl = 'https://us-east.storage.cloudconvert.com/tasks/da13a7c5-14a5-44d0-93e3-1c16ef4b0d70/download.png?X-Amz-Algorithm=AWS4-HMAC-SHA256&X-Amz-Content-Sha256=UNSIGNED-PAYLOAD&X-Amz-Credential=cloudconvert-production%2F20250730%2Fva%2Fs3%2Faws4_request&X-Amz-Date=20250730T061116Z&X-Amz-Expires=86400&X-Amz-Signature=824142ca43e80e0a722dde285f6dc17777c6beab9ceeaa39c3ec4a92d8ba4bfa&X-Amz-SignedHeaders=host&response-content-disposition=inline%3B%20filename%3D%22download.png%22&response-content-type=image%2Fpng&x-id=GetObject'
    app.obstacles = []
    app.obstacleDisplaySize = 250
    app.obstacleCollisionSize = 60
    app.obstacleSpeed = 4
    app.obstacleSpawnTimer = 0 
    app.obstacleSpawndx = 60 

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
    app.coinSpawndx = 15
    app.score = 0 

    #Game 
    app.gameOver = False
    app.gameTimer = 0

def redrawAll(app): 
    drawBackground(app)
    drawRoad(app)
    drawPlayer(app)
    drawCoins(app)
    drawScore(app)
    drawObstacles(app)
    if app.gameOver: 
        drawGameOver(app)

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
    playerX = app.lanePositions[app.playerLane]
    playerY = app.playerY
    for coin in app.coins: 
        distanceToPlayer = ((coin['baseX'] - playerX)**2 + (coin['y'] - playerY)**2)**0.5
        
        if distanceToPlayer < 150: 
            bounceAmount = (150 - distanceToPlayer) / 150
            bounceOffset = math.sin(coin['bouncePhase']) * 15 * bounceAmount
            displayX = coin['baseX'] + bounceOffset
        else:
            displayX = coin['baseX']

        drawCircle(displayX, coin['y'], app.coinSize//2 + 2, fill='yellow', opacity=30)  # Glow effect
        drawCircle(displayX, coin['y'], app.coinSize//2, fill='gold', border='orange', borderWidth=2)
        drawLabel('$', displayX, coin['y'], fill='darkGoldenRod', size=16, bold=True)

def drawObstacles(app): 
    for obs in app.obstacles: 
        # Draw large train to fill the lane visually
        drawImage(app.obstacleImageUrl, 
                  obs['x'] - app.obstacleDisplaySize//2, 
                  obs['y'] - app.obstacleDisplaySize//2, 
                  width = app.obstacleDisplaySize, height = app.obstacleDisplaySize)
        
def drawGameOver(app): 
    drawRect(0, 0, app.width, app.height, fill='black', opacity=80)
    drawLabel('GAME OVER!', app.width//2, app.height//2 - 50, fill='red', size=40, bold=True)
    drawLabel(f'Final Score: {app.score}', app.width//2, app.height//2, fill='white', size=25, bold=True)
    drawLabel('Press R to Restart', app.width//2, app.height//2 + 50, fill='white', size=20)
        
def onKeyPress(app, key): 
    if app.gameOver and key == 'r': 
        onAppStart(app)
        return 
    
    if key == 'a' or key == 'left': 
        if app.playerLane > 0: 
            app.playerLane -= 1
    
    elif key == 'd' or key == 'right': 
        if app.playerLane < 2: 
            app.playerLane += 1
    
    if app.gameOver:
        return 

def onStep(app): 
    if app.gameOver:
        return 
    
    app.roadLineOffset += 3

    if app.roadLineOffset > 50: 
        app.roadLineOffset = 0

    app.coinSpawnTimer += 1

    #Coin Spawn
    if app.coinSpawnTimer >= app.coinSpawndx: 
        spawnCoin(app)
        app.coinSpawnTimer = 0

    app.obstacleSpawnTimer += 1

    #ObstacleSpawn
    if app.obstacleSpawnTimer >= app.obstacleSpawndx:
        spawnObstacle(app)
        app.obstacleSpawnTimer = 0

    updateCoins(app)
    updateObstacles(app)
    checkCoinCollision(app)
    checkObstacleCollision(app)

def drawScore(app): #Ask how to fix the score label 
    drawRect(5, 10, 120, 40, fill = 'black', opacity = 70, border = 'white', borderWidth = 1)
    drawLabel(f'Score: {app.score}', 50, 30, fill='white', size = 20, bold = True)

def spawnCoin(app): 
    obstacleLanes = [obs['lane'] for obs in app.obstacles if -app.coinSize < obs['y'] < 150]
    availableLanes = [i for i in range(3) if i not in obstacleLanes]
    if not availableLanes:
        return
    lane = random.choice(availableLanes) #Choose a lane for coin randomly
    coin = {
        'baseX': app.lanePositions[lane],  # Store original X position
        'y': -app.coinSize, #Start above screen
        'lane': lane,
        'bouncePhase': random.uniform(0, 2 * math.pi)
    }
    app.coins.append(coin)

def spawnObstacle(app): 
    lane = random.randint(0,2)
    obs = {
        'lane': lane,
        'x': app.lanePositions[lane],
        'y': -app.obstacleDisplaySize
    }
    app.obstacles.append(obs)

def updateCoins(app): 
    for coin in app.coins: 
        coin['y'] += app.coinSpeed #Move coins down the screen
        coin['bouncePhase'] += 0.3
    
    app.coins = [coin for coin in app.coins if coin['y'] < app.height + app.coinSize]

def updateObstacles(app): 
    for obs in app.obstacles:
        obs['y'] += app.obstacleSpeed
    app.obstacles = [obs for obs in app.obstacles if obs['y'] < app.height + app.obstacleDisplaySize]

def checkCoinCollision(app): 
    playerX = app.lanePositions[app.playerLane]
    playerY = app.playerY 

    i = 0 
    while i < len(app.coins): 
        coin = app.coins[i]
        if coin['lane'] == app.playerLane:
            distance = ((playerX-coin['baseX'])**2 + (playerY-coin['y'])**2)**0.5
            if distance < (app.playerSize + app.coinSize) // 2: 
                app.coins.pop(i)
                app.score += 10
            else:
                i += 1
        else:
            i += 1

def checkObstacleCollision(app):
    playerX = app.lanePositions[app.playerLane]
    playerY = app.playerY
    
    for obs in app.obstacles:
        if obs['lane'] == app.playerLane:
            distance = ((playerX - obs['x'])**2 + (playerY - obs['y'])**2)**0.5
            # Use the smaller collision size for precise hit detection
            collisionThreshold = (app.playerSize + app.obstacleCollisionSize) // 2
            if distance < collisionThreshold:
                app.gameOver = True

#AHHHHHH
#Bugs to ask TA about: Score Label, Obstacle Crash Space, Maybe some clouds
#Things to add: Start Screen, Game Over Screen, Score increases every second, coin counter, center the obstacles
runApp()