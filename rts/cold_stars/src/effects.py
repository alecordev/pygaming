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


from resources import *
from copy import *

from GLSL_stuff import ShockWaveEffect


from render import *
from random import *


class shieldEffect(CommonInstance):
    def __init__(self, ob, texOb):
        CommonInstance.__init__(self, texOb.texture, (texOb.w, texOb.h))

        self.render = self._renderDynamicFramesLoopRot
        self.render = self._renderDynamicFrame

        self.ob = ob

        self.angle = randint(0, 360)
        self.deltaAngle = randint(0, 30) * 0.003

        self.alpha_init = 0.4
        self.d_alpha = 0.01

        self.alpha = self.alpha_init

    def _renderDynamicFramesLoopRot(self):
        if self.alpha > self.alpha_init:
            self.alpha -= self.d_alpha
        else:
            self.alpha = self.alpha_init

        glColor4f(1.0, 1.0, 1.0, self.alpha)

        self.updateAnimationFrameLoop()
        glBindTexture(GL_TEXTURE_2D, self.texture_ID[self._tex_frame])
        drawQuadPer2DVertex(
            self.ob.points.bottomFarLeft,
            self.ob.points.bottomFarRight,
            self.ob.points.topFarRight,
            self.ob.points.topFarLeft,
            -2,
        )

    def _renderDynamicFrame(self):
        if self.alpha > self.alpha_init:
            self.alpha -= self.d_alpha
        else:
            self.alpha = self.alpha_init

        glColor4f(1.0, 1.0, 1.0, self.alpha)

        glBindTexture(GL_TEXTURE_2D, self.texture_ID)
        drawQuadPer2DVertex(
            self.ob.points.bottomFarLeft,
            self.ob.points.bottomFarRight,
            self.ob.points.topFarRight,
            self.ob.points.topFarLeft,
            -2,
        )


# You might also get additional benefits from using numpy to manipulate the arrays once they exist. e.g. you could add an array of velocities to an array of positions. This might be especially good for things like particle systems, where your Python code doesn't need frequent access to the value of the resulting positions.
class tinyExplosionEffect:
    def __init__(
        self,
        texOb,
        starsystem,
        center,
        num_particles,
        pSize,
        velocity_max,
        alpha_init,
        alpha_end,
        d_alpha,
    ):
        self.alive = True
        self.timeToDie = False
        self.alreadyInRemoveQueue = False

        self.starsystem = starsystem
        self.center = [center[0], center[1]]

        self.texture = texOb.texture
        self.num_particles = num_particles
        self.pSize = pSize

        self.particles_list = []
        for i in range(1, num_particles):
            simple_particle = particleForTinyExplosionEffect(
                self.center, velocity_max, alpha_init, alpha_end, randint(3, 6) * 0.01
            )
            self.particles_list.append(simple_particle)

    def setNewCenter(self, new_center):
        self.center[0] = new_center[0]
        self.center[1] = new_center[1]

    def update(self):
        self.alive = False

        if self.timeToDie == False:
            for p in self.particles_list:
                p.updateLoop(self.center[0], self.center[1])
                self.alive = True
        else:
            for p in self.particles_list:
                if p.alive == True:
                    p.updateLast()
                    self.alive = True

        if self.alive == False:
            if self.alreadyInRemoveQueue == False:
                self.starsystem.effect_DAMAGE_remove_queue.append(self)
                self.alreadyInRemoveQueue = True

    def render(self):
        glBindTexture(GL_TEXTURE_2D, self.texture)
        glPointSize(self.pSize)

        glBegin(GL_POINTS)
        for p in self.particles_list:
            if p.alive == True:
                p.render()
        glEnd()


