from aiogram.types import (
    InlineKeyboardButton,
    InlineKeyboardMarkup
)


async def like_dislike_keyboard(tg_id):
    like_button = InlineKeyboardButton(
        text="Like👍",
        callback_data=f"like_{tg_id}"
    )
    dislike_button = InlineKeyboardButton(
        text="Dislike👎",
        callback_data=f"dislike_{tg_id}"
    )
    markup = InlineKeyboardMarkup(
        inline_keyboard=[
            [like_button],
            [dislike_button],
        ]
    )
    return markup
