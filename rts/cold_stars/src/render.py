from constants import *


def screenQuake(vpCoordinate_x, vpCoordinate_y, amlitudaDiv2):
    vpCoordinate_x = vpCoordinate_x + randint(-amlitudaDiv2, amlitudaDiv2)
    vpCoordinate_y = vpCoordinate_y + randint(-amlitudaDiv2, amlitudaDiv2)
    return vpCoordinate_x, vpCoordinate_y


def drawDynamic(
    texture_ID, x, y, angle, minus_half_w, minus_half_h, plus_half_w, plus_half_h
):
    glBindTexture(GL_TEXTURE_2D, texture_ID)

    glPushMatrix()

    glTranslatef(x, y, 0.0)
    glRotatef(angle, 0.0, 0.0, 1.0)

    glBegin(GL_QUADS)

    glTexCoord3f(0, 0, 0)
    glVertex3f(minus_half_w, minus_half_h, -2)
    glTexCoord3f(1, 0, 0)
    glVertex3f(plus_half_w, minus_half_h, -2)
    glTexCoord3f(1, 1, 0)
    glVertex3f(plus_half_w, plus_half_h, -2)
    glTexCoord3f(0, 1, 0)
    glVertex3f(minus_half_w, plus_half_h, -2)

    glEnd()

    glPopMatrix()


def drawQuadPer2DVertex(bottomLeft, bottomRight, topRight, topLeft, z):
    glBegin(GL_QUADS)

    glTexCoord3f(0, 0, 0)
    glVertex3f(bottomLeft[0], bottomLeft[1], z)
    glTexCoord3f(1, 0, 0)
    glVertex3f(bottomRight[0], bottomRight[1], z)
    glTexCoord3f(1, 1, 0)
    glVertex3f(topRight[0], topRight[1], z)
    glTexCoord3f(0, 1, 0)
    glVertex3f(topLeft[0], topLeft[1], z)

    glEnd()


def drawQuadPer3DVertex(bottomLeft, bottomRight, topRight, topLeft):
    glBegin(GL_QUADS)

    glTexCoord3f(0, 0, 0)
    glVertex3f(bottomLeft[0], bottomLeft[1], bottomLeft[2])
    glTexCoord3f(1, 0, 0)
    glVertex3f(bottomRight[0], bottomRight[1], bottomRight[2])
    glTexCoord3f(1, 1, 0)
    glVertex3f(topRight[0], topRight[1], topRight[2])
    glTexCoord3f(0, 1, 0)
    glVertex3f(topLeft[0], topLeft[1], topLeft[2])

    glEnd()


def drawFullScreenTexturedQuad(tex, w, h, z_pos):
    glBindTexture(GL_TEXTURE_2D, tex)
    drawFullScreenQuad(w, h, z_pos)


def drawFullScreenQuad(w, h, z_pos):
    glBegin(GL_QUADS)

    glTexCoord3f(0, 0, 0)
    glVertex3f(0, 0, z_pos)
    glTexCoord3f(1, 0, 0)
    glVertex3f(w, 0, z_pos)
    glTexCoord3f(1, 1, 0)
    glVertex3f(w, h, z_pos)
    glTexCoord3f(0, 1, 0)
    glVertex3f(0, h, z_pos)

    glEnd()


def drawFullScreenTexturedQuadBlurred(tex, w, h, z_pos, program_blur):
    glUseProgram(program_blur)

    glActiveTexture(GL_TEXTURE0)
    glBindTexture(GL_TEXTURE_2D, tex)

    glUniform1i(glGetUniformLocation(program_blur, "sceneTex"), 0)

    glUniform1f(glGetUniformLocation(program_blur, "rt_w"), 3 * w)
    glUniform1f(glGetUniformLocation(program_blur, "rt_h"), 3 * h)
    glUniform1f(glGetUniformLocation(program_blur, "vx_offset"), 1.0)

    glBindTexture(GL_TEXTURE_2D, tex)
    drawFullScreenQuad(w, h, z_pos)

    glUseProgram(0)


def drawTexturedRect(tex, rect, z_pos):  # z_pos = -1
    glBindTexture(GL_TEXTURE_2D, tex)
    drawRect(rect, z_pos)


def drawRect(rect, z_pos):
    glBegin(GL_QUADS)

    glTexCoord3f(0, 0, 0)
    glVertex3f(rect[0], rect[1], z_pos)
    glTexCoord3f(1, 0, 0)
    glVertex3f(rect[0] + rect[2], rect[1], z_pos)
    glTexCoord3f(1, 1, 0)
    glVertex3f(rect[0] + rect[2], rect[1] + rect[3], z_pos)
    glTexCoord3f(0, 1, 0)
    glVertex3f(rect[0], rect[1] + rect[3], z_pos)

    glEnd()


