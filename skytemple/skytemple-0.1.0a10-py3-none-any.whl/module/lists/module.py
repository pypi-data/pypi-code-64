#  Copyright 2020 Parakoopa
#
#  This file is part of SkyTemple.
#
#  SkyTemple is free software: you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation, either version 3 of the License, or
#  (at your option) any later version.
#
#  SkyTemple is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with SkyTemple.  If not, see <https://www.gnu.org/licenses/>.
from typing import List, Tuple

from gi.repository.Gtk import TreeStore

from skytemple.core.abstract_module import AbstractModule
from skytemple.core.rom_project import RomProject, BinaryName
from skytemple.core.ui_utils import recursive_up_item_store_mark_as_modified, generate_item_store_row_label
from skytemple.module.lists.controller.main import MainController, GROUND_LISTS
from skytemple.module.lists.controller.actor_list import ActorListController
from skytemple.module.lists.controller.rank_list import RankListController
from skytemple.module.lists.controller.starters_list import StartersListController
from skytemple.module.lists.controller.recruitment_list import RecruitmentListController
from skytemple.module.lists.controller.world_map import WorldMapController
from skytemple_files.data.md.model import Md
from skytemple_files.hardcoded.dungeons import MapMarkerPlacement, HardcodedDungeons
from skytemple_files.hardcoded.personality_test_starters import HardcodedPersonalityTestStarters
from skytemple_files.hardcoded.rank_up_table import Rank, HardcodedRankUpTable
from skytemple_files.hardcoded.recruitment_tables import HardcodedRecruitmentTables
from skytemple_files.list.actor.model import ActorListBin

ACTOR_LIST = 'BALANCE/actor_list.bin'


