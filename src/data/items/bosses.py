from utils.classes import Boss, Tags

BOSSES = {
    "baleia": Boss(
        id="baleia",
        name="Baleia",
        emoji="🐋",
        tags=[Tags.FISHING],
        selling=70.0,
    ),
    "leao": Boss(
        id="leao",
        name="Leão",
        emoji="🦁",
        tags=[Tags.HUNTING],
        selling=65.0,
    ),
    "lobo": Boss(
        id="lobo",
        name="Lobo",
        emoji="🐺",
        tags=[Tags.HUNTING],
        selling=30.0,
    ),
    "morcego": Boss(
        id="morcego",
        name="Morcego",
        emoji="🦇",
        tags=[Tags.MINING],
        selling=120.0,
    ),
    "naja": Boss(
        id="naja",
        name="Naja",
        emoji="🐍",
        tags=[Tags.MINING],
        selling=120.0,
    ),
    "polvo": Boss(
        id="polvo",
        name="Polvo",
        emoji="🐙",
        tags=[Tags.FISHING],
        selling=95.0,
    ),
    "tarantula": Boss(
        id="tarantula",
        name="Tarantula",
        emoji="🕷️",
        tags=[Tags.MINING],
        selling=120.0,
    ),
    "tubarao": Boss(
        id="tubarao",
        name="Tubarão",
        emoji="🦈",
        tags=[Tags.FISHING],
        selling=120.0,
    ),
    "urso": Boss(
        id="urso",
        name="Urso",
        emoji="🐻",
        tags=[Tags.HUNTING],
        selling=40.0,
    ),
}
