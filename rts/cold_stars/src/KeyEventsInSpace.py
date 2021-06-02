from constants import *


class KeyEventsInSpace:
    def __init__(self, UPDATE):
        # Global Values to local
        self.vpCoordinate_x = vpCoordinate_x
        self.vpCoordinate_y = vpCoordinate_y
        self.advanceVelocity_x = advanceVelocity_x
        self.advanceVelocity_y = advanceVelocity_y

        self.RUNNING = True
        self.UPDATE = UPDATE

        self.turn_end = 0

        self.show_ships_info_FLAG = False
        self.show_planet_info_FLAG = False
        self.show_planet_orbit_FLAG = False

        self.garpun_SELECTED = False
        self.show_RADAR = False

        self.slot_1_SELECTED = False
        self.slot_2_SELECTED = False
        self.slot_3_SELECTED = False
        self.slot_4_SELECTED = False
        self.slot_5_SELECTED = False

    def update(self):
        self.mouse_left_button_click = False
        self.mouse_right_button_click = False
        self.mx, self.my = pygame.mouse.get_pos()
        self.my = (
            VIEW_HEIGHT - self.my
        )  # change direction of the Y axis (pygame and opengl Y axis are opposite)

        for evt in pygame.event.get():
            if evt.type == pygame.QUIT:
                self.RUNNING = False
                return self.RUNNING

            elif evt.type == pygame.MOUSEBUTTONDOWN:
                if evt.button == 1:
                    self.mouse_left_button_click = True
                elif evt.button == 3:
                    self.mouse_right_button_click = True

            elif evt.type == pygame.KEYDOWN:

                if evt.key == pygame.K_LEFT:
                    self.advanceVelocity_x += -SCROLL_VELOCITY_X
                elif evt.key == pygame.K_RIGHT:
                    self.advanceVelocity_x += SCROLL_VELOCITY_X

                elif evt.key == pygame.K_UP:
                    self.advanceVelocity_y += SCROLL_VELOCITY_Y
                elif evt.key == pygame.K_DOWN:
                    self.advanceVelocity_y += -SCROLL_VELOCITY_Y

                elif evt.key == pygame.K_ESCAPE:
                    pass  # pygame.event.post(pygame.event.Event(pygame.QUIT, {}))

                elif evt.key == pygame.K_SPACE:
                    self.turn_end = 1

            elif evt.type == pygame.KEYUP:
                if evt.key == pygame.K_LEFT:
                    self.advanceVelocity_x += SCROLL_VELOCITY_X
                elif evt.key == pygame.K_RIGHT:
                    self.advanceVelocity_x += -SCROLL_VELOCITY_X

                elif evt.key == pygame.K_UP:
                    self.advanceVelocity_y += -SCROLL_VELOCITY_Y
                elif evt.key == pygame.K_DOWN:
                    self.advanceVelocity_y += SCROLL_VELOCITY_Y

                elif evt.key == pygame.K_SPACE:
                    self.turn_end = 0

                elif evt.key == pygame.K_g:
                    if self.garpun_SELECTED == False:
                        self.garpun_SELECTED = True
                        # print('garpun_SELECTED - yes'
                    else:
                        self.garpun_SELECTED = False
                        # print('garpun_SELECTED - no'

                elif evt.key == pygame.K_r:
                    if self.show_RADAR == False:
                        self.show_RADAR = True
                        # print('show_RADAR - yes'
                    else:
                        self.show_RADAR = False
                        # print('show_RADAR - no'

                elif evt.key == pygame.K_1:
                    if self.slot_1_SELECTED == False:
                        self.slot_1_SELECTED = True
                        # print('slot 1 - yes'
                    else:
                        self.slot_1_SELECTED = False
                        # print('slot 1 - no'

                elif evt.key == pygame.K_2:
                    if self.slot_2_SELECTED == False:
                        self.slot_2_SELECTED = True
                        # print('slot 2 - yes'
                    else:
                        self.slot_2_SELECTED = False
                        # print('slot 2 - no'

                elif evt.key == pygame.K_3:
                    if self.slot_3_SELECTED == False:
                        self.slot_3_SELECTED = True
                        # print('slot 3 - yes'
                    else:
                        self.slot_3_SELECTED = False
                        # print('slot 3 - no'

                elif evt.key == pygame.K_4:
                    if self.slot_4_SELECTED == False:
                        self.slot_4_SELECTED = True
                        # print('slot 4 - yes'
                    else:
                        self.slot_4_SELECTED = False
                        # print('slot 4 - no'

                elif evt.key == pygame.K_5:
                    if self.slot_5_SELECTED == False:
                        self.slot_5_SELECTED = True
                        # print('slot 5 - yes'
                    else:
                        self.slot_5_SELECTED = False
                        # print('slot 5 - no'

                elif evt.key == pygame.K_a:
                    if (
                        self.slot_1_SELECTED == True
                        and self.slot_2_SELECTED == True
                        and self.slot_3_SELECTED == True
                        and self.slot_4_SELECTED == True
                        and self.slot_5_SELECTED == True
                    ):
                        self.slot_1_SELECTED = False
                        self.slot_2_SELECTED = False
                        self.slot_3_SELECTED = False
                        self.slot_4_SELECTED = False
                        self.slot_5_SELECTED = False
                        ## print('slot 1 - no'
                        ## print('slot 2 - no'
                        ## print('slot 3 - no'
                        ## print('slot 4 - no'
                        ## print('slot 5 - no'

                    else:
                        self.slot_1_SELECTED = True
                        self.slot_2_SELECTED = True
                        self.slot_3_SELECTED = True
                        self.slot_4_SELECTED = True
                        self.slot_5_SELECTED = True
                        ## print('slot 1 - yes'
                        ## print('slot 2 - yes'
                        ## print('slot 3 - yes'
                        ## print('slot 4 - yes'
                        ## print('slot 5 - yes'

                elif evt.key == pygame.K_0:
                    # print('*****************'
                    if self.slot_1_SELECTED == True:
                        print("slot 1 - yes")
                    else:
                        print("slot 1 - no")

                    if self.slot_2_SELECTED == True:
                        print("slot 2 - yes")
                    else:
                        print("slot 2 - no")

                    if self.slot_3_SELECTED == True:
                        print("slot 3 - yes")
                    else:
                        print("slot 3 - no")
                    # print('*****************'

                elif evt.key == pygame.K_s:
                    if self.show_ships_info_FLAG == False:
                        self.show_ships_info_FLAG = True
                    else:
                        self.show_ships_info_FLAG = False

                elif evt.key == pygame.K_p:
                    if self.show_planet_info_FLAG == False:
                        self.show_planet_info_FLAG = True
                    else:
                        self.show_planet_info_FLAG = False

                elif evt.key == pygame.K_o:
                    if self.show_planet_orbit_FLAG == False:
                        self.show_planet_orbit_FLAG = True
                    else:
                        self.show_planet_orbit_FLAG = False

            elif evt.type == self.UPDATE:
                self.vpCoordinate_x += self.advanceVelocity_x
                self.vpCoordinate_y += self.advanceVelocity_y

    def readControlKeys(self):
        self.update()
        return (
            self.RUNNING,
            self.vpCoordinate_x,
            self.vpCoordinate_y,
            self.turn_end,
            self.show_ships_info_FLAG,
            self.show_planet_info_FLAG,
            self.show_planet_orbit_FLAG,
            self.show_RADAR,
            self.garpun_SELECTED,
            self.slot_1_SELECTED,
            self.slot_2_SELECTED,
            self.slot_3_SELECTED,
            self.slot_4_SELECTED,
            self.slot_5_SELECTED,
            self.mouse_left_button_click,
            self.mouse_right_button_click,
            self.mx,
            self.my,
        )
