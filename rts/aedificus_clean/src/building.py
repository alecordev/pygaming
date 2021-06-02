# AEDIFICUS: FATHERS OF ROME
# by Adam Binks   www.github.com/jellyberg/Aedificus---Fathers_of_Rome
# Read the devblog on Tumblr: bit.ly/Aedificus

import pygame, my, math, mob, ui, shadow, item, sound


def loadImg(buildingName):
    """Just to save copy pasting in my.BUILDINGSTATS"""
    return pygame.image.load(
        "assets/buildings/" + buildingName + ".png"
    ).convert_alpha()


my.BUILDINGNAMES = [
    "hut",
    "shed",
    "orchard",
    "fishing boat",
    "fish mongers",
    "pool",
    "blacksmith",
    "town hall",
]
my.BUILDINGSTATS = {}
my.BUILDINGSTATS["hut"] = {
    "description": "A new citizen is born when built.",
    "buildTime": 3000,
    "buildMaterials": {"wood": 25},
    "img": loadImg("hut"),
}
my.BUILDINGSTATS["shed"] = {
    "description": "Store all sorts of goods here.",
    "buildTime": 6000,
    "buildMaterials": {"wood": 75},
    "img": loadImg("shed"),
}
my.BUILDINGSTATS["orchard"] = {
    "description": "Feeds up to 5 nearby citizens at once.",
    "buildTime": 3000,
    "buildMaterials": {"wood": 150},
    "img": loadImg("orchard"),
}
my.BUILDINGSTATS["fishing boat"] = {
    "description": "Fishermen fish fish here. Duh.",
    "buildTime": 5000,
    "buildMaterials": {"wood": 100},
    "img": loadImg("fishingBoat"),
}
my.BUILDINGSTATS["fish mongers"] = {
    "description": "Feeds up to 9 nearby citizens when fish is brought here.",
    "buildTime": 4000,
    "buildMaterials": {"wood": 150},
    "img": loadImg("fishMongers"),
}
my.BUILDINGSTATS["pool"] = {
    "description": "UNDER DEVELOPMENT.",
    "buildTime": 5000,
    "buildMaterials": {"wood": 100, "iron": 10},
    "img": loadImg("pool"),
}
my.BUILDINGSTATS["blacksmith"] = {
    "description": "A blacksmith refines ores into building materials and metal based items here.",
    "buildTime": 8000,
    "buildMaterials": {"wood": 200},
    "img": loadImg("blacksmith"),
}
my.BUILDINGSTATS["town hall"] = {
    "description": "Control town legislation and all that jazz. UNDER DEVELOPMENT",
    "buildTime": 15000,
    "buildMaterials": {"wood": 500, "iron": 30},
    "img": loadImg("townHall"),
}

my.allBuildings = pygame.sprite.Group()
my.builtBuildings = pygame.sprite.Group()
my.buildingBeingPlaced = pygame.sprite.GroupSingle()
my.buildingsUnderConstruction = pygame.sprite.Group()
my.demolishedBuildings = pygame.sprite.Group()

my.foodBuildings = pygame.sprite.Group()
my.foodBuildingsWithSpace = pygame.sprite.Group()
my.storageBuildings = pygame.sprite.Group()
my.storageBuildingsWithSpace = pygame.sprite.Group()

my.townHall = pygame.sprite.GroupSingle()
my.huts = pygame.sprite.Group()
my.sheds = pygame.sprite.Group()
my.orchards = pygame.sprite.Group()
my.fishingBoats = pygame.sprite.Group()
my.fishMongers = pygame.sprite.Group()
my.pools = pygame.sprite.Group()
my.blacksmiths = pygame.sprite.Group()
my.blacksmithsWithSpace = pygame.sprite.Group()

cross = pygame.image.load(
    "assets/ui/cross.png"
).convert_alpha()  # indicates invalid construction site
unscaledConstructionImg = pygame.image.load(
    "assets/buildings/underConstruction.png"
).convert_alpha()

my.unlockedBuildings = my.STARTUNLOCKEDBUILDINGS[:]


