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
