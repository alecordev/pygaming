#   A quick and simple opengl font library that uses GNU freetype2, written
#   and distributed as part of a tutorial for nehe.gamedev.net.
#   Sven Olsen, 2003
#   Translated to PyOpenGL by Brian Leair, 2004


# import freetype
# We are going to use Python Image Library's font handling
# From PIL 1.1.4:
from PIL import ImageFont
from OpenGL.GL import *
from OpenGL.GLU import *


def is_font_available(ft, facename):
    """ Returns true if FreeType can find the requested face name
        Pass the basname of the font e.g. "arial" or "times new roman"
    """
    if facename in ft.available_fonts():
        return True
    return False


def next_p2(num):
    """ If num isn't a power of 2, will return the next higher power of two """
    rval = 1
    while rval < num:
        rval <<= 1
    return rval

    # make_dlist (ft, i, self.m_list_base, self.textures);


def make_dlist(ft, ch, list_base, tex_base_list):
    """ Given an integer char code, build a GL texture into texture_array,
        build a GL display list for display list number display_list_base + ch.
        Populate the glTexture for the integer ch and construct a display
        list that renders the texture for ch.
        Note, that display_list_base and texture_base are supposed
        to be preallocated for 128 consecutive display lists and and
        array of textures.
    """

    # //The first thing we do is get FreeType to render our character
    # //into a bitmap.  This actually requires a couple of FreeType commands:
    # //Load the Glyph for our character.
    # //Move the face's glyph into a Glyph object.
    # //Convert the glyph to a bitmap.
    # //This reference will make accessing the bitmap easier
    # - This is the 2 dimensional Numeric array

    # Use our helper function to get the widths of
    # the bitmap data that we will need in order to create
    # our texture.
    glyph = ft.getmask(chr(ch))
    glyph_width, glyph_height = glyph.size
    # We are using PIL's wrapping for FreeType. As a result, we don't have
    # direct access to glyph.advance or other attributes, so we add a 1 pixel pad.
    width = next_p2(glyph_width + 1)
    height = next_p2(glyph_height + 1)

    # python GL will accept lists of integers or strings, but not Numeric arrays
    # so, we buildup a string for our glyph's texture from the Numeric bitmap

    # Here we fill in the data for the expanded bitmap.
    # Notice that we are using two channel bitmap (one for
    # luminocity and one for alpha), but we assign
    # both luminocity and alpha to the value that we
    # find in the FreeType bitmap.
    # We use the ?: operator so that value which we use
    # will be 0 if we are in the padding zone, and whatever
    # is the the Freetype bitmap otherwise.
    expanded_data = ""
    for j in range(height):
        for i in range(width):
            if (i >= glyph_width) or (j >= glyph_height):
                value = chr(0)
                expanded_data += value
                expanded_data += value
            else:
                value = chr(glyph.getpixel((i, j)))
                expanded_data += value
                expanded_data += value

    # -------------- Build the gl texture ------------

    # Now we just setup some texture paramaters.
    ID = glGenTextures(1)
    tex_base_list[ch] = ID
    glBindTexture(GL_TEXTURE_2D, ID)
    # glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)
    glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR)

    border = 0
    # Here we actually create the texture itself, notice
    # that we are using GL_LUMINANCE_ALPHA to indicate that
    # we are using 2 channel data.
    glTexImage2D(
        GL_TEXTURE_2D,
        0,
        GL_RGBA,
        width,
        height,
        border,
        GL_LUMINANCE_ALPHA,
        GL_UNSIGNED_BYTE,
        expanded_data,
    )

    # With the texture created, we don't need to expanded data anymore
    expanded_data = None

    # --- Build the gl display list that draws the texture for this character ---

    # So now we can create the display list
    glNewList(list_base + ch, GL_COMPILE)

    glBindTexture(GL_TEXTURE_2D, ID)
    glPushMatrix()

    x = float(glyph_width) / float(width)
    y = float(glyph_height) / float(height)

    glBegin(GL_QUADS)

    glTexCoord2f(0, y), glVertex2f(0, 0)
    glTexCoord2f(0, 0), glVertex2f(0, glyph_height)
    glTexCoord2f(x, 0), glVertex2f(glyph_width, glyph_height)
    glTexCoord2f(x, y), glVertex2f(glyph_width, 0)

    glEnd()
    glPopMatrix()

    glTranslatef(glyph_width + 0.75, 0, 0)
    glEndList()


class font_data:
    def __init__(self, facename, pixel_height):
        # We haven't yet allocated textures or display lists
        self.m_allocated = False
        self.m_font_height = pixel_height
        self.m_facename = facename

        # Try to obtain the FreeType font
        try:
            ft = ImageFont.truetype(facename, pixel_height)
        except:
            raise ValueError("Unable to locate true type font '%s'" % (facename))

        # Here we ask opengl to allocate resources for
        # all the textures and displays lists which we
        # are about to create.
        self.m_list_base = glGenLists(128)

        # Consturct a list of 128 elements. This
        # list will be assigned the texture IDs we create for each glyph
        self.textures = [None] * 128

        # This is where we actually create each of the fonts display lists.
        for i in range(128):
            make_dlist(ft, i, self.m_list_base, self.textures)

        self.m_allocated = True
        ft = None

    def glPrint(self, x, y, string):
        glListBase(self.m_list_base)
        modelview_matrix = glGetFloatv(GL_MODELVIEW_MATRIX)

        glPushMatrix()
        glLoadIdentity()
        glTranslatef(x, y, -1)
        glMultMatrixf(modelview_matrix)
        glCallLists(string)
        glPopMatrix()
