from __future__ import annotations

import discord
import json

from typing import Dict
from pathlib import Path
from dataclasses import dataclass, field

from .Player import Player


@dataclass
class PlayerAccess:
    database: Database
    player: Player

    def __enter__(self) -> Player:
        return self.player

    def __exit__(self, _t, _v, _tb) -> None:
        self.database.update(self.player)


@dataclass
class Database:
    folder: Path
    players: Dict[int, Player] = field(default_factory=dict)

    def __post_init__(self) -> None:
        # Create the folder if it doesn't exist
        self.folder.mkdir(parents=True, exist_ok=True)

        for file in self.folder.iterdir():
            with open(file) as f:
                try:
                    player_dict = json.load(f)

                    player = Player.from_dict(player_dict)
                    player.inventory.__dict__ = player_dict["inventory"]
                except json.JSONDecodeError:
                    player = Player(int(file.stem))

                self.players[player.id] = player

    def modify(self, user_id) -> PlayerAccess:
        return PlayerAccess(database=self, player=self.get_player(user_id))

    def update(self, user: Player) -> None:
        with open(self.folder / f"{user.id}.json", "w") as f:
            player_dict = self.players[user.id].to_dict()
            player_dict["inventory"] = user.inventory.__dict__
            f.write(json.dumps(player_dict, indent=4))

    def get_player(self, user_id: int) -> Player:
        if not (user_id in self.players):
            with open(self.folder / f"{user_id}.json", "w") as f:
                player = Player(user_id)
                f.write(json.dumps(player.to_dict(), indent=4))
                self.players[user_id] = player

        return self.players[user_id]


db = Database(Path("./data/players"))
