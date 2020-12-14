from pyfbsdk import *
import os


def FindCharacter(name):
    scene = FBSystem().Scene
    characters = scene.Characters
    for c in characters:
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
