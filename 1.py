import asyncio
import logging
from aiogram import Bot, Dispatcher, types
from aiogram.dispatcher import FSMContext
from aiogram.contrib.middlewares.logging import LoggingMiddleware
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.utils import executor
from aiogram.contrib.fsm_storage.memory import MemoryStorage  # Import MemoryStorage
from config import bot_token,admin,channelLink

from keyboard import *
logging.basicConfig(level=logging.INFO)
bot = Bot(token=bot_token)
dp = Dispatcher(bot, storage=MemoryStorage())  # Set MemoryStorage to the Dispatcher
dp.middleware.setup(LoggingMiddleware())

class UserState(StatesGroup):
    waiting_for_til = State()
    waiting_for_name = State()
    waiting_for_age = State()
    waiting_for_science = State()
    waiting_for_choice = State()
    waiting_for_admin =  State()
    waiting_for_kanal =  State() 
    waiting_for_reg = State()
    waiting_for_ism = State()
    waiting_for_familya = State()
    waiting_for_telefon = State()
    waiting_for_tasdiqlash= State()
    waiting_for_tahrirlash = State()
    waiting_for_sendAdmin = State()
    waiting_for_menu = State()
    waiting_for_ismEdit = State()
    waiting_for_familyaEdit = State()
    waiting_for_telEdit = State()
    waiting_for_fanEdit = State()
    

@dp.message_handler(commands=['start'])
async def start(message: types.Message):
    await message.reply("Assalomu alaykum! tilni tanlang:",reply_markup=keyboard)
    await UserState.waiting_for_til.set()


@dp.message_handler(commands=['menu'],state=UserState.waiting_for_menu)
async def start(message: types.Message,state: FSMContext):
    data= await state.get_data()
    lang=data.get('selected_language')
    if lang == 'uzbek':
        await message.reply(text=f"{til[lang]['choice']}",reply_markup=uz_keyboard_choice)
    elif lang == 'russian':
        await message.reply(text=f"{til[lang]['choice']}",reply_markup=ru_keyboard_choice)
    
    await UserState.waiting_for_choice.set()

@dp.callback_query_handler(lambda query: query.data in ['uzbek', 'russian'], state=UserState.waiting_for_til)
async def process_language(callback_query: types.CallbackQuery, state: FSMContext):
    selected_language = callback_query.data
    lang=selected_language
    await state.update_data(selected_language=selected_language)
    if selected_language == 'uzbek':
        await bot.send_message(callback_query.from_user.id, f"Siz O'zbek tilini tanladingiz.")
        await bot.send_message(callback_query.from_user.id,text=f"{til[lang]['choice']}",reply_markup=uz_keyboard_choice)
    elif selected_language == 'russian':
        await bot.send_message(callback_query.from_user.id, f"Вы выбрали русский язык.")
        await bot.send_message(callback_query.from_user.id,text=f"{til[lang]['choice']}",reply_markup=ru_keyboard_choice)
    
    await UserState.waiting_for_choice.set()
    await bot.delete_message(callback_query.from_user.id,callback_query.message.message_id)

@dp.callback_query_handler(lambda query: True, state=UserState.waiting_for_choice)
async def process(callback_query: types.CallbackQuery, state: FSMContext):
    choice = callback_query.data
    data= await state.get_data()
    lang=data.get('selected_language')
    if choice == 'reg':
        await bot.send_message(callback_query.from_user.id, text=f"{til[lang]['ism']}")
        await UserState.waiting_for_ism.set()
    elif choice == 'kanal':
        await bot.send_message(callback_query.from_user.id,text=f"{til[lang]['Kanal']}:{channelLink}\n{til[lang]['toMenu']}")
        await UserState.waiting_for_menu.set()
    elif choice == 'admin':
        await bot.send_message(callback_query.from_user.id,text=f"{til[lang]['Admin']}:{channelLink}\n{til[lang]['toMenu']}")
        await UserState.waiting_for_menu.set()
    await bot.delete_message(callback_query.from_user.id,callback_query.message.message_id)

