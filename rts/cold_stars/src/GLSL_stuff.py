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

from ctypes import *
import sys

import pygame
from pygame.locals import *


from OpenGL.GL import *
from OpenGL.GLU import *

from OpenGL.GL.ARB.shader_objects import *
from OpenGL.GL.ARB.vertex_shader import *
from OpenGL.GL.ARB.fragment_shader import *


from OpenGL.arrays import arraydatatype
import OpenGL
from OpenGL.extensions import alternate
import ctypes
from OpenGL.GL.framebufferobjects import *
from OpenGL.GL.EXT.multi_draw_arrays import *
from OpenGL.GL.ARB.imaging import *

import numpy as np
import sys, traceback


from render import (
    drawFullScreenQuad,
    drawFullScreenTexturedQuad,
    drawFullScreenTexturedQuadBlurred,
)


class bloomEffect:
    def __init__(self, w, h, program_blur, program_ExtractBrightAreas, program_Combine):
        self.brightThreshold = 1.9

        self.fbo1_pass0 = FBO(w, h)
        self.fbo2_pass0 = FBO(w / 2, h / 2)
        self.fbo3_pass0 = FBO(w / 4, h / 4)
        self.fbo4_pass0 = FBO(w / 8, h / 8)

        self.fbo1_pass1 = FBO(w, h)
        self.fbo2_pass1 = FBO(w / 2, h / 2)
        self.fbo3_pass1 = FBO(w / 4, h / 4)
        self.fbo4_pass1 = FBO(w / 8, h / 8)

        self.fbo1_pass2 = FBO(w, h)
        self.fbo2_pass2 = FBO(w / 2, h / 2)
        self.fbo3_pass2 = FBO(w / 4, h / 4)
        self.fbo4_pass2 = FBO(w / 8, h / 8)

        self.fbo_preFinal = FBO(w, h)

        self.program_blur = program_blur
        self.program_ExtractBrightAreas = program_ExtractBrightAreas
        self.program_Combine = program_Combine

    def pass0(self, tex, w, h):
        # RENDER TO FBO1
        self.fbo1_pass0.activate()

        # render background
        glUseProgram(self.program_ExtractBrightAreas)
        glActiveTexture(GL_TEXTURE0)
        glBindTexture(GL_TEXTURE_2D, tex)
        glUniform1i(glGetUniformLocation(self.program_ExtractBrightAreas, "source"), 0)

        glUniform1f(
            glGetUniformLocation(self.program_ExtractBrightAreas, "threshold"),
            self.brightThreshold,
        )

        drawFullScreenQuad(w, h, -999.0)
        glUseProgram(0)

        self.fbo1_pass0.deactivate()

        # RENDER TO FBO2
        self.fbo2_pass0.activate()
        drawFullScreenTexturedQuad(self.fbo1_pass0.texture, w / 2, h / 2, -999.0)
        self.fbo2_pass0.deactivate()

        # RENDER TO FBO3
        self.fbo3_pass0.activate()
        drawFullScreenTexturedQuad(self.fbo1_pass0.texture, w / 4, h / 4, -999.0)
        self.fbo3_pass0.deactivate()

        # RENDER TO FBO4
        self.fbo4_pass0.activate()
        drawFullScreenTexturedQuad(self.fbo1_pass0.texture, w / 8, h / 8, -999.0)
        self.fbo4_pass0.deactivate()

    def pass1(self, w, h):
        # RENDER TO FBO1
        self.fbo1_pass1.activate()
        drawFullScreenTexturedQuadBlurred(
            self.fbo1_pass0.texture, w, h, -999.0, self.program_blur
        )
        self.fbo1_pass1.deactivate()

        # RENDER TO FBO2
        self.fbo2_pass1.activate()
        drawFullScreenTexturedQuadBlurred(
            self.fbo2_pass0.texture, w / 2, h / 2, -999.0, self.program_blur
        )
        self.fbo2_pass1.deactivate()

        # RENDER TO FBO3
        self.fbo3_pass1.activate()
        drawFullScreenTexturedQuadBlurred(
            self.fbo3_pass0.texture, w / 4, h / 4, -999.0, self.program_blur
        )
        self.fbo3_pass1.deactivate()

        # RENDER TO FBO4
        self.fbo4_pass1.activate()
        drawFullScreenTexturedQuadBlurred(
            self.fbo4_pass0.texture, w / 8, h / 8, -999.0, self.program_blur
        )
        self.fbo4_pass1.deactivate()

    def pass2(self, w, h):
        # RENDER TO FBO1
        self.fbo1_pass2.activate()
        drawFullScreenTexturedQuadBlurred(
            self.fbo1_pass1.texture, w, h, -999.0, self.program_blur
        )
        self.fbo1_pass2.deactivate()

        # RENDER TO FBO2
        self.fbo2_pass2.activate()
        drawFullScreenTexturedQuadBlurred(
            self.fbo2_pass1.texture, w / 2, h / 2, -999.0, self.program_blur
        )
        self.fbo2_pass2.deactivate()

        # RENDER TO FBO3
        self.fbo3_pass2.activate()
        drawFullScreenTexturedQuadBlurred(
            self.fbo3_pass1.texture, w / 4, h / 4, -999.0, self.program_blur
        )
        self.fbo3_pass2.deactivate()

        # RENDER TO FBO4
        self.fbo4_pass2.activate()
        drawFullScreenTexturedQuadBlurred(
            self.fbo4_pass1.texture, w / 8, h / 8, -999.0, self.program_blur
        )
        self.fbo4_pass2.deactivate()

    def combine(self, tex, w, h):
        # RENDER TO preFinalPostProcess FBO
        self.fbo_preFinal.activate()

        glUseProgram(self.program_Combine)

        glActiveTexture(GL_TEXTURE0)
        glBindTexture(GL_TEXTURE_2D, tex)
        glUniform1i(glGetUniformLocation(self.program_Combine, "Scene"), 0)

        glActiveTexture(GL_TEXTURE1)
        glBindTexture(GL_TEXTURE_2D, self.fbo1_pass0.texture)
        glUniform1i(glGetUniformLocation(self.program_Combine, "Pass0_tex1"), 1)

        glActiveTexture(GL_TEXTURE2)
        glBindTexture(GL_TEXTURE_2D, self.fbo2_pass0.texture)
        glUniform1i(glGetUniformLocation(self.program_Combine, "Pass0_tex2"), 2)

        glActiveTexture(GL_TEXTURE3)
        glBindTexture(GL_TEXTURE_2D, self.fbo3_pass0.texture)
        glUniform1i(glGetUniformLocation(self.program_Combine, "Pass0_tex3"), 3)

        glActiveTexture(GL_TEXTURE4)
        glBindTexture(GL_TEXTURE_2D, self.fbo4_pass0.texture)
        glUniform1i(glGetUniformLocation(self.program_Combine, "Pass0_tex4"), 4)

        glActiveTexture(GL_TEXTURE5)
        glBindTexture(GL_TEXTURE_2D, self.fbo1_pass1.texture)
        glUniform1i(glGetUniformLocation(self.program_Combine, "Pass1_tex1"), 5)

        glActiveTexture(GL_TEXTURE6)
        glBindTexture(GL_TEXTURE_2D, self.fbo2_pass1.texture)
        glUniform1i(glGetUniformLocation(self.program_Combine, "Pass1_tex2"), 6)

        glActiveTexture(GL_TEXTURE7)
        glBindTexture(GL_TEXTURE_2D, self.fbo3_pass1.texture)
        glUniform1i(glGetUniformLocation(self.program_Combine, "Pass1_tex3"), 7)

        glActiveTexture(GL_TEXTURE8)
        glBindTexture(GL_TEXTURE_2D, self.fbo4_pass1.texture)
        glUniform1i(glGetUniformLocation(self.program_Combine, "Pass1_tex4"), 8)

        glActiveTexture(GL_TEXTURE9)
        glBindTexture(GL_TEXTURE_2D, self.fbo1_pass2.texture)
        glUniform1i(glGetUniformLocation(self.program_Combine, "Pass2_tex1"), 9)

        glActiveTexture(GL_TEXTURE10)
        glBindTexture(GL_TEXTURE_2D, self.fbo2_pass2.texture)
        glUniform1i(glGetUniformLocation(self.program_Combine, "Pass2_tex2"), 10)

        glActiveTexture(GL_TEXTURE11)
        glBindTexture(GL_TEXTURE_2D, self.fbo3_pass2.texture)
        glUniform1i(glGetUniformLocation(self.program_Combine, "Pass2_tex3"), 11)

        glActiveTexture(GL_TEXTURE12)
        glBindTexture(GL_TEXTURE_2D, self.fbo4_pass2.texture)
        glUniform1i(glGetUniformLocation(self.program_Combine, "Pass2_tex4"), 12)

        drawFullScreenQuad(w, h, -999.0)

        self.fbo_preFinal.deactivate()


