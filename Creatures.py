import copy
import math

from scipy import integrate
import numpy as np

import Materials


class Character():
    def __init__(self, skills, traits):
        self.skills = skills
        self.traits = traits
        self.items = []


class Creature():
    strength_scaler = None


class Thing(Materials.Material):
    def __init__(self):
        super().__init__()
        self.mass = 0
        self.volume = 0

    def calc_moment_of_inertia(self, extra_length=0):
        raise NotImplementedError


class Organ(Thing):
    def __init__(self, critical):
        super().__init__()
        self.critical = critical


class FloatingOrgan(Organ):
    def __init__(self, relative_size, **kwargs):
        super().__init__(**kwargs)
        self.relative_size = relative_size


class Brain(FloatingOrgan, Materials.Fleshy):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)


class Stomach(FloatingOrgan, Materials.Fleshy):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)


class Liver(FloatingOrgan, Materials.Fleshy):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)


class Intestines(FloatingOrgan, Materials.Fleshy):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)


class Lung(FloatingOrgan, Materials.Fleshy):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)


class Heart(FloatingOrgan, Materials.Muscle):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)


class WrapperOrgan(Organ):
    layer_padding = 0

    def __init__(self, thickness, **kwargs):
        super().__init__(**kwargs)
        self.thickness = thickness


class Larynx(WrapperOrgan, Materials.Fleshy):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)


class WrappingBone(WrapperOrgan, Materials.Bone):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)


class FloatingBone(FloatingOrgan, Materials.Bone):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)


class SkinLayer(WrapperOrgan, Materials.Fleshy):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)


class MuscleLayer(WrapperOrgan, Materials.Muscle):
    def __init__(self, **kwargs):
        super().__init__(critical=False, **kwargs)

class FloatingOrganLayer(Organ, Materials.Fleshy):
    def __init__(self, contents, **kwargs):
        super().__init__(critical=False, **kwargs)
        self.contents = contents

# class BodyPlan:
#     def __init__(self):
#         self.parts_list = []

class CompoundItemLayers:
    def __init__(self, layers):
        self.layers = layers
        self.min_pierce_limit = self.layers[0].shear_plastic_limit

    def calc_damage(self, KE, volume):
        print("armour:")
        pl = self.shear_plastic_limit * volume
        el = self.shear_elastic_limit * volume

        print(KE, el, pl)

        if KE > pl:
            print('Pierced')
        elif KE > el:
            print('Bent')
            for s in np.linspace(0, self.strain_at_fracture, 100, endpoint=False):
                if integrate.quad(self.shear_stress_strain, 0, s)[0] * volume > KE:
                    print(s)
                    break
        else:
            print('Deflected')

    def calc_cutting_damage(self, KE, other):
        pass

    def calc_piercing_damage(self, KE, other):
        pass

    def calc_crushing_damage(self, KE, other):
        w = min(self.width, other.width)
        l = min(self.length, other.length)
        a = (2 * w + 2 * l) * self.thickness



