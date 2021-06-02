import Blender, math, types
from Blender import Material, NMesh, Noise, Object, Scene, Window


# ====== constants
invNorQ = (2 * math.pi) ** 0.5  # inverse of normal sigma=1 mu=1 quofficient
norQ = 1.0 / invNorQ  # actual quofficient
G = 6.67 * 10 ** -11  # universal gravitational constant


# ====== probability distributons
def Normal(x):
    """
        This is the actual normal distribution
    """
    global norQ
    return norQ * math.exp(-x * x / 2.0)


# ====== distance calculation
def distance(p1, p2):
    return (
        (p1[0] - p2[0]) * (p1[0] - p2[0])
        + (p1[1] - p2[1]) * (p1[1] - p2[1])
        + (p1[2] - p2[2]) * (p1[2] - p2[2])
    ) ** 0.5


# ====== nebulae creation+evolution functions
def add(a, b):
    return a + b


def Evolve(mesh, speeds, evolutions):
    """
        This function uses vectorial gravity to evolve the system
        through mutual attraction between particles iteratively:

                    G m1 m2 (^v1-^v2) / |^v1-^v2|**3

        However, we'll assign a sufficiently large enough mass to
        each point that will cause the system to evolve quickly

        G = 6.67x10**-11, factoring it out from the equation
        makes every particle extremely heavy, and being there
        no friction, it makes'em move pretty fast. Assuming that the
        mass of each particle is G**(-1/2), the final equation is:

                    ^v1 - ^v2 / |^v1 - ^v2| ** 3

        In the future, this may use a search-optimized kD tree, but
        the brute force method will have to do for now.
    """
    for e in range(evolutions):
        for i in range(len(mesh)):
            accel = (0, 0, 0)
            for j in range(len(mesh)):
                speeds[i] = map(add, [0.5 * coord for coord in accel], speeds[i])
                dist = distance(mesh[j], mesh[i])
                dist3 = dist * dist * dist
                # gravec     = map(add,


def MakeNebula(maxD, totalPoints=100, evolveIter=10):
    """
        We use a voronoi distance to displace the point and
        use normalized multiplicative turbulence to generate unique,
        sort of wispy, uniformly distributed points.
        Then we evolve the system using gravity.
    """
    pointsPerDimension = totalPoints ** (1.0 / 3.0)
    # prepare randomization
    Noise.setRandomSeed(0)
    # create object and mesh
    meshObj = Object.New("Mesh", "Nebula")
    mesh = NMesh.New("Nebula.mesh")
    meshObj.link(mesh)
    # add random vertexes
    step, cnt = float(maxD + 0.01) / pointsPerDimension, 0
    speeds = []
    x = -maxD / 2
    while x < maxD / 2:
        y = -maxD / 2
        while y < maxD / 2:
            z = -maxD / 2
            while z < maxD / 2:
                cnt += 1
                xt, yt, zt = [
                    Normal(coord) for coord in Noise.vTurbulence((x, y, x,), 1, 1)
                ]
                xv, yv, zv = [coord + 0.5 for coord in Noise.voronoi((x, y, z,))[1][2]]
                xf, yf, zf = xv * xt, yv * yt, zv * zt
                speeds.append((xt, yt, zt,))
                mesh.verts.append(NMesh.Vert(xf, yf, zf))
                mesh.update()
                z += step
            y += step
        Window.DrawProgressBar(0.25, "Adding points")
        x += step
    # once created, evolve them
    Evolve(mesh.verts, speeds, evolveIter)
    # mat            =   Material.New("Nebula.mat")
    # mat.mode   =   Material.Modes["HALO"]      | Material.Modes["ZTRANSP"]     \
    #           |   Material.Modes["TRACEABLE"] | Material.Modes["HALOSHADE"]   \
    #           |   Material.Modes["SHADOW"]    | Material.Modes["VCOL_PAINT"]
    # mat.alpha      = 0.0625
    # mat.add            = 0.25
    # mat.haloSize   = step*3.5
    # and put it in current scene
    Scene.GetCurrent().link(meshObj)


# MakeNebula(20, 5000)
print Vector(3, 2, 1) + Vector(1, 2, 3)
