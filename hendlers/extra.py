import random

from aiogram import types, Dispatcher
from config import bot, dp

# @dp.message_handler()
async def echo(message: types.Message):
    bad_words = ['bitch', 'dawn', 'java']
    for i in bad_words:
        if i in message.text.lower():
            await bot.send_message(message.chat.id, f"Не матерись {message.from_user.full_name}\n Это плохо!")
            await bot.delete_message(message.chat.id, message.message_id)


    if message.text.lower() == "dice":
        await bot.send_dice(message.chat.id, emoji='🎲')

    if message.text.lower() == "game":
        games = random.choice(['🎲', '🎳', '🎯', '⚽', '🏀', '🎰'])
        await bot.send_dice(message.chat.id, emoji=games)

def register_hendler_extra(dp: Dispatcher):
    dp.register_message_handler(echo)
