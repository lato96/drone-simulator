import time

from robodk import robolink    # RoboDK API
from robodk import robomath    # Robot toolbox
from random import randrange
RDK = robolink.Robolink()

g = 9.81
m = 1.0
f = m*g


class Drone:
    def __init__(self):
        self.origin = RDK.Item('world_origin', robolink.ITEM_TYPE_FRAME)
        self.drone = RDK.Item('drone_base', robolink.ITEM_TYPE_FRAME)
        self.origin.setPose(robomath.eye(4))
        self.drone.setPose(robomath.eye(4))
        self.f_drone = robomath.eye(4)
        self.a_g = robomath.Pose(0, 0, -g, 0, 0, 0)
        self.f_g = robomath.Pose(0, 0, -g*m, 0, 0, 0)
        self.f_resultant = self.f_g * self.f_drone
        self.a_resultant = None
        self.v_resultant = robomath.eye(4)
        self.drone_orientation = robomath.eye(4)
        self.drone_yaw = 0
        self.f = f
        self.v_x = 0

    def scalar_multiplication(self, a, mat: robomath.Mat):
        result = mat
        result.rows[0][3] *= a
        result.rows[1][3] *= a
        result.rows[2][3] *= a
        return result

    def set_drone_tilt(self, r, p, y):
        self.drone_orientation = robomath.Pose(0, 0, 0, r, p, y)


    def set_drone_force(self, force):
        #self.f_drone.rows[2][3] = force
        self.f = force

    def update_force_resultant(self):
        self.f_resultant = self.f_drone * self.drone_orientation
        self.f_resultant = self.f_g * self.f_resultant

    def update_acc_resultant(self):
        self.a_resultant = self.scalar_multiplication(1/m, self.f_resultant)

    def update_v(self):
        self.v_resultant = self.v_resultant * self.a_resultant

    def update_position(self):
        orientation = self.drone_orientation
        current_pose = self.drone.Pose()
        x = current_pose.rows[0][3]
        y = current_pose.rows[1][3]
        z = current_pose.rows[2][3]
        new_pose = robomath.Pose(x, y, z + self.f, 0, 0, 0)
        new_pose *= robomath.Pose(0, 0, 0, 0, 0, self.drone_yaw)
        new_pose *= robomath.Pose(self.v_x, self.v_y, 0, 0, 0, 0)
        new_pose *= orientation
        self.drone.setPose(new_pose)

    def sim_cycle(self):
        #self.update_force_resultant()
        #self.update_acc_resultant()
        #self.update_v()

        self.update_position()

    def steer(self, r, p, y):
        mat_orientation = robomath.Pose(0, 0, 0, r, p, y)
        self.drone_orientation *= mat_orientation
        self.update_position()

    def auto_steer(self, r, p, y):
        self.drone_yaw += y
        self.v_x = p / 5
        self.v_y = -r / 5
        self.drone_orientation = robomath.Pose(0, 0, 0, r, p, 0)


    def throttle(self):
        pass

    def auto_throttle(self, input):
        if input < 0:
            self.set_drone_force(input*5) # f - input
        else:
            self.set_drone_force(input*5) #  f + input


if __name__ == '__main__':
    sim = Drone()
    def random_force():
        offset = randrange(-10, 10)
        force = f-0.1*offset

        return force
    while True:
        sim.set_drone_tilt(0.2, 0, 0)
        sim.f_drone.rows[2][3] = random_force()
        sim.sim_cycle()
        time.sleep(0.1)

