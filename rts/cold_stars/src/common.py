"""
Copyright (C) ColdStars, Aleksandr Pivovarov <<coldstars8@gmail.com>>

This program is free software; you can redistribute it and/or
modify it under the terms of the GNU General Public License
as published by the Free Software Foundation; either version 2
of the License, or (at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program; if not, write to the Free Software
Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA  02110-1301, USA.
"""


from constants import *
from render import *

# size 0...9
def returnObjectSize(w, h):
    if w * h < SIZE_0 * SIZE_0:
        return 1
    elif w * h < SIZE_1 * SIZE_1:
        return 2
    elif w * h < SIZE_2 * SIZE_2:
        return 3
    elif w * h < SIZE_3 * SIZE_3:
        return 4
    elif w * h < SIZE_4 * SIZE_4:
        return 5
    elif w * h < SIZE_5 * SIZE_5:
        return 6
    elif w * h < SIZE_6 * SIZE_6:
        return 7
    elif w * h < SIZE_7 * SIZE_7:
        return 8
    elif w * h < SIZE_8 * SIZE_8:
        return 9
    elif w * h >= SIZE_8 * SIZE_8:
        return 10


def returnRandomFromTheList(list):
    return list[randint(0, len(list) - 1)]


class CommonInstance:
    def __init__(self, texture_ID, w, h, fps=0):
        self.texture_ID = texture_ID
        self.w, self.h = w, h
        if isinstance(texture_ID, list):
            self.len_texture_ID = len(texture_ID)
            self._last_update = 0
            if fps == 0:
                fps = len(texture_ID)  # * 1.3
            self._delay = 1000 / fps
            self._tex_frame = 0
            self.frames_ENDED = False
            self.animated = True
        else:
            self.animated = False

    def updateRenderConstants(self):
        # constants needs for render
        # decreases the math during game loop
        self.minus_half_w = -self.w / 2
        self.minus_half_h = -self.h / 2
        self.plus_half_w = self.w / 2
        self.plus_half_h = self.h / 2

    def updateAnimationFrame(self):
        t = pygame.time.get_ticks()
        if t - self._last_update > self._delay:
            self._tex_frame += 1
            if self._tex_frame == (self.len_texture_ID - 1):
                self.frames_ENDED = (
                    True  # this flag needs for not loop animation such as explosions
                )
            self._last_update = t

    def updateAnimationFrameLoop(self):
        t = pygame.time.get_ticks()
        if t - self._last_update > self._delay:
            self._tex_frame += 1
            if self._tex_frame == self.len_texture_ID:
                self._tex_frame = 0
            self._last_update = t

    def renderLabel(self):
        renderLabel(self.rect, self.__str__())

    def renderDynamicFrame(self):
        drawDynamic(
            self.texture_ID,
            (self.rect.centerx, self.rect.centery),
            self.angle,
            (
                self.minus_w_div_2,
                self.minus_h_div_2,
                self.plus_w_div_2,
                self.plus_h_div_2,
            ),
        )

    def renderDynamicFrameRot(self):
        self.renderDynamicFrame()
        self.angle += self.deltaAngle

    def renderDynamicFramesLoopRot(self):
        self.renderDynamicFramesLoop()
        self.angle += self.deltaAngle

    def renderDynamicFrames(self):
        drawDynamic(
            self.texture_ID[self._tex_frame],
            (self.rect.centerx, self.rect.centery),
            self.angle,
            (
                self.minus_w_div_2,
                self.minus_h_div_2,
                self.plus_w_div_2,
                self.plus_h_div_2,
            ),
        )
        self.updateAnimationFrame()

    def renderDynamicFramesLoop(self):
        drawDynamic(
            self.texture_ID[self._tex_frame],
            (self.rect.centerx, self.rect.centery),
            self.angle,
            (
                self.minus_w_div_2,
                self.minus_h_div_2,
                self.plus_w_div_2,
                self.plus_h_div_2,
            ),
        )
        self.updateAnimationFrameLoop()

    def renderDynamicFramesLoopRot(self):
        self.renderDynamicFramesLoop()
        self.angle += self.deltaAngle

    def renderStaticFrame(self):
        drawTexturedRect(self.texture_ID, self.rect, -1.0)

    def renderStaticFramesLoop(self):
        drawTexturedRect(self.texture_ID[self._tex_frame], self.rect, -1.0)
        self.updateAnimationFrameLoop()

    def renderStaticFrameOnRect(self, rect):
        # used for items render in slot
        drawTexturedRect(self.texture_ID, rect, -1.0)

    def renderStaticFramesLoopOnRect(self, rect):
        # used for items render in slot
        drawTexturedRect(self.texture_ID[self._tex_frame], rect, -1.0)
        self.updateAnimationFrameLoop()


