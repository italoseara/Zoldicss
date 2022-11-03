from utils.classes import Tool

TOOLS = {
    "picaretadepedra": Tool(
        id="picaretadepedra",
        name="Picareta De Pedra",
        emoji=":stone_pickaxe:",
        tags=["pickaxe"],
        buying=300.0,
        durability=100,
    ),
    "picaretadeferro": Tool(
        id="picaretadeferro",
        name="Picareta De Ferro",
        emoji=":iron_pickaxe:",
        tags=["pickaxe"],
        durability=200,
        crafting={
            "picaretadepedra": 1,
            "ferro": 15,
            "graveto": 5,
            "cipo": 5,
        }
    ),
    "picaretadeouro": Tool(
        id="picaretadeouro",
        name="Picareta De Ouro",
        emoji=":golden_pickaxe:",
        tags=["pickaxe"],
        durability=150,
        crafting={
            "picaretadeferro": 1,
            "ouro": 15,
            "graveto": 5,
            "cipo": 5,
        }
    ),
    "picaretadesafira": Tool(
        id="picaretadesafira",
        name="Picareta De Safira",
        emoji=":sapphire_pickaxe:",
        tags=["pickaxe"],
        durability=350,
        crafting={
            "picaretadeouro": 1,
            "safira": 10,
            "graveto": 5,
            "cipo": 5,
        }
    ),
    "picaretaderubi": Tool(
        id="picaretaderubi",
        name="Picareta De Rubi",
        emoji=":ruby_pickaxe:",
        tags=["pickaxe"],
        durability=500,
        crafting={
            "picaretadesafira": 1,
            "rubi": 10,
            "graveto": 5,
            "cipo": 5,
        }
    ),
    "picaretadeesmeralda": Tool(
        id="picaretadeesmeralda",
        name="Picareta De Esmeralda",
        emoji=":emerald_pickaxe:",
        tags=["pickaxe"],
        durability=750,
        crafting={
            "picaretaderubi": 1,
            "esmeralda": 10,
            "graveto": 5,
            "cipo": 5,
        }
    ),
    "picaretadediamante": Tool(
        id="picaretadediamante",
        name="Picareta De Diamante",
        emoji=":diamond_pickaxe:",
        tags=["pickaxe"],
        durability=1000,
        crafting={
            "picaretadeesmeralda": 1,
            "diamante": 10,
            "graveto": 5,
            "cipo": 5,
        }
    ),
}
