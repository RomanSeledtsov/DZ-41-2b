from aiogram.types import (
    InlineKeyboardButton,
    InlineKeyboardMarkup
)


async def reference_menu_keyboard():
    link_button = InlineKeyboardButton(
        text="Link 🔗",
        callback_data="reference_link"
    )
    balance_button = InlineKeyboardButton(
        text="Balance 💸",
        callback_data="reference_balance"
    )
    reference_links_button = InlineKeyboardButton(
        text="Your ref links 👨‍💼",
        callback_data="list_reference"
    )
    markup = InlineKeyboardMarkup(
        inline_keyboard=[
            [link_button],
            [balance_button],
            [reference_links_button],
        ]
    )
    return markup