@dp.message_handler(state=UserState.waiting_for_ism)
async def ism(message: types.Message, state: FSMContext):
    name = message.text
    data= await state.get_data()
    lang=data.get('selected_language')
    await state.update_data(name=name)
    await message.reply(f"{til[lang]['familya']}")
    await UserState.waiting_for_familya.set()


@dp.message_handler(state=UserState.waiting_for_familya)
async def familya(message: types.Message, state: FSMContext):
    data= await state.get_data()
    lang=data.get('selected_language')
    familya = message.text
    await state.update_data(familya=familya)
    if lang == "uzbek":
        await message.reply(f"{til[lang]['fan']}",reply_markup=uz_fanlar_keyboard)
    elif lang =="russian":
        await message.reply(f"{til[lang]['fan']}",reply_markup=ru_fanlar_keyboard)
    await UserState.waiting_for_science.set()

@dp.callback_query_handler(lambda query: query.data in uz_fanlar, state=UserState.waiting_for_science)
async def process(callback_query: types.CallbackQuery, state: FSMContext):
    data= await state.get_data()
    lang=data.get('selected_language')
    science = callback_query.data
    await state.update_data(science=science)
    if lang=="uzbek":
        await bot.send_message(callback_query.from_user.id,text=f"{til[lang]['tel']}",reply_markup=uz_telefon)
    elif lang =="russian":
        await bot.send_message(callback_query.from_user.id,text=f"{til[lang]['tel']}",reply_markup=ru_telefon)
    await UserState.waiting_for_telefon.set()

    await bot.delete_message(callback_query.from_user.id,callback_query.message.message_id)

@dp.message_handler(content_types=['contact'],state=UserState.waiting_for_telefon)
async def process_name(message: types.Message, state: FSMContext):
    telefon = message.contact.phone_number
    await state.update_data(telefon=telefon)
    data=await state.get_data()
    lang=data.get('selected_language')
    name=data.get("name")
    familya=data.get("familya")
    science=data.get("science")
    await bot.send_message(message.from_user.id,text=f"{til[lang]['ok']}",reply_markup=types.ReplyKeyboardRemove())
    if lang=="uzbek":
        await message.reply(f"{til[lang]['Ism']} {name}\n{til[lang]['Familya']} {familya}\n{til[lang]['Tel']} {telefon}\n{til[lang]['Fan']} {science}\n-------------------------\n{til[lang]['check']}",reply_markup=uz_tasdiqlash)
    elif lang =="russian":
        science=ru_fanlar[uz_fanlar.index(science)]
        await message.reply(f"{til[lang]['Ism']} {name}\n{til[lang]['Familya']} {familya}\n{til[lang]['Tel']} {telefon}\n{til[lang]['Fan']} {science}\n-------------------------\n{til[lang]['check']}",reply_markup=ru_tasdiqlash)
    
    await UserState.waiting_for_tasdiqlash.set() 

@dp.callback_query_handler(lambda query: query.data in ["tasdiqlash","tahrirlash"], state=UserState.waiting_for_tasdiqlash)
async def process(callback_query: types.CallbackQuery, state: FSMContext):

    data=await state.get_data()
   
    if callback_query.data=="tasdiqlash":
        name=data.get("name")
        familya=data.get("familya")
        science=data.get("science")
        telefon=data.get("telefon")
        lang=data.get("selected_language")
        if lang=="russian":science=ru_fanlar[uz_fanlar.index(science)]
        user_id = callback_query.from_user.id 
        user_name = callback_query.from_user.first_name 
        mention = "["+user_name+"](tg://user?id="+str(user_id)+")"
        username=callback_query.from_user.username
        await bot.send_message(chat_id=int(-1001990101304),text=f"{til[lang]['Ism']} {name}\n{til[lang]['Familya']} {familya}\n{til[lang]['Tel']} {telefon}\n{til[lang]['Fan']} {science}\nContact 1: @{username}\nContact 2:{mention}",parse_mode="Markdown")
        await bot.send_message(callback_query.from_user.id,text=f"{til[lang]['yuborildi']}")
        await UserState.waiting_for_menu.set()
    elif callback_query.data=="tahrirlash":
        lang=data.get("selected_language")
        if lang=='uzbek':
            markup=uz_select_keyboard
        elif lang=="russian":
            markup=ru_select_keyboard
        await bot.send_message(callback_query.from_user.id,f"{til[lang]['select']}",reply_markup=markup)
        await UserState.waiting_for_tahrirlash.set()
    await bot.delete_message(callback_query.from_user.id,callback_query.message.message_id)

