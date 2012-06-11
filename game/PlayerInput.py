import time
import globals

class PlayerInput:

  actionQueue = []  # queue of PlayerAction. This is for the Player to process
  actionLog = []    # list  of PlayerAction. This is for the Replay to process

  currentAim = 0.0  # should only be used for cosmetics (not for rocket firing direction)
  
  def recordAction(self, actionType, moveDir=None):
    action = self.PlayerAction(actionType, self.currentAim, moveDir)
    self.actionQueue.append(action)
    self.actionLog.append(action)
    #print "Action:", action
  
  def checkInput(self, dt):
    # do recordAction when you have corresponding input
    pass



  class PlayerAction:
    ''' A small class to hold information about a action '''
    actionTypes = ['move', 'jump', 'fire', 'fire2']

    def __init__(self, actionType, aim, moveDir=None):
      assert actionType in self.actionTypes, str(actionType) + ' is not a actionType'
      self.type = actionType
      self.aim = aim
      self.time = time.time()-globals.engine.levelStartTime
      if moveDir != None:
        self.moveDir = max(min(moveDir, 1), -1) # constraint:  -1 <= moveDir <= 1
