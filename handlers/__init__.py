from aiogram import Router


def setup_routers() -> Router:
    from . import (
        start,
        registration,
        like_dislike,
        profile,
        delete,
        Reference,
    )

    router = Router()
    router.include_router(start.router)
    router.include_router(registration.router)
    router.include_router(like_dislike.router)
    router.include_router(profile.router)
    router.include_router(delete.router)
    router.include_router(Reference.router)

    return router
