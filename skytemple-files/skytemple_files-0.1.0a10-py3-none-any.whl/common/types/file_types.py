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

from skytemple_files.compression.bma_collision_rle.handler import BmaCollisionRleHandler
from skytemple_files.compression.bma_layer_nrl.handler import BmaLayerNrlHandler
from skytemple_files.compression.bpc_image.handler import BpcImageHandler
from skytemple_files.compression.bpc_tilemap.handler import BpcTilemapHandler
from skytemple_files.compression.generic_nrl.handler import GenericNrlHandler
from skytemple_files.compression_container.pkdpx.handler import PkdpxHandler
from skytemple_files.container.bin_pack.handler import BinPackHandler
from skytemple_files.container.dungeon_bin.handler import DungeonBinHandler
from skytemple_files.container.dungeon_bin.sub.at4px_dpc import DbinAt4pxDpcHandler
from skytemple_files.container.dungeon_bin.sub.at4px_dpci import DbinAt4pxDpciHandler
from skytemple_files.container.dungeon_bin.sub.sir0_at4px import DbinSir0At4pxHandler
from skytemple_files.container.dungeon_bin.sub.sir0_at4px_dma import DbinSir0At4pxDmaHandler
from skytemple_files.container.dungeon_bin.sub.sir0_pkdpx import DbinSir0PkdpxHandler
from skytemple_files.container.dungeon_bin.sub.sir0_1035 import DbinSir01035Handler
from skytemple_files.container.dungeon_bin.sub.sir0_image_1033 import DbinSir0Image1033Handler
from skytemple_files.container.dungeon_bin.sub.sir0_image_1034 import DbinSir0Image1034Handler
from skytemple_files.container.dungeon_bin.sub.sir0_weird_data_file import DbinSir0WeirdDataFileHandler
from skytemple_files.container.dungeon_bin.sub.sir0_dpla import DbinSir0DplaHandler
from skytemple_files.container.sir0.handler import Sir0Handler
from skytemple_files.data.level_bin_entry.handler import LevelBinEntryHandler
from skytemple_files.data.md.handler import MdHandler
from skytemple_files.data.str.handler import StrHandler
from skytemple_files.data.waza_p.handler import WazaPHandler
from skytemple_files.dungeon_data.fixed_bin.handler import FixedBinHandler
from skytemple_files.dungeon_data.mappa_bin.handler import MappaBinHandler
from skytemple_files.dungeon_data.mappa_g_bin.handler import MappaGBinHandler
from skytemple_files.graphics.bgp.handler import BgpHandler
from skytemple_files.graphics.bma.handler import BmaHandler
from skytemple_files.graphics.bpa.handler import BpaHandler
from skytemple_files.graphics.bpc.handler import BpcHandler
from skytemple_files.graphics.bpl.handler import BplHandler
from skytemple_files.graphics.dma.handler import DmaHandler
from skytemple_files.graphics.dpc.handler import DpcHandler
from skytemple_files.graphics.dpci.handler import DpciHandler
from skytemple_files.graphics.dpl.handler import DplHandler
from skytemple_files.graphics.dpla.handler import DplaHandler
from skytemple_files.graphics.kao.handler import KaoHandler
from skytemple_files.compression_container.at4px.handler import At4pxHandler
from skytemple_files.compression_container.at4pn.handler import At4pnHandler
from skytemple_files.compression.px.handler import PxHandler
from skytemple_files.graphics.bg_list_dat.handler import BgListDatHandler
from skytemple_files.graphics.w16.handler import W16Handler
from skytemple_files.graphics.wan_wat.handler import WanHandler
from skytemple_files.graphics.wte.handler import WteHandler
from skytemple_files.graphics.wtu.handler import WtuHandler
from skytemple_files.list.actor.handler import ActorListBinHandler
from skytemple_files.script.lsd.handler import LsdHandler
from skytemple_files.script.ssa_sse_sss.handler import SsaHandler
from skytemple_files.script.ssb.handler import SsbHandler


class FileType:
    """A list of supported file types. Values are their data handlers."""
    UNKNOWN = None

    KAO = KaoHandler

    AT4PX = At4pxHandler
    PKDPX = PkdpxHandler
    AT4PN = At4pnHandler

    PX = PxHandler
    GENERIC_NRL = GenericNrlHandler

    BGP = BgpHandler

    BG_LIST_DAT = BgListDatHandler
    BPL = BplHandler
    BPC = BpcHandler
    BPC_IMAGE = BpcImageHandler
    BPC_TILEMAP = BpcTilemapHandler
    BMA = BmaHandler
    BMA_LAYER_NRL = BmaLayerNrlHandler
    BMA_COLLISION_RLE = BmaCollisionRleHandler
    BPA = BpaHandler

    DUNGEON_BIN = DungeonBinHandler
    DPL = DplHandler
    DPLA = DplaHandler
    DPC = DpcHandler
    DPCI = DpciHandler
    DMA = DmaHandler

    WTE = WteHandler
    WTU = WtuHandler

    WAN = WanHandler
    WAT = WanHandler

    W16 = W16Handler
    STR = StrHandler
    LSD = LsdHandler

    SSA = SsaHandler
    SSE = SsaHandler
    SSS = SsaHandler
    SSB = SsbHandler

    SIR0 = Sir0Handler
    BIN_PACK = BinPackHandler

    MD = MdHandler
    LEVEL_BIN_ENTRY = LevelBinEntryHandler
    WAZA_P = WazaPHandler

    # These handlers assume the content to be Sir0 wrapped by default:
    MAPPA_BIN = MappaBinHandler
    MAPPA_G_BIN = MappaGBinHandler
    FIXED_BIN = FixedBinHandler
    
    # dungeon.bin sub file handlers
    DBIN_SIR0_DPLA = DbinSir0DplaHandler
    DBIN_SIR0_AT4PX_DMA = DbinSir0At4pxDmaHandler
    DBIN_AT4PX_DPC = DbinAt4pxDpcHandler
    DBIN_AT4PX_DPCI = DbinAt4pxDpciHandler
    DBIN_SIR0_AT4PX = DbinSir0At4pxHandler
    DBIN_SIR0_PKDPX = DbinSir0PkdpxHandler
    DBIN_SIR0_WEIRD_DATA_FILE = DbinSir0WeirdDataFileHandler
    DBIN_SIR0_IMAGE_1033 = DbinSir0Image1033Handler
    DBIN_SIR0_IMAGE_1034 = DbinSir0Image1034Handler
    DBIN_SIR0_1035 = DbinSir01035Handler

    # Please don't use these directly, use them via the ppmdu_config instead!
    # (skytemple_files.common.util.get_ppmdu_config_for_rom).
    ACTOR_LIST_BIN = ActorListBinHandler
