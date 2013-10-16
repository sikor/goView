__author__ = 'pawsi_000'

import point
import utils
import math
import segment
from PyQt4 import QtGui
import HTML

def getSide(sega, segb, point):
    det = (sega.x - point.x)*(segb.y - point.y) - (segb.x - point.x)*(sega.y - point.y)
    return det

def setColorForSide(e, side):
    if abs(side) < 1.5e-14:
        e.color = QtGui.QColor(0, 0, 0)
        e.side = 2
    elif side > 0.0: #right
        e.color = QtGui.QColor(255, 0, 0)
        e.side = 1
    else: #left
        e.color = QtGui.QColor(0, 255, 0)
        e.side = 0




def drawEntities(entities, ui):
    ui.entities = entities
    ui.refresh()


def classifyAndDraw(entities, ui):
    sega = getLinePoint(-1.0)
    segb = getLinePoint(1.0)
    for e in entities:
        side = getSide(sega, segb, e)
        setColorForSide(e, side)
    seg = segment.Segment(getLinePoint(-110), getLinePoint(110))
    ui.entities.append(seg)

    drawEntities(entities, ui)


def getLinePoint(x):
    a = 0.05
    b = 0.05
    return  point.Point(x, a * x + b)

def generatePoints(pointMaxA, pointMinA, pointNA):
    pointMin = pointMinA
    pointMax = pointMaxA
    pointN = pointNA
    entities = [point.Point(utils.random.uniform(pointMin, pointMax), utils.random.uniform(pointMin, pointMax))
                for unused in range(pointN)]
    return entities


def ex1a():
    pointNA = 100000
    pointMinA = -100
    pointMaxA = 100
    entities = generatePoints(pointMaxA, pointMinA, pointNA)
    return entities


def ex1b():
    pointNB = 100000
    pointMinB = -100000000000000.0
    pointMaxB = 100000000000000.0
    entities =  generatePoints(pointMaxB, pointMinB, pointNB)
    return entities

def ex1c():
    entities = []
    for i in range(1000):
        alpha = utils.random.uniform(0, 2.0 * math.pi)
        y = 100 * math.sin(alpha)
        x = 100 * math.cos(alpha)
        entities.append(point.Point(x, y))
    return entities


def ex1d():
    entities = []
    a = 0.05
    b = 0.05
    for i in range(1000):
        x = utils.random.uniform(-1000.0, 1000.0)
        y = a * x + b
        entities.append(point.Point(x, y))

    return entities


def savePointsToFile(points, fileName):
    file = open(fileName, "w")
    for p in points:
        file.write(str(p.x)+" "+str(p.y)+"\n")
    file.close()


exercises = [ex1a, ex1b, ex1c, ex1d]
dataNames = [e.__name__ for e in exercises]
functionNames = ["det1", "det2", "orient2dfast", "orient2dexact", "orient2dslow"]


def saveData():
    exercises = [ex1a, ex1b, ex1c, ex1d]
    for ex in exercises:
        entities = ex()
        savePointsToFile(entities, ex.__name__)

def loadClassifiedData(fileName):
    f = open(fileName)
    entities = []
    for line in f:
        p = point.Point(float(line.split()[0]), float(line.split()[1]))
        setColorForSide(p, float(line.split()[2]))
        entities.append(p)

    f.close()
    return entities


def getDataPath(data, function):
    return "../lab1/classifications/" + data + ".classified." + function


def countClassifications(ui):
    header_row = ["algorytm", " - ", " + ", " 0 "]
    for data in dataNames:
        table = []
        print(data)
        for function in functionNames:
            entities = loadClassifiedData(getDataPath(data, function))
            stats = [0, 0, 0]
            row = [function]
            for e in entities:
                stats[e.side] +=1
            table.append(row+[str(s) for s in stats])
        htmlcode = HTML.table(table, header_row=header_row)
        print(htmlcode)

def init(ui):
    countClassifications(ui)
  #  ent = loadClassifiedData(getDataPath("ex1d", "orient2dslow"))
  #  seg = segment.Segment(getLinePoint(-110), getLinePoint(110))
  ##  ent.append(seg)
  #  drawEntities(ent, ui)
