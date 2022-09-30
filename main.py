from RoboDKSim import Drone
from controller import Controller
import threading

def main():
    drone = Drone()
    controller = Controller()
    running = True
    manual_steer = False
    while running:
        try:
            pitch, roll = controller.get_left_stick()
            _, yaw = controller.get_right_stick()
            throttle = controller.get_right_bumper() - controller.get_left_bumper()


            if manual_steer:
                drone.steer(roll, pitch, yaw)
            else:
                drone.auto_steer(roll * 30, pitch * 30, yaw * 10)
                drone.auto_throttle(throttle)
        except KeyboardInterrupt:
            pass
        drone.sim_cycle()



if __name__ == '__main__':
    main()

