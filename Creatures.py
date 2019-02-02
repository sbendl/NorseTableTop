import copy
import math

import Materials


class Character():
    def __init__(self, skills, traits):
        self.skills = skills
        self.traits = traits
        self.items = []


class Thing(Materials.Material):
    def __init__(self):
        super().__init__()


# class BodyPlan:
#     def __init__(self):
#         self.parts_list = []


class BodyPart:
    def __init__(self, parent, children, contents, can_grasp, can_attack):
        self.name = type(self).__name__
        self.parent = parent
        self.children = children
        self.contents = contents
        self.equipped = []
        self._can_grasp = can_grasp
        self.held = None
        self.can_attack = can_attack

    def scale(self, factor):
        raise NotImplementedError

    def can_grasp(self):
        return self._can_grasp and self.held is None

    def equip(self, item, held=False):
        if held and self.can_grasp and self.held is None:
            self.held = item
        else:
            if item not in self.equipped:
                self.equipped.append(item)

    def unequip(self, item, body_part):
        if body_part.can_grasp and item in self.equipped:
            body_part.equip(item, held=True)
            self.equipped.remove(item)

    def drop(self, item):
        if item in self.held:
            self.held = None

    def __repr__(self):
        return self.name

    def __str__(self):
        return self.name


class Digit(BodyPart, Materials.Fleshy):
    def __init__(self, parent=None, children=[].copy(), contents=None, opposable=False, joints=3.0, length=95.0,
                 width=17.0):
        super().__init__(parent, children, contents, can_grasp=False)
        self.num_joints = joints
        self.opposable = opposable
        self.length = length / 1000
        self.width = width / 1000
        self.volume = math.pi * (self.width / 2) ** 2 * self.length
        self.mass = self.volume * self.density

    def scale(self, factor):
        self.length = self.length * factor
        self.width = self.width * factor
        self.volume = math.pi * (self.width / 2) ** 2 * self.length
        self.mass = self.volume * self.density


class LimbTerminus(BodyPart, Materials.Fleshy):
    def __init__(self, parent=None, children=[].copy(), contents=None, length=96.0, width=84.0, thickness=35.0,
                 can_grasp=True):
        super().__init__(parent, children, contents, can_grasp)
        self.length = length / 1000
        self.width = width / 1000
        self.thickness = thickness / 1000
        self.volume = self.length * self.width * self.thickness
        self.mass = self.volume * self.density

    def scale(self, factor):
        self.length = self.length * factor
        self.width = self.width * factor
        self.thickness = self.thickness * factor
        self.volume = self.length * self.width * self.thickness
        self.mass = self.volume * self.density


class LimbSegment(BodyPart, Materials.Fleshy):
    def __init__(self, parent=None, children=[].copy(), contents=None, length=460.0, width=80.0, can_grasp=False):
        super().__init__(parent, children, contents, can_grasp)
        self.length = length
        self.width = width
        self.volume = math.pi * (self.width / 2) ** 2 * self.length
        self.mass = self.volume * self.density

    def scale(self, factor):
        self.length = self.length * factor
        self.width = self.width * factor
        self.volume = math.pi * (self.width / 2) ** 2 * self.length
        self.mass = self.volume * self.density


class Joint(BodyPart, Materials.Fleshy):
    def scale(self, factor):
        pass

    def __init__(self, parent=None, children=[].copy(), contents=None):
        super().__init__(parent, children, contents, False)



class TorsoSegment(BodyPart, Materials.Fleshy):
    def __init__(self, parent=None, children=[].copy(), contents=None, length=300.0, width=142.0, thickness=86.0):
        super().__init__(parent, children, contents, can_grasp=False)
        self.length = length
        self.width = width
        self.thickness = thickness
        self.volume = self.length * self.width * self.thickness
        self.mass = self.volume * self.density

    def scale(self, factor):
        self.length = self.length * factor
        self.width = self.width * factor
        self.thickness = self.thickness * factor
        self.volume = self.length * self.width * self.thickness
        self.mass = self.volume * self.density


class Neck(BodyPart, Materials.Fleshy):
    def __init__(self, parent=None, children=[].copy(), contents=None, length=110.0, width=113.0):
        super().__init__(parent, children, contents, can_grasp=False)
        self.length = length / 1000
        self.width = width / 1000
        self.volume = math.pi * (self.width / 2) ** 2 * self.length
        self.mass = self.volume * self.density

    def scale(self, factor):
        self.length = self.length * factor
        self.width = self.width * factor
        self.volume = math.pi * (self.width / 2) ** 2 * self.length
        self.mass = self.volume * self.density


