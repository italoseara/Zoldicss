from utils.classes import Boss, Tags

BOSSES = {
    "baleia": Boss(
        id="baleia",
        name="Baleia",
        emoji="๐",
        tags=[Tags.FISHING],
        selling=70.0,
    ),
    "leao": Boss(
        id="leao",
        name="Leรฃo",
        emoji="๐ฆ",
        tags=[Tags.HUNTING],
        selling=65.0,
    ),
    "lobo": Boss(
        id="lobo",
        name="Lobo",
        emoji="๐บ",
        tags=[Tags.HUNTING],
        selling=30.0,
    ),
    "morcego": Boss(
        id="morcego",
        name="Morcego",
        emoji="๐ฆ",
        tags=[Tags.MINING],
        selling=120.0,
    ),
    "naja": Boss(
        id="naja",
        name="Naja",
        emoji="๐",
        tags=[Tags.MINING],
        selling=120.0,
    ),
    "polvo": Boss(
        id="polvo",
        name="Polvo",
        emoji="๐",
        tags=[Tags.FISHING],
        selling=95.0,
    ),
    "tarantula": Boss(
        id="tarantula",
        name="Tarantula",
        emoji="๐ท๏ธ",
        tags=[Tags.MINING],
        selling=120.0,
    ),
    "tubarao": Boss(
        id="tubarao",
        name="Tubarรฃo",
        emoji="๐ฆ",
        tags=[Tags.FISHING],
        selling=120.0,
    ),
    "urso": Boss(
        id="urso",
        name="Urso",
        emoji="๐ป",
        tags=[Tags.HUNTING],
        selling=40.0,
    ),
}
