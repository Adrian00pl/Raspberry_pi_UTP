from DobotEDU import *
magician.ptp(mode=0,x=222,y=-13.59,z=0,r=90)
magician.set_endeffector_gripper(enable=True,on=False)
magician.wait(second=6)
magician.ptp(mode=0,x=222,y=-13.59,z=-36.1,r=90)
magician.set_endeffector_gripper(enable=True,on=True)
magician.wait(second=6)
magician.ptp(mode=0,x=222,y=-13.59,z=0,r=90)
magician.ptp(mode=0,x=222,y=-13.59,z=0,r=0)
magician.ptp(mode=0,x=222,y=-137,z=-0,r=0)
magician.ptp(mode=0,x=222,y=-137,z=-36.15,r=0)
magician.set_endeffector_gripper(enable=True,on=False)
magician.wait(second=6)
magician.ptp(mode=0,x=222,y=-137,z=0,r=0)
magician.ptp(mode=0,x=222,y=-137,z=0,r=90)
magician.ptp(mode=0,x=222y=-137,z=-36.15,r=90)
magician.set_endeffector_gripper(enable=True,on=True)
magician.wait(second=6)





magician.ptp(mode=0,x=222,y=-137,z=0,r=90)
magician.ptp(mode=0,x=222,y=-13.59,z=0,r=90)
magician.ptp(mode=0,x=222,y=-13.59,z=-36.15,r=90)
magician.set_endeffector_gripper(enable=True,on=False)
magician.wait(second=6)

magician.ptp(mode=0,x=222,y=-13.59,z=0,r=90)
magician.ptp(mode=0,x=222,y=-13.59,z=0,r=0)
magician.ptp(mode=0, x=222, y=-13.59, z=-36.15, r=0)
magician.set_endeffector_gripper(enable=True, on=True)
magician.wait(second=6)

magician.ptp(mode=0, x=222, y=-13.59, z=0, r=0)
magician.ptp(mode=0, x=222, y=-13.59, z=0, r=90)
magician.ptp(mode=0, x=222, y=137, z=0, r=90)
magician.ptp(mode=0, x=222, y=137, z=-36.15, r=90)
magician.set_endeffector_gripper(enable=True, on=True)
magician.wait(second=6)

magician.ptp(mode=0, x=222, y=137, z=0, r=90)
magician.ptp(mode=0, x=222, y=137, z=0, r=0)
magician.ptp(mode=0, x=222, y=-13.59, z=0, r=0)
magician.ptp(mode=0, x=222, y=-13.59, z=-36.15, r=0)
magician.set_endeffector_gripper(enable=True, on=False)
magician.wait(second=6)

magician.ptp(mode=0, x=222, y=-13.59, z=0, r=0)
magician.set_endeffector_gripper(enable=False, on=True)
magician.wait(second=6)
