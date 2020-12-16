from pyfbsdk import *
import os


def FindCharacter(name):
    scene = FBSystem().Scene
    characters = scene.Characters
    for c in characters:
        if c.Name == name:
            return c


def FindPose(name):
    scene = FBSystem().Scene
    poses = scene.CharacterPoses
    for p in poses:
        print p.Name
        if p.Name == name:
            return p


def FindConstraint(name):
    constraints = FBSystem().Scene.Constraints
    for c in constraints:
        if c.Name == name:
            return c


def PlotToSkeleton(character):
    plotOptions = FBPlotOptions()
    plotOptions.ConstantKeyReducerKeepOneKey = False
    plotOptions.PlotAllTakes = False
    plotOptions.PlotOnFrame = True
    plotOptions.PlotPeriod = FBTime(0, 0, 0, 1)
    plotOptions.PlotTranslationOnRootOnly = True
    plotOptions.PreciseTimeDiscontinuities = False
    plotOptions.RotationFilterToApply = FBRotationFilter.kFBRotationFilterUnroll
    plotOptions.UseConstantKeyReducer = False
    character.PlotAnimation(FBCharacterPlotWhere.kFBCharacterPlotOnSkeleton, plotOptions)
    FBSystem().Scene.Evaluate()
    print "Plotted to Skeleton"


def PlotToControlRig(character):
    plotOptions = FBPlotOptions()
    plotOptions.ConstantKeyReducerKeepOneKey = False
    plotOptions.PlotAllTakes = False
    plotOptions.PlotOnFrame = True
    plotOptions.PlotPeriod = FBTime(0, 0, 0, 1)
    plotOptions.PlotTranslationOnRootOnly = True
    plotOptions.PreciseTimeDiscontinuities = False
    plotOptions.RotationFilterToApply = FBRotationFilter.kFBRotationFilterUnroll
    plotOptions.UseConstantKeyReducer = False
    character.PlotAnimation(FBCharacterPlotWhere.kFBCharacterPlotOnControlRig, plotOptions)
    FBSystem().Scene.Evaluate()
    print "Plotted to Control Rig"


def Pose(character, pose, mirror):
    """
    Adds a pose to a character
    @param character: FBCharacter
    @param pose: FBPose
    @param mirror: bool
    """
    poseOptions = FBCharacterPoseOptions()
    poseOptions.mCharacterPoseKeyingMode = FBCharacterPoseKeyingMode.kFBCharacterPoseKeyingModeBodyPart
    poseOptions.SetFlag(FBCharacterPoseFlag.kFBCharacterPoseMirror, mirror)
    character.SelectModels(True, False, True, False)
    pose.PastePose(character, poseOptions)
    FBSystem().Scene.Evaluate()


def DeselectAll():
    for comp in FBSystem().Scene.Components:
        comp.Selected = False
    FBSystem().Scene.Evaluate()


def SelectEffectors(root, pattern):
    if root and pattern:
        for child in root.Children:
            if child.Name.find(pattern) != -1 and child.Name.find("Effector") != -1:
                child.Selected = True
    else:
        print "Error selecting models: Root or pattern not available"
    FBSystem().Scene.Evaluate()


def SelectModels(root, pattern):
    if root and pattern:
        for child in root.Children:
            if child.Name.find(pattern) != -1:
                # print "Selected model:", child.Name
                child.Selected = True
            SelectModels(child, pattern)
    else:
        print "Error selecting models: Root or pattern not available"
    FBSystem().Scene.Evaluate()


def DeleteConstraints():
    constraints = FBSystem().Scene.Constraints
    toDelete = []
    for c in constraints:
        if c.Name != "Character":
            toDelete.append(c)
    for t in toDelete:
        t.FBDelete()
    FBSystem().Scene.Evaluate()


def DeleteCharacters():
    characters = FBSystem().Scene.Characters
    toDelete = []
    for c in characters:
        toDelete.append(c)
    for t in toDelete:
        t.FBDelete()
    FBSystem().Scene.Evaluate()


def DeleteControlRigs():
    sets = FBSystem().Scene.ControlSets
    toDelete = []
    for c in sets:
        toDelete.append(c)
    for t in toDelete:
        t.FBDelete()
    FBSystem().Scene.Evaluate()


def DeleteModel(model):
    # Always destroy from the last children to the first
    while len(model.Children) > 0:
        DeleteModel(model.Children[-1])
    model.FBDelete()


def SetLinearTangents(fCurve):
    for key in fCurve.Keys:
        key.Interpolation = FBInterpolation.kFBInterpolationLinear

def SetConstantTangents(fCurve):
    for key in fCurve.Keys:
        key.Interpolation = FBInterpolation.kFBInterpolationConstant
