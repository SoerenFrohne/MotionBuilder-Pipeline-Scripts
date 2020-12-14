from pyfbsdk import *
import os 
import SceneUtils as su; reload(su)

scene = FBSystem().Scene
pose = su.FindPose("GrabBall")
character = su.FindCharacter("Character")
playerControl = FBPlayerControl()
playerControl.GotoStart()
FBSystem().Scene.Evaluate()

# Key T-Pose at first frame
poseOptions = FBCharacterPoseOptions()
poseOptions.mCharacterPoseKeyingMode = FBCharacterPoseKeyingMode.kFBCharacterPoseKeyingModeBodyPart
character.SelectModels(True, False, True, False)
scene.Evaluate()
playerControl.Key()

# Key normal hand poses at following frame
playerControl.Goto(FBTime(0,0,0,1))
scene.Evaluate()
su.Pose(character, pose, False)
playerControl.Key()
scene.Evaluate()
#su.Pose(character, pose, True)