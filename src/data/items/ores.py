from utils.classes import Ore

ORES = {
    "carvao": Ore(
        id="carvao",
        name="Carvão",
        emoji=":coal:",
        tags=["mining"],
        selling=15.75,
    ),
    "diamante": Ore(
        id="diamante",
        name="Diamante",
        emoji=":diamond:",
        tags=["mining"],
        selling=235.0,
    ),
    "esmeralda": Ore(
        id="esmeralda",
        name="Esmeralda",
        emoji=":emerald:",
        tags=["mining"],
        selling=79.0,
    ),
    "ferro": Ore(
        id="ferro",
        name="Ferro",
        emoji=":iron_ingot:",
        tags=["mining"],
        selling=36.75,
    ),
    "ouro": Ore(
        id="ouro",
        name="Ouro",
        emoji=":gold_ingot:",
        tags=["mining"],
        selling=68.25,
    ),
    "rubi": Ore(
        id="rubi",
        name="Rubi",
        emoji=":ruby:",
        tags=["mining"],
        selling=100.0,
    ),
    "safira": Ore(
        id="safira",
        name="Safira",
        emoji=":sapphire:",
        tags=["mining"],
        selling=115.0,
    ),
}
