from pyfbsdk import *
import os 
import SceneUtils as su; reload(su)

scene = FBSystem().Scene
pose = su.FindPose("GrabBall")
character = su.FindCharacter("Character")
su.Pose(character, pose, False)
su.Pose(character, pose, True)