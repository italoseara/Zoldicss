from utils.classes.Item import Economy

ECONOMY = {
    "banco": Economy(
        id="banco",
        name="Conta Bancária",
        emoji="🏦",
        buying=5000.0,
        add_bank=1000.0,
    ),
    "cartao": Economy(
        id="cartao",
        name="Cartão De Crédito",
        emoji="💳",
        buying=1500.0,
        add_bank=500.0,
    ),
    "cheque": Economy(
        id="cheque",
        name="Cheque $500.00",
        emoji="📜",
        buying=510.0,
        add_wallet=500.0,
    ),
}
