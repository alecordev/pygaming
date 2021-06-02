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


from random import randint
from resources import *


class skill:
    def __init__(self):
        self.attack = randint(1, 10)
        self.defence = randint(1, 10)
        self.leader = randint(1, 10)
        self.trader = randint(1, 10)
        self.technic = randint(1, 10)
        self.diplomat = randint(1, 10)  # each skill has they max depends on race/class

        self.acknowledge()

        self.free_points = 3

        self.expirience = randint(40, 400)
        self.next_level_expirience = 1000
        self.GUI = None

    def addExpirience(self, expirience):
        self.expirience += expirience
        if self.expirience > self.next_level_expirience:
            self.free_points += 1
            self.next_level_expirience = 2 * self.next_level_expirience

    def acknowledge(self):
        self.attackRevertBuffer = 0
        self.defenceRevertBuffer = 0
        self.leaderRevertBuffer = 0
        self.traderRevertBuffer = 0
        self.technicRevertBuffer = 0
        self.diplomatRevertBuffer = 0

    ######### ATTACK ###############
    def incrementAttack(self):
        if self.free_points > 0:
            self.free_points -= 1
            self.attack += 1
            self.attackRevertBuffer += 1

    def decrementAttack(self):
        if self.attackRevertBuffer > 0:
            self.attack -= 1
            self.free_points += 1
            self.attackRevertBuffer -= 1

    ######### DEFENCE ###############
    def incrementDefence(self):
        if self.free_points > 0:
            self.free_points -= 1
            self.defence += 1
            self.defenceRevertBuffer += 1

    def decrementDefence(self):
        if self.defenceRevertBuffer > 0:
            self.defence -= 1
            self.free_points += 1
            self.defenceRevertBuffer -= 1

    ######### LEADER ###############
    def incrementLeader(self):
        if self.free_points > 0:
            self.free_points -= 1
            self.leader += 1
            self.leaderRevertBuffer += 1

    def decrementLeader(self):
        if self.leaderRevertBuffer > 0:
            self.leader -= 1
            self.free_points += 1
            self.leaderRevertBuffer -= 1

    ######### TRADER ###############
    def incrementTrader(self):
        if self.free_points > 0:
            self.free_points -= 1
            self.trader += 1
            self.traderRevertBuffer += 1

    def decrementTrader(self):
        if self.traderRevertBuffer > 0:
            self.trader -= 1
            self.free_points += 1
            self.traderRevertBuffer -= 1

    ######### TECHNIC ###############
    def incrementTechnic(self):
        if self.free_points > 0:
            self.free_points -= 1
            self.technic += 1
            self.technicRevertBuffer += 1

    def decrementTechnic(self):
        if self.technicRevertBuffer > 0:
            self.technic -= 1
            self.free_points += 1
            self.technicRevertBuffer -= 1

    ######### DIMPLOMAT ###############
    def incrementDiplomat(self):
        if self.free_points > 0:
            self.free_points -= 1
            self.diplomat += 1
            self.diplomatRevertBuffer += 1

    def decrementDiplomat(self):
        if self.diplomatRevertBuffer > 0:
            self.diplomat -= 1
            self.free_points += 1
            self.diplomatRevertBuffer -= 1
