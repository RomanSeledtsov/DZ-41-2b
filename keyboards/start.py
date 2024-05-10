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
    markup = InlineKeyboardMarkup(
        inline_keyboard=[
            [registration_button],
            [my_profile_button],
            [profile_button]
        ]
    )
    return markup
