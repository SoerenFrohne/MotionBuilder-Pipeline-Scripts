from pyfbsdk import *
import os

# GLOBAL_PARAMETERS
CONSTRAINT_NAME = "Ball2RightHand"

def FindConstraintByName(name):
    constraints = FBSystem().Scene.Constraints
    for constraint in constraints:
        if constraint.Name == name:
            print "Constraint found"
            return constraint 
    print "No constraint found"

# Load dependencies
scene = FBSystem().Scene
playerControl = FBPlayerControl()
fStart = int(playerControl.ZoomWindowStart.GetFrame())
fStop = int(playerControl.ZoomWindowStop.GetFrame())
playerControl.GotoStart()

# Load animation node
constraint = FindConstraintByName(CONSTRAINT_NAME)
weightNode = constraint.Weight.GetAnimationNode()

# Filter curve and clean up
keyreducer = FBFilterManager().CreateFilter ('Key Reducing')
keyreducer.Start = FBTime(0, 0, 0, fStart)
keyreducer.Stop = FBTime(0, 0, 0, fStop)
keyreducer.Apply(weightNode, True)

butterworth = FBFilterManager().CreateFilter ('Butterworth')
butterworth.Start = FBTime(0, 0, 0, fStart)
butterworth.Stop = FBTime(0, 0, 0, fStop)
butterworth.Apply(weightNode, True)
constraint.Active = True 