class BodyPart(Thing):
    def __init__(self, parent, children, layers, can_grasp, can_attack, core=False):
        super().__init__()
        self.name = type(self).__name__
        self.parent = parent
        self.children = children
        self.layers = layers
        self.equipped = []
        self._can_grasp = can_grasp
        self.held = None
        self.can_attack = can_attack
        self.core = core
        self.length = None
        self.width = None
        self.thickness = None
        self.mom_inertia = None
        self.creature = None

    def scale(self, factor):
        self.length = self.length * factor
        self.width = self.width * factor
        self.volume = self.calc_volume()
        self.mass = self.volume * self.density

    def calc_volume(self):
        return self.length * self.width * self.thickness

    def calc_moment_of_inertia(self, extra_length=0):
        return (1 / 3) * self.mass * (self.length + extra_length) ** 2

    def calc_moment_of_inertia_below(self, len_to_part=0):
        I = self.calc_moment_of_inertia(len_to_part)

        if self.held is not None:
            I += self.held.calc_moment_of_inertia(len_to_part + self.length)

        if self.children is None:
            return I
        else:
            for part in self.children:
                I += part.calc_moment_of_inertia_below(len_to_part=len_to_part + self.length)

            return I

    def can_grasp(self):
        return self._can_grasp and self.held is None

    def equip(self, item, held=False):
        if held and self.can_grasp and self.held is None:
            self.held = item
        else:
            if item not in self.equipped:
                self.equipped.append(item)
                self.mass += item.mass

    def unequip(self, item, body_part):
        if body_part.can_grasp and item in self.equipped:
            body_part.equip(item, held=True)
            self.equipped.remove(item)
            self.mass -= item.mass

    def drop(self, item):
        if item in self.held:
            self.held = None

    def get_parts_below(self):
        parts = [self]

        if self.children is None:
            return parts
        else:
            for part in self.children:
                parts.extend(part.get_parts_below())

            return parts

    def get_parts_above(self, num_joints=-1, joints_found=0):
        parts = [self]
        if self.core:
            if num_joints == -1:
                return []
            elif joints_found < num_joints:
                raise Exception("That many joints don't exist above this part")
        if isinstance(self, Joint):
            joints_found += 1
            if joints_found == num_joints:
                return parts

        return parts + self.parent.get_parts_above(num_joints, joints_found)

    def calc_slash_speed(self, num_joints, joints_found=0):
        joint_speed = 0
        if self.core:
            if num_joints == -1:
                return 0, 0
            elif joints_found < num_joints:
                raise Exception("That many joints don't exist above this part")
        if isinstance(self, Joint):
            joints_found += 1
            joint_speed = self.rel_strength * self.creature.traits[
                'strength'] / self.calc_moment_of_inertia_below() * self.creature.strength_scaler
            if joints_found == num_joints:
                return joint_speed, self.length

        speed, length = self.parent.calc_slash_speed(num_joints, joints_found)
        return speed + joint_speed, length + self.length

    def calc_jab_speed(self, num_joints, joints_found=0):
        joint_speed = 0
        if self.core:
            if num_joints == -1:
                return 0, 0
            elif joints_found < num_joints:
                raise Exception("That many joints don't exist above this part")
        if isinstance(self, Joint):
            joints_found += 1
            joint_speed = self.rel_strength * self.creature.traits[
                'strength'] / self.calc_moment_of_inertia_below() * self.creature.strength_scaler
            if joints_found == num_joints:
                return joint_speed

        speed = self.parent.calc_jab_speed(num_joints, joints_found)
        return speed + joint_speed * self.length

    def calc_damage(self, KE, volume):
        print("armour:")
        pl = self.shear_plastic_limit * volume
        el = self.shear_elastic_limit * volume

        print(KE, el, pl)

        if KE > pl:
            print('Pierced')
        elif KE > el:
            print('Bent')
            for s in np.linspace(0, self.strain_at_fracture, 100, endpoint=False):
                if integrate.quad(self.shear_stress_strain, 0, s)[0] * volume > KE:
                    print(s)
                    break
        else:
            print('Deflected')

    def calc_cutting_damage(self, KE, other):
        pass

    def calc_piercing_damage(self, KE, other):
        pass

    def calc_crushing_damage(self, KE, other):
        w = min(self.width, other.width)
        l = min(self.length, other.length)
        a = (2 * w + 2 * l) * self.thickness

    def _swing_helper(self, other, num_joints):
        ang_vel, body_len = self.calc_slash_speed(num_joints)

        if self.held is not None:
            self.held.foreswing(other, ang_vel, body_len)
        else:
            impact_length = min(self.length, self.width, other.width, other.length)
            tip_velocity = ang_vel * (body_len + self.length)
            KE = .5 * self.mass * tip_velocity ** 2

            if impact_length == self.length or impact_length == self.width:
                self.calc_crushing_damage(KE, other)
            else:
                self.calc_cutting_damage(KE, other)
            other.calc_cutting_damage(KE, self)

    def foreswing(self, other, num_joints):
        self._swing_helper(other, num_joints)

    def backswing(self, other, num_joints):
        self._swing_helper(other, num_joints)

    def upswing(self, other, num_joints):
        self._swing_helper(other, num_joints)

    def downswing(self, other, num_joints):
        self._swing_helper(other, num_joints)

    def jab(self, other, num_joints):
        vel = self.calc_jab_speed(num_joints)
        print(vel)
        if self.held is not None:
            self.held.jab(other, vel)
        else:
            pass
            # impact_length = min(self.length, self.width, other.width, other.length)
            # tip_velocity = ang_vel * (body_len + self.length)
            # KE = .5 * self.mass * tip_velocity ** 2
            #
            # if impact_length == self.length or impact_length == self.width:
            #     self.calc_crushing_damage(KE, other)
            # else:
            #     self.calc_cutting_damage(KE, other)
            # other.calc_cutting_damage(KE, self)

    def __repr__(self):
        return self.name

    def __str__(self):
        return self.name