def updateBuildings(dt):
    """To keep logic.update() nice and tidy"""
    if my.input.mousePressed == 3:  # right click
        my.buildingBeingPlaced.empty()
        my.mode = "look"
    for building in my.builtBuildings.sprites():
        building.handleShadow()
    my.allBuildings.update(dt)
    if my.buildingBeingPlaced:
        my.buildingBeingPlaced.update(dt)
        ui.UItip(
            (my.hud.minimap.rect.left - 100, my.hud.minimap.rect.bottom - 35),
            "Left click to place, right click to cancel",
        )

    # if there are no builders and an unconstructed building, alert the player via a UItip
    if my.buildingsUnderConstruction:
        unconstructedSite = None
        for site in my.buildingsUnderConstruction.sprites():
            if site.buildProgress == 0:
                unconstructedSite = site.name
        if unconstructedSite:
            if not mob.checkForOccupation("builder"):
                ui.UItip(
                    (
                        my.hud.occupationAssigner.rect.left - 5,
                        my.hud.occupationAssigner.rect.top + 40,
                    ),
                    "You need a builder to build your %s" % (unconstructedSite),
                )


def findBuildingAtCoord(coord):
    if coord not in ["grass", "stone", "tree", "coal", "iron", "gold"]:
        for site in my.allBuildings:
            if coord in site.allCoords:
                return site
        for buildSite in my.buildingsUnderConstruction:
            if coord in buildSite.allCoords:
                return buildSite


