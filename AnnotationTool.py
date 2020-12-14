# This tool helps to annotate intervals of frames.

from pyfbsdk import *
from pyfbsdk_additions import *
import AnnotationFlags as af; reload(af)

CURVE_OBJECT = "CharacterRoot"
flags = af.Flags()
startFrame = FBEditNumber()
endFrame = FBEditNumber()
annotationsCurve = FBFCurve()

# Load dependencies
scene = FBSystem().Scene
playerControl = FBPlayerControl()
fStart = int(playerControl.ZoomWindowStart.GetFrame())
fStop = int(playerControl.ZoomWindowStop.GetFrame())
playerControl.GotoStart()

def LoadCurve():
    global annotationsCurve
    character = FBFindModelByLabelName(CURVE_OBJECT)
    annotations = character.PropertyList.Find('AnnotationFlags')
    annotations.SetAnimated(True)
    annotationsNode = annotations.GetAnimationNode()
    annotationsCurve = annotationsNode.FCurve

def SetFlag(control, event):
    af.SetValue(flags, control.Caption, control.State)
    print "Flag changed to", bin(flags.asByte), "(", flags.asByte,")"

def ClearCurve(control, event):
    annotationsCurve.EditClear()

def SetCurve(control, event):
    LoadCurve()
    time = FBTime(0, 0, 0, int(startFrame.Value))
    annotationsCurve.KeyAdd(time, flags.asByte)
    time = FBTime(0, 0, 0, int(endFrame.Value))
    annotationsCurve.KeyAdd(time, flags.asByte)
    for key in annotationsCurve.Keys:
        key.Interpolation = FBInterpolation.kFBInterpolationConstant

def PopulateLayout(mainLayout):
    x = FBAddRegionParam(5, FBAttachType.kFBAttachLeft, "")
    y = FBAddRegionParam(5, FBAttachType.kFBAttachTop, "")
    w = FBAddRegionParam(-5, FBAttachType.kFBAttachRight, "")
    h = FBAddRegionParam(-5, FBAttachType.kFBAttachBottom, "")
    main = FBHBoxLayout()
    mainLayout.AddRegion("main", "main", x, y, w, h)
    mainLayout.SetControl("main", main)

    # Left Side: Layout with checkboxes for the flags
    checkboxes = FBVBoxLayout(FBAttachType.kFBAttachTop)
    ratio = 1.0 / (len(af.FlagsBits._fields_) + 1)
    header = FBLabel()
    header.Caption = "Labels"
    checkboxes.AddRelative(header, ratio)
    for field in af.FlagsBits._fields_:
        print field[0]
        b = FBButton()
        b.Style = FBButtonStyle.kFBCheckbox
        b.Caption = field[0]
        b.OnClick.Add(SetFlag)
        checkboxes.AddRelative(b, ratio)
    main.AddRelative(checkboxes, 1.0)

    # RightSide
    rightBox = FBVBoxLayout(FBAttachType.kFBAttachTop)

    # Start and end frame edits
    startFrameLabel = FBLabel()
    startFrameLabel.Caption = "Start Frame (inclusive)"
    rightBox.AddRelative(startFrameLabel, 0.25)
    startFrame.Min = fStart
    startFrame.Max = fStop
    rightBox.AddRelative(startFrame, 0.5)

    endFrameLabel = FBLabel()
    endFrameLabel.Caption = "End Frame (inclusive)"
    rightBox.AddRelative(endFrameLabel, 0.25)
    endFrame.Min = fStart
    endFrame.Max = fStop
    rightBox.AddRelative(endFrame, 0.5)

    # Add clear button
    applyButton = FBButton()
    applyButton.Caption = "Clear Curve"
    applyButton.Justify = FBTextJustify.kFBTextJustifyCenter
    applyButton.OnClick.Add(ClearCurve)
    rightBox.AddRelative(applyButton, 1.0)

    # Add apply button
    applyButton = FBButton()
    applyButton.Caption = "Apply"
    applyButton.Justify = FBTextJustify.kFBTextJustifyCenter
    applyButton.OnClick.Add(SetCurve)
    rightBox.AddRelative(applyButton, 1.0)

    main.AddRelative(rightBox, 1.0)

def CreateTool():
    t = FBCreateUniqueTool("Annotator")
    t.StartSizeX = 300
    t.StartSizeY = 400
    PopulateLayout(t)
    ShowTool(t)

CreateTool()
