from utils.classes import Block
from utils.classes._helper import MiningLevel

from . import ORES

BLOCKS = {
    "background": Block(
        emoji=":bg:",
        rarity=0.0,
        tags=["mining"],
        drop=None,
        mining_level=MiningLevel.ANY, 
    ),
    "pedra": Block(
        emoji=":st:",
        rarity=0.0,
        tags=["mining"],
        drop=None,
        mining_level=MiningLevel.ANY,
    ),
    "carvao": Block(
        emoji=":co:",
        rarity=0.0,
        tags=["mining"],
        drop=ORES["carvao"],
        mining_level=MiningLevel.STONE_PICKAXE,
    ),
    "ferro": Block(
        emoji=":ir:",
        rarity=0.0,
        tags=["mining"],
        drop=ORES["ferro"],
        mining_level=MiningLevel.STONE_PICKAXE,
    ),
    "ouro": Block(
        emoji=":go:",
        rarity=0.0,
        tags=["mining"],
        drop=ORES["ouro"],
        mining_level=MiningLevel.IRON_PICKAXE,
    ),
    "rubi": Block(
        emoji=":ru:",
        rarity=0.0,
        tags=["mining"],
        drop=ORES["rubi"],
        mining_level=MiningLevel.GOLD_PICKAXE,
    ),
    "safira": Block(
        emoji=":sa:",
        rarity=0.0,
        tags=["mining"],
        drop=ORES["safira"],
        mining_level=MiningLevel.RUBY_PICKAXE,
    ),
    "esmeralda": Block(
        emoji=":em:",
        rarity=0.0,
        tags=["mining"],
        drop=ORES["esmeralda"],
        mining_level=MiningLevel.RUBY_PICKAXE,
    ),
    "diamante": Block(
        emoji=":di:",
        rarity=0.0,
        tags=["mining"],
        drop=ORES["diamante"],
        mining_level=MiningLevel.EMERALD_PICKAXE,
    ),
}