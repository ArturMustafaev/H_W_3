from aiogram import types, Dispatcher
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text
from aiogram.dispatcher.filters.state import State, StatesGroup

from config import bot
from keyboards.client_kb import cancel_marcup

class FSMAdmin(StatesGroup):
    photo_dish = State()
    name_dish = State()
    discription_dish = State()
    price_dish = State()


async def fsm_start(message: types.Message):
    if message.chat.type == 'private':
        await FSMAdmin.photo_dish.set()
        await bot.send_message(message.chat.id, f"Отправте фото блюда...",
                               reply_markup=cancel_marcup)
    else:
        await message.answer("Пиши в личку!")


async def load_photo_dish(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['photo'] = message.photo[0].file_id
    await FSMAdmin.next()
    await message.answer("Как называется это блюдо?")


async def load_name_dish(message: types.Message, state:FSMContext):
    async with state.proxy() as data:
        data['name'] = message.text
    await FSMAdmin.next()
    await message.answer("Цена блюда?")


async def load_discription_dish(message: types.Message, state:FSMContext):
    try:
        async with state.proxy() as data:
            data['age'] = int(message.text)
        await FSMAdmin.next()
        await message.answer("Описание блюда?")
    except:
        await  message.answer("Только числа!!!")


async def load_price_dish(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['region'] = message.text
    await state.finish()
    await message.answer("Прекрасно, на этом ты свободен)")


async def cancel_registation(message: types.Message, state: FSMContext):
    current_state = await state.get_state()
    if current_state is None:
        return
    else:
        await state.finish()
        await message.reply("Регистрация отменена!")

def register_hendler_fsmadminmenu(dp: Dispatcher):
    dp.register_message_handler(cancel_registation, state='*', commands="cancel")
    dp.register_message_handler(cancel_registation, Text(equals='cancel', ignore_case=True), state='*')

    dp.register_message_handler(fsm_start, commands=['register_menu'])
    dp.register_message_handler(load_photo_dish, state=FSMAdmin.photo_dish, content_types=["photo"])
    dp.register_message_handler(load_name_dish, state=FSMAdmin.name_dish)
    dp.register_message_handler(load_discription_dish, state=FSMAdmin.discription_dish)
    dp.register_message_handler(load_price_dish, state=FSMAdmin.price_dish)