class Building(pygame.sprite.Sprite):
    """Base class for buildings with basic functions"""

    def __init__(self, name, size, stats, AOEsize=None, displayShadow=True):
        """
		buildCost {'material1': amount1, 'material2': amount2} ad infinity
		buildTime is actually amount of production needed to construct
		AOEsize is number of cells from centre the area of effect should cover
		"""
        pygame.sprite.Sprite.__init__(self)
        self.name, self.buildingImage = name, stats["img"]
        self.buildCost, self.totalBuildProgress, self.displayShadow = (
            stats["buildMaterials"],
            stats["buildTime"],
            displayShadow,
        )
        self.buildProgress = 0
        self.xsize, self.ysize = size
        self.add(my.buildingBeingPlaced)
        self.scaledCross = pygame.transform.scale(
            cross, (self.xsize * my.CELLSIZE, self.ysize * my.CELLSIZE)
        )
        self.constructionImg = pygame.transform.scale(
            unscaledConstructionImg,
            (self.xsize * my.CELLSIZE, self.ysize * my.CELLSIZE),
        )
        self.allCoords = []
        if AOEsize:
            self.AOE = True
            self.AOEsize = AOEsize
        else:
            self.AOE = False
        self.buildableTerrain = "grass"
        self.menu = None  # created in the building's onPlace() function
        self.orders = []

    def addToMapFile(self, topleftcell):
        """For every (x, y) of my.map.map the building occupies, make my.map.map[x][y] = self.name"""
        leftx, topy = topleftcell
        self.rect = pygame.Rect(
            (leftx * my.CELLSIZE, topy * my.CELLSIZE),
            (self.xsize * my.CELLSIZE, self.ysize * my.CELLSIZE),
        )
        for x in range(self.xsize):
            for y in range(self.ysize):
                my.map.map[leftx + x][topy + y] = self.name
        my.map.genSurf()

    def updateBasic(self):
        """To be called in a specialised building's self.update() function"""
        if my.buildingBeingPlaced.has(self):
            self.placeMode()
        else:
            self.construct()
            if my.builtBuildings.has(self):
                if self.AOE:
                    self.updateAOE()
                    if self.rect.collidepoint(my.input.hoveredPixel):
                        self.drawAOE()
            self.blit()

    def placeMode(self):
        """Show ghost building on hover"""
        my.mode = "build"
        if my.input.hoveredCell:
            hoveredPixels = my.map.cellsToPixels(my.input.hoveredCell)
            my.surf.blit(self.buildingImage, hoveredPixels)
            if not self.canPlace(my.input.hoveredCell):
                my.surf.blit(self.scaledCross, hoveredPixels)
            if my.input.mouseUnpressed == 1:
                if self.canPlace(my.input.hoveredCell):
                    self.place()
                else:
                    sound.play("error", 0.8, 1)

    def place(self):
        """Place the building on the map"""
        self.coords = my.input.hoveredCell
        self.addToMapFile(my.input.hoveredCell)
        self.remove(my.buildingBeingPlaced)
        self.add(my.buildingsUnderConstruction)
        self.add(my.allBuildings)
        for key in self.buildCost.keys():
            item.spendResource(key, self.buildCost[key])

        self.buildersPositions = []
        for x in range(self.xsize):
            row = []
            for y in range(self.ysize):
                row.append(None)
            self.buildersPositions.append(row)

        self.buildersPositionsCoords = []
        for x in range(self.xsize):
            row = []
            for y in range(self.ysize):
                row.append((0, 0))
            self.buildersPositionsCoords.append(row)
        myx, myy = self.coords
        for x in range(self.xsize):
            for y in range(self.ysize):
                self.buildersPositionsCoords[x][y] = (myx + x, myy + y)

        leftx, topy = self.coords
        for x in range(leftx, self.xsize + leftx):
            for y in range(topy, self.ysize + topy):
                self.allCoords.append((x, y))
        my.mode = "look"

        if self.AOE:
            self.initAOE(self.AOEsize)
        self.initTooltip()

        if my.camera.isVisible(self.rect):
            if self.buildableTerrain == "water":
                sound.play("splash")
            else:
                sound.play("thud")

    def canPlace(self, topLeftCoord):
        """Check if the building can be placed if its top left is at topLeftCoord"""
        leftx, topy = topLeftCoord
        if leftx + self.xsize >= my.MAPXCELLS or topy + self.ysize >= my.MAPYCELLS:
            return False
        for x in range(leftx, leftx + self.xsize):
            for y in range(topy, topy + self.ysize):
                if my.map.cellType((x, y)) not in self.buildableTerrain:
                    return False
        for key in self.buildCost.keys():
            if self.buildCost[key] > my.resources[key]:
                return False
        return True

    def construct(self):
        if my.buildingsUnderConstruction.has(self):
            if self.buildProgress > self.totalBuildProgress:
                my.buildingsUnderConstruction.remove(self)
                my.builtBuildings.add(self)
                self.image = self.buildingImage
                self.onPlace()
                self.shadow = shadow.Shadow(self, self.buildingImage)
                if self.menu:
                    self.tooltip.rect.x += self.menu.rect.width
                return
            else:
                progress = self.buildProgress / self.totalBuildProgress
                height = int(progress * self.buildingImage.get_height())
                progressRect = pygame.Rect(
                    (0, self.buildingImage.get_height() - height),
                    (self.buildingImage.get_width(), height),
                )
                self.image = self.constructionImg
                self.image.blit(self.buildingImage, progressRect.topleft, progressRect)

    def demolish(self):
        """Destroys the building, removing it from the map"""
        try:
            self.onDestroy()  # remove reservations etc if need be
            self.menu.kill()
        except:
            pass
        for coord in self.allCoords:
            x, y = coord
            my.map.map[x][y] = self.buildableTerrain
            my.map.genSurf()
            self.kill()
            self.add(my.demolishedBuildings)

    def blit(self):
        if my.camera.isVisible(self.rect):
            my.surf.blit(self.image, self.rect)

    def initAOE(self, AOEsize):
        """Creates an area of effect which extends xdist and ydist from building's centre"""
        leftx, topy = self.coords
        xdist, ydist = AOEsize
        centrex, centrey = (
            leftx + int(math.ceil(self.xsize / 2)),
            topy + int(math.ceil(self.ysize / 2)),
        )
        self.AOEcoords = []
        for x in range(centrex - xdist, centrex + xdist):
            for y in range(centrey - ydist, centrey + ydist):
                self.AOEcoords.append((x, y))
        self.AOEmobsAffected = pygame.sprite.Group()
        self.AOEhumansAffected = pygame.sprite.Group()
        self.AOEbuildingsAffected = pygame.sprite.Group()
        self.AOEsurf = pygame.Surface(
            (xdist * my.CELLSIZE * 2, ydist * my.CELLSIZE * 2)
        )
        self.AOEsurf.fill(my.YELLOW)
        self.AOEsurf.set_alpha(100)

    def updateAOE(self):
        """Updates the groups of mobs and buildings in the AOE"""
        for nearbyMob in my.allMobs.sprites():
            if nearbyMob.coords in self.AOEcoords:
                self.AOEmobsAffected.add(nearbyMob)
                if my.allHumans.has(nearbyMob):
                    self.AOEhumansAffected.add(nearbyMob)
            elif self.AOEmobsAffected.has(nearbyMob):
                self.AOEmobsAffected.remove(nearbyMob)
                if my.allHumans.has(nearbyMob):
                    self.AOEhumansAffected.remove(nearbyMob)
        done = False
        for building in my.builtBuildings.sprites():
            for coord in building.allCoords:
                if coord in self.AOEcoords:
                    self.AOEbuildingsAffected.add(building)
                    done = True
                if done:
                    break
            if not done and self.AOEbuildingsAffected.has(building):
                self.AOEbuildingsAffected.remove(building)

    def drawAOE(self):
        my.surf.blit(self.AOEsurf, my.map.cellsToPixels(self.AOEcoords[0]))

    def initTooltip(self):
        """Initialises a tooltip that appears when the mob is hovered"""
        tooltipPos = (self.rect.right + ui.GAP, self.rect.top)
        self.tooltip = ui.Tooltip(
            "This " + self.name + " is under construction", tooltipPos
        )
        self.tooltip.topleft = tooltipPos

    def handleTooltip(self):
        """Updates a tooltip that appears when the mob is hovered"""
        self.tooltip.simulate(self.rect.collidepoint(my.input.hoveredPixel), True)

    def handleShadow(self):
        """Draw the shadow to my.surf"""
        if self.displayShadow:
            self.shadow.draw(my.surf, my.sunPos)


