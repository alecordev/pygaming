from math import *
from random import randint
from render import drawTexturedRect, drawDynamic


class distantStar:
    def __init__(self, texOb, posx, posy, size):
        self.texture = texOb.texture
        self.pos_x = posx
        self.pos_y = posy
        self.size = size
        self.distance_rate = size / 1000.0
        self.alpha_threshold = randint(90, 98) * 0.01
        self.d_alpha = randint(80, 100) * 0.00005

        self.alpha = self.alpha_threshold
        self.increase = True

    def update(self):
        pass  # due to current problem with bright pass in bloom
        # if self.alpha >= 1.0:
        # self.increase = False
        # elif self.alpha <= self.alpha_threshold:
        # self.increase = True

        # if self.increase == True:
        # self.alpha += self.d_alpha
        # else:
        # self.alpha -= self.d_alpha


class distantNebulaStatic:
    def __init__(self, texOb, posx, posy):
        self.texOb = texOb
        self.pos_x = posx
        self.pos_y = posy

    def linkTexture(self):
        self.texture = self.texOb.texture
        self.w, self.h = self.texOb.w, self.texOb.h
        if self.w > 1000:
            self.distance_rate = 1 / 60.0
        else:
            self.distance_rate = 1 / 40.0

    def render(self, vx, vy):
        drawTexturedRect(
            self.texture,
            [
                self.pos_x - vx * self.distance_rate,
                self.pos_y - vy * self.distance_rate,
                self.w,
                self.h,
            ],
            -1.0,
        )


class distantNebulaRotated:
    def __init__(self, texOb, posx, posy):
        self.texOb = texOb
        self.pos_x = posx
        self.pos_y = posy

        self.angle = randint(0, 360)
        self.d_angle = randint(5, 12) * 0.001

        if randint(1, 2) == 1:
            self.d_angle = -self.d_angle

    def linkTexture(self):
        self.texture = self.texOb.texture
        self.w, self.h = self.texOb.w, self.texOb.h
        if self.w > 1000:
            self.distance_rate = 1 / 60.0
        else:
            self.distance_rate = 1 / 40.0

    def update(self):
        self.angle += self.d_angle

    def render(self, vx, vy):
        drawDynamic(
            self.texture,
            (
                self.pos_x - vx * self.distance_rate,
                self.pos_y - vy * self.distance_rate,
            ),
            self.angle,
            (-self.w / 2, -self.h / 2, self.w / 2, self.h / 2),
        )


