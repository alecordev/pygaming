from constants import *
from starsystem import *
from SpaceObjects import *
from player import *
from render import *
from resources import *


class worldMap:
    def __init__(self):
        self.border_rect = pygame.Rect(
            (MAPOFFSETX, MAPOFFSETY),
            (VIEW_WIDTH - 2 * MAPOFFSETX, VIEW_HEIGHT - 2 * MAPOFFSETX),
        )

    def updateRange(self, k):
        if k.korpus.drive_slot.item != None and k.korpus.bak_slot.item != None:
            radius_min = min(
                k.korpus.drive_slot.item.hyper, k.korpus.bak_slot.item.fuel
            )
            self.range_list_x, self.range_list_y = getCircleCoordinateRangeLowPrecision(
                k.starsystem.rectOnMap.centerx,
                k.starsystem.rectOnMap.centery,
                radius_min,
            )
            self.GL_LIST_range_ID = GlListCompileDirection(
                DOT_RED_TEX,
                self.range_list_x,
                self.range_list_y,
                len(self.range_list_x),
                1,
                10,
            )
        else:
            self.GL_LIST_range_ID = None

    def selectStarSystem(self, player, lb, mx, my):
        if player.ableTo_JUMP:
            mxvp = mx + vpCoordinate_x
            myvp = my + vpCoordinate_y
            for ss in global_STARSYSTEM_list:
                if ss != player.starsystem:
                    ss_cursor_dist = lengthBetweenPoints(
                        (ss.rectOnMap.centerx, ss.rectOnMap.centery), (mx, my)
                    )
                    if ss_cursor_dist < 10:
                        ss_ss_dist = lengthBetweenPoints(
                            (ss.rectOnMap.centerx, ss.rectOnMap.centery),
                            (
                                player.starsystem.rectOnMap.centerx,
                                player.starsystem.rectOnMap.centery,
                            ),
                        )
                        if (
                            ss_ss_dist < player.korpus.drive_slot.item.hyper
                            and ss_ss_dist < player.korpus.bak_slot.item.fuel
                        ):
                            if lb == True:
                                player.hyperJumpPreparation(ss)
                                # player.calculateTraceToCoord((player.jump_pos_x, player.jump_pos_y))
                                return True
            return False

    def render(self):
        drawTexturedRect(BLACK_TEX, self.border_rect, -1)

        glEnable(GL_BLEND)
        for ss in global_STARSYSTEM_list:
            drawTexturedRect(s_000_tex_ID, ss.rectOnMap, -1)
            drawSimpleText((ss.label_pos_x, ss.label_pos_y), ss.name)
            if ss.CAPTURED == True:
                drawTexturedRect(
                    mark_enemy_ss_tex,
                    [
                        ss.rectOnMap[0] - 10,
                        ss.rectOnMap[1] - 10,
                        ss.rectOnMap[2] + 20,
                        ss.rectOnMap[3] + 20,
                    ],
                    -1,
                )

        drawTexturedRect(
            mark_ss_tex,
            [
                player.starsystem.rectOnMap[0] - 10,
                player.starsystem.rectOnMap[1] - 10,
                player.starsystem.rectOnMap[2] + 20,
                player.starsystem.rectOnMap[3] + 20,
            ],
            -1,
        )

        if self.GL_LIST_range_ID != None:
            glCallList(self.GL_LIST_range_ID)

        # glDisable(GL_BLEND)
