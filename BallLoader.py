from pyfbsdk import *
# from pyfbsdk_additions import *

# Load default objects
scene = FBSystem().Scene
constraintManager = FBConstraintManager()

# Find Ball and rescale ball
scaleFactor = 8
ball = FBFindModelByLabelName('Ball')
ball.Scaling = FBVector3d(scaleFactor, scaleFactor, scaleFactor)
ball.Show = True

# Pin ball to characters hand
parentChildConstraint = constraintManager.TypeCreateConstraint('Parent/Child')