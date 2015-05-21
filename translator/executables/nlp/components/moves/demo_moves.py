from translator.executables.nlp.components.robot_commands import move_command

__author__ = 'NBUCHINA'

wave = move_command()
wave.params["name"] = "Wave"
wave.params["move"] = """movem (
LHand, 0, 1000, 57, 1000, 0, 1000,
RHand, 0, 1000, 57, 1000, 0, 1000)"""
wave.tags = ["wave"]
wave.regexp = r"waves? .{0,20} (hand)?"

nod = move_command()
nod.params["name"] = "Nod"
nod.params["move"] = """movem (
LHand, 0, 1000, 57, 1000, 0, 1000,
RHand, 0, 1000, 57, 1000, 0, 1000)"""
nod.tags = ["nod"]
nod.regexp = r"nodes? .{0,20} (head)?"

handshake = move_command()
handshake.params["name"] = "Handshake"
handshake.params["move"] = """movem (
HeadPitch,
25.1,1000,25.1,600,25.1,440,25.1,600,25.1,240,
25.1,600,25.1,440,25.1,600,25.2,560,25.1,560,
25.1,440,17.1,720,11.8,600,
HeadYaw,
-29.0,1000,-29.0,600,-29.0,440,-29.0,600,-29.0,240,
-29.0,600,-29.0,440,-29.0,600,-29.1,560,-29.1,560,
-29.1,440,-28.0,720,-2.8,600,
LAnklePitch,
-68.1,1000,-68.1,600,-68.1,440,-68.1,600,-68.1,240,
-68.1,600,-68.1,440,-68.1,600,-68.0,560,-68.1,560,
-68.1,440,-68.1,720,-68.1,600,
LAnkleRoll,
4.2,1000,4.2,600,4.2,440,4.2,600,4.2,240,
4.2,600,4.2,440,4.2,600,4.2,560,4.2,560,
4.2,440,4.2,720,4.2,600,
LElbowRoll,
-58.1,1000,-58.5,600,-58.5,440,-58.5,600,-58.5,240,
-58.5,600,-58.5,440,-58.5,600,-58.5,560,-58.5,560,
-58.5,440,-58.7,720,-58.1,600,
LElbowYaw,
-61.4,1000,-61.4,600,-61.3,440,-61.4,600,-61.3,240,
-61.4,600,-61.3,440,-61.4,600,-61.4,560,-61.3,560,
-61.4,440,-61.3,720,-61.4,600,
LHand,
1.0,1000,0.1,600,0.1,440,0.1,600,0.1,240,
0.1,600,0.1,440,0.1,600,0.1,560,0.1,560,
0.1,440,0.1,720,0.1,600,
LHipPitch,
-42.0,1000,-42.0,600,-42.0,440,-42.0,600,-42.0,240,
-42.0,600,-42.0,440,-42.0,600,-42.0,560,-42.0,560,
-42.0,440,-42.0,720,-42.1,600,
LHipRoll,
-4.4,1000,-4.4,600,-4.4,440,-4.4,600,-4.4,240,
-4.4,600,-4.4,440,-4.4,600,-4.4,560,-4.4,560,
-4.4,440,-4.4,720,-4.4,600,
LHipYawPitch,
-12.6,1000,-12.6,600,-12.6,440,-12.6,600,-12.6,240,
-12.6,600,-12.6,440,-12.6,600,-12.6,560,-12.6,560,
-12.6,440,-12.6,720,-12.6,600,
LKneePitch,
121.0,1000,121.0,600,121.0,440,121.0,600,121.0,240,
121.0,600,121.0,440,121.0,600,121.0,560,121.0,560,
121.0,440,121.0,720,121.0,600,
LShoulderPitch,
87.7,1000,87.5,600,87.5,440,87.5,600,87.5,240,
87.5,600,87.5,440,87.5,600,87.6,560,87.6,560,
87.5,440,86.9,720,87.7,600,
LShoulderRoll,
1.5,1000,1.4,600,1.5,440,1.4,600,1.5,240,
1.4,600,1.5,440,1.4,600,1.5,560,1.5,560,
1.5,440,1.5,720,1.5,600,
LWristYaw,
-5.4,1000,-5.0,600,-5.0,440,-5.0,600,-5.0,240,
-5.0,600,-5.0,440,-5.0,600,-4.9,560,-5.0,560,
-5.0,440,-5.0,720,-5.3,600,
RAnklePitch,
-68.0,1000,-68.0,600,-68.0,440,-68.0,600,-68.0,240,
-68.0,600,-68.0,440,-68.0,600,-68.0,560,-68.0,560,
-68.0,440,-68.0,720,-68.0,600,
RAnkleRoll,
-4.3,1000,-4.3,600,-4.3,440,-4.3,600,-4.3,240,
-4.3,600,-4.3,440,-4.3,600,-4.3,560,-4.3,560,
-4.3,440,-4.3,720,-4.3,600,
RElbowRoll,
57.7,1000,42.7,600,58.5,440,42.7,600,58.5,240,
42.7,600,58.5,440,42.7,600,60.0,560,60.1,560,
60.0,440,42.6,720,59.6,600,
RElbowYaw,
59.6,1000,54.8,600,60.6,440,54.8,600,60.6,240,
54.8,600,60.6,440,54.8,600,65.9,560,65.9,560,
65.9,440,69.3,720,48.7,600,
RHand,
30.0,1000,30.0,600,30.0,440,30.0,600,30.0,240,
30.0,600,30.0,440,30.0,600,30.0,560,30.0,560,
30.0,440,30.0,720,0.2,600,
RHipPitch,
-41.8,1000,-41.8,600,-41.8,440,-41.8,600,-41.8,240,
-41.8,600,-41.8,440,-41.8,600,-41.8,560,-41.8,560,
-41.8,440,-41.8,720,-41.8,600,
RHipRoll,
4.7,1000,4.7,600,4.7,440,4.7,600,4.7,240,
4.7,600,4.7,440,4.7,600,4.7,560,4.7,560,
4.7,440,4.7,720,4.7,600,
RHipYawPitch,
-12.6,1000,-12.6,600,-12.6,440,-12.6,600,-12.6,240,
-12.6,600,-12.6,440,-12.6,600,-12.6,560,-12.6,560,
-12.6,440,-12.6,720,-12.6,600,
RKneePitch,
121.0,1000,121.0,600,121.0,440,121.0,600,121.0,240,
121.0,600,121.0,440,121.0,600,121.0,560,121.0,560,
121.0,440,121.0,720,121.0,600,
RShoulderPitch,
63.6,1000,65.2,600,59.7,440,65.2,600,59.7,240,
65.2,600,59.7,440,65.2,600,65.0,560,64.9,560,
64.9,440,77.0,720,83.6,600,
RShoulderRoll,
-8.4,1000,-8.7,600,-9.9,440,-8.7,600,-9.9,240,
-8.7,600,-9.9,440,-8.7,600,-8.7,560,-8.7,560,
-8.7,440,-4.3,720,0.3,600,
RWristYaw,
20.5,1000,17.0,600,20.0,440,17.0,600,20.0,240,
17.0,600,20.0,440,17.0,600,12.7,560,12.7,560,
12.7,440,17.6,720,21.3,600)"""
handshake.tags = ["hand", "make", "handshake", "greet"]
handshake.regexp = r"(shak(es?)|(ing).{0,20}( hand)?)|(mak(es?|ing).{0,20} handshake)"