class FoodBuilding(Building):
    """Base class for food buildings"""

    def __init__(self, name, size, stats, AOEsize, feedSpeed, maxCustomers):
        Building.__init__(self, name, size, stats, AOEsize)
        self.feedSpeed, self.maxCustomers = feedSpeed, maxCustomers

    def updateFood(self, dt):
        """Update self.currentCustomers and feed those in it. Update my.foodBuildingsWithSpace too."""
        if my.builtBuildings.has(self):
            self.currentCustomers = pygame.sprite.Group()
            # keep feeding previous customers
            for customer in self.lastCustomers.sprites():
                if (
                    customer in self.AOEhumansAffected.sprites()
                    and customer.hunger < my.FULLMARGIN
                    and customer.intention == "find food"
                ):
                    self.feedCustomer(customer, dt)
            # if there's still space, feed any new customers
            for customer in self.AOEhumansAffected.sprites():
                if (
                    customer.hunger < my.FULLMARGIN
                    and customer.intention == "find food"
                    and len(self.currentCustomers) < self.maxCustomers
                    and customer not in self.currentCustomers
                ):
                    self.feedCustomer(customer, dt)
            self.tooltip.text = "%s/%s customers being fed at this %s" % (
                len(self.currentCustomers),
                self.maxCustomers,
                self.name,
            )
            if len(self.currentCustomers) >= self.maxCustomers:
                self.remove(my.foodBuildingsWithSpace)
            else:
                self.add(my.foodBuildingsWithSpace)
            for (
                customer
            ) in self.AOEhumansAffected:  # reset none eating customers thoughts
                if (
                    customer.thought == "eating"
                    and customer not in self.currentCustomers
                ):
                    customer.thought = None
            self.lastCustomers = self.currentCustomers.copy()

    def onPlaceFood(self):
        self.add(my.foodBuildings)
        self.add(my.foodBuildingsWithSpace)
        self.currentCustomers = pygame.sprite.Group()
        self.lastCustomers = self.currentCustomers.copy()

    def feedCustomer(self, customer, dt):
        """Feeds the customer, adds them to self.currentCustomers"""
        customer.hunger += self.feedSpeed * dt
        customer.thought = "eating"
        customer.thoughtIsUrgent = False
        self.currentCustomers.add(customer)


