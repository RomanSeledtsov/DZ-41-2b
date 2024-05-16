from aiogram import Router


def setup_routers() -> Router:
    from . import (
        start,
        registration,
        like_dislike,
        profile,
        delete,
        Reference,
        donate,
        like_history,
        wallet,
    )

    router = Router()
    router.include_router(start.router)
    router.include_router(registration.router)
    router.include_router(like_dislike.router)
    router.include_router(profile.router)
    router.include_router(delete.router)
    router.include_router(Reference.router)
    router.include_router(donate.router)
    router.include_router(like_history.router)
    router.include_router(wallet.router)

    return router