stand = move_command()
stand.params["name"] = "Stand"
stand.params[
    "move"] = """wait(3000)& ledoff(FaceLeds) & wait (500) & ledon(FaceLeds) & wait (500) & ledoff(FaceLeds) & wait (500) & ledon(FaceLeds)"""
stand.tags = ["stand", "up"]
stand.regexp = r"stand(s?)|(ing).{0,20}(up)?"
stand.params["base_pose"] = "Stand"

crouch = move_command()
crouch.params["name"] = "Crouch"
crouch.params[
    "move"] = """wait(3000)& ledoff(FaceLeds) & wait (500) & ledon(FaceLeds) & wait (500) & ledoff(FaceLeds) & wait (500) & ledon(FaceLeds)"""
crouch.tags = ["crouch", "down", "kneel"]
crouch.regexp = r"(crouch|kneel)(s?)|(ing).{0,20}(down)?"

cry = move_command()
cry.params["name"] = "Cry"
cry.params["move"] = """[movem (HeadYaw, -0.090527, 2000, -0.090527, 2000,HeadPitch, 29.265538, 2000, 29.265538, 2000,LShoulderPitch,
     89.295472, 2000, 89.295472, 2000,LShoulderRoll, 8.698645, 2000, 8.698645, 2000,LElbowYaw, -85.433164, 2000,
     -85.433164, 2000,LElbowRoll, -17.927276, 2000, -17.927276, 2000,LWristYaw, -9.055025, 2000, -9.055025, 2000,LHand,
      1.321241, 2000, 1.321241, 2000,RShoulderPitch, 87.806355, 2000, 87.806355, 2000,RShoulderRoll, -5.539356, 2000,
       -5.539356, 2000,RElbowYaw, 94.217753, 2000, 94.217753, 2000,RElbowRoll, 18.987248, 2000, 18.987248, 2000,RWristYaw,
       -1.408903, 2000, -1.408903, 2000,RHand, 0.001719, 2000, 0.001719, 2000,LHipYawPitch, 0.002292, 2000, 0.002292, 2000,
       LHipRoll, 0.002292, 2000, 0.002292, 2000,LHipPitch, -25.046850, 2000, -25.046850, 2000,LKneePitch, 39.988443, 2000, 39.988443, 2000,
       LAnklePitch, -20.041491, 2000, -20.041491, 2000,LAnkleRoll, 0.002292, 2000, 0.002292, 2000,RHipRoll, 0.002292, 2000, 0.002292, 2000,
       RHipPitch, -25.051434, 2000, -25.051434, 2000,RKneePitch, 40.081263, 2000, 40.081263, 2000,RAnklePitch, -20.036907, 2000, -20.036907, 2000,
       RAnkleRoll, 0.002292, 2000, 0.002292, 2000)] |
       [ledoff(AllLeds) & ledfade(FaceLedsBottom,1,1000) &ledoff(AllLeds) & ledfade(FaceLedsBottom,1,1000) &ledoff(AllLeds) & ledfade(FaceLedsBottom,1,1000)
       &ledoff(AllLeds) & ledfade(FaceLedsBottom,1,1000) &ledoff(AllLeds) & ledfade(FaceLedsBottom,1,1000) &ledoff(AllLeds) & ledfade(FaceLedsBottom,1,1000)
       &ledoff(AllLeds) & ledfade(FaceLedsBottom,1,1000) &ledoff(AllLeds) & ledfade(FaceLedsBottom,1,1000) &ledoff(AllLeds) & ledfade(FaceLedsBottom,1,1000)
       &ledoff(AllLeds) & ledfade(FaceLedsBottom,1,1000)]"""