class particleForTinyExplosionEffect:
    def __init__(self, center, velocity_max, alpha_init, alpha_end, d_alpha):
        self.alive = True

        self.pos = [center[0], center[1]]

        self.alpha_init = alpha_init
        self.alpha_end = alpha_end

        self.d_alpha = d_alpha

        self.alpha = alpha_init

        self.velocity_max = velocity_max

        if randint(1, 2) == 1:
            self.updateVelocityForExplosion()
        else:
            self.updateVelocityForCircle()

    def updateVelocityForExplosion(self):
        self.dx_n = randint(-10, 10) * 0.1
        self.dy_n = randint(-10, 10) * 0.1

        self.velocity_x = self.dx_n * self.velocity_max
        self.velocity_y = self.dy_n * self.velocity_max

    def updateVelocityForCircle(self):
        _len = randint(50, 100)
        _angle = randint(0, 360) / 57.0

        target_x = self.pos[0] + sin(_angle) * _len
        target_y = self.pos[1] + cos(_angle) * _len

        xl = target_x - self.pos[0]
        yl = target_y - self.pos[1]
        l = _len

        self.dx_n = xl / float(l)
        self.dy_n = yl / float(l)

        self.velocity_x = self.dx_n * self.velocity_max
        self.velocity_y = self.dy_n * self.velocity_max

    def updateLoop(self, new_pos_x, new_pos_y):
        self.pos[0] += self.velocity_x
        self.pos[1] += self.velocity_y
        self.alpha -= self.d_alpha

        if self.alpha < self.alpha_end:
            self.alpha = self.alpha_init
            self.pos[0] = new_pos_x
            self.pos[1] = new_pos_y

            if randint(1, 2) == 1:
                self.updateVelocityForExplosion()
            else:
                self.updateVelocityForCircle()

    def updateLast(self):
        self.pos[0] += self.velocity_x
        self.pos[1] += self.velocity_y
        self.alpha -= self.d_alpha

        if self.alpha < self.alpha_end:
            self.alive = False

    def render(self):
        glColor4f(1.0, 1.0, 1.0, self.alpha)
        glVertex3f(self.pos[0], self.pos[1], -2)


class explosionEffect:
    def __init__(
        self,
        texOb,
        starsystem,
        center,
        num_particles,
        pSize,
        d_pSize,
        velocity_max,
        d_velocity,
        alpha_init,
        alpha_end,
        d_alpha,
    ):
        self.alive = True
        self.alreadyInRemoveQueue = False

        self.starsystem = starsystem
        self.texture = texOb.texture
        self.center = center

        self.num_particles = num_particles

        self.particles_list = []
        for i in range(1, num_particles):
            simple_particle = particleForExplosionEffect(
                self.center,
                pSize,
                d_pSize,
                velocity_max,
                d_velocity,
                randint(70, 100) * 0.01,
                alpha_end,
                d_alpha,
                i,
            )
            self.particles_list.append(simple_particle)

    def update(self):
        self.alive = False
        for p in self.particles_list:
            if p.alive == True:
                p.update()
                self.alive = True

        if self.alive == False:
            if self.alreadyInRemoveQueue == False:
                self.starsystem.effect_EXPLOSION_remove_queue.append(self)
                self.alreadyInRemoveQueue = True

    def render(self):
        glBindTexture(GL_TEXTURE_2D, self.texture)
        for p in self.particles_list:
            if p.alive == True:
                glPointSize(p.pSize)

                glBegin(GL_POINTS)
                p.render()
                glEnd()

    def __del__(self):
        del self.particles_list


class particleForExplosionEffect:
    def __init__(
        self,
        center,
        pSize,
        d_pSize,
        velocity_max,
        d_velocity,
        alpha_init,
        alpha_end,
        d_alpha,
        num,
    ):
        self.alive = True

        self.num = num

        self.pos_orig = [center[0], center[1]]
        self.pos = [center[0], center[1]]

        self.alpha_init = alpha_init
        self.alpha_end = alpha_end
        # self.d_alpha = randint(int(10000*d_alpha), int(30000*d_alpha))/float(10000)
        self.d_alpha = d_alpha

        self.alpha = alpha_init
        self.c = 1.0

        self.pSize_init = pSize
        self.d_pSize = d_pSize

        self.pSize = pSize

        self.velocity_max = velocity_max
        self.d_velocity = d_velocity

        if randint(1, 2) == 1:
            self.updateVelocityForExplosion()
        else:
            self.updateVelocityForCircle()

    def updateVelocityForExplosion(self):
        self.dx_n = randint(-10, 10) * 0.1
        self.dy_n = randint(-10, 10) * 0.1

        self.velocity_x = self.dx_n * self.velocity_max
        self.velocity_y = self.dy_n * self.velocity_max

    def updateVelocityForCircle(self):
        _len = randint(50, 100)
        _angle = randint(0, 360) / 57.0

        target_x = self.pos[0] + sin(_angle) * _len
        target_y = self.pos[1] + cos(_angle) * _len

        xl = target_x - self.pos[0]
        yl = target_y - self.pos[1]
        l = _len

        self.dx_n = xl / float(l)
        self.dy_n = yl / float(l)

        self.velocity_x = self.dx_n * self.velocity_max
        self.velocity_y = self.dy_n * self.velocity_max

    def update(self):
        self.pos[0] += self.velocity_x
        self.pos[1] += self.velocity_y
        # self.velocity_x -= self.d_velocity
        # self.velocity_y -= self.d_velocity
        # self.d_alpha  += self.d_alpha/200
        self.alpha -= self.d_alpha
        # self.c -= self.d_alpha/2.0
        self.pSize -= self.d_pSize

        if self.alpha < self.alpha_end or self.pSize < 4:
            self.alpha = 0
            self.alive = False

    def render(self):
        glColor4f(self.c, self.c, self.c, self.alpha)
        glVertex3f(self.pos[0], self.pos[1], -2)


