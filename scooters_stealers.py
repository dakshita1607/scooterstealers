from cmu_graphics import *
import random
import math

def onAppStart(app):
    app.width = 400
    app.height = 600

    app.gameState = 'start' 

    #Road Properties 
    app.roadWidth = 300 
    app.roadX = (app.width- app.roadWidth) //2

    #Animation for road lines
    app.roadLineOffset = 0

    #Player
    app.playerImageUrl = 'https://us-east.storage.cloudconvert.com/tasks/78e95300-86a8-4a40-88b9-4b0b1c7536c3/image-removebg-preview%20%281%29.png?X-Amz-Algorithm=AWS4-HMAC-SHA256&X-Amz-Content-Sha256=UNSIGNED-PAYLOAD&X-Amz-Credential=cloudconvert-production%2F20250730%2Fva%2Fs3%2Faws4_request&X-Amz-Date=20250730T153900Z&X-Amz-Expires=86400&X-Amz-Signature=70fc150bbac489cc9ee8be99b9cc3b3cb82f41fcf83033477c524bf34630e661&X-Amz-SignedHeaders=host&response-content-disposition=inline%3B%20filename%3D%22image-removebg-preview%20%281%29.png%22&response-content-type=image%2Fpng&x-id=GetObject'
    app.playerSize = 70
    app.playerY = app.height - 100
    app.playerLane = 1

    #Obstacle - Molly's Trolleys
    app.obstacles = []
    app.obstacleSpeed = 4
    app.obstacleSpawnTimer = 0 
    app.obstacleSpawndx = 60 
    app.obstacleCollisionSize = 50

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
    if app.gameState == 'start':
        drawStartScreen(app)
    elif app.gameState == 'playing':
        drawBackground(app)
        drawRoad(app)
        drawPlayer(app)
        drawCoins(app)
        drawScore(app)
        drawObstacles(app)
    elif app.gameState == 'gameOver':
        drawBackground(app)
        drawRoad(app)
        drawPlayer(app)
        drawCoins(app)
        drawScore(app)
        drawObstacles(app)
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
    for obs in app.obstacles:    # Main trolley body dimensions
        obstacleWidth = 50
        obstacleHeight = 80
        
        drawRect(obs['x'] - obstacleWidth//2, # Main dark green body
                 obs['y'] - obstacleHeight//2, 
                 obstacleWidth, obstacleHeight, 
                 fill='darkGreen', border='black', borderWidth=2)
        
        drawRect(obs['x'] - obstacleWidth//2 + 5,     # Front of the trolley 
                 obs['y'] - obstacleHeight//2 + 5, 
                 obstacleWidth - 10, 15, 
                 fill='lightGreen')
        
        interiorWidth = obstacleWidth - 30  # White interior/window area with red border 
        interiorHeight = obstacleHeight - 30
        drawRect(obs['x'] - interiorWidth//2, 
                 obs['y'] - interiorHeight//2 + 5, 
                 interiorWidth, interiorHeight, 
                 fill='white', border='red', borderWidth=2)
        
        tireWidth = 8 
        tireHeight = 12 
        tireOffset = obstacleWidth//2 + 2  # Position slightly outside the body
        
        drawRect(obs['x'] - tireOffset - tireWidth//2, obs['y'] - 28,        # Front left tire
                 tireWidth, tireHeight, fill='black', border='darkGray', borderWidth=1)
    
        drawRect(obs['x'] + tireOffset - tireWidth//2, obs['y'] - 28,         # Front right tire  
                 tireWidth, tireHeight, fill='black', border='darkGray', borderWidth=1)
    
        drawRect(obs['x'] - tireOffset - tireWidth//2, obs['y'] + 16,         # Rear left tire
                 tireWidth, tireHeight, fill='black', border='darkGray', borderWidth=1)
    
        drawRect(obs['x'] + tireOffset - tireWidth//2, obs['y'] + 16,         # Rear right tire
                 tireWidth, tireHeight, fill='black', border='darkGray', borderWidth=1)
        
        #WHY IS THIS NOT CENTERED AHHHHH 
        
def drawGameOver(app): 
    drawRect(0, 0, app.width, app.height, fill='black', opacity=80)
    drawLabel('GAME OVER!', app.width//2, app.height//2 - 50, fill='red', size=40, bold=True)
    drawLabel(f'Final Score: {app.score}', app.width//2, app.height//2, fill='white', size=25, bold=True)
    drawLabel('Press R to Restart', app.width//2, app.height//2 + 50, fill='white', size=20)

def drawStartScreen(app): 
        # Background
    drawRect(0, 0, app.width, app.height, fill='white')
    
    # Title
    drawLabel('ScooterStealers :((', app.width//2, app.height//2 - 100, 
              fill='Black', size=40, bold=True, font = 'times new roman')
    
    # Subtitle
    drawLabel("Avoid the Molley's Trolleys to Survive!", app.width//2, app.height//2 - 50, 
              fill='black', size=20, font = 'times new roman')
    
    # Instructions
    drawLabel('Use A/D or Arrow Keys to move', app.width//2, app.height//2, 
              fill='black', size=16, font = 'times new roman')
    drawLabel('Collect coins for points!', app.width//2, app.height//2 + 40, 
              fill='gold', size=16, bold=True, font = 'times new roman')
    
    # Start instruction
    drawLabel('Click anywhere to start!', app.width//2, app.height//2 + 80, 
              fill='red', size=18, bold=True, font = 'times new roman')
        
def onKeyPress(app, key): 
    if app.gameState == 'gameOver' and key == 'r': 
        onAppStart(app)
        return 
    
    if app.gameState != 'playing':
        return
    
    if key == 'a' or key == 'left': 
        if app.playerLane > 0: 
            app.playerLane -= 1
    
    elif key == 'd' or key == 'right': 
        if app.playerLane < 2: 
            app.playerLane += 1

def onMousePress(app, mouseX, mouseY):
    if app.gameState == 'start':
        app.gameState = 'playing'

def onStep(app): 
    if app.gameState != 'playing':
        return 
       
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
        'y': -40  # Changed from -app.obstacleDisplaySize since not using Image anymore
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
    app.obstacles = [obs for obs in app.obstacles if obs['y'] < app.height + 80]  # Remove obstacles that have gone off screen

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
            collisionThreshold = (app.playerSize + app.obstacleCollisionSize) // 2
            if distance < collisionThreshold:
                app.gameOver = 'gameOver'

#AHHHHHH
#Bugs to ask TA about: Score Label, Maybe some clouds, IMAGES
#Things to add: Start Screen, Game Over Screen(still a work in progress), Score increases every second, coin counter
runApp()