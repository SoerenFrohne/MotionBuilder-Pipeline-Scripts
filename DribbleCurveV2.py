from pyfbsdk import *
import os
import MatVecUtils as mvu; reload(mvu)

# 1. Betrachte alle Ups
# 2. Es duerfen maximal zwei Ups aufeinanderfolgen: Entferne den letzten Up,
# wenn ein dritter folgt.
# 3: Betrachte alle Downs
# 4: Berechne die Ballposition fuer jeden Frame(Down) durch die Position
# der umliegenden Ups

def IsUp(key):
    return key.Value > 0.5

BALL_NAME = "BallR"
ROOT_NAME = "mixamorig:Hips"

# Load dependencies
scene = FBSystem().Scene
playerControl = FBPlayerControl()
fStart = int(playerControl.ZoomWindowStart.GetFrame())
fStop = int(playerControl.ZoomWindowStop.GetFrame())
#playerControl.GotoStart()

# Load models
root = FBFindModelByLabelName(ROOT_NAME)
ball = FBFindModelByLabelName(BALL_NAME)

# Prepare animation
ball.Translation.SetAnimated(True)
ballAnimNode = ball.Translation.GetAnimationNode()
ballTXCurve = ballAnimNode.Nodes[0].FCurve
ballTYCurve = ballAnimNode.Nodes[1].FCurve
ballTZCurve = ballAnimNode.Nodes[2].FCurve
ballTXCurve.EditClear()
ballTYCurve.EditClear()
ballTZCurve.EditClear()

# Load candidates
candidate = ball.PropertyList.Find('IsUpCandidate')
candidateAnimNode = candidate.GetAnimationNode()
candidateFCurve = candidateAnimNode.FCurve

# Reduce keys
consecutivesUps = 0
redundantKeyIntervals = []
for frame in range(len(candidateFCurve.Keys)):
    key = candidateFCurve.Keys[frame]
    
    if IsUp(key):
        consecutivesUps += 1
        if consecutivesUps == 3:
            redundantKeyIntervals.append(candidateFCurve.Keys[frame-2].Time)
    else:
        if consecutivesUps >= 3:
            redundantKeyIntervals.append(candidateFCurve.Keys[frame-1].Time)
        consecutivesUps = 0
                
    key.Interpolation = FBInterpolation.kFBInterpolationLinear 

for r in range(0, len(redundantKeyIntervals), 2):
    candidateFCurve.KeyDelete(redundantKeyIntervals[r], redundantKeyIntervals[r+1], False)
    
# Calculate down positions
for frame in range(1, len(candidateFCurve.Keys)):
    key = candidateFCurve.Keys[frame]
    
    pos = FBVector4d()
    if not IsUp(key):
        preUp = candidateFCurve.Keys[frame - 1]
        nextUp = candidateFCurve.Keys[frame + 1]
        previousPos = mvu.GetGlobalPositionAtTime(ball, preUp.Time)
        nextUpPos= mvu.GetGlobalPositionAtTime(ball, nextUp.Time)
        
        globalPos = nextUpPos - previousPos
        globalPos /= 2.0
        globalPos += previousPos
        globalPos[1] = 0     
        #print globalPos
        
        # Lokale Position bestimmen
        rootPos = mvu.GetGlobalPositionAtTime(root, key.Time)
        pos = globalPos - rootPos
        
        #rootTransform = mvu.GetTransform(root)
        #ballTransform = mvu.GetTransform(ball)
        #localTransform = FBMatrix()
        #FBGetLocalMatrix(localTransform, rootTransform, ballTransform)
        
        #rootTransform.Inverse()
        
        #FBVectorMatrixMult(lVector4d, lMatrix, lVector4d)
        #pos = mvu.Multiply(rootTransform, globalPos)
        
        #ball.GetVector(pos, FBModelTransformationType.kModelInverse_Translation, True)
        print pos
        
        ballTXCurve.KeyAdd(key.Time, pos[0])
        ballTYCurve.KeyAdd(key.Time, pos[1])
        ballTZCurve.KeyAdd(key.Time, pos[2])
    #else:
    #    pos = mvu.GetRelativePositionAtTime(ball, root, key.Time)
        



    
    