class StorageBuilding(Building):
    """Base class for storage buildings"""

    def __init__(self, name, size, stats, storageCapacity, withSpaceGroup):
        Building.__init__(self, name, size, stats)
        self.storageCapacity = storageCapacity
        self.withSpaceGroup = withSpaceGroup
        self.stored = {}
        for resource in my.resources.keys():
            self.stored[resource] = 0
        self.totalStored = 0

    def onPlaceStorage(self):
        self.add(my.storageBuildings)

    def updateStorage(self):
        """Updates the sprite's tooltip and the groups it is in"""
        self.totalStored = 0
        for resourceAmount in self.stored.values():
            self.totalStored += resourceAmount
        text = "This %s contains: " % (self.name)
        for resource in my.RESOURCENAMEORDER:
            if self.stored[resource]:
                text += "%s %s " % (self.stored[resource], resource)
        if text == "This %s contains: " % (self.name):  # no resources
            text = "This %s is empty" % (self.name)
        self.tooltip.text = "%s. %s/%s storage crates are full." % (
            text,
            self.totalStored,
            self.storageCapacity,
        )
        if self.totalStored >= self.storageCapacity and self.withSpaceGroup.has(self):
            self.remove(self.withSpaceGroup)
        elif self.totalStored < self.storageCapacity and not self.withSpaceGroup.has(
            self
        ):
            self.withSpaceGroup.add(self)

    def storeResource(self, resource, quantity):
        """Store a resource in this building, also adds to global quantity of that resource"""
        if self.totalStored + quantity < self.storageCapacity:
            self.stored[resource] += quantity
            my.resources[resource] += quantity

    def removeResource(self, resource, quantity):
        """
		Extract a resource from this building, also subtracts from global quantity of that resource.
		If trying to remove more of the resource than is available, remove as much as possible then
		return what it couldn't remove.
		"""
        self.stored[resource] -= quantity
        my.resources[resource] -= quantity
        if self.stored[resource] < 0:
            excess = -self.stored[resource]
            self.stored[resource] = 0
            my.resources[resource] += excess
            return excess


# MMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMM
# MMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMM    BUILDINGS    MMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMM
# MMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMM


class Hut(Building):
    """Spawns a human when placed"""

    def __init__(self):
        Building.__init__(self, "hut", (2, 2), my.BUILDINGSTATS["hut"])
        self.add(my.huts)

    def update(self, dt):
        self.updateBasic()

    def onPlace(self):
        x, y = self.coords
        newHuman = mob.Human((x, y + 1))
        newHuman.destination = (x - 1, y + 2)
        self.humansName = newHuman.name
        self.tooltip.text = "The home of " + self.humansName


class Shed(StorageBuilding):
    """Basic storage building, stores any item without a special storage place."""

    my.shedHasBeenPlaced = False

    def __init__(self):
        StorageBuilding.__init__(
            self,
            "shed",
            (3, 3),
            my.BUILDINGSTATS["shed"],
            500,
            my.storageBuildingsWithSpace,
        )
        self.add(my.sheds)

    def update(self, dt):
        if my.builtBuildings.has(self):
            self.updateStorage()
        self.updateBasic()

    def onPlace(self):
        self.onPlaceStorage()
        my.shedHasBeenPlaced = True


class Orchard(FoodBuilding):
    """Basic food place"""

    my.orchardHasBeenPlaced = False

    def __init__(self):
        FoodBuilding.__init__(
            self, "orchard", (4, 2), my.BUILDINGSTATS["orchard"], (3, 2), 100, 5
        )

    def onPlace(self):
        my.orchardHasBeenPlaced = True
        self.onPlaceFood()

    def update(self, dt):
        self.updateBasic()
        if my.builtBuildings.has(self):
            self.updateFood(dt)


class FishingBoat(Building):
    def __init__(self):
        Building.__init__(self, "fishingBoat", (2, 1), my.BUILDINGSTATS["fishing boat"])
        self.buildableTerrain = "water"

    def onPlace(self):
        self.seats = {}  # to allow reservations and destinations for fishermen
        x, y = self.coords
        for offsetx in range(2):
            self.seats[(x + offsetx, y)] = None
        self.add(my.fishingBoats)

    def update(self, dt):
        self.updateBasic()
        if my.builtBuildings.has(self):
            self.tooltip.text = "Fishing boat"


