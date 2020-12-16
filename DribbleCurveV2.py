from pyfbsdk import *
import os
import MatVecUtils as mvu

reload(mvu)
import SceneUtils as su

reload(su)


# 1. Betrachte alle Ups
# 2. Es duerfen maximal zwei Ups aufeinanderfolgen: Entferne den letzten Up,
# wenn ein dritter folgt.
# 3: Betrachte alle Downs
# 4: Berechne die Ballposition fuer jeden Frame(Down) durch die Position
# der umliegenden Ups

def IsUp(key):
    return key.Value > 0.5


GROUND_OFFSET = 9.0
BALL_NAME = "Ball"
ROOT_NAME = "mixamorig:Hips"
CONSTRAINT_NAME = "Ball2RightHand"
CONSTRAINT_TIME = 6

# Load dependencies
scene = FBSystem().Scene
playerControl = FBPlayerControl()
fStart = int(playerControl.ZoomWindowStart.GetFrame())
fStop = int(playerControl.ZoomWindowStop.GetFrame())
playerControl.GotoStart()

# Load models
root = FBFindModelByLabelName(ROOT_NAME)
ball = FBFindModelByLabelName(BALL_NAME)
constraint = su.FindConstraint(CONSTRAINT_NAME)

# Prepare animation
ball.Translation.SetAnimated(True)
ballAnimNode = ball.Translation.GetAnimationNode()
ballTXCurve = ballAnimNode.Nodes[0].FCurve
ballTYCurve = ballAnimNode.Nodes[1].FCurve
ballTZCurve = ballAnimNode.Nodes[2].FCurve
ballTXCurve.EditClear()
ballTYCurve.EditClear()
ballTZCurve.EditClear()

constraint.Active = True
constraint.Weight.SetAnimated(True)
weightNode = constraint.Weight.GetAnimationNode()
weightCurve = weightNode.FCurve
weightCurve.EditClear()

# Load candidates
candidate = ball.PropertyList.Find('IsUpCandidate')
candidateAnimNode = candidate.GetAnimationNode()
candidateFCurve = candidateAnimNode.FCurve

# Reduce keys
# consecutivesUps = 0
# redundantKeyIntervals = []
# for frame in range(len(candidateFCurve.Keys)):
#     key = candidateFCurve.Keys[frame]
#
#     if IsUp(key):
#         consecutivesUps += 1
#         if consecutivesUps == 3:
#             redundantKeyIntervals.append(candidateFCurve.Keys[frame-2].Time)
#     else:
#         if consecutivesUps >= 3:
#             redundantKeyIntervals.append(candidateFCurve.Keys[frame-1].Time)
#         consecutivesUps = 0
#
#     key.Interpolation = FBInterpolation.kFBInterpolationLinear
#
# for r in range(0, len(redundantKeyIntervals), 2):
#     candidateFCurve.KeyDelete(redundantKeyIntervals[r], redundantKeyIntervals[r+1], False)

# Calculate down positions
for frame in range(1, len(candidateFCurve.Keys)):
    key = candidateFCurve.Keys[frame]
    time = key.Time
    timeFrame = int(key.Time.GetFrame())
    if fStart <= timeFrame <= fStop:
        pos = FBVector4d()
        if not IsUp(key):
            preUp = candidateFCurve.Keys[frame - 1]
            nextUp = candidateFCurve.Keys[frame + 1]

            # Calculate global ground coordinates
            previousUpPos = mvu.GetGlobalPositionAtTime(ball, preUp.Time)
            nextUpPos = mvu.GetGlobalPositionAtTime(ball, nextUp.Time)
            direction = nextUpPos - previousUpPos
            direction /= 2.0
            globalPos = previousUpPos + direction
            globalPos[1] = GROUND_OFFSET

            # Get local coordinates
            FBPlayerControl().Goto(time)
            FBSystem().Scene.Evaluate()
            pos = mvu.GetRelativeVectorPosition(globalPos, root)
        else:
            print "Up:", key.Time
            pos = mvu.GetRelativePositionAtTime(ball, root, key.Time)

        ballTXCurve.KeyAdd(key.Time, pos[0])
        ballTYCurve.KeyAdd(key.Time, pos[1])
        ballTZCurve.KeyAdd(key.Time, pos[2])

# Set constraints (This have to be in an extra loop)
for frame in range(1, len(candidateFCurve.Keys)):
    key = candidateFCurve.Keys[frame]
    time = key.Time
    timeFrame = int(key.Time.GetFrame())
    if fStart <= timeFrame <= fStop:
        if not IsUp(key):
            weightCurve.KeyAdd(key.Time, 0.0)
        else:
            weightCurve.KeyAdd(FBTime(0, 0, 0, timeFrame), 100.0)
            #weightCurve.KeyAdd(FBTime(0,0,0,timeFrame + CONSTRAINT_TIME), 100.0)

# Set Interpolation to linear
su.SetLinearTangents(ballTXCurve)
su.SetLinearTangents(ballTYCurve)
su.SetLinearTangents(ballTZCurve)
su.SetLinearTangents(weightCurve)

# constraint.Active = False
playerControl.GotoStart()
