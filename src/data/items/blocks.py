from utils.classes import Block
from utils.classes._helper import MiningLevel

from . import ORES

BLOCKS = {
    "background": Block(
        emoji=":bg:",
        chance=0.0,
        tags=["mining"],
        drop=None,
        mining_level=MiningLevel.ANY,
    ),
    "pedra": Block(
        emoji=":st:",
        chance=0.90,
        tags=["mining"],
        drop=None,
        mining_level=MiningLevel.ANY,
    ),
    "carvao": Block(
        emoji=":co:",
        chance=0.05,
        tags=["mining"],
        drop=ORES["carvao"],
        mining_level=MiningLevel.STONE_PICKAXE,
    ),
    "ferro": Block(
        emoji=":ir:",
        chance=0.02,
        tags=["mining"],
        drop=ORES["ferro"],
        mining_level=MiningLevel.STONE_PICKAXE,
    ),
    "ouro": Block(
        emoji=":go:",
        chance=0.02,
        tags=["mining"],
        drop=ORES["ouro"],
        mining_level=MiningLevel.IRON_PICKAXE,
    ),
    "rubi": Block(
        emoji=":ru:",
        chance=0.01,
        tags=["mining"],
        drop=ORES["rubi"],
        mining_level=MiningLevel.GOLD_PICKAXE,
    ),
    "safira": Block(
        emoji=":sa:",
        chance=0.0,
        tags=["mining"],
        drop=ORES["safira"],
        mining_level=MiningLevel.RUBY_PICKAXE,
    ),
    "esmeralda": Block(
        emoji=":em:",
        chance=0.0,
        tags=["mining"],
        drop=ORES["esmeralda"],
        mining_level=MiningLevel.RUBY_PICKAXE,
    ),
    "diamante": Block(
        emoji=":di:",
        chance=0.0,
        tags=["mining"],
        drop=ORES["diamante"],
        mining_level=MiningLevel.EMERALD_PICKAXE,
    ),
}
