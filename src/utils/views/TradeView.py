import asyncio
from datetime import datetime
from dataclasses import dataclass, field

import discord
from discord.ext import commands
from discord import ButtonStyle, SelectOption
from discord.ui import View, Button, button, Select, select

from data.items import *
from utils.classes.Player import Player
from utils.messages import default_embed, select_amount, warning

from utils.consts import EMOJIS


MENU_OPTIONS = [
    SelectOption(
        emoji="💵",
        label="Dinheiro",
        value="menu__money",
    ),
    SelectOption(
        emoji="🦁",
        label="Bosses",
        value="menu__bosses",
    ),
    SelectOption(
        emoji="🍌",
        label="Consumíveis",
        value="menu__consumable",
    ),
    SelectOption(
        emoji="🪙",
        label="Economia",
        value="menu__economy",
    ),
    SelectOption(
        emoji=EMOJIS["diamond"],
        label="Minérios",
        value="menu__ores",
    ),
    SelectOption(
        emoji="🔨",
        label="Ferramentas",
        value="menu__tools",
    ),
    SelectOption(
        emoji="🧩",
        label="Diversos",
        value="menu__misc",
    ),
]


@dataclass
class Trade:
    @dataclass
    class User:
        ready: bool = False

        money: int = 0
        selected: dict = field(default_factory=dict)

        profile: Player = None
        user: discord.Member = None
        interaction: discord.Interaction = None

        @property
        def offer(self) -> str:
            return "\n".join(
                f"{amount}x {ITEMS[item]}" for item, amount in self.selected.items()
            )

    canceled: bool = False
    finished: bool = False
    author: User = field(default_factory=User)
    target: User = field(default_factory=User)

    bot: commands.Bot = None

    async def wait(self) -> None:
        while not self.finished:
            await asyncio.sleep(0.1)


