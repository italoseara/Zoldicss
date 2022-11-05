from utils.classes import Block, MiningLevel, Tags

from . import ORES

BLOCKS = {
    "background": Block(
        emoji=":bg:",
        chance=0.0,
        tags=[Tags.MINING],
        drop=None,
        mining_level=MiningLevel.ANY,
    ),
    "pedra": Block(
        emoji=":st:",
        chance=90.2,
        tags=[Tags.MINING],
        drop=None,
        mining_level=MiningLevel.ANY,
    ),
    "carvao": Block(
        emoji=":co:",
        chance=4.5,
        tags=[Tags.MINING],
        drop=ORES["carvao"],
        mining_level=MiningLevel.STONE_PICKAXE,
    ),
    "ferro": Block(
        emoji=":ir:",
        chance=2.5,
        tags=[Tags.MINING],
        drop=ORES["ferro"],
        mining_level=MiningLevel.STONE_PICKAXE,
    ),
    "ouro": Block(
        emoji=":go:",
        chance=1.5,
        tags=[Tags.MINING],
        drop=ORES["ouro"],
        mining_level=MiningLevel.IRON_PICKAXE,
    ),
    "rubi": Block(
        emoji=":ru:",
        chance=0.5,
        tags=[Tags.MINING],
        drop=ORES["rubi"],
        mining_level=MiningLevel.GOLD_PICKAXE,
    ),
    "safira": Block(
        emoji=":sa:",
        chance=0.4,
        tags=[Tags.MINING],
        drop=ORES["safira"],
        mining_level=MiningLevel.RUBY_PICKAXE,
    ),
    "esmeralda": Block(
        emoji=":em:",
        chance=0.6,
        tags=[Tags.MINING],
        drop=ORES["esmeralda"],
        mining_level=MiningLevel.RUBY_PICKAXE,
    ),
    "diamante": Block(
        emoji=":di:",
        chance=0.3,
        tags=[Tags.MINING],
        drop=ORES["diamante"],
        mining_level=MiningLevel.EMERALD_PICKAXE,
    ),
}
