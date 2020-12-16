from pyfbsdk import *
import os
import SceneUtils as su

reload(su)

scene = FBSystem().Scene
pose = su.FindPose("GrabBallBoth")
character = su.FindCharacter("Character")
characterRoot = FBFindModelByLabelName("Character_Ctrl:Reference")
playerControl = FBPlayerControl()
playerControl.GotoStart()
FBSystem().Scene.Evaluate()

# Key T-Pose at first frame
#poseOptions = FBCharacterPoseOptions()
#poseOptions.mCharacterPoseKeyingMode = FBCharacterPoseKeyingMode.kFBCharacterPoseKeyingModeBodyPart
#character.SelectModels(True, False, True, False)
#scene.Evaluate()
#playerControl.Key()

# Key normal hand poses at following frame
playerControl.Goto(FBTime(0, 0, 0, 0))
scene.Evaluate()
su.DeselectAll()
su.SelectModels(characterRoot, "Hand")
#su.Pose(character, pose, False)
# Flat key manually playerControl.Key()


#scene.Evaluate()