class effectNebula:
    def __init__(self):
        self.ax = randint(0, 360)
        self.ay = randint(0, 360)
        self.az = randint(0, 360)
        self.a_dx = randint(5, 10) * 0.01
        self.a_dy = randint(5, 10) * 0.01
        self.a_dz = randint(5, 10) * 0.01
        self.nebula_tex, (w, h) = upload_texture("data/bg_space/nebula.bak/mod.png")

        self.bottomLeft_orig = [-200, -200, 0]
        self.bottomRight_orig = [200, -200, 0]
        self.topRight_orig = [200, 200, 0]
        self.topLeft_orig = [-200, 200, 0]

        self.verticles_orig = [
            self.bottomLeft_orig,
            self.bottomRight_orig,
            self.topRight_orig,
            self.topLeft_orig,
        ]

    def update(self):
        self.ax += self.a_dx
        self.ay += self.a_dy
        self.az += self.a_dz

    def updateVerticles(self):  # should be asked
        cos_ax = cos(self.ax * 2 * pi / 360)
        sin_ax = sin(self.ax * 2 * pi / 360)

        for v in self.verticles:
            tmp = [v[0], 0, 0]
            tmp[1] = v[1] * cos_ax - v[2] * sin_ax
            tmp[2] = v[1] * sin_ax + v[2] * cos_ax
            v = [tmp[0], tmp[1], tmp[2]]

    def verticleRotationX(self, v):
        cos_ax = cos(self.ax * 2 * pi / 360)
        sin_ax = sin(self.ax * 2 * pi / 360)

        """
      self.RotX_mat1 = np.array( [ [ 1.0, 0.0,    0.0     ],\
                                   [ 0.0, cos_ax, -sin_ax ],\
                                   [ 0.0, sin_ax, cos_ax  ] ] )
      """
        tmp = [v[0], 0, 0]
        tmp[1] = v[1] * cos_ax - v[2] * sin_ax
        tmp[2] = v[1] * sin_ax + v[2] * cos_ax

        return tmp

    def verticleRotationY(self, v):
        cos_ay = cos(self.ay * 2 * pi / 360)
        sin_ay = sin(self.ay * 2 * pi / 360)

        """ 
      self.RotY_mat = np.array( [ [ cos_ay,  0.0,  sin_ay ],\
                                  [ 0.0,     1.0,  0.0    ],\
                                  [ -sin_ay, 0.0,  cos_ay ] ] )
      """
        tmp = [0, v[1], 0]
        tmp[0] = v[0] * cos_ay + v[2] * sin_ay
        tmp[2] = -v[0] * sin_ay + v[2] * cos_ay

        return tmp

    def verticleRotationZ(self, v):
        cos_az = cos(self.az * 2 * pi / 360)
        sin_az = sin(self.az * 2 * pi / 360)

        """
      self.RotZ_mat = np.array( [ [ cos_az,  -sin_az, 0.0  ],\
                                  [ sin_az,  cos_az,  0.0  ],\
                                  [ 0.0,     0.0,     1.0  ] ] )
    
      """
        tmp = [0, 0, v[2]]
        tmp[0] = v[0] * cos_az - v[1] * sin_az
        tmp[1] = v[0] * sin_az + v[1] * cos_az

        return tmp

    def getNormal(self, v1, v2, v3):
        l1 = [0, 0, 0]
        l2 = [0, 0, 0]
        result = [0, 0, 0]

        ##########
        # n = axb
        #     _
        #     b
        # v1-----v2
        # |_     |
        # |a     |
        # |      |
        # v3-----v4
        ##########

        l1[0] = v2[0] - v1[0]
        l1[1] = v2[1] - v1[1]
        l1[2] = v2[2] - v1[2]

        l2[0] = v3[0] - v1[0]
        l2[1] = v3[1] - v1[1]
        l2[2] = v3[2] - v1[2]

        result[0] = l1[1] * l2[2] - l1[2] * l2[1]
        result[1] = l1[2] * l2[0] - l1[0] * l2[2]
        result[2] = l1[0] * l2[1] - l1[1] * l2[0]

        length = sqrt(
            result[0] * result[0] + result[1] * result[1] + result[2] * result[2]
        )
        ilength = 1 / length

        result[0] = result[0] * ilength
        result[1] = result[1] * ilength
        result[2] = result[2] * ilength
        return result

    def verticleTranslation(self, v, x, y, z):
        return [v[0] + x, v[1] + y, v[2] + z]

    def render(self):
        self.update()
        glBindTexture(GL_TEXTURE_2D, self.nebula_tex)

        self.bottomLeft = self.verticleRotationX(self.bottomLeft_orig)
        self.bottomRight = self.verticleRotationX(self.bottomRight_orig)
        self.topRight = self.verticleRotationX(self.topRight_orig)
        self.topLeft = self.verticleRotationX(self.topLeft_orig)

        self.bottomLeft = self.verticleRotationY(self.bottomLeft)
        self.bottomRight = self.verticleRotationY(self.bottomRight)
        self.topRight = self.verticleRotationY(self.topRight)
        self.topLeft = self.verticleRotationY(self.topLeft)

        self.bottomLeft = self.verticleRotationZ(self.bottomLeft)
        self.bottomRight = self.verticleRotationZ(self.bottomRight)
        self.topRight = self.verticleRotationZ(self.topRight)
        self.topLeft = self.verticleRotationZ(self.topLeft)

        self.bottomLeft = self.verticleTranslation(self.bottomLeft, 400, 400, -500)
        self.bottomRight = self.verticleTranslation(self.bottomRight, 400, 400, -500)
        self.topRight = self.verticleTranslation(self.topRight, 400, 400, -500)
        self.topLeft = self.verticleTranslation(self.topLeft, 400, 400, -500)

        normal = self.getNormal(self.bottomLeft, self.bottomRight, self.topRight)
        glColor4f(1.0, 1.0, 1.0, abs(normal[2]))
        drawQuadPer3DVertex(
            self.bottomLeft, self.bottomRight, self.topRight, self.topLeft
        )
