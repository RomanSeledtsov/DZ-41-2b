from aiogram.types import (
    InlineKeyboardButton,
    InlineKeyboardMarkup
)


async def start_menu_keyboard_registration():
    registration_button = InlineKeyboardButton(
        text="Registration",
        callback_data="registration"
    )
    profile_button = InlineKeyboardButton(
        text="My profile",
        callback_data="profile"
    )
    markup = InlineKeyboardMarkup(
        inline_keyboard=[
            [registration_button],
            [profile_button]
        ]
    )
    return markup
