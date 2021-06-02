# taken from here
# http://www.pygame.org/wiki/OBJFileLoader
# with small modification

import pygame
from OpenGL.GL import *
import os

MAIN_DIR = os.path.split(os.path.abspath(__file__))[0]
from numpy import *


def MTL(local_path, filename):
    contents = {}
    mtl = None

    path = os.path.join(MAIN_DIR, local_path, filename)

    for line in open(path, "r"):
        if line.startswith("#"):
            continue
        values = line.split()
        if not values:
            continue
        if values[0] == "newmtl":
            mtl = contents[values[1]] = {}
        elif mtl is None:
            raise ValueError("mtl file doesn't start with newmtl stmt")
        elif values[0] == "map_Kd":
            # load the texture referred to by this declaration
            mtl[values[0]] = values[1]
            surf = pygame.image.load(local_path + mtl["map_Kd"])
            image = pygame.image.tostring(surf, "RGBA", 1)
            ix, iy = surf.get_rect().size
            texid = mtl["texture_Kd"] = glGenTextures(1)
            glBindTexture(GL_TEXTURE_2D, texid)
            glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR)
            glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)
            glTexImage2D(
                GL_TEXTURE_2D, 0, GL_RGBA, ix, iy, 0, GL_RGBA, GL_UNSIGNED_BYTE, image
            )
        else:
            mtl[values[0]] = map(float, values[1:])
    return contents


class OBJ:
    def __init__(self, local_path, filename, swapyz=False, textured=False):
        """Loads a Wavefront OBJ file. """
        self.vertices = []
        self.normals = []
        self.texcoords = []
        self.faces = []

        material = None
        path = os.path.join(MAIN_DIR, local_path, filename)  # new

        for line in open(path, "r"):
            if line.startswith("#"):
                continue
            values = line.split()
            if not values:
                continue
            if values[0] == "v":
                v = list(map(float, values[1:4]))
                if swapyz:
                    v = v[0], v[2], v[1]
                self.vertices.append(v)
            elif values[0] == "vn":
                v = list(map(float, values[1:4]))
                if swapyz:
                    v = v[0], v[2], v[1]
                self.normals.append(v)
            elif values[0] == "vt":
                self.texcoords.append(map(float, values[1:3]))

            elif values[0] in ("usemtl", "usemat"):
                if textured == True:
                    material = values[1]

            elif values[0] == "mtllib":
                self.mtl = MTL(local_path, values[1])
            elif values[0] == "f":
                face = []
                texcoords = []
                norms = []
                for v in values[1:]:
                    w = v.split("/")
                    face.append(int(w[0]))
                    if len(w) >= 2 and len(w[1]) > 0:
                        texcoords.append(int(w[1]))
                    else:
                        texcoords.append(0)
                    if len(w) >= 3 and len(w[2]) > 0:
                        norms.append(int(w[2]))
                    else:
                        norms.append(0)

                if textured == True:
                    self.faces.append((face, norms, texcoords, material))
                else:
                    self.faces.append((face, norms, texcoords))

        self.gl_list = glGenLists(1)
        glNewList(self.gl_list, GL_COMPILE)
        glFrontFace(GL_CCW)
        for face in self.faces:
            if textured == True:
                vertices, normals, texture_coords, material = face
            else:
                vertices, normals, texture_coords = face

            if textured == True:
                mtl = self.mtl[material]
                self.colors = mtl
                if "texture_Kd" in mtl:
                    ## use diffuse texmap
                    glBindTexture(GL_TEXTURE_2D, mtl["texture_Kd"])
                else:
                    ## just use diffuse colour
                    glColor(*mtl["Kd"])

            glBegin(GL_POLYGON)
            for i in range(len(vertices)):
                if normals[i] > 0:
                    glNormal3fv(self.normals[normals[i] - 1])
                if texture_coords[i] > 0:
                    glTexCoord2fv(self.texcoords[texture_coords[i] - 1])
                glVertex3fv(self.vertices[vertices[i] - 1])
            glEnd()
        glEndList()
