import ctypes

c_uint16 = ctypes.c_uint16


class FlagsBits(ctypes.LittleEndianStructure):
    _fields_ = [
        ("idle", c_uint16, 1),
        ("forwards", c_uint16, 1),
        ("backwards", c_uint16, 1),
        ("walk", c_uint16, 1),
        ("jog", c_uint16, 1),
        ("sprint", c_uint16, 1),
        ("dribble", c_uint16, 1),
        ("defense", c_uint16, 1),
        ("stumble", c_uint16, 1),
        ("accelerate", c_uint16, 1),
        ("throw", c_uint16, 1),
        ("catch", c_uint16, 1),
        ("shot", c_uint16, 1),
        ("feint", c_uint16, 1),
        ("standard", c_uint16, 1),
        ("lift", c_uint16, 1)
    ]


class Flags(ctypes.Union):
    _anonymous_ = ("bit",)
    _fields_ = [
        ("bit", FlagsBits),
        ("asByte", c_uint16)
    ]


def SetValue(flags, label, value):
        setattr(flags, label, value)
        
#for field in FlagsBits._fields_:
#    print field[0]
#flags.asByte = 0b1111111111111111
#print "Result:", bin(flags.asByte)
#print(flags.asByte)
#print("idle: %i" % flags.idle)
#print("forwards: %i" % flags.forwards)
#print("standard: %i" % flags.standard)