class driveTrailEffect:
    def __init__(
        self, ob, texOb, num_particles, pSize, velocity, alpha_init, alpha_end, d_alpha
    ):
        self.texture = texOb.texture
        self.ob = ob

        self.pos = ob.points.midLeft
        self.target = ob.points.midFarLeft

        self.num_particles = num_particles

        self.pSize = pSize

        self.velocity_orig = velocity
        self.velocity = velocity

        self.delay = (alpha_init - alpha_end) / float(self.num_particles)

        self.particles_list = []
        for i in range(1, num_particles + 1):
            simple_particle = particleForDriveTrailEffect(
                ob, alpha_init, alpha_end, d_alpha, i
            )
            self.particles_list.append(simple_particle)

        self.updateVelocity()
        self.putParticlesToInitPos()

    def updateVelocity(self):
        xl = self.target[0] - self.pos[0]
        yl = self.target[1] - self.pos[1]
        l = sqrt(xl * xl + yl * yl)

        self.dx_n = xl / float(l)
        self.dy_n = yl / float(l)

        self.velocity_x = self.dx_n * self.velocity
        self.velocity_y = self.dy_n * self.velocity

        self.last_angle = self.ob.points.angle

    def putParticlesToInitPos(self):
        i = 0
        while i <= self.num_particles - 1:
            p = self.particles_list[i]
            while p.alpha >= (p.alpha_init - i * self.delay):
                p.update(self.velocity_x, self.velocity_y)
            i += 1

    def update(self):
        if self.ob.points.angle != self.last_angle:
            self.updateVelocity()
            self.last_angle = self.ob.points.angle

        for p in self.particles_list:
            p.update(self.velocity_x, self.velocity_y)

    def render(self):
        glBindTexture(GL_TEXTURE_2D, self.texture)

        glPointSize(self.pSize)

        glBegin(GL_POINTS)
        for p in self.particles_list:
            p.render()
        glEnd()


class particleForDriveTrailEffect:
    def __init__(self, ob, alpha_init, alpha_end, d_alpha, num):
        self.num = num
        self.pos_orig = ob.points.midLeft

        self.pos = [ob.points.midLeft[0], ob.points.midLeft[1]]

        self.alpha_init = alpha_init
        self.alpha_end = alpha_end
        self.d_alpha = d_alpha

        self.alpha = alpha_init

    def update(self, dx, dy):
        self.pos[0] += dx
        self.pos[1] += dy
        self.alpha -= self.d_alpha

        if self.alpha < self.alpha_end:
            self.pos[0] = self.pos_orig[0]
            self.pos[1] = self.pos_orig[1]
            self.alpha = self.alpha_init

    def render(self):
        glColor4f(1.0, 1.0, 1.0, self.alpha)
        glVertex3f(self.pos[0], self.pos[1], -2)