class Digit(BodyPart, Materials.Fleshy):
    def __init__(self, parent=None, children=None, opposable=False, joints=3.0, length=95.0,
                 width=17.0, thickness=17.0, **kwargs):
        children = children if children is not None else []
        super().__init__(parent, children, **kwargs)
        self.num_joints = joints
        self.opposable = opposable
        self.length = length
        self.width = width
        self.thickness = thickness
        self.volume = self.calc_volume()
        self.mass = self.volume * self.density


class LimbTerminus(BodyPart, Materials.Fleshy):
    def __init__(self, parent=None, children=None, length=96.0, width=84.0, thickness=35.0,
                 **kwargs):
        children = children if children is not None else []
        super().__init__(parent, children, **kwargs)
        self.length = length
        self.width = width
        self.thickness = thickness
        self.volume = self.calc_volume()
        self.mass = self.volume * self.density


class LimbSegment(BodyPart, Materials.Fleshy):
    def __init__(self, parent=None, children=None, length=460.0, width=80.0, thickness=80.0,
                 **kwargs):
        children = children if children is not None else []
        super().__init__(parent, children, **kwargs)
        self.length = length
        self.width = width
        self.thickness = thickness
        self.volume = self.calc_volume()
        self.mass = self.volume * self.density


class Joint(BodyPart, Materials.Fleshy):
    def scale(self, factor):
        pass

    def __init__(self, rel_strength, parent=None, children=None, **kwargs):
        super().__init__(parent, children, layers=[], **kwargs)
        children = children if children is not None else []
        self.length = 0
        self.width = 0
        self.thickness = 0
        self.rel_strength = rel_strength


class TorsoSegment(BodyPart, Materials.Fleshy):
    def __init__(self, parent=None, children=None, length=300.0, width=142.0, thickness=86.0,
                 **kwargs):
        children = children if children is not None else []
        super().__init__(parent, children, **kwargs)
        self.length = length
        self.width = width
        self.thickness = thickness
        self.volume = self.calc_volume()
        self.mass = self.volume * self.density


class Neck(BodyPart, Materials.Fleshy):
    def __init__(self, parent=None, children=None, length=110.0, width=113.0, thickness=113.0,
                 **kwargs):
        children = children if children is not None else []
        super().__init__(parent, children, **kwargs)
        self.length = length
        self.width = width
        self.thickness = thickness
        self.volume = self.calc_volume()
        self.mass = self.volume * self.density


class Head(BodyPart, Materials.Fleshy):
    def __init__(self, parent=None, children=None, length=218.0, width=186.0, thickness=186.0,
                 **kwargs):
        children = children if children is not None else []
        super().__init__(parent, children, **kwargs)
        self.length = length
        self.width = width
        self.thickness = thickness
        self.volume = self.calc_volume()
        self.mass = self.volume * self.density


