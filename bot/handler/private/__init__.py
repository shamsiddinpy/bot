from aiogram import Router

from bot.handler.private.main_handler import handler_start_router
from bot.handler.private.start_check import star_check_router

private_handler_router = Router()
private_handler_router.include_routers(
    handler_start_router,
    star_check_router
)
