import math

import Materials


class BodyPart:
    name = ""
    
    def __init__(self, parent, child, contents):
        self.parent = parent
        self.child = child
        self.contents = contents

class Digit(BodyPart, Materials.Fleshy):

    def __init__(self, parent, child, contents, opposable=False, joints=3, length=95, width=17):
        super().__init__(parent, child, contents)
        self.num_joints = joints
        self.opposable = opposable
        self.length = length/1000
        self.width = width / 1000
        self.volume = math.pi * (self.width / 2) **2 * self.length
        self.mass = self.volume * self.density


class LimbTerminus(BodyPart, Materials.Fleshy):

    def __init__(self, parent, child, contents, length=96, width=84, thickness=35):
        super().__init__(parent, child, contents)
        self.length = length / 1000
        self.width = width / 1000
        self.thickness = thickness / 1000
        self.volume = self.length * self.width * self.thickness
        self.mass = self.volume * self.density


class LimbSegment(BodyPart, Materials.Fleshy):

    def __init__(self, parent, child, contents, length=460, width=80):
        super().__init__(parent, child, contents)
        self.length = length
        self.width = width
        self.volume = math.pi * (self.width / 2) **2 * self.length
        self.mass = self.volume * self.density


class TorsoSegment(BodyPart, Materials.Fleshy):

    def __init__(self, parent, child, contents, length=300, width=142, thickness=86):
        super().__init__(parent, child, contents)
        self.length = length
        self.width = width
        self.thickness = thickness
        self.volume = self.length * self.width * self.thickness
        self.mass = self.volume * self.density


class Neck(BodyPart, Materials.Fleshy):

    def __init__(self, parent, child, contents, length=110, width=113):
        super().__init__(parent, child, contents)
        self.length = length/1000
        self.width = width / 1000
        self.volume = math.pi * (self.width / 2) **2 * self.length
        self.mass = self.volume * self.density


class Head(BodyPart, Materials.Fleshy):

    def __init__(self, parent, child, contents, length=218, width=186):
        super().__init__(parent, child, contents)
        self.length = length/1000
        self.width = width / 1000
        self.volume = math.pi * (self.width / 2) **2 * self.length
        self.mass = self.volume * self.density


class BodyPlan:
    parts_list = []


class Bipedal(BodyPlan):

    def 
    

class Human:
    num_arms = 2
    num_legs = 2
    elbow_len = 460 / 1000
