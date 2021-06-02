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
from resources import *


class textureManager:
    def __init__(self):
        self.texOb_list = []

        self.nebulaStaticBig_texOb_list = []
        self.nebulaStaticMid_texOb_list = []
        self.nebulaRotatedMid_texOb_list = []

        self.star_texOb_list = []

        self.planet_texOb_list = []

        self.angarBg_texOb_list = []
        self.storeBg_texOb_list = []
        self.shopBg_texOb_list = []
        self.govermentBg_texOb_list = []

        self.landBg_texOb_list = []

        ######### ALL TIME LOADED INTO VRAM
        #### ITEMS
        self.driveItem_texOb_list = []
        self.lazerItem_texOb_list = []
        self.rocketItem_texOb_list = []
        self.torpedItem_texOb_list = []
        self.protectorItem_texOb_list = []
        self.droidItem_texOb_list = []
        self.grappleItem_texOb_list = []
        self.bakItem_texOb_list = []
        self.energyBlockItem_texOb_list = []
        self.freezerItem_texOb_list = []
        self.radarItem_texOb_list = []
        self.scanerItem_texOb_list = []

        ### BULLETS/EFFECTS
        self.rocketBullet_texOb_list = []
        self.torpedBullet_texOb_list = []

        self.particles_texOb_list = []
        self.distStar_texOb_list = []

        self.lazerEffect_texOb_list = []
        self.shieldEffect_texOb_list = []

        ### SHIPS
        self.sputnik_texOb_list = []
        self.ship_texOb_list = []

        self.RACE0_SHIP_SUBTYPE_list = []
        self.RACE0_SHIP_SIZE_list = []
        self.RACE0_SHIP_MOD_list = []

        self.RACE1_SHIP_SUBTYPE_list = []
        self.RACE1_SHIP_SIZE_list = []
        self.RACE1_SHIP_MOD_list = []

        self.RACE2_SHIP_SUBTYPE_list = []
        self.RACE2_SHIP_SIZE_list = []
        self.RACE2_SHIP_MOD_list = []

        self.RACE3_SHIP_SUBTYPE_list = []
        self.RACE3_SHIP_SIZE_list = []
        self.RACE3_SHIP_MOD_list = []

        self.RACE4_SHIP_SUBTYPE_list = []
        self.RACE4_SHIP_SIZE_list = []
        self.RACE4_SHIP_MOD_list = []

        self.RACE6_SHIP_SUBTYPE_list = []
        self.RACE6_SHIP_SIZE_list = []
        self.RACE6_SHIP_MOD_list = []

        self.RACE7_SHIP_SUBTYPE_list = []
        self.RACE7_SHIP_SIZE_list = []
        self.RACE7_SHIP_MOD_list = []

        ### FACES
        self.race0Face_texOb_list = []
        self.race1Face_texOb_list = []
        self.race2Face_texOb_list = []
        self.race3Face_texOb_list = []
        self.race4Face_texOb_list = []
        self.race6Face_texOb_list = []
        self.race7Face_texOb_list = []

        ### ASTEROIDS/MINERALS
        self.asteroid_texOb_list = []
        self.mineral_texOb_list = []
        self.container_texOb_list = []
        self.bomb_texOb_list = []
        self.blackhole_texOb_list = []

        self.active_ss = None

    def manage(self, texOb):
        if texOb.type_id == NEBULA_TEXTURE_ID:
            if texOb.size_id >= 4:
                self.nebulaStaticBig_texOb_list.append(texOb)
            elif texOb.size_id < 4:
                if texOb.rotated == False:
                    self.nebulaStaticMid_texOb_list.append(texOb)
                else:
                    self.nebulaRotatedMid_texOb_list.append(texOb)

        ########## INSIDE KOSMOPORT
        elif texOb.type_id == ANGAR_BG_TEXTURE_ID:
            self.angarBg_texOb_list.append(texOb)

        elif texOb.type_id == STORE_BG_TEXTURE_ID:
            self.storeBg_texOb_list.append(texOb)

        elif texOb.type_id == SHOP_BG_TEXTURE_ID:
            self.shopBg_texOb_list.append(texOb)

        elif texOb.type_id == GOVERMENT_BG_TEXTURE_ID:
            self.govermentBg_texOb_list.append(texOb)
        ###############################################

        elif texOb.type_id == LAND_BG_TEXTURE_ID:
            self.landBg_texOb_list.append(texOb)

        elif texOb.type_id == STAR_TEXTURE_ID:
            self.star_texOb_list.append(texOb)

        elif texOb.type_id == PLANET_TEXTURE_ID:
            self.planet_texOb_list.append(texOb)

        ###### ALL TIME LOADED INTO VRAM
        elif texOb.type_id == SPUTNIK_TEXTURE_ID:
            self.sputnik_texOb_list.append(texOb)

        elif texOb.type_id == SHIP_TEXTURE_ID:
            self.ship_texOb_list.append(texOb)
            self.sortShips(texOb)

        elif texOb.type_id == PARTICLE_TEXTURE_ID:
            self.particles_texOb_list.append(texOb)

        elif texOb.type_id == DISTANTSTAR_TEXTURE_ID:
            self.distStar_texOb_list.append(texOb)

        ### BULLETS/EFFECTS
        elif texOb.type_id == ROCKET_BULLET_TEXTURE_ID:
            self.rocketBullet_texOb_list.append(texOb)

        elif texOb.type_id == TORPED_BULLET_TEXTURE_ID:
            self.torpedBullet_texOb_list.append(texOb)

        elif texOb.type_id == LAZER_EFFECT_TEXTURE_ID:
            self.lazerEffect_texOb_list.append(texOb)

        elif texOb.type_id == SHIELD_EFFECT_TEXTURE_ID:
            self.shieldEffect_texOb_list.append(texOb)

        ### ASTEROIDS/MINERALS
        elif texOb.type_id == ASTEROID_TEXTURE_ID:
            self.asteroid_texOb_list.append(texOb)

        elif texOb.type_id == MINERAL_TEXTURE_ID:
            self.mineral_texOb_list.append(texOb)

        elif texOb.type_id == CONTAINER_TEXTURE_ID:
            self.container_texOb_list.append(texOb)

        elif texOb.type_id == BOMB_TEXTURE_ID:
            self.bomb_texOb_list.append(texOb)

        elif texOb.type_id == BLACKHOLE_TEXTURE_ID:
            self.blackhole_texOb_list.append(texOb)

    def manageFace(self, texOb):
        if texOb.race_id == RACE_0_ID:
            self.race0Face_texOb_list.append(texOb)
        elif texOb.race_id == RACE_1_ID:
            self.race1Face_texOb_list.append(texOb)
        elif texOb.race_id == RACE_2_ID:
            self.race2Face_texOb_list.append(texOb)
        elif texOb.race_id == RACE_3_ID:
            self.race3Face_texOb_list.append(texOb)
        elif texOb.race_id == RACE_4_ID:
            self.race4Face_texOb_list.append(texOb)
        elif texOb.race_id == RACE_6_ID:
            self.race6Face_texOb_list.append(texOb)
        elif texOb.race_id == RACE_7_ID:
            self.race7Face_texOb_list.append(texOb)

    def returnRandomFaceTexObByRaceId(self, race_id):
        if race_id == RACE_0_ID:
            texOb = self.race0Face_texOb_list[
                randint(0, len(self.race0Face_texOb_list) - 1)
            ]
        elif race_id == RACE_1_ID:
            texOb = self.race1Face_texOb_list[
                randint(0, len(self.race1Face_texOb_list) - 1)
            ]
        elif race_id == RACE_2_ID:
            texOb = self.race2Face_texOb_list[
                randint(0, len(self.race2Face_texOb_list) - 1)
            ]
        elif race_id == RACE_3_ID:
            texOb = self.race3Face_texOb_list[
                randint(0, len(self.race3Face_texOb_list) - 1)
            ]
        elif race_id == RACE_4_ID:
            texOb = self.race4Face_texOb_list[
                randint(0, len(self.race4Face_texOb_list) - 1)
            ]
        elif race_id == RACE_6_ID:
            texOb = self.race6Face_texOb_list[
                randint(0, len(self.race6Face_texOb_list) - 1)
            ]
        elif race_id == RACE_7_ID:
            texOb = self.race7Face_texOb_list[
                randint(0, len(self.race7Face_texOb_list) - 1)
            ]
        elif race_id == None:
            texOb = None
        return texOb

    def manageItem(self, texOb):
        if texOb.type_id == DRIVE_ITEM_TEXTURE_ID:
            self.driveItem_texOb_list.append(texOb)

        elif texOb.type_id == LAZER_ITEM_TEXTURE_ID:
            self.lazerItem_texOb_list.append(texOb)

        elif texOb.type_id == ROCKET_ITEM_TEXTURE_ID:
            self.rocketItem_texOb_list.append(texOb)

        elif texOb.type_id == TORPED_ITEM_TEXTURE_ID:
            self.torpedItem_texOb_list.append(texOb)

        elif texOb.type_id == PROTECTOR_ITEM_TEXTURE_ID:
            self.protectorItem_texOb_list.append(texOb)

        elif texOb.type_id == DROID_ITEM_TEXTURE_ID:
            self.droidItem_texOb_list.append(texOb)

        elif texOb.type_id == GRAPPLE_ITEM_TEXTURE_ID:
            self.grappleItem_texOb_list.append(texOb)

        elif texOb.type_id == BAK_ITEM_TEXTURE_ID:
            self.bakItem_texOb_list.append(texOb)

        elif texOb.type_id == ENERGYBLOCK_ITEM_TEXTURE_ID:
            self.energyBlockItem_texOb_list.append(texOb)

        elif texOb.type_id == FREEZER_ITEM_TEXTURE_ID:
            self.freezerItem_texOb_list.append(texOb)

        elif texOb.type_id == RADAR_ITEM_TEXTURE_ID:
            self.radarItem_texOb_list.append(texOb)

        elif texOb.type_id == SCANER_ITEM_TEXTURE_ID:
            self.scanerItem_texOb_list.append(texOb)

    def returnParticleTexObBy_ColorID(self, color_id):
        for texOb in self.particles_texOb_list:
            if texOb.color_id == color_id:
                return texOb

    def returnLazerEffectTexObBy_RevisionID_and_ColorID(self, revision_id, color_id):
        for texOb in self.lazerEffect_texOb_list:
            if texOb.revision_id == revision_id:
                if texOb.color_id == color_id:
                    return texOb

    def returnShieldEffectTexObBy_RevisionID_and_ColorID(self, revision_id, color_id):
        for texOb in self.shieldEffect_texOb_list:
            if texOb.revision_id == revision_id:
                if texOb.color_id == color_id:
                    return texOb

    def returnItemTexOb(self, item_type_id, revision_id):
        if item_type_id == -1:
            pass  # add

        item_list = self.returnListByType(item_type_id)
        if revision_id != -1:
            for item_texOb in item_list:
                if item_texOb.revision_id == revision_id:
                    return item_texOb
        else:
            item_texOb = item_list[randint(0, len(item_list) - 1)]
            return item_texOb

    def returnListByType(self, item_type_id):
        if item_type_id == ROCKET_ITEM_TEXTURE_ID:
            return self.rocketItem_texOb_list
        elif item_type_id == TORPED_ITEM_TEXTURE_ID:
            return self.torpedItem_texOb_list
        elif item_type_id == LAZER_ITEM_TEXTURE_ID:
            return self.lazerItem_texOb_list
        elif item_type_id == RADAR_ITEM_TEXTURE_ID:
            return self.radarItem_texOb_list
        elif item_type_id == GRAPPLE_ITEM_TEXTURE_ID:
            return self.grappleItem_texOb_list
        elif item_type_id == DRIVE_ITEM_TEXTURE_ID:
            return self.driveItem_texOb_list
        elif item_type_id == PROTECTOR_ITEM_TEXTURE_ID:
            return self.protectorItem_texOb_list
        elif item_type_id == BAK_ITEM_TEXTURE_ID:
            return self.bakItem_texOb_list
        elif item_type_id == DROID_ITEM_TEXTURE_ID:
            return self.droidItem_texOb_list
        elif item_type_id == SCANER_ITEM_TEXTURE_ID:
            return self.scanerItem_texOb_list
        elif item_type_id == FREEZER_ITEM_TEXTURE_ID:
            return self.freezerItem_texOb_list
        elif item_type_id == ENERGYBLOCK_ITEM_TEXTURE_ID:
            return self.energyBlockItem_texOb_list

    def sortShips(self, texOb):
        if texOb.race_id == RACE_0_ID:
            self.RACE0_SHIP_SUBTYPE_list.append(texOb.subtype_id)
            self.RACE0_SHIP_SIZE_list.append(texOb.size_id)
            self.RACE0_SHIP_MOD_list.append(texOb.mod_id)

        elif texOb.race_id == RACE_1_ID:
            self.RACE1_SHIP_SUBTYPE_list.append(texOb.subtype_id)
            self.RACE1_SHIP_SIZE_list.append(texOb.size_id)
            self.RACE1_SHIP_MOD_list.append(texOb.mod_id)

        elif texOb.race_id == RACE_2_ID:
            self.RACE2_SHIP_SUBTYPE_list.append(texOb.subtype_id)
            self.RACE2_SHIP_SIZE_list.append(texOb.size_id)
            self.RACE2_SHIP_MOD_list.append(texOb.mod_id)

        elif texOb.race_id == RACE_3_ID:
            self.RACE3_SHIP_SUBTYPE_list.append(texOb.subtype_id)
            self.RACE3_SHIP_SIZE_list.append(texOb.size_id)
            self.RACE3_SHIP_MOD_list.append(texOb.mod_id)

        elif texOb.race_id == RACE_4_ID:
            self.RACE4_SHIP_SUBTYPE_list.append(texOb.subtype_id)
            self.RACE4_SHIP_SIZE_list.append(texOb.size_id)
            self.RACE4_SHIP_MOD_list.append(texOb.mod_id)

        elif texOb.race_id == RACE_6_ID:
            self.RACE6_SHIP_SUBTYPE_list.append(texOb.subtype_id)
            self.RACE6_SHIP_SIZE_list.append(texOb.size_id)
            self.RACE6_SHIP_MOD_list.append(texOb.mod_id)

        elif texOb.race_id == RACE_7_ID:
            self.RACE7_SHIP_SUBTYPE_list.append(texOb.subtype_id)
            self.RACE7_SHIP_SIZE_list.append(texOb.size_id)
            self.RACE7_SHIP_MOD_list.append(texOb.mod_id)

    def loadAllTexturesInStarsystem(self, starsystem):
        for n in starsystem.NEBULA_static_effect_list:
            n.texOb.loadToVRAM()
            n.linkTexture()

        for n in starsystem.NEBULA_rotated_effect_list:
            n.texOb.loadToVRAM()
            n.linkTexture()

        for s in starsystem.STAR_list:
            s.texOb.loadToVRAM()
            s.linkTexture()

        for p in starsystem.PLANET_list:
            p.texOb.loadToVRAM()
            p.linkTexture()

        # for sa in starsystem.SPUTNIK_list:
        #    sa.texOb.loadToVRAM()
        #    sa.linkTexture()

        # for k in starsystem.SHIP_list:
        #    k.texOb.loadToVRAM()
        #    k.linkTexture()

        self.active_ss = starsystem

        # ...

    """   
      def loadDynamicObTex(self, ob):
          if ob.starsystem == self.active_ss:
             if ob.TexOb.loaded == False:
                ob.texOb.loadToVRAM()
                ob.texOb.linkTexture()
          else:
             if ob.TexOb.loaded == True:
                ob.texOb.removeFromVRAM()
                ob.texOb.unlinkTexture()
      """

    def removeAllTexturesInStarsystem(self, starsystem):
        for n in starsystem.NEBULA_static_effect_list:
            n.texOb.removeFromVRAM()
            n.unlinkTexture()

        for n in starsystem.NEBULA_rotated_effect_list:
            n.texOb.removeFromVRAM()
            n.unlinkTexture()

        for s in starsystem.STAR_list:
            s.texOb.removeFromVRAM()
            s.unlinkTexture()

        for p in starsystem.PLANET_list:
            p.texOb.removeFromVRAM()
            p.unlinkTexture()

        for sa in starsystem.SPUTNIK_list:
            sa.texOb.removeFromVRAM()
            sa.unlinkTexture()

        for k in starsystem.SPIP_list:
            k.texOb.removeFromVRAM()
            k.unlinkTexture()

        # ...

    def loadKosmoportDataToVRAM(self, planet):
        planet.port.angar.bg_texOb.loadToVRAM()
        planet.port.angar.linkTexture()

        planet.port.store.bg_texOb.loadToVRAM()
        planet.port.store.linkTexture()

        planet.port.shop.bg_texOb.loadToVRAM()
        planet.port.shop.linkTexture()

        planet.port.goverment.bg_texOb.loadToVRAM()
        planet.port.goverment.linkTexture()

    def removeKosmoportDataFromVRAM(self, planet):
        planet.port.angar.bg_texOb.removeFromVRAM()
        planet.port.angar.unlinkTexture()

        planet.port.store.bg_texOb.removeFromVRAM()
        planet.port.store.unlinkTexture()

        planet.port.shop.bg_texOb.removeFromVRAM()
        planet.port.shop.unlinkTexture()

        planet.port.goverment.bg_texOb.removeFromVRAM()
        planet.port.goverment.unlinkTexture()

    def loadLandDataToVRAM(self, planet):
        planet.land.bg_texOb.loadToVRAM()
        planet.land.linkTexture()

    def removeLandDataFromVRAM(self, planet):
        planet.land.bg_texOb.removeFromVRAM()
        planet.land.unlinkTexture()


