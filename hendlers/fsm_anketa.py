from aiogram import types, Dispatcher
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text
from aiogram.dispatcher.filters.state import State, StatesGroup

from config import bot
from keyboards.client_kb import cancel_marcup

class FSMAdmin(StatesGroup):
    photo = State()
    name = State()
    surname = State()
    age = State()
    region = State()


async def fsm_start(message: types.Message):
    if message.chat.type == 'private':
        await FSMAdmin.photo.set()
        await bot.send_message(message.chat.id, f"Привет {message.from_user.full_name}, скинь фотку...",
                               reply_markup=cancel_marcup)
    else:
        await message.answer("Пиши в личку!")


async def load_photo(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['photo'] = message.photo[0].file_id
    await FSMAdmin.next()
    await message.answer("Как тебя зовут?")


async def load_name(message: types.Message, state:FSMContext):
    async with state.proxy() as data:
        data['name'] = message.text
    await FSMAdmin.next()
    await message.answer("Какая фамилия?")

async def load_surname(message: types.Message, state:FSMContext):
    async with state.proxy() as data:
        data['surname'] = message.text
    await FSMAdmin.next()
    await message.answer("Сколько лет?")


async def load_age(message: types.Message, state:FSMContext):
    try:
        async with state.proxy() as data:
            data['age'] = int(message.text)
        await FSMAdmin.next()
        await message.answer("Где живешь?")
    except:
        await  message.answer("Только числа!!!")


async def load_region(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['region'] = message.text
    await state.finish()
    await message.answer("Свободен)")

async def cancel_registation(message: types.Message, state: FSMContext):
    current_state = await state.get_state()
    if current_state is None:
        return
    else:
        await state.finish()
        await message.reply("Регистрация отменена!")

def register_hendler_fsmanketa(dp: Dispatcher):
    dp.register_message_handler(cancel_registation, state='*', commands="cancel")
    dp.register_message_handler(cancel_registation, Text(equals='cancel', ignore_case=True), state='*')

    dp.register_message_handler(fsm_start, commands=['register'])
    dp.register_message_handler(load_photo, state=FSMAdmin.photo, content_types=["photo"])
    dp.register_message_handler(load_name, state=FSMAdmin.name)
    dp.register_message_handler(load_surname, state=FSMAdmin.surname)
    dp.register_message_handler(load_age, state=FSMAdmin.age)
    dp.register_message_handler(load_region, state=FSMAdmin.region)
