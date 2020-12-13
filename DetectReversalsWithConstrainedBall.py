#######################################################
# author: Soeren Frohne                               #
# date: 2020/12/10                                    #
# This script helps to animate a ball dribble motion  #
# considering the rotation of a characters forearm.   #
# Ensure that you have an "Ball"-Model inside your    #
# character hierarchy and feel free to play with      #
# the GLOBAL_PARAMETERS.                              #
#######################################################

from pyfbsdk import *
import os

# GLOBAL_PARAMETERS
NAMESPACE = "mixamorig"
FOREARM_NAME = "RightForeArm"
HAND_NAME = "RightHand"
BALL_NAME = "BallR"
ROOT_NAME = "mixamorig:Hips"  # Name of the skeletons root (leave empty when it has no root)
N = 6  # number of neighbours with unchanged gradient
ROT_MIN = 18.5  # Forearm rotation threshold to detect, when the ball should be grounded
BALL_OFFSET = 9.0  # Radius of the ball


# Calculate transform matrix of an object (t1) relative to another one (t2)
# You can also use FBGetLocalMatrix(result, mat2, mat1) directly on matrices.
def get_relative_transform(t1, t2):
    mat1 = FBMatrix(); 
    t1.GetMatrix(mat1)
    
    mat2 = FBMatrix(); 
    t2.GetMatrix(mat2)
    mat2.Inverse()

    return mat2 * mat1

# Load dependencies
scene = FBSystem().Scene
playerControl = FBPlayerControl()
fStart = int(playerControl.ZoomWindowStart.GetFrame())
fStop = int(playerControl.ZoomWindowStop.GetFrame())
playerControl.GotoStart()

# Load models and clean up previous edits
if ROOT_NAME != "":
    root = FBFindModelByLabelName(ROOT_NAME)
else :
    root = FBCreateObject( "Browsing/Templates/Elements", "Null", "root" )
    print "No character root existing: Root created manually"
    root.Show = True
rightArm = FBFindModelByLabelName(NAMESPACE + ":" + FOREARM_NAME)
rightHand = FBFindModelByLabelName(NAMESPACE + ":" + HAND_NAME)
ball = FBFindModelByLabelName(BALL_NAME)

candidate = ball.PropertyList.Find('IsUpCandidate')
candidate.SetAnimated(True)
candidateAnimNode = candidate.GetAnimationNode()
candidateFCurve = candidateAnimNode.FCurve
candidateFCurve.EditClear()

# Get local ground value
if root: 
    origin = FBMatrix()
    localOrigin = FBMatrix()
    rootTransform = FBMatrix(); 
    root.GetMatrix(rootTransform)
    FBGetLocalMatrix(localOrigin, rootTransform, origin)
    LOCAL_GROUND = localOrigin[13]
else: 
    LOCAL_GROUND = 0

# Access rotation curve of arm
rotationProperty = rightArm.PropertyList.Find("Rotation (Lcl)")
animNode = rotationProperty.GetAnimationNode()
yCurve = animNode.Nodes[1].FCurve
print "Right Arm animated with", len(yCurve.Keys), "Keyframes"

# detect reversal points
history = 0  # number of observed frames
gradient = 0
reversalsX = []
for k in range(fStart, fStop):
    current = yCurve.Keys[k]
    last = yCurve.Keys[k - 1]
    currentGradient = -1 if (current.Value - last.Value) < 0 else 1

    if currentGradient != gradient and history >= N:
        reversalsX.append(last.Time.GetFrame())
        history = 0
    else:
        history += 1
    gradient = currentGradient
print "Found Reversals:", reversalsX

# Loop 1: Add keys and set non-numeric properties
isLastUp = True
isCurrentUp = True    
for i in range(len(reversalsX)):    
    time = FBTime(0, 0, 0, reversalsX[i])
    playerControl.Goto(time)
    scene.Evaluate()

    # set up y-translation curve
    isCurrentUp = rightArm.Rotation[1] > ROT_MIN
    
    if isCurrentUp == False and isLastUp == True:
        y = candidateFCurve.KeyAdd(time, 0)
    else:
        y = candidateFCurve.KeyAdd(time, 100)
    isLastUp = isCurrentUp
    
    key = candidateFCurve.Keys[y]
    key.Interpolation = FBInterpolation.kFBInterpolationLinear
    
# Clean up
if ROOT_NAME is "":
    FBDeleteObjectsByName(root.Name)
