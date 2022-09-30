import pygame


class Controller:
    pygame.init()
    pygame.joystick.init()

    def __init__(self):
        self.xbox_controller = pygame.joystick.Joystick(0)
        self.id = self.xbox_controller.get_name()

    def pump_event(self):
        pygame.event.pump()

    def filter_deadzone(self, axis):

        val = abs(axis)
        if val < 0.1:
            return 0.0
        elif val > 0.9:
            if axis < 0:
                return -0.9
            else:
                return 0.9
        else:
            return axis

    def get_left_stick(self):
        self.pump_event()
        horizontal = self.filter_deadzone(self.xbox_controller.get_axis(0))
        vertical = self.filter_deadzone(self.xbox_controller.get_axis(1))
        return (-vertical, horizontal)

    def get_right_stick(self):
        self.pump_event()
        horizontal = self.filter_deadzone(self.xbox_controller.get_axis(2))
        vertical = self.filter_deadzone(self.xbox_controller.get_axis(3))
        return (vertical, -horizontal)

    def get_left_bumper(self):
        self.pump_event()
        bumper = self.xbox_controller.get_axis(4)
        if bumper < 0:
            return 0.0
        else:
            return bumper

    def get_right_bumper(self):
        self.pump_event()
        bumper = self.xbox_controller.get_axis(5)
        if bumper < 0:
            return 0.0
        else:
            return bumper

    def get_button(self, index):
        self.pump_event()
        button_state = self.xbox_controller.get_button(index)
        return button_state

    def get_hat(self, index):
        self.pump_event()
        hat_state = self.xbox_controller.get_hat(index)
        return hat_state


if __name__ == '__main__':
    c = Controller()
    print(c.id)
    axes = c.xbox_controller.get_numaxes()
    print(axes)
    while True:
        pygame.event.pump()


        #print(f'left {c.get_left_stick()}')
        #print(f'right {c.get_right_stick()}')
        print(c.get_button())
    pygame.quit()