def drawLine(texture, start_pos_x, start_pos_y, z_pos, len, angle, half_h):
    glBindTexture(GL_TEXTURE_2D, texture)
    glPushMatrix()

    glTranslatef(start_pos_x, start_pos_y, 0.0)
    glRotatef(angle, 0.0, 0.0, 1.0)

    glBegin(GL_QUADS)

    glTexCoord3f(0, 0, 0)
    glVertex3f(0, -half_h, z_pos)
    glTexCoord3f(1, 0, 0)
    glVertex3f(len, -half_h, z_pos)
    glTexCoord3f(1, 1, 0)
    glVertex3f(len, half_h, z_pos)
    glTexCoord3f(0, 1, 0)
    glVertex3f(0, half_h, z_pos)

    glEnd()

    glPopMatrix()


def drawSimpleText(x, y, str):
    COMMON_FONT.glPrint(x, y, str)


def drawSimpleColoredText(x, y, str, color):
    glColor3f(*color)
    COMMON_FONT.glPrint(x, y, str)


def drawDynamicLabelList(tex, x, y, str_list):
    offset = 20
    xOffset = offset
    yOffset = offset

    l = len(str_list)
    b = 1
    bmax = len(str_list[0])
    while b <= len(str_list) - 1:
        if len(str_list[b]) > bmax:
            bmax = len(str_list[b])
        b += 1

    w = bmax * (LETTER_WIDTH + LETTER_WIDTH_empty)
    h = l * (LETTER_HEIGHT + LETTER_HEIGHT_empty)

    glPushMatrix()
    drawTexturedRect(tex, [x, y, w, h], -1.0)
    for str in str_list:
        COMMON_FONT.glPrint(int(x + xOffset), int(y + h - yOffset), str)
        yOffset += offset
    glPopMatrix()


def drawVpCoord(vpCoordinate_x, vpCoordinate_y):
    glLoadIdentity()
    FPS_FONT.glPrint(
        VIEW_WIDTH - 300,
        VIEW_HEIGHT - TEXT_OFFSET,
        "%i:%i" % (vpCoordinate_x, vpCoordinate_y),
    )


def GlListCompileDirection(
    texture_ID, list_x, list_y, list_len, step, pointer_size=DOT_SIZE
):
    GL_LIST_ID = glGenLists(1)

    i = 0
    minus_pointer_size_div_2 = -pointer_size / 2

    glNewList(GL_LIST_ID, GL_COMPILE)
    glBindTexture(GL_TEXTURE_2D, texture_ID)
    while i < list_len:
        glPushMatrix()
        # glTranslatef(list_x[i], list_y[i], 0)
        drawRect([list_x[i], list_y[i], pointer_size, pointer_size], -1.0)
        # draw_quad((minus_pointer_size_div_2, minus_pointer_size_div_2), (pointer_size, pointer_size))
        i += step
        glPopMatrix()
    glEndList()

    return GL_LIST_ID


# def renderObj(obj, (pos_x, pos_y, pos_z), (ax, ay, az), scale):
#    glPushMatrix()

#    glTranslate(pos_x, pos_y, pos_z)
#    glScalef(scale, scale, scale)
#    glRotate(ax, 1, 0, 0)
#    glRotate(ay, 0, 1, 0)
#    glRotate(az, 0, 0, 1)

"""
    # va
    glEnableClientState(GL_VERTEX_ARRAY)         # Enable vertex array
    glEnableClientState(GL_NORMAL_ARRAY)         # Enable normal array
    glEnableClientState(GL_TEXTURE_COORD_ARRAY)  # Enable textcoord array

    glVertexPointerf(obj.vertices)
    glNormalPointerf(obj.normals)
    glTexCoordPointerf(obj.texcoords)
    #glTexCoordPointerf(obj.colors)
    #GL_TRIANGLES
    #GL_POLYGON
    glDrawArrays(GL_TRIANGLES, 0, len(obj.vertices) -1)


    glDisableClientState(GL_VERTEX_ARRAY)        # Disable vertex array
    glDisableClientState(GL_NORMAL_ARRAY)        # Disable normal array
    glDisableClientState(GL_TEXTURE_COORD_ARRAY) # Disable textcoord array
"""
#    glCallList(obj.gl_list)
#    glPopMatrix()