class textureOb:
    def __init__(
        self, type_id, path, use_alpha=True, arg=[], slice_w=None, slice_h=None
    ):
        self.path = path
        self.type_id = type_id
        self.use_alpha = use_alpha

        self.id = TEXTURE_ID_GENERATOR.returnNextID()

        if slice_w == None:
            self.texture = None
            self.loadToVRAM = self.loadSingleToVRAM
            self.removeFromVRAM = self.removeSingleFromVRAM
            self.animated = False
        else:
            self.texture = []
            self.loadToVRAM = self.loadSlicedToVRAM
            self.removeFromVRAM = self.removeSlicedFromVRAM
            self.slice_w, self.slice_h = slice_w, slice_h
            self.animated = True

        self.loaded = False
        self.shared = False

        if self.type_id == NEBULA_TEXTURE_ID:
            self.nebulaArgManager(arg)

        elif self.type_id == STAR_TEXTURE_ID:
            self.starArgManager(arg)

        elif self.type_id == PLANET_TEXTURE_ID:
            self.planetArgManager(arg)

        elif self.type_id == LAND_BG_TEXTURE_ID:
            self.landBgArgManager(arg)

        ######### IN KOSMOPORT
        elif self.type_id == ANGAR_BG_TEXTURE_ID:
            self.angarBgArgManager(arg)

        elif self.type_id == STORE_BG_TEXTURE_ID:
            self.storeBgArgManager(arg)

        elif self.type_id == SHOP_BG_TEXTURE_ID:
            self.shopBgArgManager(arg)

        elif self.type_id == GOVERMENT_BG_TEXTURE_ID:
            self.govermentBgArgManager(arg)
        #########################################

        elif self.type_id == FACE_TEXTURE_ID:
            self.loadToVRAM()
            self.faceArgManager(arg)

        elif self.type_id == SPUTNIK_TEXTURE_ID:
            self.loadToVRAM()
            self.sputnikArgManager(arg)

        elif self.type_id == SHIP_TEXTURE_ID:
            self.loadToVRAM()
            self.shipArgManager(arg)

        elif self.type_id == PARTICLE_TEXTURE_ID:
            self.loadToVRAM()
            self.particleArgManager(arg)

        elif self.type_id == DISTANTSTAR_TEXTURE_ID:
            self.loadToVRAM()
            self.distStarArgManager(arg)

        elif self.type_id == LAZER_EFFECT_TEXTURE_ID:
            self.loadToVRAM()
            self.lazerEffectArgManager(arg)

        elif self.type_id == SHIELD_EFFECT_TEXTURE_ID:
            self.loadToVRAM()
            self.shieldEffectArgManager(arg)

        # ITEMS
        elif self.type_id == DRIVE_ITEM_TEXTURE_ID:
            self.loadToVRAM()  # remove
            self.driveItemArgManager(arg)

        elif self.type_id == LAZER_ITEM_TEXTURE_ID:
            self.loadToVRAM()  # remove
            self.lazerItemArgManager(arg)

        elif (
            self.type_id == ROCKET_ITEM_TEXTURE_ID
            or self.type_id == TORPED_ITEM_TEXTURE_ID
        ):
            self.loadToVRAM()  # remove
            self.rocketItemArgManager(arg)

        elif self.type_id == PROTECTOR_ITEM_TEXTURE_ID:
            self.loadToVRAM()  # remove
            self.protectorItemArgManager(arg)

        elif self.type_id == DROID_ITEM_TEXTURE_ID:
            self.loadToVRAM()  # remove
            self.droidItemArgManager(arg)

        elif self.type_id == GRAPPLE_ITEM_TEXTURE_ID:
            self.loadToVRAM()  # remove
            self.grappleItemArgManager(arg)

        elif self.type_id == BAK_ITEM_TEXTURE_ID:
            self.loadToVRAM()  # remove
            self.bakItemArgManager(arg)

        elif self.type_id == ENERGYBLOCK_ITEM_TEXTURE_ID:
            self.loadToVRAM()  # remove
            self.energyBlockItemArgManager(arg)

        elif self.type_id == FREEZER_ITEM_TEXTURE_ID:
            self.loadToVRAM()  # remove
            self.freezerItemArgManager(arg)

        elif self.type_id == RADAR_ITEM_TEXTURE_ID:
            self.loadToVRAM()  # remove
            self.radarItemArgManager(arg)

        elif self.type_id == SCANER_ITEM_TEXTURE_ID:
            self.loadToVRAM()  # remove
            self.scanerItemArgManager(arg)

        # BULLETS
        elif self.type_id == ROCKET_BULLET_TEXTURE_ID:
            self.loadToVRAM()  # remove
            self.rocketBulletArgManager(arg)

        elif self.type_id == TORPED_BULLET_TEXTURE_ID:
            self.loadToVRAM()  # remove
            self.torpedBulletArgManager(arg)

        ### ASTEROIDS/MINERALS
        elif self.type_id == ASTEROID_TEXTURE_ID:
            self.loadToVRAM()  # remove
            self.asteroidArgManager(arg)

        elif self.type_id == MINERAL_TEXTURE_ID:
            self.loadToVRAM()  # remove
            self.mineralArgManager(arg)

        elif self.type_id == CONTAINER_TEXTURE_ID:
            self.loadToVRAM()  # remove
            self.containerArgManager(arg)

        elif self.type_id == BOMB_TEXTURE_ID:
            self.loadToVRAM()  # remove
            self.bombArgManager(arg)

        elif self.type_id == BLACKHOLE_TEXTURE_ID:
            self.loadToVRAM()  # remove
            self.blackholeArgManager(arg)

    def nebulaArgManager(self, arg):
        self.color = arg[0]
        self.size_id = arg[1]
        self.rotated = arg[2]

    def starArgManager(self, arg):
        self.class_id = arg[0]
        self.size_id = arg[1]
        self.brightThreshold = arg[2]
        self.color = arg[3]

    def planetArgManager(self, arg):
        self.class_id = arg[0]
        self.size_id = arg[1]

    def landBgArgManager(self, arg):
        pass

    ########## KOSMOPORT
    def angarBgArgManager(self, arg):
        self.race_id = arg[0]

    def storeBgArgManager(self, arg):
        self.race_id = arg[0]

    def shopBgArgManager(self, arg):
        self.race_id = arg[0]

    def govermentBgArgManager(self, arg):
        self.race_id = arg[0]

    #############################################

    def sputnikArgManager(self, arg):
        pass

    def shipArgManager(self, arg):
        self.race_id = arg[0]
        self.subtype_id = arg[1]  # warrior/trader and so on
        self.color_id = arg[2]
        self.mod_id = 0

        self.size_id = returnObjectSize(self.w, self.h)

    def particleArgManager(self, arg):
        self.color_id = arg[0]

    def distStarArgManager(self, arg):
        pass

    def lazerEffectArgManager(self, arg):
        self.revision_id = arg[0]
        self.color_id = arg[1]

    def shieldEffectArgManager(self, arg):
        self.revision_id = arg[0]
        self.race_id = arg[1]
        self.color_id = arg[2]

    def driveItemArgManager(self, arg):
        self.revision_id = arg[0]
        self.race_id = arg[1]
        self.color_id = arg[2]

    def lazerItemArgManager(self, arg):
        self.revision_id = arg[0]
        self.race_id = arg[1]
        self.color_id = arg[2]

    def rocketItemArgManager(self, arg):
        #'single rocket', TECH_LEVEL_0_ID, 1, 1, RACE_0_ID, YELLOW_COLOR_ID]
        self.title = arg[0]
        self.revision_id = arg[1]
        self.ammo_size_id = arg[2]
        self.ammo_num = arg[3]

        self.race_id = arg[4]
        self.color_id = arg[5]

    def protectorItemArgManager(self, arg):
        self.revision_id = arg[0]
        self.race_id = arg[1]
        self.color_id = arg[2]

    def droidItemArgManager(self, arg):
        self.revision_id = arg[0]
        self.race_id = arg[1]

    def grappleItemArgManager(self, arg):
        self.revision_id = arg[0]
        self.race_id = arg[1]

    def bakItemArgManager(self, arg):
        self.revision_id = arg[0]
        self.race_id = arg[1]

    def energyBlockItemArgManager(self, arg):
        self.revision_id = arg[0]
        self.race_id = arg[1]

    def freezerItemArgManager(self, arg):
        self.revision_id = arg[0]
        self.race_id = arg[1]

    def radarItemArgManager(self, arg):
        self.revision_id = arg[0]
        self.race_id = arg[1]

    def scanerItemArgManager(self, arg):
        self.revision_id = arg[0]
        self.race_id = arg[1]

    def faceArgManager(self, arg):
        self.race_id = arg[0]

    # BULLETS
    def rocketBulletArgManager(self, arg):
        pass

    def torpedBulletArgManager(self, arg):
        pass

    ### ASTEROID/MINERAL
    def asteroidArgManager(self, arg):
        pass

    def mineralArgManager(self, arg):
        pass

    def containerArgManager(self, arg):
        pass

    def bombArgManager(self, arg):
        pass

    def blackholeArgManager(self, arg):
        pass

    def loadSingleToVRAM(self):
        if self.loaded == False:
            self.texture, (self.w, self.h) = upload_texture(self.path, self.use_alpha)
            self.shared = False
            self.loaded = True
        else:
            self.shared = True
            self.loaded = True

    def loadSlicedToVRAM(self):
        if self.loaded == False:
            self.texture, (self.w, self.h) = uploadSlicedTextures(
                self.path, (self.slice_w, self.slice_h)
            )
            self.shared = False
            self.loaded = True
        else:
            self.shared = True
            self.loaded = True

    def removeSingleFromVRAM(self):
        if self.loaded == True:
            # check that no one other is using this texOb in current ss
            if self.shared == False:
                glDeleteTextures(self.texture)
                self.texture = None
                self.loaded = False

    def removeSlicedFromVRAM(self):
        if self.loaded == True:
            # check that no one other is using this texOb in current ss
            if self.shared == False:
                for tex in self.texture:
                    glDeleteTextures(tex)
                self.texture = None
                self.loaded = False


