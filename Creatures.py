import math


class BodyPart:
    name = ""
    parent = None

class Finger(BodyPart, ):

    def __init__(self, opposable=False, joints=3, length=95, diameter=17):
        self.num_joints = joints
        self.opposable = opposable
        self.length = length/1000
        self.diameter = diameter / 1000
        self.volume = math.pi * (self.diameter / 2) **2 * self.length
        self.mass = self.volume * self.density

class Hand(BodyPart):


class BodyPlan:
    base_part = None
    parts_list = []

class Bipedal(BodyPlan):


class Human:
    num_arms = 2
    num_legs = 2
    elbow_len = 460 / 1000
