from pyfbsdk import *
import os    
import math

# Rotate a vector around the y axis by angle alpha
def RotateAroundYAxis(vector, alpha):
    rotMat = FBMatrix()
    rotMat[0] = math.cos(alpha)
    rotMat[2] = math.sin(alpha)
    rotMat[5] = 1
    rotMat[8] = -math.sin(alpha)
    rotMat[10] = math.cos(alpha)
    return Multiply(mat, vector)

def Multiply(matrix, vector):
    if len(vector) <= 3:
        vector = [vector[0], vector[1], vector[2], 1]
    result = [0,0,0,0]      
    result[0] = matrix[0] * vector[0] + matrix[1] * vector[1] + matrix[2] * vector[2] + matrix[3] * vector[3]
    result[1] = matrix[4] * vector[0] + matrix[5] * vector[1] + matrix[6] * vector[2] + matrix[7] * vector[3]
    result[2] = matrix[8] * vector[0] + matrix[9] * vector[1] + matrix[10] * vector[2] + matrix[11] * vector[3]
    result[3] = matrix[12] * vector[0] + matrix[13] * vector[1] + matrix[14] * vector[2] + matrix[15] * vector[3]
    return FBVector3d(-result[0], -result[1], result[2]) 

def GetAngleBetweenVectors(v1, v2):
    a = FBVector3d(v1[0], v1[1], v1[2])
    b = FBVector3d(v2[0], v2[1], v2[2])
    a.Normalize()
    b.Normalize()
    dot = a.DotProduct(b)
    return math.acos(dot)

RAD2DEGREE = 57.295779513082

# Load default setup
scene = FBSystem().Scene
playerControl = FBPlayerControl()
fStart = int(playerControl.ZoomWindowStart.GetFrame())
fStop = int(playerControl.ZoomWindowStop.GetFrame())
playerControl.GotoStart()

# Prepare models
hips = FBFindModelByLabelName("mixamorig:Hips")
hipsTanslation = hips.Translation.GetAnimationNode()
hipsRotation = hips.Rotation.GetAnimationNode()
rootMotion = FBFindModelByLabelName("RootMotion")
rootMotion.Translation.SetAnimated(True)
rootMotion.Rotation.SetAnimated(True)
rootTranslation = rootMotion.Translation.GetAnimationNode()
rootRotation = rootMotion.Rotation.GetAnimationNode()

tXCurve = rootTranslation.Nodes[0].FCurve
tYCurve = rootTranslation.Nodes[1].FCurve
tZCurve = rootTranslation.Nodes[2].FCurve
rXCurve = rootRotation.Nodes[0].FCurve
rYCurve = rootRotation.Nodes[1].FCurve
rZCurve = rootRotation.Nodes[2].FCurve
tXCurve.EditClear()
tYCurve.EditClear()
tZCurve.EditClear()
rXCurve.EditClear()
rYCurve.EditClear()
rZCurve.EditClear()

for i in range(fStart, fStop):    
    time = FBTime(0, 0, 0, i)
    playerControl.Goto(time)
    scene.Evaluate()
    
    # Set translation to follow hips to ground projection
    position = FBVector3d()
    hips.GetVector(position, FBModelTransformationType.kModelInverse_Translation, True)
    tXCurve.KeyAdd(time, position[0])
    tZCurve.KeyAdd(time, position[2])

    # Set to rotation to follow hips forward vector
    mat = FBMatrix()
    rot = FBMatrix()
    rotation = FBVector3d()
    hips.GetMatrix(mat)
    FBMatrixToRotation(rotation, mat, FBRotationOrder.kFBXYZ)
    
    # Nullify rotation around the x and z axis while avoiding gimbal lock
    up = FBVector3d(0,100,0)
    forward = FBVector4d(0,0,100,1) 

    print hips.RotationOrder
    rotationMatrix = FBMatrix()
    FBRotationToMatrix(rotationMatrix, rotation, FBRotationOrder.kFBXYZ)
    
    forwardResult = FBMatrix()
    forwardResult = Multiply(rotationMatrix, forward)
    forwardResult[1] = 0
    #forwardResult += position
    #left = forwardResult.CrossProduct(up)
    #left.Normalize()
    #left *= 100
    
    angle = GetAngleBetweenVectors(forward, forwardResult)
    
    #FBMult(forwardResult, rotationMatrix, forward)
    #forwardResult = rotationMatrix * forward
    print angle * RAD2DEGREE
    
    #quaternion = FBVector4d()
    #FBRotationToQuaternion(quaternion, rotation, FBRotationOrder.kFBXYZ)
    #FBQuaternionToRotation(rotation, quaternion, FBRotationOrder.kFBXYZ)
   
    rXCurve.KeyAdd(time, 0)
    rYCurve.KeyAdd(time, angle * RAD2DEGREE)
    rZCurve.KeyAdd(time, 0)