# quick function to load an image
def load_image(name):
    path = os.path.join(MAIN_DIR, "data", name)
    return pygame.image.load(path).convert_alpha()


def upload_texture(filename, use_alpha=True):
    # Read an image file and upload a texture
    if use_alpha:
        format, gl_format, bits_per_pixel = "RGBA", GL_RGBA, 4
    else:
        format, gl_format, bits_per_pixel = "RGB", GL_RGB, 3

    img_surface = pygame.image.load(filename)

    data = pygame.image.tostring(img_surface, format, True)

    texture_id = glGenTextures(1)

    # glActiveTexture(GL_TEXTURE0)
    glBindTexture(GL_TEXTURE_2D, texture_id)

    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR)

    glPixelStorei(GL_UNPACK_ALIGNMENT, 1)

    width, height = img_surface.get_rect().size

    glTexImage2D(
        GL_TEXTURE_2D,
        0,
        bits_per_pixel,
        width,
        height,
        0,
        gl_format,
        GL_UNSIGNED_BYTE,
        data,
    )

    # Return the texture id, so we can use glBindTexture
    return texture_id, (width, height)


def upload_texture_from_surface(img_surface, use_alpha=True):
    # Read an image file and upload a texture
    if use_alpha:
        format, gl_format, bits_per_pixel = "RGBA", GL_RGBA, 4
    else:
        format, gl_format, bits_per_pixel = "RGB", GL_RGB, 3

    data = pygame.image.tostring(img_surface, format, True)

    texture_id = glGenTextures(1)

    glBindTexture(GL_TEXTURE_2D, texture_id)

    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR)

    glPixelStorei(GL_UNPACK_ALIGNMENT, 1)

    width, height = img_surface.get_rect().size

    glTexImage2D(
        GL_TEXTURE_2D,
        0,
        bits_per_pixel,
        width,
        height,
        0,
        gl_format,
        GL_UNSIGNED_BYTE,
        data,
    )

    # Return the texture id, so we can use glBindTexture
    return texture_id


def uploadSlicedTextures(filename, frame_width, frame_height):
    texture_ID = []

    master_surface = pygame.image.load(filename).convert_alpha()
    master_width, master_height = master_surface.get_size()

    for i in range(int(master_height / frame_height)):
        for j in range(int(master_width / frame_width)):
            surf = master_surface.subsurface(
                (j * frame_width, i * frame_height, frame_width, frame_height)
            )
            texture_ID.append(upload_texture_from_surface(surf))
    return texture_ID, (frame_width, frame_height)


"""
class textureOb1():
      def __init__(self, data, type = 1, w_slice = None, h_slice = None, use_alpha = True):
          self.type = type

          # single image
          if self.type == 1:
             path = data
             self.texture, (self.w, self.h) = upload_texture(path, use_alpha)
             self.frames_num = 1

          # multiple images
          elif self.type == 2:
             path = data
             self.texture, (self.w, self.h) = uploadSlicedTextures(path, (w_slice, h_slice), use_alpha)
             self.frames_num = len(self.texture)

          # array
          elif self.type == 3:
             array = data

          # surface
          elif self.type == 4:
             surface = data
 
"""
