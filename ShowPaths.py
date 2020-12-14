from pyfbsdk import *
import os 
import SceneUtils as su; reload(su)

sourceCharacter = su.FindCharacter("Source")
character = su.FindCharacter("Character")

#su.PlotToSkeleton(character)
su.PlotToControlRig(character)