def rocketWayCalc111(x1, y1, x2, y2, ob_angle, d_angle, step):
    x = x2 - x1
    y = y2 - y1

    d_angle = d_angle * 2
    step = step / 4.0

    t_angle = atan2(y, x) * 57.295779

    if y2 > y1:
        k = 1
    elif y1 > y2:
        k = -1
    else:
        k = 0

    if abs(ob_angle) > 360:
        ob_angle = ob_angle % 360

    # if abs(360 - t_angle) < abs(t_angle):
    # k2 = -1
    # else:
    # k2 = 1

    ## print('rocket, mouse =', int(ob_angle), int(t_angle)
    if ob_angle > t_angle:
        ob_angle = ob_angle - d_angle

    if ob_angle < t_angle:
        ob_angle = ob_angle + d_angle

    ## print('rocket, mouse =', int(ob_angle), int(t_angle)
    # if ob_angle > t_angle:
    # if t_angle < 0:
    # ob_angle = ob_angle - d_angle
    # if t_angle > 0:
    # ob_angle = ob_angle - d_angle

    # if ob_angle < t_angle:
    # if t_angle < 0:
    # ob_angle = ob_angle + d_angle
    # if t_angle > 0:
    # ob_angle = ob_angle + d_angle

    # if t_angle > ob_angle:
    # ob_angle = ob_angle - k*k2*d_angle

    dx = step * cos(ob_angle / 57.295779)
    dy = step * sin(ob_angle / 57.295779)

    return (dx, dy), ob_angle

    # >>> if -2 >-3: # print('dada'
    # ...
    # dada


def rocketWayCalc(x1, y1, x2, y2, ob_angle, d_angle, step):
    x = x2 - x1
    y = y2 - y1

    d_angle = d_angle * 2
    step = step / 4.0

    t_angle = atan2(y, x) * 57.295779

    ## print('rocket_angle, mouse_angle =', int(ob_angle), int(t_angle)

    if ob_angle > t_angle:
        ob_angle = ob_angle - d_angle
    elif ob_angle < t_angle:
        ob_angle = ob_angle + d_angle

    dx = step * cos(ob_angle / 57.295779)
    dy = step * sin(ob_angle / 57.295779)

    return (dx, dy), ob_angle


def get_dX_dY_Angle_ToPoint(x1, y1, x2, y2, step):
    # step = step
    x = x2 - x1
    y = y2 - y1

    l = sqrt(x * x + y * y)

    if l != 0:
        xn, yn = x / l, y / l
    else:
        xn, yn = 0, 0

    angle = atan2(y, x) * 57.295779

    dx = xn * step
    dy = yn * step

    # if abs(dx)

    return (dx, dy), angle


def get_dX_dY_ToPoint(x1, y1, x2, y2, step):
    x = x2 - x1
    y = y2 - y1

    l = sqrt(x * x + y * y)

    if l != 0:
        xn, yn = x / l, y / l
    else:
        xn, yn = 0, 0

    dx = xn * step
    dy = yn * step

    return dx, dy


def follow_static_obj(self_x, self_y, target_x, target_y, speed):
    direction_list_x = []
    direction_list_y = []
    angle_list = []

    step = speed / 100.0

    if (self_x != target_x or self_y != target_y) and speed != 0:
        x = target_x - self_x
        y = target_y - self_y

        l = sqrt(x * x + y * y)
        x_normalized, y_normalized = x / l, y / l

        it = int(l / step)

        x_step = x_normalized * step
        y_step = y_normalized * step

        i = 0
        while i < it:
            self_x += x_step
            self_y += y_step
            angle = atan2(target_y - self_y, target_x - self_x) * 57.295779

            direction_list_x.append(self_x)
            direction_list_y.append(self_y)
            angle_list.append(angle)

            i += 1

    return direction_list_x, direction_list_y, angle_list


