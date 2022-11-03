from utils.classes import Boss

BOSSES = {
    "baleia": Boss(
        id="baleia",
        name="Baleia",
        emoji="🐋",
        tags=["fishing"],
        selling=70.0,
    ),
    "leao": Boss(
        id="leao",
        name="Leão",
        emoji="🦁",
        tags=["hunting"],
        selling=65.0,
    ),
    "lobo": Boss(
        id="lobo",
        name="Lobo",
        emoji="🐺",
        tags=["hunting"],
        selling=30.0,
    ),
    "morcego": Boss(
        id="morcego",
        name="Morcego",
        emoji="🦇",
        tags=["mining"],
        selling=120.0,
    ),
    "naja": Boss(
        id="naja",
        name="Naja",
        emoji="🐍",
        tags=["mining"],
        selling=120.0,
    ),
    "polvo": Boss(
        id="polvo",
        name="Polvo",
        emoji="🐙",
        tags=["fishing"],
        selling=95.0,
    ),
    "tarantula": Boss(
        id="tarantula",
        name="Tarantula",
        emoji="🕷️",
        tags=["mining"],
        selling=120.0,
    ),
    "tubarao": Boss(
        id="tubarao",
        name="Tubarão",
        emoji="🦈",
        tags=["fishing"],
        selling=120.0,
    ),
    "urso": Boss(
        id="urso",
        name="Urso",
        emoji="🐻",
        tags=["hunting"],
        selling=40.0,
    ),
}
