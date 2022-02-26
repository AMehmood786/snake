def OnPowerup(object, hero):
 if (object == 'powerup5'):
speakNoCB('minute_man', 'MISSPCH_1_MM_12')
elif (object == 'powerup1') or (object == 'powerup6'):
speakNoCB('minute_man', 'MISSPCH_1_MM_11')
Object_SetAttr(object, 'used', 1)
UpdateTrainArrow(object)

def OnInterrogation(char, hero):
print 'OnInterrogation'
Object_SetAttr(char, 'used', 1)
UpdateTrainArrow(char)



:
:


def startChase(event):
startPatrol('runfciv', 3, run = 1, priority = ai.goal.PRI_HI)
addMoveGoal('thugb16', Get_ObjectPos('runfciv'), fn =
'continueChase')

def continueChase(event):
addMoveGoal('thugb16', Get_ObjectPos('runfciv'), fn =
'continueChase')

def endChase(event):
clearGoals('runfciv')
speakNoCB('runfciv', 'MISSPCH_1_F1_02')