def glLibTestErrors(function):
    try:
        function()
    except Exception as e:
        tb = sys.exc_info()[2]
        traceback.print_exception(e.__class__, e, tb)
        pygame.quit()
        input()
        sys.exit()


def init_globals():
    global glCreateShader, glShaderSource, glCompileShader, glDeleteShader, glCreateProgram
    global glAttachShader, glLinkProgram, glUseProgram, glGetUniformLocation
    glCreateShader = glCreateShaderObjectARB
    glShaderSource = glShaderSourceARB
    glCompileShader = glCompileShaderARB
    glDeleteShader = glDeleteObjectARB
    glCreateProgram = glCreateProgramObjectARB
    glAttachShader = glAttachObjectARB
    glLinkProgram = glLinkProgramARB
    glUseProgram = glUseProgramObjectARB
    glGetUniformLocation = glGetUniformLocation


def compile_shader(source, shader_type):
    shader = glCreateShader(shader_type)
    glShaderSource(shader, [source])
    glCompileShader(shader)

    return shader


def compile_program(vertex_source, fragment_source):
    vertex_shader = None
    fragment_shader = None

    try:
        program = glCreateProgram()
    except:
        program = None

    if program != None:
        if vertex_source:
            vertex_shader = compile_shader(vertex_source, GL_VERTEX_SHADER)
            glAttachShader(program, vertex_shader)
        if fragment_source:
            fragment_shader = compile_shader(fragment_source, GL_FRAGMENT_SHADER)
            glAttachShader(program, fragment_shader)

        glLinkProgram(program)

        if vertex_shader:
            glDeleteShader(vertex_shader)
        if fragment_shader:
            glDeleteShader(fragment_shader)

    return program


