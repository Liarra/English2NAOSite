from translator.executables.nlp.components.robot_commands import move_command

__author__ = 'NBUCHINA'
sit = move_command()
sit.params["body_part"] = "sit"
sit.params["name"] = "Sit"
sit.name = "Sit"
sit.summary = "The robot sits down."
sit.params[
    "move"] = """wait(3000)& ledoff(FaceLeds) & wait (500) & ledon(FaceLeds) & wait (500) & ledoff(FaceLeds) & wait (500) & ledon(FaceLeds)"""
sit.tags = ["sit", "down", "sits", "sitting"]
sit.params["base_pose"] = "Sit"

nod = move_command()
nod.params["body_part"] = "crouch"
nod.params["name"] = "Nod"
nod.name = "Nod"
nod.summary = "The robot nods."
nod.params["move"] = """

movem (
HeadPitch,
8.6,1400,21.4,480,8.6,400,21.4,360,8.6,400,
21.4,320,8.6,360,
HeadYaw,
-2.3,1400,-2.2,480,-2.3,400,-2.2,360,-2.3,400,
-2.2,320,-2.3,360,
LAnklePitch,
-68.1,1400,-68.1,480,-68.1,400,-68.1,360,-68.1,400,
-68.1,320,-68.1,360,
LAnkleRoll,
4.2,1400,4.3,480,4.2,400,4.3,360,4.2,400,
4.3,320,4.2,360,
LElbowRoll,
-69.1,1400,-69.2,480,-69.1,400,-69.2,360,-69.1,400,
-69.2,320,-69.1,360,
LElbowYaw,
-59.9,1400,-59.9,480,-59.9,400,-59.9,360,-59.9,400,
-59.9,320,-59.9,360,
LHand,
0.0,1400,0.0,480,0.0,400,0.0,360,0.0,400,
0.0,320,0.0,360,
LHipPitch,
-41.6,1400,-42.5,480,-41.6,400,-42.5,360,-41.6,400,
-42.5,320,-41.6,360,
LHipRoll,
-4.9,1400,-4.9,480,-4.9,400,-4.9,360,-4.9,400,
-4.9,320,-4.9,360,
LHipYawPitch,
-13.5,1400,-13.4,480,-13.5,400,-13.4,360,-13.5,400,
-13.4,320,-13.5,360,
LKneePitch,
120.9,1400,120.9,480,120.9,400,120.9,360,120.9,400,
120.9,320,120.9,360,
LShoulderPitch,
91.8,1400,91.8,480,91.8,400,91.8,360,91.8,400,
91.8,320,91.8,360,
LShoulderRoll,
13.1,1400,13.2,480,13.1,400,13.2,360,13.1,400,
13.2,320,13.1,360,
LWristYaw,
-26.0,1400,-26.0,480,-26.0,400,-26.0,360,-26.0,400,
-26.0,320,-26.0,360,
RAnklePitch,
-67.8,1400,-67.7,480,-67.8,400,-67.7,360,-67.8,400,
-67.7,320,-67.8,360,
RAnkleRoll,
-4.5,1400,-4.6,480,-4.5,400,-4.6,360,-4.5,400,
-4.6,320,-4.5,360,
RElbowRoll,
55.6,1400,55.6,480,55.6,400,55.6,360,55.6,400,
55.6,320,55.6,360,
RElbowYaw,
18.9,1400,18.9,480,18.9,400,18.9,360,18.9,400,
18.9,320,18.9,360,
RHand,
0.0,1400,0.0,480,0.0,400,0.0,360,0.0,400,
0.0,320,0.0,360,
RHipPitch,
-41.1,1400,-42.2,480,-41.1,400,-42.2,360,-41.1,400,
-42.2,320,-41.1,360,
RHipRoll,
5.1,1400,5.2,480,5.1,400,5.2,360,5.1,400,
5.2,320,5.1,360,
RHipYawPitch,
-13.5,1400,-13.4,480,-13.5,400,-13.4,360,-13.5,400,
-13.4,320,-13.5,360,
RKneePitch,
120.9,1400,120.9,480,120.9,400,120.9,360,120.9,400,
120.9,320,120.9,360,
RShoulderPitch,
65.6,1400,65.6,480,65.6,400,65.6,360,65.6,400,
65.6,320,65.6,360,
RShoulderRoll,
-11.1,1400,-11.1,480,-11.1,400,-11.1,360,-11.1,400,
-11.1,320,-11.1,360,
RWristYaw,
54.3,1400,54.3,480,54.3,400,54.3,360,54.3,400,
54.3,320,54.3,360)

"""
nod.tags = ["nod", "head", "nods", "nodding"]
nod.params["base_pose"] = "Crouch"

