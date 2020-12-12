#######################################################
# author: Soeren Frohne                               #
# date: 2020/12/12                                    #
# This script helps to stabilize ball position by     #
# constraining it depending on the distance between   #
# its psoition and the characters hand.               #
#######################################################

from pyfbsdk import *
import os

# GLOBAL_PARAMETERS
HAND_NAME = "mixamorig:RightHand"
BALL_NAME = "Ball"
REFERENCE_NAME = "mixamorig:Hips"
CONSTRAINT_NAME = "Ball-Hand"
DISTANCE_THRESHOLD = 15.0

def GetDistance(v1, v2):
    v = v2 - v1
    return v.Length()
    
def FindConstraintByName(name):
    constraints = FBSystem().Scene.Constraints
    for constraint in constraints:
        if constraint.Name == name:
            print "Constraint found"
            return constraint 
    print "No constraint found"
    
        
# Load dependencies
scene =FBSystem().Scene
playerControl = FBPlayerControl()
fStart = int(playerControl.ZoomWindowStart.GetFrame())
fStop = int(playerControl.ZoomWindowStop.GetFrame())
playerControl.GotoStart()

# Load models
hand = FBFindModelByLabelName(HAND_NAME)
ball = FBFindModelByLabelName(BALL_NAME)
reference = FBFindModelByLabelName(REFERENCE_NAME)
constraint = FindConstraintByName(CONSTRAINT_NAME)

# Prepare animation


# Calculate distances and set constraint weights
for f in range(fStart, fStop):    
    time = FBTime(0, 0, 0, f)
    playerControl.Goto(time)
    scene.Evaluate()
    
    # Calculate global hand and ball positions
    handPos = FBVector3d()
    ballPos = FBVector3d()
    hand.GetVector(handPos, FBModelTransformationType.kModelInverse_Translation, True)
    ball.GetVector(ballPos, FBModelTransformationType.kModelInverse_Translation, True)
    distance = GetDistance(handPos, ballPos)
    print time.GetFrame(), ":", distance
    
    # Set constraint weight
     