def getCircleCoordinateRangeLowPrecision(x0, y0, radius, lstep=30):
    # returns small lists of x, y coordinates for circle
    # used for visualisation of radiuses (weapons, radar, ranges)
    circle_list_x = []
    circle_list_y = []

    alfa_step = atan(float(lstep) / radius)

    alfa = 0
    while alfa < 360 / 57.295779:
        x = x0 + radius * cos(alfa)
        y = y0 + radius * sin(alfa)

        circle_list_x.append(x)
        circle_list_y.append(y)
        alfa += alfa_step

    return circle_list_x, circle_list_y


def getEllipseCoordinateRangeHighPrecision(x_0, y_0, radius_A, radius_B, speed, fi):
    # returns the x,y lists for planet, asteroid orbit. This algorythm is weight, that is why it must be used once, for static orbit calculation. Use get_orbit_coord_low_precision for better merfomance
    orbit_list_x = []
    orbit_list_y = []
    alfa_LIST = []

    dalfa = speed / 2500.0 / 57.295779
    max_alfa = 360 / 57.295779

    alfa = 0
    while alfa < max_alfa:
        alfa_LIST.append(alfa)
        alfa += dalfa

    if radius_A != radius_B:
        for alfa in alfa_LIST:
            x_coord = (
                x_0 + radius_A * cos(alfa) * cos(fi) - radius_B * sin(alfa) * sin(fi)
            )
            y_coord = (
                y_0 + radius_A * cos(alfa) * sin(fi) + radius_B * sin(alfa) * cos(fi)
            )
            orbit_list_x.append(x_coord)
            orbit_list_y.append(y_coord)
    else:
        for alfa in alfa_LIST:
            x_coord = x_0 + radius_A * cos(alfa)
            y_coord = y_0 + radius_A * sin(alfa)
            orbit_list_x.append(x_coord)
            orbit_list_y.append(y_coord)

    return orbit_list_x, orbit_list_y


def getSputnikCoordinateRange(x0_list, y0_list, radius, speed):
    orbit_list_x = []
    orbit_list_y = []

    _len = len(x0_list)
    dalfa = speed / 2500.0 / 57.295779

    alfa = 0
    i = 0

    while i < (_len - 1):
        x_coord = x0_list[i] + radius * cos(alfa)
        y_coord = y0_list[i] + radius * sin(alfa)
        orbit_list_x.append(x_coord)
        orbit_list_y.append(y_coord)

        alfa += dalfa
        i += 1

    return orbit_list_x, orbit_list_y


def getStepForEllipseDraw(radius_A, radius_B, len_list):
    "this function counts the fixed step between two points for all planet/asteroid orbits"
    if radius_A >= radius_B:
        max_rad = radius_A
    else:
        max_rad = radius_B

    maxlen = 2 * pi * max_rad
    quantity = int(maxlen) / DISTANCE_BETWEEN_POINTS
    step = len_list / quantity
    return int(step)


def returnSlotWithGoodsBySubtype(item_subtype, slot_list):
    for slot in slot_list:
        if slot.item != None and slot.item.type == CONTAINER_ID:
            if slot.item.item.subtype == item_subtype:
                return slot
    return None


def returnFirstSlotWithItemByItem(item, slot_list):
    for slot in slot_list:
        if slot.item != None and slot.item == item:
            return slot
    return None


def returnFirstFreeSlotBySlotType(slot_type, slot_subtype, slot_list):
    if slot_type == WEAPON_ID:  # huck
        slot_subtype = None

    for slot in slot_list:
        if (
            slot.item == None
            and slot.type == slot_type
            and slot.subtype == slot_subtype
        ):
            return slot
    return None


def lengthBetweenPoints(x1, y1, x2, y2):
    xl = x2 - x1
    yl = y2 - y1
    return sqrt(xl * xl + yl * yl)


def returnLengthAngleBetweenPoints(x1, y1, x2, y2):
    xl = x2 - x1
    yl = y2 - y1
    angle_radian = atan2(yl, xl)
    return sqrt(xl * xl + yl * yl), angle_radian


def returnGeneratedTargetCoordinates(len, alfa, xc, yc):
    return xc + sin(alfa) * len, yc + cos(alfa) * len