class FishMongers(FoodBuilding):
    """Fish() are taken here, then can be eaten"""

    def __init__(self):
        FoodBuilding.__init__(
            self,
            "fishMongers",
            (2, 2),
            my.BUILDINGSTATS["fish mongers"],
            (3, 2),
            315,
            9,
        )

    def onPlace(self):
        self.onPlaceFood()
        self.remove(my.foodBuildingsWithSpace)
        self.add(my.fishMongers)
        self.currentCustomers = pygame.sprite.Group()
        self.totalStored = 0
        self.storageCapacity = 500

    def update(self, dt):
        """If has fish, act like a food building. Else, do nowt."""
        self.updateBasic()
        if my.builtBuildings.has(self):
            if self.totalStored > 0:
                self.updateFood(dt)
                self.totalStored -= len(self.currentCustomers) * my.FISHCONSUMEDPERTICK
                self.tooltip.text = (
                    "%s/%s customers being fed at this %s. It contains %s/%s fish."
                    % (
                        len(self.currentCustomers),
                        self.maxCustomers,
                        self.name,
                        int(self.totalStored),
                        self.storageCapacity,
                    )
                )
            else:
                self.remove(my.foodBuildingsWithSpace)
                self.tooltip.text = "This fishmongers has no fish!"
                self.currentCustomers = None
                for (
                    customer
                ) in self.AOEhumansAffected:  # reset none eating customers thoughts
                    if customer.thought == "eating":
                        customer.thought = None

    def storeResource(self, resource, quantity):
        """Add Fish().quantity to self.fish."""
        assert (
            resource == "fish"
        ), "Serf is storing item other than fish in a fishmonger. Stupid serf."
        self.totalStored += quantity


class Pool(Building):
    """Splish splash"""

    def __init__(self):
        Building.__init__(self, "pool", (3, 2), my.BUILDINGSTATS["pool"])
        self.add(my.pools)
        self.displayShadow = False

    def update(self, dt):
        self.updateBasic()

    def onPlace(self):
        pass


class Blacksmith(StorageBuilding):
    my.blacksmithHasBeenPlaced = False

    def __init__(self):
        StorageBuilding.__init__(
            self,
            "blacksmith",
            (4, 4),
            my.BUILDINGSTATS["blacksmith"],
            20,
            my.blacksmithsWithSpace,
        )

    def update(self, dt):
        self.updateBasic()
        if my.builtBuildings.has(self):
            self.updateStorage()
            if self.orders == []:
                self.reserved = None
            if self.reserved and self.reserved.coords == self.smithCoords:
                smithAnim = False
                for order in self.orders:
                    lastProgress = order.constructionProgress
                    order.update(self, dt)
                    if order.constructionProgress > lastProgress:
                        smithAnim = True
                        if my.camera.isVisible(self.rect) and self.rect.collidepoint(
                            my.input.hoveredPixel
                        ):
                            order.inProgressImgRect.center = self.rect.center
                            my.surf.blit(order.inProgressImg, order.inProgressImgRect)
                            self.tooltip.text += ", constructing a %s (%s/%s)" % (
                                order.name,
                                order.constructionProgress,
                                order.constructionTicks,
                            )
                        break  # if constructing an order, just construct that one
                if smithAnim:
                    self.reserved.animation = mob.Human.smithAnim
                elif self.reserved.animation == mob.Human.smithAnim:
                    self.reserved.animation = self.reserved.idleAnim
                    self.reserved.animFrame = 0

    def onPlace(self):
        self.add(my.blacksmiths)
        self.onPlaceStorage()
        orderMenuList = []
        orderMenuList.append(item.Order("sword", {"iron": 2, "coal": 1}, self, 200, 1))
        orderMenuList.append(item.Order("ingot", {"iron": 2, "coal": 2}, self, 250, 1))
        orderMenuList.append(item.Order("standard", {"gold": 3}, self, 300, 1))
        self.menu = ui.BuildingMenu(
            self,
            orderMenuList,
            [
                "Sword: your swordsmen will use this in battle",
                "Ingot: a common construction component",
                "Standard: a fine looking standard bearing an eagle",
            ],
        )
        self.reserved = None
        leftx, topy = self.coords
        self.smithCoords = (leftx + 1, topy + 3)
        my.blacksmithHasBeenPlaced = True


class TownHall(Building):
    """Control town legislation etc"""

    def __init__(self):
        Building.__init__(self, "townHall", (4, 3), my.BUILDINGSTATS["town hall"])
        self.add(my.townHall)
        self.menu = False

    def update(self, dt):
        self.updateBasic()
        if (
            my.input.mousePressed == 1
            and my.input.hoveredCell
            and my.input.hoveredCellType == "townHall"
        ):  # or self.menu:
            self.showMenu()

    def showMenu(self):
        self.menu = True
        my.camera.focus = self.coords

    def onPlace(self):
        pass
