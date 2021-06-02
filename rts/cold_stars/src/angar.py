from constants import *
from common import *
from render import *
from resources import *
from slot import SlotForAngar


class Angar:
    def __init__(self, bg_texOb):
        self.bg_texOb = bg_texOb
        self.slot_tex_ID, (self.slot_w, self.slot_h) = slot_tex_ID, (slot_w, slot_h)

        self.ship_list = []

        self.angar_slot_tex = H_tex_ID
        self.slot_w = 4 * self.slot_w
        self.slot_h = 4 * self.slot_h

        self.slot_list = []
        self.observed_ob = None

        self.createSlots()
        self.createButtons()

    def linkTexture(self):
        self.background_tex = self.bg_texOb.texture

    def unlinkTexture(self):
        self.background_tex = None

    def createSlots(self):
        slot = SlotForAngar(
            self.angar_slot_tex,
            (VIEW_WIDTH / 2 - self.slot_w, VIEW_HEIGHT / 2 - self.slot_h),
            (self.slot_w, self.slot_h),
            ANGAR_SLOT_ID,
            None,
        )
        slot.item = None
        self.slot_list.append(slot)

        slot = SlotForAngar(
            self.angar_slot_tex,
            (VIEW_WIDTH / 2 - self.slot_w + 150, VIEW_HEIGHT / 2 - self.slot_h),
            (self.slot_w, self.slot_h),
            ANGAR_SLOT_ID,
            None,
        )
        slot.item = None
        self.slot_list.append(slot)

        slot = SlotForAngar(
            self.angar_slot_tex,
            (VIEW_WIDTH / 2 - self.slot_w - 150, VIEW_HEIGHT / 2 - self.slot_h),
            (self.slot_w, self.slot_h),
            ANGAR_SLOT_ID,
            None,
        )
        slot.item = None
        self.slot_list.append(slot)

        slot = SlotForAngar(
            self.angar_slot_tex,
            (VIEW_WIDTH / 2 - self.slot_w, VIEW_HEIGHT / 2 - self.slot_h + 150),
            (self.slot_w, self.slot_h),
            ANGAR_SLOT_ID,
            None,
        )
        slot.item = None
        self.slot_list.append(slot)

        slot = SlotForAngar(
            self.angar_slot_tex,
            (VIEW_WIDTH / 2 - self.slot_w, VIEW_HEIGHT / 2 - self.slot_h - 150),
            (self.slot_w, self.slot_h),
            ANGAR_SLOT_ID,
            None,
        )
        slot.item = None
        self.slot_list.append(slot)

    def createButtons(self):
        self.repair_button_tex = repair_ICON_tex
        self.fuel_button_tex = fuel_ICON_tex
        self.launch_button_tex = launch_ICON_tex

        self.repair_button_rect = pygame.Rect(
            (VIEW_WIDTH - (INTERFACE_ICON_SIZE + 5), 1 * (INTERFACE_ICON_SIZE + 5)),
            (INTERFACE_ICON_SIZE, INTERFACE_ICON_SIZE),
        )
        self.fuel_button_rect = pygame.Rect(
            (VIEW_WIDTH - (INTERFACE_ICON_SIZE + 5), 2 * (INTERFACE_ICON_SIZE + 5)),
            (INTERFACE_ICON_SIZE, INTERFACE_ICON_SIZE),
        )
        self.launch_button_rect = pygame.Rect(
            (VIEW_WIDTH - (INTERFACE_ICON_SIZE + 5), 3 * (INTERFACE_ICON_SIZE + 5)),
            (INTERFACE_ICON_SIZE, INTERFACE_ICON_SIZE),
        )

    def renderBackground(self):
        drawFullScreenTexturedQuad(self.background_tex, VIEW_WIDTH, VIEW_HEIGHT, -1)

    def renderInternals(self):
        for slot in self.slot_list:
            slot.render()

    def renderButtons(self):
        drawTexturedRect(self.repair_button_tex, self.repair_button_rect, -1)
        drawTexturedRect(self.fuel_button_tex, self.fuel_button_rect, -1)
        drawTexturedRect(self.launch_button_tex, self.launch_button_rect, -1)

    def manageMouse(self, player, (mx, my), lb):
        self.goto_SPACE = False

        CURSOR_INTERSECT_OBJECT = False

        for slot in self.slot_list:
            slot_cursor_dist = lengthBetweenPoints(
                (slot.rect.centerx, slot.rect.centery), (mx, my)
            )
            if slot_cursor_dist < slot.rect[2] / 2:
                CURSOR_INTERSECT_OBJECT = True
                if slot.item != None:
                    if lb == True:
                        self.observed_ob = slot.item

        if CURSOR_INTERSECT_OBJECT == False:
            repairbutton_cursor_dist = lengthBetweenPoints(
                (self.repair_button_rect.centerx, self.repair_button_rect.centery),
                (mx, my),
            )
            if repairbutton_cursor_dist < self.repair_button_rect[2] / 2:
                CURSOR_INTERSECT_OBJECT = True
                if lb == True:
                    player.buyRepair()

        if CURSOR_INTERSECT_OBJECT == False:
            fuelbutton_cursor_dist = lengthBetweenPoints(
                (self.fuel_button_rect.centerx, self.fuel_button_rect.centery), (mx, my)
            )
            if fuelbutton_cursor_dist < self.fuel_button_rect[2] / 2:
                CURSOR_INTERSECT_OBJECT = True
                if lb == True:
                    player.buyFuel()

        if CURSOR_INTERSECT_OBJECT == False:
            launchbutton_cursor_dist = lengthBetweenPoints(
                (self.launch_button_rect.centerx, self.launch_button_rect.centery),
                (mx, my),
            )
            if launchbutton_cursor_dist < self.launch_button_rect[2] / 2:
                CURSOR_INTERSECT_OBJECT = True
                if lb == True:
                    self.goto_SPACE = True

    def render(self):
        self.renderBackground()
        self.renderInternals()
        self.renderButtons()
