from pyfbsdk import *
import os 

# GLOBAL_PARAMETERS
ROOT_NAME = "Hips" 

# Load dependencies
scene = FBSystem().Scene
playerControl = FBPlayerControl()
fStart = int(playerControl.ZoomWindowStart.GetFrame())
fStop = int(playerControl.ZoomWindowStop.GetFrame())
playerControl.GotoStart()

# Load model
root = FBFindModelByLabelName(ROOT_NAME)

# Change namespace
root.ProcessNamespaceHierarchy(FBNamespaceAction.kFBRemoveAllNamespace, '', '')
root.ProcessNamespaceHierarchy(FBNamespaceAction.kFBReplaceNamespace, '', 'Source')

# Load joints
joints = FBComponentList()
FBFindObjectsByName('Source:*', joints, True, True)
for comp in joints:
    print comp, comp.LongName

# Add character
sourceCharacter = FBCharacter('Source')

# Define skeleton
#sourceCharacter.PropertyList.Find('HipsLink').append(hips)
for joint in joints:
    slot = sourceCharacter.PropertyList.Find(joint.Name + 'Link')  # This only works for HIK naming convention
    if slot is not None:
        slot.append(joint)
    else:
        print "No joints found for", joint.Name

sourceCharacter.SetCharacterizeOn(True)
FBSystem().Scene.Evaluate()
