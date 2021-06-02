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


from korpus import *
from items import *
from modules import *
from player import *

korpus1 = korpusGenerator(RACE_0_ID, WARRIOR_ID, 3, 0)

korpus1.space = 400
korpus1.armor_max = 400
korpus1.armor = 300
korpus1.protection = 2

bomb1 = bombGenerator()
bomb2 = bombGenerator()
bomb3 = bombGenerator()

generatorModule1 = generatorModuleGenerator()
generatorModule2 = generatorModuleGenerator()
generatorModule3 = generatorModuleGenerator()

freezerModule1 = freezerModuleGenerator()
freezerModule2 = freezerModuleGenerator()
freezerModule3 = freezerModuleGenerator()

grappleModule1 = grappleModuleGenerator()
grappleModule2 = grappleModuleGenerator()
grappleModule3 = grappleModuleGenerator()

radarModule1 = radarModuleGenerator()
driveModule1 = driveModuleGenerator()
protectorModule1 = protectorModuleGenerator()
bakModule1 = bakModuleGenerator()
droidModule1 = droidModuleGenerator()
scanerModule1 = scanerModuleGenerator()

lazerModule1 = lazerModuleGenerator()
lazerModule2 = lazerModuleGenerator()
lazerModule3 = lazerModuleGenerator()

rocketModule1 = rocketModuleGenerator()
rocketModule2 = rocketModuleGenerator()
rocketModule3 = rocketModuleGenerator()

lazer1 = lazerGenerator(RACE_0_ID)
lazer1.damage_orig = 80
lazer1.radius_orig = 250
lazer1.modules_num_max = 2

lazer1.mass = 13
lazer1.condition_max = 1000
lazer1.condition = 1000
lazer1.deterioration_rate = 1

lazer1.updatePropetries()
lazer1.countPrice()
lazer1.updateInfo()


lazer2 = lazerGenerator(RACE_0_ID)
lazer2.damage_orig = 70
lazer2.radius_orig = 300
lazer2.modules_num_max = 2

lazer2.mass = 12
lazer2.condition_max = 1000
lazer2.condition = 1000
lazer2.deterioration_rate = 1

lazer2.updatePropetries()
lazer2.countPrice()
lazer2.updateInfo()


lazer3 = lazerGenerator(RACE_0_ID)
lazer3.damage_orig = 6
lazer3.radius_orig = 350
lazer3.modules_num_max = 2

lazer3.mass = 10
lazer3.condition_max = 1000
lazer3.condition = 1000
lazer3.deterioration_rate = 1

lazer3.updatePropetries()
lazer3.countPrice()
lazer3.updateInfo()


rocket1 = torpedGenerator(RACE_0_ID, 0)

rocket1.ammo_max_orig = 30
rocket1.ammo = 10
rocket1.damage_orig = 10
rocket1.radius_orig = 450
rocket1.modules_num_max = 2

rocket1.mass = 10
rocket1.condition_max = 1000
rocket1.condition = 1000
rocket1.deterioration_rate = 1

rocket1.updatePropetries()
rocket1.countPrice()
rocket1.updateInfo()


rocket2 = rocketGenerator(RACE_0_ID, 0)
rocket2.ammo_max_orig = 2
rocket2.ammo = 20
rocket2.damage_orig = 5
rocket2.radius_orig = 500
rocket2.modules_num_max = 2

rocket2.mass = 20
rocket2.condition_max = 1000
rocket2.condition = 1000
rocket2.deterioration_rate = 1

rocket2.updatePropetries()
rocket2.countPrice()
rocket2.updateInfo()

rocket3 = rocketGenerator(RACE_0_ID, 0)
rocket3.ammo_max_orig = 44
rocket3.ammo = 44
rocket3.damage_orig = 6
rocket3.radius_orig = 550
rocket3.modules_num_max = 2

rocket3.mass = 30
rocket3.condition_max = 1000
rocket3.condition = 99
rocket3.deterioration_rate = 1
rocket3.speed = 5 * ROCKET_SPEED_MAX