shake_no = move_command()
shake_no.params["body_part"] = "crouch"
shake_no.params["name"] = "Shake head"
shake_no.name = "Shake head"
shake_no.summary = "The robot shakes its head to say no."
shake_no.params[
    "move"] = """

movem (
HeadPitch,
6.9,1600,6.5,1200,6.4,1600,6.5,1600,6.4,1600,
6.9,1200,
HeadYaw,
-2.4,1600,-37.7,1200,30.8,1600,-37.7,1600,30.8,1600,
-2.4,1200,
LAnklePitch,
-68.1,1600,-68.1,7200,
LAnkleRoll,
4.3,1600,4.3,7200,
LElbowRoll,
-59.8,1600,-59.8,7200,
LElbowYaw,
-46.4,1600,-46.4,7200,
LHand,
0.0,1600,0.0,7200,
LHipPitch,
-41.9,1600,-41.9,7200,
LHipRoll,
-4.8,1600,-4.8,7200,
LHipYawPitch,
-14.2,1600,-14.2,7200,
LKneePitch,
121.0,1600,121.0,7200,
LShoulderPitch,
77.7,1600,77.7,7200,
LShoulderRoll,
6.2,1600,6.2,7200,
LWristYaw,
7.5,1600,7.5,7200,
RAnklePitch,
-67.8,1600,-67.8,7200,
RAnkleRoll,
-4.4,1600,-4.4,7200,
RElbowRoll,
62.8,1600,62.8,7200,
RElbowYaw,
43.9,1600,43.9,7200,
RHand,
0.0,1600,0.0,7200,
RHipPitch,
-41.5,1600,-41.5,7200,
RHipRoll,
4.9,1600,4.9,7200,
RHipYawPitch,
-14.2,1600,-14.2,7200,
RKneePitch,
120.9,1600,120.9,7200,
RShoulderPitch,
80.5,1600,80.5,7200,
RShoulderRoll,
-7.4,1600,-7.4,7200,
RWristYaw,
-8.0,1600,-8.0,7200)

    """
shake_no.tags = ["shake", "head", "negatively", "no"]
shake_no.params["base_pose"] = "Crouch"


stretch_hand = move_command()
stretch_hand.params["body_part"] = "crouch"
stretch_hand.params["name"] = "Provide hand for handshake"
stretch_hand.name = "Provide hand for handshake"
stretch_hand.summary = "The robot stretches its arm for the handshake"
stretch_hand.params[
    "move"] = """

    [movem(RShoulderRoll, -10, 1000,
      RShoulderPitch, 70, 1000,
      RElbowRoll,     -30, 1000,
      RHand,           0, 1000,
      HeadPitch,       0, 1000, RElbowYaw, 90, 1000, RWristYaw, 0, 1000)
&
movem(RShoulderPitch, 78, 200, 71, 200, 59, 200, 48, 200, 36, 200, 32, 200,
      RElbowRoll,     15, 200, 19, 200, 23, 200, 32, 200, 35, 200, 37, 200,
                      39, 200,
      RHand,           0, 400, 57,1000)]&[wait(10000)]

    """
stretch_hand.tags = ["stretch", "hand", "provide", "provides", "stretches","providing", "stretching"]
stretch_hand.params["base_pose"] = "Crouch"