class Humanoid(Thing, Creature):
    num_arms = 2
    num_legs = 2
    num_fingers = 5
    num_toes = 5
    ideal_skin = SkinLayer(thickness=1 / 11.5 / 72.5, critical=False)
    ideal_cranium = WrappingBone(thickness=1 / 11.5 / 20, critical=False)
    ideal_arm_bone = WrappingBone(thickness=1 / 11.5 / 29, critical=False)
    ideal_hand_bone = WrappingBone(thickness=.2 / 11.5, critical=False)
    ideal_leg_bone = WrappingBone(thickness=1 / 11.5 / 18, critical=False)
    ideal_foot_bone = WrappingBone(thickness=1 / 11.5 / 20, critical=False)
    ideal_ribcage = WrappingBone(thickness=1 / 11.5 / 14.5, critical=False)
    ideal_spine = WrappingBone(thickness=1 / 11.5 / 11, critical=True)
    ideal_brain = Brain(relative_size=.9, critical=True)
    ideal_stomach = Stomach(relative_size=.2, critical=True)
    ideal_liver = Liver(relative_size=.3, critical=True)
    ideal_intestine = Intestines(relative_size=.5, critical=False)
    ideal_larynx = Larynx(thickness=1 / 11.5 / 15, critical=True)
    ideal_heart = Heart(relative_size=.1, critical=True)
    ideal_lung = Lung(relative_size=.4, critical=True)

    ideal_head = Head(layers=[ideal_skin, ideal_cranium, FloatingOrganLayer(contents=[ideal_brain])], length=1 / 7.5, width=1 / 11.5,
                      thickness=1 / 11.5,
                      can_attack=True, core=True, can_grasp=False)
    ideal_neck = Neck(layers=[ideal_skin, MuscleLayer(thickness=1 / 11.5 / 3), ideal_larynx, ideal_spine],
                      length=1 / 11.5, width=1 / 11.5, thickness=1 / 11.5, can_attack=False, core=True, can_grasp=False)
    ideal_upper_torso = TorsoSegment(layers=[ideal_skin, MuscleLayer(thickness=1 / 11.5 / 20), ideal_ribcage, FloatingOrganLayer(contents=[ideal_lung, ideal_lung, ideal_heart]),
                                             ideal_spine], length=1.5 / 7.5, width=2 / 11.5, thickness=1.25 / 11.5,
                                     can_attack=True, core=True, can_grasp=False)
    ideal_upper_torso.name = 'Upper Torso'
    ideal_lower_torso = TorsoSegment(layers=[ideal_skin, MuscleLayer(thickness=1 / 11.5 / 15), FloatingOrganLayer(contents=[ideal_intestine, ideal_liver, ideal_stomach]), ideal_spine],
                                     length=1.25 / 7.5, width=1.75 / 11.5, thickness=1.5 / 11.5, can_attack=False,
                                     core=True, can_grasp=False)
    ideal_lower_torso.name = 'Lower Torso'
    ideal_upper_leg = LimbSegment(layers=[ideal_skin, MuscleLayer(thickness=1 / 11.5 / 2), ideal_leg_bone],
                                  length=2 / 7.5, width=1 / 11.5, thickness=1 / 11.5, can_attack=False, can_grasp=False)
    ideal_lower_leg = LimbSegment(layers=[ideal_skin, MuscleLayer(thickness=1 / 11.5 / 3), ideal_leg_bone],
                                  length=1.75 / 7.5, width=.5 / 11.5, thickness=.5 / 11.5, can_attack=False,
                                  can_grasp=False)
    ideal_foot = LimbTerminus(layers=[ideal_skin, ideal_foot_bone], length=1.5 / 11.5, width=.5 / 11.5,
                              thickness=.4 / 11.5, can_attack=True, can_grasp=False)
    ideal_toe = Digit(layers=[ideal_skin, ideal_foot_bone], length=.2 / 11.5, width=.1 / 11.5,
                      thickness=.1 / 11.5, can_attack=False, can_grasp=False)
    ideal_upper_arm = LimbSegment(layers=[ideal_skin, MuscleLayer(thickness=1 / 11.5 / 3), ideal_arm_bone],
                                  length=2 / 11.5, width=.4 / 11.5, thickness=.4 / 11.5, can_attack=False,
                                  can_grasp=False)
    ideal_lower_arm = LimbSegment(layers=[ideal_skin, MuscleLayer(thickness=1 / 11.5 / 4), ideal_arm_bone],
                                  length=2 / 11.5, width=.25 / 11.5, thickness=.2 / 11.5, can_attack=False,
                                  can_grasp=False)
    ideal_palm = LimbTerminus(layers=[ideal_skin, ideal_hand_bone], length=.8 / 11.5, width=.8 / 11.5,
                              thickness=.2 / 11.5, can_attack=True, can_grasp=True)
    ideal_finger = Digit(layers=[ideal_skin, ideal_hand_bone], length=.5 / 11.5, width=.15 / 11.5,
                         thickness=.15 / 11.5, can_attack=False, can_grasp=False)
    ideal_hip = Joint(.5, can_attack=True, can_grasp=False)
    ideal_knee = Joint(.3, can_attack=True, can_grasp=False)
    ideal_shoulder = Joint(.4, can_attack=True, can_grasp=False)
    ideal_elbow = Joint(.2, can_attack=True, can_grasp=False)

    def __init__(self, height):
        super().__init__()
        self.head = copy.deepcopy(self.ideal_head)
        self.head.contents = [self.ideal_skin, self.ideal_cranium, self.ideal_brain]
        self.neck = copy.deepcopy(self.ideal_neck)
        self.neck.contents = []
        self.upper_torso = copy.deepcopy(self.ideal_upper_torso)
        self.lower_torso = copy.deepcopy(self.ideal_lower_torso)

        self.hip = copy.deepcopy(self.ideal_hip)
        self.hip.name = 'Hip'

        self.left_upper_leg = copy.deepcopy(self.ideal_upper_leg)
        self.left_upper_leg.name = 'Left Upper Leg'

        self.right_upper_leg = copy.deepcopy(self.ideal_upper_leg)
        self.right_upper_leg.name = 'Right Upper Leg'

        self.left_knee = copy.deepcopy(self.ideal_knee)
        self.left_knee.name = 'Left Knee'

        self.right_knee = copy.deepcopy(self.ideal_knee)
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

        self.left_shoulder = copy.deepcopy(self.ideal_shoulder)
        self.left_shoulder.name = 'Left Shoulder'

        self.right_shoulder = copy.deepcopy(self.ideal_shoulder)
        self.right_shoulder.name = 'Right Shoulder'

        self.left_upper_arm = copy.deepcopy(self.ideal_upper_arm)
        self.left_upper_arm.name = 'Left Upper Arm'

        self.right_upper_arm = copy.deepcopy(self.ideal_upper_arm)
        self.right_upper_arm.name = 'Right Upper Arm'

        self.left_elbow = copy.deepcopy(self.ideal_elbow)
        self.left_elbow.name = 'Left Elbow'

        self.right_elbow = copy.deepcopy(self.ideal_elbow)
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
        self.upper_torso.children = [self.lower_torso, self.right_shoulder, self.left_shoulder]
        self.lower_torso.parent = self.upper_torso
        self.lower_torso.children = [self.hip]
        self.hip.parent = self.lower_torso
        self.hip.children = [self.left_upper_leg, self.right_upper_leg]
        self.left_upper_leg.parent = self.hip
        self.left_upper_leg.children = [self.left_knee]
        self.right_upper_leg.parent = self.hip
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
        self.left_shoulder.parent = self.upper_torso
        self.left_shoulder.children = [self.left_upper_arm]
        self.right_shoulder.parent = self.upper_torso
        self.right_shoulder.children = [self.right_upper_arm]
        self.left_upper_arm.parent = self.right_shoulder
        self.left_upper_arm.children = [self.left_elbow]
        self.right_upper_arm.parent = self.right_shoulder
        self.right_upper_arm.children = [self.right_elbow]
        self.left_elbow.parent = self.left_upper_arm
        self.left_elbow.children = [self.left_lower_arm]
        self.right_elbow.parent = self.right_upper_arm
        self.right_elbow.children = [self.right_lower_arm]
        self.left_lower_arm.parent = self.left_elbow
        self.left_lower_arm.children = [self.left_palm]
        self.right_lower_arm.parent = self.right_elbow
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
                           self.right_lower_arm, self.left_palm, self.right_palm, self.right_shoulder, self.hip,
                           self.left_shoulder, self.right_elbow, self.left_elbow, self.left_knee, self.right_knee]

        self.parts_list.extend(self.left_fingers)
        self.parts_list.extend(self.right_fingers)
        self.parts_list.extend(self.left_toes)
        self.parts_list.extend(self.right_toes)

        for part in self.parts_list:
            part.scale(height)

        self.attacking_parts = [part for part in self.parts_list if part.can_attack]


class Human(Humanoid, Character):
    max_height = 2.7
    min_height = .6
    max_bmi = 70
    min_bmi = 10
    strength_scaler = .04

    def __init__(self, height, bmi, skills, traits):
        super().__init__(height)
        self.traits = traits
        for part in self.parts_list:
            part.creature = self


h = Human(2, 20, {}, {'strength': 40})
print(h.right_palm.calc_slash_speed(1))
# TODO Attacks don't come from body level but from part level - i.e. leg can attack
# TODO if part is wielding an object use the corresponding attack method from the object
# TODO Attacks come in: Jab Foreswing Backswing Downswing Upswing (Swing come in slap and strike)
