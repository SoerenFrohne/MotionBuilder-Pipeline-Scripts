from pyfbsdk import *
import os


def GetRelativeTransform(nodeA, nodeB):
    mat1 = FBMatrix();
    nodeA.GetMatrix(mat1)

    mat2 = FBMatrix();
    nodeB.GetMatrix(mat2)
    mat2.Inverse()

    return mat2 * mat1


def GetRelativeTransformAtTime(nodeA, nodeB, time):
    FBPlayerControl().Goto(time)
    FBSystem().Scene.Evaluate()
    return GetRelativeTransform(nodeA, nodeB)


def GetRelativeNodePosition(nodeA, nodeB):
    t = GetRelativeTransform(nodeA, nodeB)
    return FBVector3d(t[12], t[13], t[14])


def GetRelativeVectorPosition(vector, node):
    # Get relative coordinate system
    nodeTransform = FBMatrix()
    node.GetMatrix(nodeTransform)
    rootInverseTransform = FBMatrix()
    FBMatrixInverse(rootInverseTransform, nodeTransform)

    # Calculate local Position:
    pos = FBVector4d()
    pos[0] = vector[0]
    pos[1] = vector[1]
    pos[2] = vector[2]
    pos[3] = 1.0

    localPos = FBVector4d()
    FBVectorMatrixMult(localPos, rootInverseTransform, pos)
    return localPos


def GetRelativePositionAtTime(nodeA, nodeB, time):
    t = GetRelativeTransformAtTime(nodeA, nodeB, time)
    return FBVector3d(t[12], t[13], t[14])


def GetGlobalPositionAtTime(node, time):
    FBPlayerControl().Goto(time)
    FBSystem().Scene.Evaluate()
    position = FBVector3d()
    node.GetVector(position, FBModelTransformationType.kModelInverse_Translation, True)
    return position


# Matrix 4x4
def Multiply(vector, matrix):
    print len(vector)
    if len(vector) <= 3:
        vector = [vector[0], vector[1], vector[2], 0]
    result = [0, 0, 0, 0]
    result[0] = matrix[0] * vector[0] + matrix[1] * vector[1] + matrix[2] * vector[2] + matrix[3] * vector[3]
    result[1] = matrix[4] * vector[0] + matrix[5] * vector[1] + matrix[6] * vector[2] + matrix[7] * vector[3]
    result[2] = matrix[8] * vector[0] + matrix[9] * vector[1] + matrix[10] * vector[2] + matrix[11] * vector[3]
    result[3] = matrix[12] * vector[0] + matrix[13] * vector[1] + matrix[14] * vector[2] + matrix[15] * vector[3]
    return FBVector3d(result[0], result[1], result[2])


def GetTranslation(matrix):
    return FBVector3d(matrix[12], matrix[13], matrix[14])


def GetTransform(node):
    transform = FBMatrix();
    node.GetMatrix(transform)
    return transform