@dp.callback_query_handler(lambda query: True, state=UserState.waiting_for_tahrirlash)
async def process(callback_query: types.CallbackQuery, state: FSMContext):
    data = await state.get_data()
    lang = data.get("selected_language")
    if callback_query.data=="ism":
        await bot.send_message(callback_query.from_user.id, text=f"{til[lang]['ism']}")
        await UserState.waiting_for_ismEdit.set()
    elif callback_query.data=="familya":
        await bot.send_message(callback_query.from_user.id, text=f"{til[lang]['familya']}")
        await UserState.waiting_for_familyaEdit.set()
    elif callback_query.data=="tel":
        await bot.send_message(callback_query.from_user.id, text=f"{til[lang]['etel']}")
        await UserState.waiting_for_telEdit.set()
    elif callback_query.data=="fan":
        if lang=='uzbek':
            markup=uz_fanlar_keyboard
        elif lang=="russian":
            markup=ru_fanlar_keyboard
        await bot.send_message(callback_query.from_user.id, text=f"{til[lang]['fan']}",reply_markup=markup)
        await UserState.waiting_for_fanEdit.set()
    await bot.delete_message(callback_query.from_user.id,callback_query.message.message_id)

@dp.message_handler(state=UserState.waiting_for_ismEdit)
async def ismEdit(message: types.Message, state: FSMContext):
    name = message.text
    data= await state.get_data()
    lang=data.get('selected_language')
    await state.update_data(name=name)
    data=await state.get_data()
    lang=data.get('selected_language')
    name=data.get("name")
    familya=data.get("familya")
    science=data.get("science")
    telefon=data.get("telefon")
    await bot.send_message(message.from_user.id,text=f"{til[lang]['ok']}",reply_markup=types.ReplyKeyboardRemove())
    if lang=="uzbek":
        await message.reply(f"{til[lang]['Ism']} {name}\n{til[lang]['Familya']} {familya}\n{til[lang]['Tel']} {telefon}\n{til[lang]['Fan']} {science}\n-------------------------\n{til[lang]['check']}",reply_markup=uz_tasdiqlash)
    elif lang =="russian":
        science=ru_fanlar[uz_fanlar.index(science)]
        await message.reply(f"{til[lang]['Ism']} {name}\n{til[lang]['Familya']} {familya}\n{til[lang]['Tel']} {telefon}\n{til[lang]['Fan']} {science}\n-------------------------\n{til[lang]['check']}",reply_markup=ru_tasdiqlash)
    
    await UserState.waiting_for_tasdiqlash.set()
    

@dp.message_handler(state=UserState.waiting_for_familyaEdit)
async def familyaEdit(message: types.Message, state: FSMContext):
    familya = message.text
    await state.update_data(familya=familya)
    data=await state.get_data()
    lang=data.get('selected_language')
    name=data.get("name")
    familya=data.get("familya")
    science=data.get("science")
    telefon=data.get("telefon")
    await bot.send_message(message.from_user.id,text=f"{til[lang]['ok']}",reply_markup=types.ReplyKeyboardRemove())
    if lang=="uzbek":
        await message.reply(f"{til[lang]['Ism']} {name}\n{til[lang]['Familya']} {familya}\n{til[lang]['Tel']} {telefon}\n{til[lang]['Fan']} {science}\n-------------------------\n{til[lang]['check']}",reply_markup=uz_tasdiqlash)
    elif lang =="russian":
        science=ru_fanlar[uz_fanlar.index(science)]
        await message.reply(f"{til[lang]['Ism']} {name}\n{til[lang]['Familya']} {familya}\n{til[lang]['Tel']} {telefon}\n{til[lang]['Fan']} {science}\n-------------------------\n{til[lang]['check']}",reply_markup=ru_tasdiqlash)
    
    await UserState.waiting_for_tasdiqlash.set()