class Head(BodyPart, Materials.Fleshy):
    def __init__(self, parent=None, children=[].copy(), contents=None, length=218.0, width=186.0):
        super().__init__(parent, children, contents, can_grasp=False)
        self.length = length / 1000
        self.width = width / 1000
        self.volume = math.pi * (self.width / 2) ** 2 * self.length
        self.mass = self.volume * self.density

    def scale(self, factor):
        self.length = self.length * factor
        self.width = self.width * factor
        self.volume = math.pi * (self.width / 2) ** 2 * self.length
        self.mass = self.volume * self.density


class Humanoid(Thing):
    num_arms = 2
    num_legs = 2
    num_fingers = 5
    num_toes = 5
    ideal_head = Head(contents=None, length=1 / 7.5, width=1 / 11.5)
    ideal_neck = Neck(contents=None, length=1 / 11.5, width=1 / 11.5)
    ideal_upper_torso = TorsoSegment(contents=None, length=1.5 / 7.5, width=2 / 11.5, thickness=1.25 / 11.5)
    ideal_upper_torso.name = 'Upper Torso'
    ideal_lower_torso = TorsoSegment(contents=None, length=1.25 / 7.5, width=1.75 / 11.5, thickness=1.5 / 11.5)
    ideal_lower_torso.name = 'Lower Torso'
    ideal_upper_leg = LimbSegment(contents=None, length=2 / 7.5, width=1 / 11.5)
    ideal_lower_leg = LimbSegment(contents=None, length=1.75 / 7.5, width=.5 / 11.5)
    ideal_foot = LimbTerminus(contents=None, length=1.5 / 11.5, width=.5 / 11.5, thickness=.4 / 11.5)
    ideal_toe = Digit(contents=None, length=.2 / 11.5, width=.1 / 11.5)
    ideal_upper_arm = LimbSegment(contents=None, length=2 / 11.5, width=.4 / 11.5)
    ideal_lower_arm = LimbSegment(contents=None, length=2 / 11.5, width=.25 / 11.5)
    ideal_palm = LimbTerminus(contents=None, length=.8 / 11.5, width=.8 / 11.5, thickness=.2 / 11.5)
    ideal_finger = Digit(contents=None, length=.5 / 11.5, width=.15 / 11.5)
    ideal_joint = Joint()

    def __init__(self, height):
        super().__init__()
        self.head = copy.deepcopy(self.ideal_head)
        self.neck = copy.deepcopy(self.ideal_neck)
        self.upper_torso = copy.deepcopy(self.ideal_upper_torso)
        self.lower_torso = copy.deepcopy(self.ideal_lower_torso)

        self.left_upper_leg = copy.deepcopy(self.ideal_upper_leg)
        self.left_upper_leg.name = 'Left Upper Leg'

        self.right_upper_leg = copy.deepcopy(self.ideal_upper_leg)
        self.right_upper_leg.name = 'Right Upper Leg'

        self.left_knee = copy.deepcopy(self.ideal_joint)
        self.left_knee.name = 'Left Knee'

        self.right_knee = copy.deepcopy(self.ideal_joint)
        self.right_knee.name = 'Right Knee'

        self.left_lower_leg = copy.deepcopy(self.ideal_lower_leg)
        self.left_lower_leg.name = 'Left Lower Leg'

        self.right_lower_leg = copy.deepcopy(self.ideal_lower_leg)
        self.right_lower_leg.name = 'Right Lower Leg'

        self.left_foot = copy.deepcopy(self.ideal_foot)
        self.left_foot.name = 'Left Foot'

        self.right_foot = copy.deepcopy(self.ideal_foot)
        self.right_foot.name = 'Right Foot'

        self.left_toes = copy.deepcopy([copy.deepcopy(self.ideal_toe) for i in range(5)])
        self.right_toes = copy.deepcopy([copy.deepcopy(self.ideal_toe) for i in range(5)])

        self.left_upper_arm = copy.deepcopy(self.ideal_upper_arm)
        self.left_upper_arm.name = 'Left Upper Arm'

        self.right_upper_arm = copy.deepcopy(self.ideal_upper_arm)
        self.right_upper_arm.name = 'Right Upper Arm'

        self.left_elbow = copy.deepcopy(self.ideal_joint)
        self.left_elbow.name = 'Left Elbow'

        self.right_elbow = copy.deepcopy(self.ideal_joint)
        self.right_elbow.name = 'Right Elbow'

        self.left_lower_arm = copy.deepcopy(self.ideal_lower_arm)
        self.left_lower_arm.name = 'Left Lower Arm'

        self.right_lower_arm = copy.deepcopy(self.ideal_lower_arm)
        self.right_lower_arm.name = 'Right Lower Arm'

        self.left_palm = copy.deepcopy(self.ideal_palm)
        self.left_palm.name = 'Left Hand'

        self.right_palm = copy.deepcopy(self.ideal_palm)
        self.right_palm.name = 'Right Hand'

        self.left_fingers = copy.deepcopy([copy.deepcopy(self.ideal_finger) for i in range(5)])
        self.right_fingers = copy.deepcopy([copy.deepcopy(self.ideal_finger) for i in range(5)])

        self.head.children = [self.neck]
        self.neck.parent = self.head
        self.neck.children = [self.upper_torso]
        self.upper_torso.parent = self.neck
        self.upper_torso.children = [self.lower_torso, self.right_upper_arm, self.left_upper_arm]
        self.lower_torso.parent = self.upper_torso
        self.lower_torso.children = [self.left_upper_leg, self.right_upper_leg]
        self.left_upper_leg.parent = self.lower_torso
        self.left_upper_leg.children = [self.left_knee]
        self.right_upper_leg.parent = self.lower_torso
        self.right_upper_leg.children = [self.right_knee]
        self.right_knee.parent = self.right_upper_leg
        self.right_knee.children = [self.right_lower_leg]
        self.left_knee.parent = self.left_upper_leg
        self.left_knee.children = [self.left_lower_leg]
        self.left_lower_leg.parent = self.left_knee
        self.left_lower_leg.children = [self.left_foot]
        self.right_lower_leg.parent = self.right_knee
        self.right_lower_leg.children = [self.right_foot]
        self.left_foot.parent = self.left_lower_leg
        self.left_foot.children = self.left_toes
        self.right_foot.parent = self.right_lower_leg
        self.right_foot.children = self.right_toes
        self.left_upper_arm.parent = self.upper_torso
        self.left_upper_arm.children = [self.left_lower_arm]
        self.right_upper_arm.parent = self.upper_torso
        self.right_upper_arm.children = [self.right_lower_arm]
        self.left_lower_arm.parent = self.left_upper_arm
        self.left_lower_arm.children = [self.left_palm]
        self.right_lower_arm.parent = self.right_upper_arm
        self.right_lower_arm.children = [self.right_palm]
        self.left_palm.parent = self.left_lower_arm
        self.left_palm.children = self.left_fingers
        self.right_palm.parent = self.right_lower_arm
        self.right_palm.children = self.right_fingers

        for i, finger in enumerate(self.right_fingers):
            finger.name = "Right Finger %s" % str(i + 1)
            finger.parent = self.right_palm
            finger.children = []
        for i, finger in enumerate(self.left_fingers):
            finger.name = "Left Finger %s" % str(i + 1)
            finger.parent = self.left_palm
            finger.children = []

        for i, toe in enumerate(self.right_toes):
            toe.name = "Right toe %s" % str(i + 1)
            toe.parent = self.right_foot
            toe.children = []
        for i, toe in enumerate(self.left_toes):
            toe.name = "Left toe %s" % str(i + 1)
            toe.parent = self.left_foot
            toe.children = []

        self.parts_list = [self.head, self.neck, self.upper_torso, self.lower_torso, self.left_upper_leg,
                           self.right_upper_leg, self.left_lower_leg, self.right_lower_leg, self.left_foot,
                           self.right_foot, self.left_upper_arm, self.right_upper_arm, self.left_lower_arm,
                           self.right_lower_arm, self.left_palm, self.right_palm]

        self.parts_list.extend(self.left_fingers)
        self.parts_list.extend(self.right_fingers)
        self.parts_list.extend(self.left_toes)
        self.parts_list.extend(self.right_toes)

        for part in self.parts_list:
            part.scale(height)


class Human(Humanoid, Character):
    max_height = 2.7
    min_height = .6
    max_bmi = 70
    min_bmi = 10

    def __init__(self, height):
        super().__init__(height)


# TODO Attacks don't come from body level but from part level - i.e. leg can attack
# TODO if part is weilding an object use the corresponding attack method from the object
# TODO Attacks come in: Jab Foreswing Backswing Downswing Upswing