def print_log(program):
    errors = glGetInfoLogARB(program)
    print(errors)


class ShockWaveEffect:
    def __init__(
        self, starsystem, center_x, center_y, x, y, z, time, dx, dy, dz, dtime
    ):
        self.alive = True
        self.alreadyInRemoveQueue = False

        self.starsystem = starsystem
        self.center = [center_x, center_y]

        self.x, self.y, self.z, self.time = x, y, z, time
        self.dx, self.dy, self.dz, self.dtime = dx, dy, dz, dtime

    def update(self):
        self.x -= self.dx

        if self.y > 0:
            self.y -= self.dy
        else:
            self.alive = False

        self.z -= self.dz
        self.time -= self.dtime

        if self.alive == False:
            if self.alreadyInRemoveQueue == False:
                self.starsystem.effect_SHOCKWAVE_remove_queue.append(self)
                self.alreadyInRemoveQueue = True


def returnShockWavesDataInArrays(effect_list, vpCoordinate_x, vpCoordinate_y):
    center_list = []
    xyz_list = []
    time_list = []

    for e in effect_list:
        center_list.append(
            (
                e.center[0] - float(vpCoordinate_x) / VIEW_WIDTH,
                e.center[1] - float(vpCoordinate_y) / VIEW_HEIGHT,
            )
        )
        xyz_list.append((e.x, e.y, e.z))
        time_list.append(e.time)

    return (
        np.array(center_list, dtype=np.float32),
        np.array(xyz_list, dtype=np.float32),
        np.array(time_list, dtype=np.float32),
    )

    # http://www.flashbang.se/archives/48
    # HDR http://prideout.net/archive/bloom/


class FBO:
    def __init__(self, width, height):
        # create a color texture
        self.texture = glGenTextures(1)
        glBindTexture(GL_TEXTURE_2D, self.texture)
        glTexImage2D(
            GL_TEXTURE_2D, 0, GL_RGBA, width, height, 0, GL_RGBA, GL_INT, None
        )  # no data transferred
        # glTexImage2D(GL_TEXTURE_2D, 0, GL_RGBA8,  width, height, 0, GL_RGBA16F_ARB, GL_INT, None) # no data transferred

        glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)
        glBindTexture(GL_TEXTURE_2D, 0)

        # create depth renderbuffer
        self.depthbuffer = glGenRenderbuffers(1)
        glBindRenderbufferEXT(GL_RENDERBUFFER_EXT, self.depthbuffer)
        glRenderbufferStorageEXT(
            GL_RENDERBUFFER_EXT, GL_DEPTH_COMPONENT24, width, height
        )

        # create FBO
        self.fbo = glGenFramebuffers(1)
        glBindFramebuffer(
            GL_FRAMEBUFFER, self.fbo
        )  # switch to our fbo so we can bind stuff to it
        glFramebufferTexture2DEXT(
            GL_FRAMEBUFFER_EXT, GL_COLOR_ATTACHMENT0_EXT, GL_TEXTURE_2D, self.texture, 0
        )
        glFramebufferRenderbufferEXT(
            GL_FRAMEBUFFER_EXT, GL_DEPTH_ATTACHMENT, GL_RENDERBUFFER, self.depthbuffer
        )

        # Go back to regular frame buffer rendering
        glBindFramebufferEXT(GL_FRAMEBUFFER_EXT, 0)

    def activate(self):
        glBindTexture(GL_TEXTURE_2D, 0)  # unbind texture
        glBindFramebuffer(GL_FRAMEBUFFER, self.fbo)  # bind fbo

        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        glLoadIdentity()

        glPushAttrib(GL_VIEWPORT_BIT)  # viewport is shared with the main context
        glViewport(0, 0, VIEW_WIDTH, VIEW_HEIGHT)

    def deactivate(self):
        glActiveTexture(GL_TEXTURE0)  # debug
        glPopAttrib()  # restore viewport