class lazerEffect(CommonInstance):
    def __init__(self, (texture_ID_list, (w, h)), owner, target, particle_texOb, pSize):
        CommonInstance.__init__(self, texture_ID_list, (w, h), fps=10)
        if self.animated == True:
            self.render = self._renderDynamicLineFramesLoop
        else:
            self.render = self._renderDynamicLineFrame

        self.owner = owner
        self.target = target
        self.starsystem = self.owner.starsystem
        self.particle_texOb = particle_texOb
        self.pSize = pSize

        self.existance_time = randint(40, 45)

        if randint(1, 2) == 1:
            self.deltaAngle_radian = 0.0005 * self.target.size
        else:
            self.deltaAngle_radian = -0.0005 * self.target.size

        self.angle_additional_radian = 0

        # NEW!!!
        self.damage_effect = None
        # NEW!!!

        self.updateAngleAndLen()
        self.alreadyInRemoveQueue = False

    def update(self, timer):
        if timer > 0:
            self.updateAngleAndLen()

        if self.existance_time < 0:
            if self.alreadyInRemoveQueue == False:
                self.starsystem.effect_LAZER_remove_queue.append(self)
                self.damage_effect.timeToDie = True
                self.alreadyInRemoveQueue = True

        self.existance_time -= 1

    def updateAngleAndLen(self):
        # performs within game loop
        self.p1 = (self.owner.points.center[0], self.owner.points.center[1])
        self.p2 = (self.target.points.center[0], self.target.points.center[1])

        XL = self.p2[0] - self.p1[0]
        YL = self.p2[1] - self.p1[1]

        self.Len = sqrt((XL * XL) + (YL * YL))

        self.angle_radian = atan2(YL, XL)
        self.angle_radian += self.angle_additional_radian

        self.angle_degree = self.angle_radian * DEGREES_IN_RADIAN
        self.angle_additional_radian += self.deltaAngle_radian

        self.ex = (
            sin(DEGREES_90_IN_RADIAN - self.angle_radian) * self.Len
            + self.owner.points.center[0]
        )
        self.ey = sin(self.angle_radian) * self.Len + self.owner.points.center[1]

        # NEW !!!!
        if self.damage_effect == None:
            ###                                                    texture,             starsystem,      center,  num_particles, pSize,              velocity_max, alpha_init, alpha_end, d_alpha):
            # self.damage_effect = tinyExplosionEffect(self.particle_texOb  self.starsystem, self.p2, 10,             15,                1.5,          1.0,        0.2,       0.05)
            self.damage_effect = tinyExplosionEffect(
                self.particle_texOb,
                self.starsystem,
                self.p2,
                5,
                self.pSize,
                0.5,
                0.7,
                0.2,
                0.1,
            )
            self.starsystem.effect_DAMAGE_list.append(self.damage_effect)

        self.damage_effect.setNewCenter([self.ex, self.ey])

    def _renderDynamicLineFrame(self):
        drawLine(
            self.texture_ID,
            (self.p1[0], self.p1[1], -2),
            self.Len,
            self.angle_degree,
            self.h / 2,
        )

    def _renderDynamicLineFramesLoop(self):
        drawLine(
            self.texture_ID[self._tex_frame],
            (self.p1[0], self.p1[1], -2),
            self.Len,
            self.angle_degree,
            self.h / 2,
        )
        self.updateAnimationFrameLoop()


# def addExplosion(ob):
#### debug
##ob.size = 4 #randint(1, 8)
##print "ob.size = ", ob.size
#### debug

# num_particles = randint(15 * ob.size, 20 * ob.size)
# pSize         = randint(25 * ob.size, 35 * ob.size)

# d_pSize       = randint(60,80) * 0.01
# velocity_max  = randint(13,17) * 0.1
# d_velocity    = 0

# alpha_init    = 1.0
# alpha_end     = 0.0
# d_alpha       = randint(5,8) * 0.001

# pe = explosionEffect(TEXTURE_MANAGER.returnParticleTexObBy_ColorID(RED_COLOR_ID), ob.starsystem, ob.points.center, num_particles, pSize, d_pSize, velocity_max, d_velocity, alpha_init, alpha_end, d_alpha)
# ob.starsystem.effect_EXPLOSION_list.append(pe)


