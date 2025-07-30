from cmu_graphics import *

def onAppStart(app):
    app.width = 400
    app.height = 600

    #Road Properties 
    app.roadWidth = 300 
    app.roadX = (app.width- app.roadWidth) //2

    #Animation for road lines
    app.roadLineOffset = 0

def redrawAll(app): 
    drawRoad(app)

def drawRoad(app): 
    drawRect(app.roadX, 0, app.roadWidth, app.height, fill = 'darkGrey') #Main Road
    
    drawRect(app.roadX - 10, 0, 10, app.height, fill = 'grey')
    drawRect(app.roadX + app.roadWidth, 0, 10, app.height, fill = 'grey')
    

runApp()