class ListsModule(AbstractModule):
    """Module to modify lists."""
    @classmethod
    def depends_on(cls):
        return ['monster', 'map_bg']

    @classmethod
    def sort_order(cls):
        return 20

    def __init__(self, rom_project: RomProject):
        self.project = rom_project

        self._tree_model = None
        self._actor_tree_iter = None
        self._starters_tree_iter = None
        self._recruitment_tree_iter = None
        self._world_map_tree_iter = None
        self._rank_list_tree_iter = None

    def load_tree_items(self, item_store: TreeStore, root_node):
        root = item_store.append(root_node, [
            'view-list-symbolic', GROUND_LISTS, self, MainController, 0, False, '', True
        ])
        self._actor_tree_iter = item_store.append(root, [
            'view-list-symbolic', 'Actors', self, ActorListController, 0, False, '', True
        ])
        self._starters_tree_iter = item_store.append(root, [
            'view-list-symbolic', 'Starters', self, StartersListController, 0, False, '', True
        ])
        self._recruitment_tree_iter = item_store.append(root, [
            'view-list-symbolic', 'Recruitment List', self, RecruitmentListController, 0, False, '', True
        ])
        self._world_map_tree_iter = item_store.append(root, [
            'view-list-symbolic', 'World Map Markers', self, WorldMapController, 0, False, '', True
        ])
        self._rank_list_tree_iter = item_store.append(root, [
            'view-list-symbolic', 'Rank List', self, RankListController, 0, False, '', True
        ])
        generate_item_store_row_label(item_store[root])
        generate_item_store_row_label(item_store[self._actor_tree_iter])
        generate_item_store_row_label(item_store[self._starters_tree_iter])
        generate_item_store_row_label(item_store[self._recruitment_tree_iter])
        generate_item_store_row_label(item_store[self._world_map_tree_iter])
        generate_item_store_row_label(item_store[self._rank_list_tree_iter])
        self._tree_model = item_store

    def has_actor_list(self):
        return self.project.file_exists(ACTOR_LIST)

    def get_actor_list(self) -> ActorListBin:
        return self.project.open_sir0_file_in_rom(ACTOR_LIST, ActorListBin)

    def mark_actors_as_modified(self):
        """Mark as modified"""
        self.project.mark_as_modified(ACTOR_LIST)
        # Mark as modified in tree
        row = self._tree_model[self._actor_tree_iter]
        recursive_up_item_store_mark_as_modified(row)

    def mark_str_as_modified(self):
        self.project.get_string_provider().mark_as_modified()
        # Mark as modified in tree
        row = self._tree_model[self._starters_tree_iter]
        recursive_up_item_store_mark_as_modified(row)

    def get_monster_md(self) -> Md:
        return self.project.get_module('monster').monster_md

    def get_starter_ids(self) -> Tuple[List[int], List[int]]:
        """Returns players & partner starters"""
        ov13 = self.project.get_binary(BinaryName.OVERLAY_13)
        static_data = self.project.get_rom_module().get_static_data()
        player = HardcodedPersonalityTestStarters.get_player_md_ids(ov13, static_data)
        partner = HardcodedPersonalityTestStarters.get_partner_md_ids(ov13, static_data)
        return player, partner

    def set_starter_ids(self, player, partner):
        def update(ov13):
            static_data = self.project.get_rom_module().get_static_data()
            HardcodedPersonalityTestStarters.set_player_md_ids(player, ov13, static_data)
            HardcodedPersonalityTestStarters.set_partner_md_ids(partner, ov13, static_data)
        self.project.modify_binary(BinaryName.OVERLAY_13, update)

        row = self._tree_model[self._starters_tree_iter]
        recursive_up_item_store_mark_as_modified(row)

    def get_recruitment_list(self) -> Tuple[List[int], List[int], List[int]]:
        """Returns the recruitment lists: species, levels, locations"""
        ov11 = self.project.get_binary(BinaryName.OVERLAY_11)
        static_data = self.project.get_rom_module().get_static_data()
        species = HardcodedRecruitmentTables.get_monster_species_list(ov11, static_data)
        level = HardcodedRecruitmentTables.get_monster_levels_list(ov11, static_data)
        location = HardcodedRecruitmentTables.get_monster_locations_list(ov11, static_data)
        return species, level, location

    def set_recruitment_list(self, species, level, location):
        """Sets the recruitment lists: species, levels, locations"""
        def update(ov11):
            static_data = self.project.get_rom_module().get_static_data()
            HardcodedRecruitmentTables.set_monster_species_list(species, ov11, static_data)
            HardcodedRecruitmentTables.set_monster_levels_list(level, ov11, static_data)
            HardcodedRecruitmentTables.set_monster_locations_list(location, ov11, static_data)
        self.project.modify_binary(BinaryName.OVERLAY_11, update)

        row = self._tree_model[self._recruitment_tree_iter]
        recursive_up_item_store_mark_as_modified(row)

    def get_world_map_markers(self) -> List[MapMarkerPlacement]:
        """Returns the world map markers"""
        arm9bin = self.project.get_binary(BinaryName.ARM9)
        static_data = self.project.get_rom_module().get_static_data()
        markers = HardcodedDungeons.get_marker_placements(arm9bin, static_data)
        return markers

    def set_world_map_markers(self, markers: List[MapMarkerPlacement]):
        """Sets the world map markers"""
        def update(arm9bin):
            static_data = self.project.get_rom_module().get_static_data()
            HardcodedDungeons.set_marker_placements(markers, arm9bin, static_data)
        self.project.modify_binary(BinaryName.ARM9, update)

        row = self._tree_model[self._world_map_tree_iter]
        recursive_up_item_store_mark_as_modified(row)

    def get_rank_list(self) -> List[Rank]:
        """Returns the rank up table."""
        arm9bin = self.project.get_binary(BinaryName.ARM9)
        static_data = self.project.get_rom_module().get_static_data()
        return HardcodedRankUpTable.get_rank_up_table(arm9bin, static_data)

    def set_rank_list(self, values: List[Rank]):
        """Sets the rank up table."""
        def update(arm9bin):
            static_data = self.project.get_rom_module().get_static_data()
            HardcodedRankUpTable.set_rank_up_table(values, arm9bin, static_data)
        self.project.modify_binary(BinaryName.ARM9, update)

        row = self._tree_model[self._rank_list_tree_iter]
        recursive_up_item_store_mark_as_modified(row)
