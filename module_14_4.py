from aiogram import Bot, Dispatcher, types, executor
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import StatesGroup, State
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardButton, InlineKeyboardMarkup
import asyncio
import config
from crud_functions import get_all_products


class UserState(StatesGroup):
    age = State()
    growth = State()
    weight = State()

bot = Bot(token=config.TOKEN)
dp = Dispatcher(bot, storage=MemoryStorage())

btn_main_menu = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton('Рассчитать'),
            KeyboardButton('Информация')
        ],
        [
            KeyboardButton('Купить')
        ]
    ],resize_keyboard=True)

inline_button_calcul = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text='Рассчитать норму калорий', callback_data='calories'),
            InlineKeyboardButton(text='Формулы расчёта', callback_data='formulas')
        ]
    ]
)

inline_button_products = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text='Продукт 1', callback_data='product_buying'),
            InlineKeyboardButton(text='Продукт 2', callback_data='product_buying'),
            InlineKeyboardButton(text='Продукт 3', callback_data='product_buying'),
            InlineKeyboardButton(text='Продукт 4', callback_data='product_buying')
        ]
    ]
)

@dp.message_handler(commands=['start'])
async def start(message: types.Message):
    await message.answer('Привет! Я бот помогающий твоему здоровью.', reply_markup=btn_main_menu)


@dp.message_handler(text="Рассчитать")
async def main_menu(message):
    await message.answer('Выберите опцию', reply_markup=inline_button_calcul)


@dp.message_handler(text="Информация")
async def btn_info(message: types.Message):
    await message.answer('Информация о боте')

@dp.message_handler(text="Купить")
async def get_buying_list(message: types.Message):
    data = get_all_products()
    for i in range(3):
        with open(f'BAA/pr{i+1}.jpg', 'rb') as prod:
            await message.answer_photo(prod, f"Название: {data[i][1]} | Описание: {data[i][2]} | Цена: {data[i][3]}")
    with open(f'BAA/pr{4}.jpg', 'rb') as prod:
        await message.answer_photo(prod, f"Название: {data[3][1]} | Описание: {data[3][2]} | Цена: {data[3][3]}", reply_markup=inline_button_products)



@dp.message_handler()
async def all_messages(message: types.Message):
    await message.answer("Введите команду /start, чтобы начать общение.")

@dp.callback_query_handler(text="product_buying")
async def send_confirm_message(call):
    await call.message.answer('Вы успешно приобрели продукт!')
    await call.answer()

@dp.callback_query_handler(text="formulas")
async def get_formulas(call):
    await call.message.answer('10 х вес (кг) + 6,25 x рост (см) – 5 х возраст (г) + 5')
    await call.answer()


@dp.callback_query_handler(text="calories")
async def set_age(call):
    await call.message.answer('Введите свой возраст:')
    await UserState.age.set()


@dp.message_handler(state=UserState.age)
async def set_growth(message: types.Message, state: FSMContext):
    await state.update_data(age=message.text)
    await message.answer('Введите свой рост:')
    await UserState.growth.set()


@dp.message_handler(state=UserState.growth)
async def set_weight(message: types.Message, state: FSMContext):
    await state.update_data(growth=message.text)
    await message.answer('Введите свой вес:')
    await UserState.weight.set()


@dp.message_handler(state=UserState.weight)
async def send_calories(message: types.Message, state: FSMContext):
    await state.update_data(weight=message.text)
    data = await state.get_data()
    calcul_calories = 10 * int(data['weight']) + 6.25 * int(data['growth']) - 5 * int(data['age']) + 5
    await message.answer(f'Ваши калории составляют: {round(calcul_calories, 2)}')
    await state.finish()


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)