from aiogram.types import (
    InlineKeyboardButton,
    InlineKeyboardMarkup
)


async def start_menu_keyboard_registration():
    registration_button = InlineKeyboardButton(
        text="Registration 💥",
        callback_data="registration"
    )
    my_profile_button = InlineKeyboardButton(
        text="My profile 😎",
        callback_data="my_profile"
    )
    profile_button = InlineKeyboardButton(
        text="View profile 🤔",
        callback_data="view_profiles"
    )
    reference_button = InlineKeyboardButton(
        text="Reference menu 👨‍💼",
        callback_data="reference_menu"
    )
    like_history_button = InlineKeyboardButton(
        text="Liked Profiles ❤️",
        callback_data="history"
    )
    wallet_button = InlineKeyboardButton(
        text="Wallet 💰",
        callback_data="wallet_",
    )
    ur_money_button = InlineKeyboardButton(
        text="Send Money 🤝",
        callback_data="money_",
    )
    grammar_button = InlineKeyboardButton(
        text="Grammar lessons",
        callback_data="grammar",
    )
    markup = InlineKeyboardMarkup(
        inline_keyboard=[
            [registration_button],
            [my_profile_button],
            [profile_button],
            [reference_button],
            [like_history_button],
            [wallet_button],
            [ur_money_button],
            [grammar_button],
        ]
    )
    return markup
