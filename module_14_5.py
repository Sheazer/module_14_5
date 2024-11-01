from aiogram import Bot, Dispatcher, executor, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from crud_functions import *

import asyncio

api = '7346802944:AAE-'
Bot = Bot(token=api)
dp = Dispatcher(Bot, storage=MemoryStorage())

kb = ReplyKeyboardMarkup(resize_keyboard=True)
button = KeyboardButton(text='Рассчитать')
button2 = KeyboardButton(text='Информация')
button3 = KeyboardButton(text='Купить')
button4 = KeyboardButton(text='Регистрация')
kb.row(button, button2)
kb.row(button3)
kb.row(button4)

inline_kb = InlineKeyboardMarkup()
button1 = InlineKeyboardButton(text='Рассчитать норму калорий', callback_data='Calories')
button2 = InlineKeyboardButton(text='Формулы расчета', callback_data='Formulas')
inline_kb.add(button1, button2)

inline_bud_kb = InlineKeyboardMarkup()
btn1 = InlineKeyboardButton(text='Product1', callback_data='product_buying')
btn2 = InlineKeyboardButton(text='Product2', callback_data='product_buying')
btn3 = InlineKeyboardButton(text='Product3', callback_data='product_buying')
btn4 = InlineKeyboardButton(text='Product4', callback_data='product_buying')
inline_bud_kb.row(btn1, btn2, btn3, btn4)


class UserState(StatesGroup):
    age = State()
    growth = State()
    weight = State()


class RegistrationState(StatesGroup):
    username = State()
    email = State()
    age = State()


@dp.message_handler(commands=['start'])
async def start(message):
    await message.answer('Привет! Я бот помогающий твоему здоровью!', reply_markup=kb)


@dp.message_handler(text='Информация')
async def info(message):
    await message.answer('Это бот Эржана!')


@dp.message_handler(text='Рассчитать')
async def show(message):
    await message.answer('Выберите опцию:', reply_markup=inline_kb)


@dp.message_handler(text='Купить')
async def buy_bud(message):
    products = get_all_products()
    for product in products:
        with open(f'files/pic{product[0]}.jpg', 'rb') as img:
            await message.answer(f'Название: {product[1]} Описание: {product[2]}| Цена: {product[3]}')
            await message.answer_photo(img)
    await message.answer(text='Выберите продукт для покупки', reply_markup=inline_bud_kb)


@dp.callback_query_handler(text='product_buying')
async def succes_buyed(call):
    await call.message.answer("Вы успешно приобрели продукт!")
    await call.answer()


@dp.callback_query_handler(text='Formulas')
async def formula(call):
    await call.message.answer('для мужчин: 10 х вес (кг) + 6,25 x рост (см) – 5 х возраст (г) + 5;')
    await call.answer()


@dp.callback_query_handler(text='Calories')
async def set_age(call):
    await call.message.answer('Введите ваш возраст:')
    await UserState.age.set()
    await call.answer()


@dp.message_handler(state=UserState.age)
async def set_growth(message, state):
    await state.update_data(age=message.text)
    await message.answer('Введите свой рост:')
    await UserState.growth.set()


@dp.message_handler(state=UserState.growth)
async def set_weight(message, state):
    await state.update_data(growth=message.text)
    await message.answer('Введите свой вес:')
    await UserState.weight.set()


@dp.message_handler(state=UserState.weight)
async def send_calories(message, state):
    await state.update_data(weight=message.text)
    data = await state.get_data()
    result = 10 * int(data['weight']) + 6.25 * int(data['growth']) - 5 * int(data['age']) + 5
    await message.answer(f"{result} ккал вам нужно в день")
    await state.finish()


@dp.message_handler(text='Регистрация')
async def sign_up(message):
    await message.answer('Введите имя пользователя (только латинский алфавит):')
    await RegistrationState.username.set()


@dp.message_handler(state=RegistrationState.username)
async def set_username(message, state):
    if is_included(message.text):
        await message.answer('Пользователь существует, введите другое имя')
        await RegistrationState.username.set()
    else:
        await state.update_data(username=message.text)
        await message.answer("Введите свой email:")
        await RegistrationState.email.set()


@dp.message_handler(state=RegistrationState.email)
async def set_email(message, state):
    await state.update_data(email=message.text)
    await message.answer('Введите свой возраст:')
    await RegistrationState.age.set()


@dp.message_handler(state=RegistrationState.age)
async def set_age(message, state):
    await state.update_data(age=message.text)
    data = await state.get_data()
    add_user(data['username'], data['email'], int(data['age']))
    await state.finish()
    await message.answer('Success registration!')


@dp.message_handler()
async def alls_message(message):
    await message.answer('Введите команду /start, чтобы начать общение.')


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
