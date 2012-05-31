import time
import globals

class PlayerInput:
  actionTypes = ['move', 'jump', 'fire', 'fire2']

  actionQueue = []  #          queue of (type, data). This is for the Player to process
  actionLog = {}    # dict from time to (type, data). This is for the Replay to process

  currentAim = 0.0  # should only be used for cosmetics (not for rocket firing direction)
  
  def recordAction(self, actionType, data=None):
    assert actionType in self.actionTypes, str(actionType) + ' is not a actionType'
    if data == None: 
      data = self.currentAim
    action = (actionType, data)
    self.actionQueue.append(action)
    self.actionLog[time.time()-globals.engine.levelStartTime] = action
    #print "Action:", action
    
  
  def checkInput(self, dt):
    # do recordAction when you have corresponding input
    pass
