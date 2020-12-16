from pyfbsdk import *
import os 
import SceneUtils as su; reload(su)


character = su.FindCharacter("Character")

layer = FBSystem().CurrentTake.GetLayerByName("HandPoses")
if layer: 
    layer.FBDelete()
su.PlotToSkeleton(character)
su.DeleteConstraints()
su.DeleteCharacters()
su.DeleteControlRigs()
skeleton = FBFindModelByLabelName("Reference")
su.DeleteModel(skeleton)