class TradeView(View):
    def __init__(self, trade: Trade, trade_embed: callable, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.trade = trade
        self.trade_embed = trade_embed

    @select(
        placeholder="Menu Principal",
        options=MENU_OPTIONS,
    )
    async def select_items(
        self, select: Select, interaction: discord.Interaction
    ) -> None:
        await interaction.response.defer()

        option = select.values[0]
        ctx = await self.trade.bot.get_application_context(interaction)
        interaction_author = (
            self.trade.author
            if interaction.user == self.trade.author.user
            else self.trade.target
        )

        match option:
            case "menu__money":
                if not interaction_author.profile.balance:
                    await warning(
                        ctx, "Você não possui dinheiro para negociar.", delete_after=5
                    )
                    return

                interaction_author.money = await select_amount(
                    self.trade.bot,
                    ctx,
                    message="Selecione a quantidade de 💵 Dinheiro que você deseja oferecer.",
                    max_value=int(interaction_author.profile.balance),
                )

                await asyncio.wait(
                    [
                        asyncio.create_task(
                            self.trade.author.interaction.edit(embed=self.trade_embed())
                        ),
                        asyncio.create_task(
                            self.trade.target.interaction.edit(embed=self.trade_embed())
                        ),
                    ],
                    return_when=asyncio.ALL_COMPLETED,
                )

            case "menu__consumable":
                select.placeholder = "Consumíveis"
                select.options = [
                    SelectOption(
                        emoji="⬅️",
                        label="Voltar para o menu",
                        value="menu__back",
                    ),
                    *(
                        SelectOption(
                            emoji=item.partial_emoji(),
                            label=item.name,
                            value=item.id,
                        )
                        for item in CONSUMABLES.values()
                    ),
                ]

            case "menu__bosses":
                select.placeholder = "Bosses"
                select.options = [
                    SelectOption(
                        emoji="⬅️",
                        label="Voltar para o menu",
                        value="menu__back",
                    ),
                    *(
                        SelectOption(
                            emoji=item.partial_emoji(),
                            label=item.name,
                            value=item.id,
                        )
                        for item in BOSSES.values()
                    ),
                ]

            case "menu__economy":
                select.placeholder = "Economia"
                select.options = [
                    SelectOption(
                        emoji="⬅️",
                        label="Voltar para o menu",
                        value="menu__back",
                    ),
                    *(
                        SelectOption(
                            emoji=item.partial_emoji(),
                            label=item.name,
                            value=item.id,
                        )
                        for item in ECONOMY.values()
                    ),
                ]

            case "menu__ores":
                select.placeholder = f"Minérios"
                select.options = [
                    SelectOption(
                        emoji="⬅️",
                        label="Voltar para o menu",
                        value="menu__back",
                    ),
                    *(
                        SelectOption(
                            emoji=item.partial_emoji(),
                            label=item.name,
                            value=item.id,
                        )
                        for item in ORES.values()
                    ),
                ]

            case "menu__tools":
                select.placeholder = "Ferramentas"
                select.options = [
                    SelectOption(
                        emoji="⬅️",
                        label="Voltar para o menu",
                        value="menu__back",
                    ),
                    *(
                        SelectOption(
                            emoji=item.partial_emoji(),
                            label=item.name,
                            value=item.id,
                        )
                        for item in TOOLS.values()
                    ),
                ]

            case "menu__misc":
                select.placeholder = "Diversos"
                select.options = [
                    SelectOption(
                        emoji="⬅️",
                        label="Voltar para o menu",
                        value="menu__back",
                    ),
                    *(
                        SelectOption(
                            emoji=item.partial_emoji(),
                            label=item.name,
                            value=item.id,
                        )
                        for item in MISC.values()
                    ),
                ]

            case "menu__back":
                select.placeholder = "Menu Principal"
                select.options = [
                    SelectOption(
                        emoji="💵",
                        label="Dinheiro",
                        value="menu__money",
                    ),
                    SelectOption(
                        emoji="🦁",
                        label="Bosses",
                        value="menu__bosses",
                    ),
                    SelectOption(
                        emoji="🍌",
                        label="Consumíveis",
                        value="menu__consumable",
                    ),
                    SelectOption(
                        emoji="🪙",
                        label="Economia",
                        value="menu__economy",
                    ),
                    SelectOption(
                        emoji=EMOJIS["diamond"],
                        label="Minérios",
                        value="menu__ores",
                    ),
                    SelectOption(
                        emoji="🔨",
                        label="Ferramentas",
                        value="menu__tools",
                    ),
                    SelectOption(
                        emoji="🧩",
                        label="Diversos",
                        value="menu__misc",
                    ),
                ]

            case "menu__misc":
                select.placeholder = "Diversos"
                select.options = [
                    SelectOption(
                        emoji="⬅️",
                        label="Voltar para o menu",
                        value="menu__back",
                    ),
                    *(
                        SelectOption(
                            emoji=item.partial_emoji(),
                            label=item.name,
                            value=item.id,
                        )
                        for item in MISC.values()
                    ),
                ]

            case "menu__back":
                select.placeholder = "Menu Principal"
                select.options = MENU_OPTIONS

            case _:
                max_amount = interaction_author.profile.inventory[option]

                if max_amount == 0:
                    await ctx.send(
                        embed=default_embed(
                            ctx.author,
                            color=0xEA3333,
                            title=f"Você não possui {ITEMS[option]} em seu inventário.",
                        ),
                        delete_after=5,
                    )
                    return

                amount = await select_amount(
                    self.trade.bot,
                    ctx,
                    message=f"Selecione ou digite a quantidade de {ITEMS[option]} que deseja trocar.",
                    max_value=max_amount,
                )

                if interaction_author.ready:
                    return

                interaction_author.selected[option] = amount

                await asyncio.wait(
                    [
                        asyncio.create_task(
                            self.trade.author.interaction.edit(embed=self.trade_embed())
                        ),
                        asyncio.create_task(
                            self.trade.target.interaction.edit(embed=self.trade_embed())
                        ),
                    ],
                    return_when=asyncio.ALL_COMPLETED,
                )

        await interaction.message.edit(view=self)

    @button(label="Cancelar", emoji="❌", style=ButtonStyle.grey, custom_id="cancel")
    async def cancel(self, button: Button, interaction: discord.Interaction) -> None:
        self.trade.canceled = True
        interaction_author = (
            self.trade.author
            if interaction.user == self.trade.author.user
            else self.trade.target
        )
        interaction_target = (
            self.trade.target
            if interaction.user == self.trade.author.user
            else self.trade.author
        )

        await asyncio.wait(
            [
                asyncio.create_task(
                    interaction_author.interaction.edit(
                        embed=default_embed(
                            interaction_author.user,
                            title="Troca cancelada",
                            description=f"Você cancelou a troca com {interaction_target.user.mention}.",
                        ),
                        view=None,
                    )
                ),
                asyncio.create_task(
                    interaction_target.interaction.edit(
                        embed=default_embed(
                            interaction_target.user,
                            title="Troca Cancelada",
                            description=f"{interaction_author.user.mention} cancelou a troca com você.",
                        ),
                        view=None,
                    )
                ),
            ],
            return_when=asyncio.ALL_COMPLETED,
        )

        await interaction.response.defer()

    @button(
        label="Estou pronto!", style=ButtonStyle.green, emoji="👍", custom_id="ready"
    )
    async def ready(self, button: Button, interaction: discord.Interaction) -> None:
        button.label = (
            "Estou pronto!"
            if button.label == "Não estou pronto!"
            else "Não estou pronto!"
        )
        button.emoji = "👍" if button.label == "Estou pronto!" else "👎"
        button.style = (
            ButtonStyle.green if button.style == ButtonStyle.grey else ButtonStyle.grey
        )

        interaction_author = (
            self.trade.author
            if interaction.user == self.trade.author.user
            else self.trade.target
        )

        # toggle select options
        self.children[0].disabled = not self.children[0].disabled

        await interaction.response.edit_message(view=self)

        interaction_author.ready = not interaction_author.ready

        await asyncio.wait(
            [
                asyncio.create_task(
                    self.trade.author.interaction.edit(embed=self.trade_embed())
                ),
                asyncio.create_task(
                    self.trade.target.interaction.edit(embed=self.trade_embed())
                ),
            ],
            return_when=asyncio.ALL_COMPLETED,
        )

        # Check if both users are ready
        if self.trade.author.ready and self.trade.target.ready:

            if (not self.trade.author.selected and not self.trade.target.selected) and (
                self.trade.author.money == 0 and self.trade.target.money == 0
            ):
                return

            # Wait 5 seconds to confirm the trade, but if one of the users cancel the trade, cancel the trade
            for i in range(3):
                # Show in the embed that the trade is being confirmed
                await asyncio.wait(
                    [
                        asyncio.create_task(
                            self.trade.author.interaction.edit(
                                embed=self.trade_embed(
                                    f"⏳ Confirmando troca em {3 - i}..."
                                )
                            )
                        ),
                        asyncio.create_task(
                            self.trade.target.interaction.edit(
                                embed=self.trade_embed(
                                    f"⏳ Confirmando troca em {3 - i}..."
                                )
                            )
                        ),
                    ],
                    return_when=asyncio.ALL_COMPLETED,
                )

                await asyncio.sleep(1)

                if self.trade.canceled or not (
                    self.trade.author.ready and self.trade.target.ready
                ):
                    return

            # Confirm the trade
            for item, amount in self.trade.author.selected.items():
                self.trade.author.profile.inventory.remove(item, amount)
                self.trade.target.profile.inventory.add(item, amount)

            for item, amount in self.trade.target.selected.items():
                self.trade.target.profile.inventory.remove(item, amount)
                self.trade.author.profile.inventory.add(item, amount)

            # Exchange the money
            self.trade.author.profile.balance -= self.trade.author.money
            self.trade.target.profile.balance -= self.trade.target.money

            self.trade.author.profile.balance += self.trade.target.money
            self.trade.target.profile.balance += self.trade.author.money

            author_embed = default_embed(
                self.trade.author.user,
                title="Troca confirmada",
                description=f"Você trocou com {self.trade.target.user.mention}.\n\u2800",
            )
            author_embed.add_field(
                name="⬇️ Recebido",
                value=(
                    f"**Dinheiro**: ${self.trade.target.money:.2f}\n\n"
                    + (
                        "\n".join(
                            f"{ITEMS[item]} x{amount}"
                            for item, amount in self.trade.target.selected.items()
                        )
                        or "Nenhum Item"
                    )
                    + "\n\u2800"
                ),
            )
            author_embed.add_field(
                name="⬆️ Enviado",
                value=(
                    f"**Dinheiro**: ${self.trade.author.money:.2f}\n\n"
                    + (
                        "\n".join(
                            f"{ITEMS[item]} x{amount}"
                            for item, amount in self.trade.author.selected.items()
                        )
                        or "Nenhum Item"
                    )
                    + "\n\u2800"
                ),
            )
            author_embed.set_footer(
                text=f"Troca concluída em {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}"
            )

            target_embed = default_embed(
                self.trade.target.user,
                title="Troca confirmada",
                description=f"Você trocou com {self.trade.author.user.mention}.\n\u2800",
            )
            target_embed.add_field(
                name="⬇️ Recebido",
                value=(
                    f"**Dinheiro**: ${self.trade.author.money:.2f}\n\n"
                    + (
                        "\n".join(
                            f"{ITEMS[item]} x{amount}"
                            for item, amount in self.trade.author.selected.items()
                        )
                        or "Nenhum Item"
                    )
                    + "\n\u2800"
                ),
            )
            target_embed.add_field(
                name="⬆️ Enviado",
                value=(
                    f"**Dinheiro**: ${self.trade.target.money:.2f}\n\n"
                    + (
                        "\n".join(
                            f"{ITEMS[item]} x{amount}"
                            for item, amount in self.trade.target.selected.items()
                        )
                        or "Nenhum Item"
                    )
                    + "\n\u2800"
                ),
            )
            target_embed.set_footer(
                text=f"Troca concluída em {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}"
            )

            await asyncio.wait(
                [
                    asyncio.create_task(
                        self.trade.author.interaction.edit(
                            embed=author_embed, view=None, delete_after=None
                        )
                    ),
                    asyncio.create_task(
                        self.trade.target.interaction.edit(
                            embed=target_embed, view=None, delete_after=None
                        )
                    ),
                ],
                return_when=asyncio.ALL_COMPLETED,
            )

            self.trade.finished = True


class AuthorView(View):
    def __init__(self, trade: Trade, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.trade = trade

    @button(label="Cancelar", style=ButtonStyle.grey, emoji="❌", custom_id="cancel")
    async def cancel(self, button: Button, interaction: discord.Interaction) -> None:
        self.trade.canceled = True

        await asyncio.wait(
            [
                asyncio.create_task(
                    self.trade.author.interaction.edit(
                        embed=default_embed(
                            self.trade.author.user,
                            title="Troca Cancelada",
                            description=f"Você cancelou a troca com {self.trade.target.mention}.",
                        ),
                        view=None,
                    )
                ),
                asyncio.create_task(
                    self.trade.target.interaction.edit(
                        embed=default_embed(
                            self.target.user,
                            title="Troca Cancelada",
                            description=f"{self.trade.author.user.mention} cancelou a troca com você.",
                        ),
                        view=None,
                    )
                ),
            ],
            return_when=asyncio.ALL_COMPLETED,
        )

        await interaction.response.defer()


class TargetView(View):
    def __init__(self, trade: Trade, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.trade = trade

    @button(label="Aceitar", style=ButtonStyle.grey, emoji="✅", custom_id="accept")
    async def accept(self, button: Button, interaction: discord.Interaction) -> None:
        def trade_embed(title="Proposta de troca") -> discord.Embed:
            embed = default_embed(
                self.trade.author.user,
                title=title,
                description="Selecione os itens que deseja trocar.\n\u2800",
                color=0x66FF66
                if (self.trade.author.ready and self.trade.target.ready)
                else 0xEA3333,
            )

            embed.add_field(
                name=f"{'✅' if self.trade.author.ready else '❌'} {self.trade.author.user}"
                + ("\u2800" * 3),
                value=(
                    f"**Dinheiro**: ${self.trade.author.money:.2f}\n\n"
                    + (self.trade.author.offer or "Nenhum item selecionado")
                    + "\n\u2800"
                ),
            )
            embed.add_field(
                name=f"{'✅' if self.trade.target.ready else '❌'} {self.trade.target.user}",
                value=(
                    f"**Dinheiro**: ${self.trade.target.money:.2f}\n\n"
                    + (self.trade.target.offer or "Nenhum item selecionado")
                    + "\n\u2800"
                ),
            )
            embed.set_footer(
                text="Clique em 'Estou pronto!' quando terminar de selecionar os itens."
            )

            return embed

        await asyncio.wait(
            [
                asyncio.create_task(
                    self.trade.author.interaction.edit(
                        embed=trade_embed(),
                        view=TradeView(self.trade, trade_embed),
                        delete_after=300,
                    )
                ),
                asyncio.create_task(
                    self.trade.target.interaction.edit(
                        embed=trade_embed(),
                        view=TradeView(self.trade, trade_embed),
                        delete_after=300,
                    )
                ),
            ],
            return_when=asyncio.ALL_COMPLETED,
        )

        await interaction.response.defer()

    @button(label="Recusar", style=ButtonStyle.grey, emoji="❌", custom_id="deny")
    async def deny(self, button: Button, interaction: discord.Interaction) -> None:
        await asyncio.wait(
            [
                asyncio.create_task(
                    self.trade.author.interaction.edit(
                        embed=default_embed(
                            self.trade.author.user,
                            title=f"{self.trade.target.user} recusou sua proposta de troca.",
                        ),
                        view=None,
                    )
                ),
                asyncio.create_task(
                    self.trade.target.interaction.edit(
                        embed=default_embed(
                            self.trade.target.user,
                            title=f"Você recusou a proposta de troca de {self.trade.author.user}.",
                        ),
                        view=None,
                    )
                ),
            ],
            return_when=asyncio.ALL_COMPLETED,
        )

        await interaction.response.defer()