# if ob.size >= 4 and len(ob.starsystem.effect_SHOCKWAVE_list) < 10:
# w, h = VIEW_WIDTH, VIEW_HEIGHT     #x, y,   z,    time, dx, dy,   dz,    dtime
# x, y, z, time, dx, dy, dz, dtime = 10, 1.8, 0.13, 0.0,  0,  0.02, 0.0005, -(0.002 + 0.3 * ob.size * 0.001)     # 10, 1.8, 0.13, 0.0,  0,  0.02, 0.0005, -0.004
# try:
# w = ShockWaveEffect(ob.starsystem, float(ob.points.center[0])/w, float(ob.points.center[1])/h, x, y, z, time, dx, dy, dz, dtime)
# except:
# w = ShockWaveEffect(ob.starsystem, float(ob.rect.centerx)/w, float(ob.rect.centery)/h, x, y, z, time, dx, dy, dz, dtime)

# ob.starsystem.effect_SHOCKWAVE_list.append(w)

# explosion.play()


def addExplosion(ob):
    ### debug
    # ob.size = randint(1, 8)
    # print "ob.size = ", ob.size
    ### debug

    d_pSize = randint(60, 80) * 0.01
    velocity_max = randint(13, 17) * 0.1
    d_velocity = 0

    alpha_init = 1.0
    alpha_end = 0.0
    d_alpha = randint(5, 8) * 0.001

    if ob.size < 4:
        num_particles = randint(10 * ob.size, 15 * ob.size)
        pSize = 25 * ob.size

        pe = explosionEffect(
            TEXTURE_MANAGER.returnParticleTexObBy_ColorID(RED_COLOR_ID),
            ob.starsystem,
            ob.points.center,
            num_particles,
            pSize,
            d_pSize,
            velocity_max,
            d_velocity,
            alpha_init,
            alpha_end,
            d_alpha,
        )
        ob.starsystem.effect_EXPLOSION_list.append(pe)

    elif ob.size >= 4:
        num_particles = 40
        pSize = 25 * ob.size

        pe = explosionEffect(
            TEXTURE_MANAGER.returnParticleTexObBy_ColorID(RED_COLOR_ID),
            ob.starsystem,
            ob.points.center,
            num_particles,
            pSize,
            d_pSize,
            velocity_max,
            d_velocity,
            alpha_init,
            alpha_end,
            d_alpha,
        )
        ob.starsystem.effect_EXPLOSION_list.append(pe)

        num_particles2 = 50
        pSize2 = 25 * (ob.size - 1)
        pe = explosionEffect(
            TEXTURE_MANAGER.returnParticleTexObBy_ColorID(YELLOW_COLOR_ID),
            ob.starsystem,
            ob.points.center,
            num_particles2,
            pSize2,
            d_pSize,
            velocity_max,
            d_velocity,
            alpha_init,
            alpha_end,
            d_alpha,
        )
        ob.starsystem.effect_EXPLOSION_list.append(pe)

        num_particles2 = 100
        pSize2 = 25 * (ob.size - 2)
        pe = explosionEffect(
            TEXTURE_MANAGER.returnParticleTexObBy_ColorID(RED_COLOR_ID),
            ob.starsystem,
            ob.points.center,
            num_particles2,
            pSize2,
            d_pSize,
            velocity_max,
            d_velocity,
            alpha_init,
            alpha_end,
            d_alpha,
        )
        ob.starsystem.effect_EXPLOSION_list.append(pe)

    if ob.size >= 4 and len(ob.starsystem.effect_SHOCKWAVE_list) < 10:
        w, h = VIEW_WIDTH, VIEW_HEIGHT  # x, y,   z,    time, dx, dy,   dz,    dtime
        x, y, z, time, dx, dy, dz, dtime = (
            10,
            1.8,
            0.13,
            0.0,
            0,
            0.02,
            0.0005,
            -(0.002 + 0.3 * ob.size * 0.001),
        )  # 10, 1.8, 0.13, 0.0,  0,  0.02, 0.0005, -0.004
        try:
            w = ShockWaveEffect(
                ob.starsystem,
                float(ob.points.center[0]) / w,
                float(ob.points.center[1]) / h,
                x,
                y,
                z,
                time,
                dx,
                dy,
                dz,
                dtime,
            )
        except:
            w = ShockWaveEffect(
                ob.starsystem,
                float(ob.rect.centerx) / w,
                float(ob.rect.centery) / h,
                x,
                y,
                z,
                time,
                dx,
                dy,
                dz,
                dtime,
            )

        ob.starsystem.effect_SHOCKWAVE_list.append(w)

    explosion.play()