@dp.message_handler(state=UserState.waiting_for_familyaEdit)
async def familyaEdit(message: types.Message, state: FSMContext):
    familya = message.text
    await state.update_data(familya=familya)
    data=await state.get_data()
    lang=data.get('selected_language')
    name=data.get("name")
    familya=data.get("familya")
    science=data.get("science")
    telefon=data.get("telefon")
    await bot.send_message(message.from_user.id,text=f"{til[lang]['ok']}",reply_markup=types.ReplyKeyboardRemove())
    if lang=="uzbek":
        await message.reply(f"{til[lang]['Ism']} {name}\n{til[lang]['Familya']} {familya}\n{til[lang]['Tel']} {telefon}\n{til[lang]['Fan']} {science}\n-------------------------\n{til[lang]['check']}",reply_markup=uz_tasdiqlash)
    elif lang =="russian":
        science=ru_fanlar[uz_fanlar.index(science)]
        await message.reply(f"{til[lang]['Ism']} {name}\n{til[lang]['Familya']} {familya}\n{til[lang]['Tel']} {telefon}\n{til[lang]['Fan']} {science}\n-------------------------\n{til[lang]['check']}",reply_markup=ru_tasdiqlash)
    
    await UserState.waiting_for_tasdiqlash.set()

@dp.message_handler(state=UserState.waiting_for_telEdit)
async def telEdit(message: types.Message, state: FSMContext):
    telefon = message.text
    await state.update_data(telefon=telefon)
    data=await state.get_data()
    lang=data.get('selected_language')
    name=data.get("name")
    familya=data.get("familya")
    science=data.get("science")
    telefon=data.get("telefon")
    await bot.send_message(message.from_user.id,text=f"{til[lang]['ok']}",reply_markup=types.ReplyKeyboardRemove())
    if lang=="uzbek":
        await message.reply(f"{til[lang]['Ism']} {name}\n{til[lang]['Familya']} {familya}\n{til[lang]['Tel']} {telefon}\n{til[lang]['Fan']} {science}\n-------------------------\n{til[lang]['check']}",reply_markup=uz_tasdiqlash)
    elif lang =="russian":
        science=ru_fanlar[uz_fanlar.index(science)]
        await message.reply(f"{til[lang]['Ism']} {name}\n{til[lang]['Familya']} {familya}\n{til[lang]['Tel']} {telefon}\n{til[lang]['Fan']} {science}\n-------------------------\n{til[lang]['check']}",reply_markup=ru_tasdiqlash)
    
    await UserState.waiting_for_tasdiqlash.set()

@dp.callback_query_handler(lambda query: query.data in uz_fanlar, state=UserState.waiting_for_fanEdit)
async def fanEdit(callback_query: types.CallbackQuery, state: FSMContext):
    data= await state.get_data()
    lang=data.get('selected_language')
    science = callback_query.data
    await state.update_data(science=science)
    data=await state.get_data()
    lang=data.get('selected_language')
    name=data.get("name")
    familya=data.get("familya")
    science=data.get("science")
    telefon=data.get("telefon")
    await bot.send_message(callback_query.from_user.id,text=f"{til[lang]['ok']}",reply_markup=types.ReplyKeyboardRemove())
    if lang=="uzbek":
        await bot.send_message(callback_query.from_user.id,f"{til[lang]['Ism']} {name}\n{til[lang]['Familya']} {familya}\n{til[lang]['Tel']} {telefon}\n{til[lang]['Fan']} {science}\n-------------------------\n{til[lang]['check']}",reply_markup=uz_tasdiqlash)
    elif lang =="russian":
        science=ru_fanlar[uz_fanlar.index(science)]
        await bot.send_message(callback_query.from_user.id,f"{til[lang]['Ism']} {name}\n{til[lang]['Familya']} {familya}\n{til[lang]['Tel']} {telefon}\n{til[lang]['Fan']} {science}\n-------------------------\n{til[lang]['check']}",reply_markup=ru_tasdiqlash)
    
    await UserState.waiting_for_tasdiqlash.set()
    await bot.delete_message(callback_query.from_user.id,callback_query.message.message_id)
async def on_startup(dispatcher):
    # Botni ishga tushirish
    await dispatcher.start_polling()

if __name__ == '__main__':
    executor.start_polling(dp, on_startup=on_startup)
