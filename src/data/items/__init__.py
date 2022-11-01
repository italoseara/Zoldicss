from .bosses import *
from .consumable import *
from .economy import *
from .misc import *
from .ores import *
from .tools import *

ITEMS = {
    **CONSUMABLES,
    **BOSSES,
    **ECONOMY,
    **MISC,
    **ORES,
    **TOOLS,
}

CRAFTABLES = {item.id: item for item in ITEMS.values() if item.crafting}