cry.tags = ["cry", "tears"]
cry.regexp = r"cry(es?)|(ing)"
cry.params["base_pose"] = "Stand"

dance = move_command()
dance.params["name"] = "Dance"
dance.params["move"] = """[[movem (
HeadPitch,
5.6,1600,5.6,2400,5.6,1400,5.6,1360,5.6,1400,
5.6,1520,5.6,1520,5.6,760,
HeadYaw,
-1.1,1600,11.0,2400,16.3,1400,16.3,1360,16.3,1400,
-25.5,1520,-29.4,1520,11.2,760,
LAnklePitch,
-68.1,1600,-68.1,2400,-68.1,1400,-68.1,1360,-68.1,1400,
-68.1,1520,-64.1,1520,-68.1,760,
LAnkleRoll,
4.3,1600,4.2,2400,4.2,1400,4.2,1360,4.2,1400,
-4.4,1520,-4.9,1520,4.2,760,
LElbowRoll,
-69.0,1600,-73.0,1240,-71.5,1160,-57.4,1400,-56.7,1360,
-57.4,1400,-48.5,1520,-47.2,1520,-71.4,760,
LElbowYaw,
-39.0,1600,-78.9,1240,-75.7,1160,-67.2,1400,-66.9,1360,
-67.2,1400,-29.3,1520,-34.1,1520,-75.5,760,
LHand,
0.3,1600,0.3,1240,0.3,1160,0.3,1400,0.3,1360,
0.3,1400,0.3,1520,0.3,1520,0.3,760,
LHipPitch,
-39.5,1600,-40.1,2400,-41.7,1400,-48.3,1360,-41.7,1400,
-40.8,1520,-35.2,1520,-40.1,760,
LHipRoll,
-4.6,1600,-4.3,2400,-3.7,1400,12.0,1360,-3.7,1400,
5.1,1520,-8.6,1520,-4.3,760,
LHipYawPitch,
-14.5,1600,-15.3,2400,-15.6,1400,-9.1,1360,-15.6,1400,
-9.6,1520,-7.5,1520,-15.3,760,
LKneePitch,
121.0,1600,121.0,2400,121.0,1400,121.0,1360,121.0,1400,
121.0,1520,107.1,1520,121.0,760,
LShoulderPitch,
84.7,1600,10.2,1240,-53.8,1160,-51.4,1400,-52.5,1360,
-51.4,1400,-70.8,1520,-67.4,1520,-53.8,760,
LShoulderRoll,
5.6,1600,4.2,1240,14.9,1160,54.8,1400,46.8,1360,
54.8,1400,0.4,1520,2.4,1520,15.8,760,
LWristYaw,
25.3,1600,26.4,1240,31.4,1160,30.2,1400,30.1,1360,
30.2,1400,30.1,1520,30.1,1520,31.4,760,
RAnklePitch,
-68.0,1600,-68.0,2400,-68.0,1400,-65.6,1360,-68.0,1400,
-68.0,1520,-68.0,1520,-68.0,760,
RAnkleRoll,
-4.3,1600,-4.5,2400,-4.7,1400,5.5,1360,-4.7,1400,
-4.7,1520,0.8,1520,-4.6,760,
RElbowRoll,
71.1,1600,74.3,1240,65.8,1160,57.4,1400,59.6,1360,
57.4,1400,58.1,1520,59.2,1520,65.6,760,
RElbowYaw,
50.8,1600,79.4,1240,72.6,1160,25.6,1400,24.5,1360,
25.6,1400,17.4,1520,25.8,1520,71.8,760,
RHand,
0.5,1600,0.5,1240,0.5,1160,0.5,1400,0.5,1360,
0.5,1400,0.5,1520,0.5,1520,0.5,760,
RHipPitch,
-39.9,1600,-41.0,2400,-41.5,1400,-30.1,1360,-41.5,1400,
-41.0,1520,-49.0,1520,-41.0,760,
RHipRoll,
4.5,1600,4.3,2400,4.2,1400,9.8,1360,4.2,1400,
3.1,1520,-15.2,1520,4.3,760,
RHipYawPitch,
-14.5,1600,-15.3,2400,-15.6,1400,-9.1,1360,-15.6,1400,
-9.6,1520,-7.5,1520,-15.3,760,
RKneePitch,
121.0,1600,121.0,2400,121.0,1400,102.8,1360,121.0,1400,
121.0,1520,121.0,1520,121.0,760,
RShoulderPitch,
91.1,1600,7.1,1240,-52.5,1160,-73.5,1400,-73.9,1360,
-73.5,1400,-80.6,1520,-77.7,1520,-53.7,760,
RShoulderRoll,
-0.0,1600,-3.2,1240,-13.7,1160,-1.7,1400,-6.6,1360,
-1.7,1400,-58.6,1520,-54.7,1520,-13.7,760,
RWristYaw,
-29.2,1600,-29.2,1240,-29.2,1160,-29.2,1400,-29.2,1360,
-29.2,1400,-29.2,1520,-29.2,1520,-29.2,760)]

&

[stiff(1,500,0)]& [movem (
HeadPitch,
5.6,1000,5.6,2400,5.6,1400,5.6,1360,5.6,1400,
5.6,1520,5.6,1520,5.6,760,
HeadYaw,
-1.1,1000,11.0,2400,16.3,1400,16.3,1360,16.3,1400,
-25.5,1520,-29.4,1520,11.2,760,
LAnklePitch,
-68.1,1000,-68.1,2400,-68.1,1400,-68.1,1360,-68.1,1400,
-68.1,1520,-64.1,1520,-68.1,760,
LAnkleRoll,
4.3,1000,4.2,2400,4.2,1400,4.2,1360,4.2,1400,
-4.4,1520,-4.9,1520,4.2,760,
LElbowRoll,
-69.0,1000,-73.0,1240,-71.5,1160,-57.4,1400,-56.7,1360,
-57.4,1400,-48.5,1520,-47.2,1520,-71.4,760,
LElbowYaw,
-39.0,1000,-78.9,1240,-75.7,1160,-67.2,1400,-66.9,1360,
-67.2,1400,-29.3,1520,-34.1,1520,-75.5,760,
LHand,
0.3,1000,0.3,1240,0.3,1160,0.3,1400,0.3,1360,
0.3,1400,0.3,1520,0.3,1520,0.3,760,
LHipPitch,
-39.5,1000,-40.1,2400,-41.7,1400,-48.3,1360,-41.7,1400,
-40.8,1520,-35.2,1520,-40.1,760,
LHipRoll,
-4.6,1000,-4.3,2400,-3.7,1400,12.0,1360,-3.7,1400,
5.1,1520,-8.6,1520,-4.3,760,
LHipYawPitch,
-14.5,1000,-15.3,2400,-15.6,1400,-9.1,1360,-15.6,1400,
-9.6,1520,-7.5,1520,-15.3,760,
LKneePitch,
121.0,1000,121.0,2400,121.0,1400,121.0,1360,121.0,1400,
121.0,1520,107.1,1520,121.0,760,
LShoulderPitch,
84.7,1000,10.2,1240,-53.8,1160,-51.4,1400,-52.5,1360,
-51.4,1400,-70.8,1520,-67.4,1520,-53.8,760,
LShoulderRoll,
5.6,1000,4.2,1240,14.9,1160,54.8,1400,46.8,1360,
54.8,1400,0.4,1520,2.4,1520,15.8,760,
LWristYaw,
25.3,1000,26.4,1240,31.4,1160,30.2,1400,30.1,1360,
30.2,1400,30.1,1520,30.1,1520,31.4,760,
RAnklePitch,
-68.0,1000,-68.0,2400,-68.0,1400,-65.6,1360,-68.0,1400,
-68.0,1520,-68.0,1520,-68.0,760,
RAnkleRoll,
-4.3,1000,-4.5,2400,-4.7,1400,5.5,1360,-4.7,1400,
-4.7,1520,0.8,1520,-4.6,760,
RElbowRoll,
71.1,1000,74.3,1240,65.8,1160,57.4,1400,59.6,1360,
57.4,1400,58.1,1520,59.2,1520,65.6,760,
RElbowYaw,
50.8,1000,79.4,1240,72.6,1160,25.6,1400,24.5,1360,
25.6,1400,17.4,1520,25.8,1520,71.8,760,
RHand,
0.5,1000,0.5,1240,0.5,1160,0.5,1400,0.5,1360,
0.5,1400,0.5,1520,0.5,1520,0.5,760,
RHipPitch,
-39.9,1000,-41.0,2400,-41.5,1400,-30.1,1360,-41.5,1400,
-41.0,1520,-49.0,1520,-41.0,760,
RHipRoll,
4.5,1000,4.3,2400,4.2,1400,9.8,1360,4.2,1400,
3.1,1520,-15.2,1520,4.3,760,
RHipYawPitch,
-14.5,1000,-15.3,2400,-15.6,1400,-9.1,1360,-15.6,1400,
-9.6,1520,-7.5,1520,-15.3,760,
RKneePitch,
121.0,1000,121.0,2400,121.0,1400,102.8,1360,121.0,1400,
121.0,1520,121.0,1520,121.0,760,
RShoulderPitch,
91.1,1000,7.1,1240,-52.5,1160,-73.5,1400,-73.9,1360,
-73.5,1400,-80.6,1520,-77.7,1520,-53.7,760,
RShoulderRoll,
-0.0,1000,-3.2,1240,-13.7,1160,-1.7,1400,-6.6,1360,
-1.7,1400,-58.6,1520,-54.7,1520,-13.7,760,
RWristYaw,
-29.2,1000,-29.2,1240,-29.2,1160,-29.2,1400,-29.2,1360,
-29.2,1400,-29.2,1520,-29.2,1520,-29.2,760)]]"""
dance.tags = ["dance", "joy"]
dance.regexp = r"dance(es?)|(ing)"
# dance.params["base_pose"] = "Stand"