rocket3.updatePropetries()
rocket3.countPrice()
rocket3.updateInfo()


freezer1 = freezerGenerator(RACE_0_ID)
freezer1.modules_num_max = 2


generator1 = energyBlockGenerator(RACE_0_ID)
generator1.energy_max_orig = 700
generator1.energy = 100
generator1.restoration_orig = 200
generator1.modules_num_max = 2

generator1.mass = 30
generator1.condition_max = 2000
generator1.condition = 1000
generator1.deterioration_rate = 1

generator1.updatePropetries()
generator1.countPrice()
generator1.updateInfo()


grapple1 = grappleGenerator(RACE_0_ID)
grapple1.strength_orig = 220
grapple1.radius_orig = 100
grapple1.speed_orig = 180
grapple1.maxNumItem_orig = 2
grapple1.modules_num_max = 2

grapple1.mass = 20
grapple1.condition_max = 1000
grapple1.condition = 1000
grapple1.deterioration_rate = 1

grapple1.updatePropetries()
grapple1.countPrice()
grapple1.updateInfo()


radar1 = radarGenerator(RACE_0_ID)
radar1.radius_orig = 4500
radar1.modules_num_max = 2

radar1.mass = 15
radar1.condition_max = 1000
radar1.condition = 1000
radar1.deterioration_rate = 1

radar1.updatePropetries()
radar1.countPrice()
radar1.updateInfo()


drive1 = driveGenerator(RACE_0_ID)
drive1.speed_orig = 400
drive1.hyper_orig = 800
drive1.modules_num_max = 2

drive1.mass = 23
drive1.condition_max = 1000
drive1.condition = 1000
drive1.deterioration_rate = 1

drive1.updatePropetries()
drive1.countPrice()
drive1.updateInfo()


protector1 = protectorGenerator(RACE_0_ID)
protector1.protection_orig = 30
protector1.modules_num_max = 2

protector1.mass = 40
protector1.condition_max = 1000
protector1.condition = 1000
protector1.deterioration_rate = 1

protector1.updatePropetries()
protector1.countPrice()
protector1.updateInfo()


bak1 = bakGenerator(RACE_0_ID)

bak1.fuel_max_orig = 800
bak1.fuel = 700
bak1.modules_num_max = 2

bak1.mass = 20
bak1.condition_max = 1000
bak1.condition = 1000
bak1.deterioration_rate = 1

bak1.updatePropetries()
bak1.countPrice()
bak1.updateInfo()


droid1 = droidGenerator(RACE_0_ID)
droid1.repair_orig = 3
droid1.modules_num_max = 2

droid1.mass = 20
droid1.condition_max = 1000
droid1.condition = 1000
droid1.deterioration_rate = 1

droid1.updatePropetries()
droid1.countPrice()
droid1.updateInfo()


scaner1 = scanerGenerator(RACE_0_ID)
scaner1.scan_orig = 40
scaner1.modules_num_max = 2

scaner1.mass = 10
scaner1.condition_max = 1000
scaner1.condition = 1000
scaner1.deterioration_rate = 1

scaner1.updatePropetries()
scaner1.countPrice()
scaner1.updateInfo()


# rocketModule1, rocketModule2, lazerModule1, generatorModule2, radarModule1, grappleModule1, freezerModule1, driveModule1, protectorModule1,

player = PlayerShip(
    None,
    "plr",
    RACE_0_ID,
    TEXTURE_MANAGER.returnRandomFaceTexObByRaceId(RACE_0_ID),
    WARRIOR_ID,
)
player.item_list = [
    bakModule1,
    droidModule1,
    scanerModule1,
    rocket1,
    rocket2,
    lazer1,
    lazer2,
    lazer3,
    generator1,
    freezer1,
    grapple1,
    radar1,
    drive1,
    protector1,
    bak1,
    droid1,
    scaner1,
    bomb1,
    bomb2,
    bomb3,
]
player.setKorpus(korpus1)
player.updateAllStuff()

player.GlListCompileRadius()
player.target_reset()
player.initPositionInSpace((500, 300), 0)

global_SHIP_list.append(player)
