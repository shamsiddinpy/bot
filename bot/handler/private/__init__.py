from aiogram import Router

from bot.handler.private.main_handler import handler_start_router

private_handler_router = Router()
private_handler_router.include_routers(
    handler_start_router
)
