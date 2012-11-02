#!/usr/bin/python2

import os 
import xml.etree.ElementTree as ET

from pymunk import Vec2d

def vector(x, y):
    return Vec2d(float(x), -float(y))

def getVector(element, xAttrib, yAttrib):
    return vector(element.attrib[xAttrib], element.attrib[yAttrib])

def getPolygon(element, offset):
    polyPoints = []
    polygonString = element.find('polygon').attrib['points'] # TODO: test
    for xy in polygonString.split(' '):
        polyPoints.append(vector(*xy.split(',')))
    polyPoints=[tuple(v+offset) for v in polyPoints]
    polyPoints.reverse()
    return polyPoints

def is_int(s):
    try:
        int(s)
        return True
    except ValueError:
        return False



currentDir = os.path.dirname(__file__)
for fileName in filter(lambda x: x.endswith('.tmx'), os.listdir(currentDir)):
    tree = ET.parse(os.path.join(currentDir, fileName))
    root = tree.getroot()

    size = getVector(root, 'width', 'height')
    tilesize = getVector(root, 'tilewidth', 'tileheight')

    nextID = 9001
    entities = {}

    for obj in root.findall('.objectgroup/object'):
        offset = getVector(obj, 'x', 'y')

        entityType = obj.attrib.get('type')
        if entityType == None:
            entityType = 'Platform'
        args = ()
        if entityType == 'Platform':
            args = (getPolygon(obj, offset),)
        elif entityType == 'LevelEnd':
            args = (getPolygon(obj, offset),)
        elif entityType == 'SpawnPoint':
            args = (tuple(offset),)
        elif entityType == 'Trigger':
            thingsToTrigger = {}
            for prop in obj.findall("./properties/property[@name]"):
                if not is_int(prop.attrib['name']): continu
                thingsToTrigger[int(prop.attrib['name'])] = str(prop.attrib['value'])
            args = (getPolygon(obj, offset), thingsToTrigger)
        else:
            if entityType == None: print 'type == none'
            else:                  print 'unknown entityType:', entityType
            continue

        idProperty = obj.find("./properties/property[@name='id']")
        if idProperty is not None:
            entityID = int(idProperty.attrib['value'])
        else:
            entityID = nextID
            nextID += 1
        if entityID in entities: print 'PANIC! 2 IDs for the same thing!  id:', entityID
        entities[entityID] = (entityType,)+args

    outFileName = os.path.join(currentDir, '..', 'uncompressed', fileName[:-4], 'level.txt')
    dirName = os.path.dirname(outFileName)
    if not os.path.exists(dirName):
        os.makedirs(dirName)


    with open(outFileName, 'w') as f:
        for entityID in sorted(entities.iterkeys()):
            f.write(repr((entityID,) +entities[entityID]) + '\n')