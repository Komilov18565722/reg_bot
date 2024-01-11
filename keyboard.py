from aiogram import types
from dict import *
keyboard = types.InlineKeyboardMarkup()
uz_button = types.InlineKeyboardButton(text="Uzbek", callback_data="uzbek")
rus_button = types.InlineKeyboardButton(text="Русский", callback_data="russian")
keyboard.add(uz_button, rus_button)
uz_keyboard_choice = types.InlineKeyboardMarkup(row_width=2)
uz_reg_button = types.InlineKeyboardButton(text=uz_reg,callback_data="reg")
uz_kanal_button = types.InlineKeyboardButton(text=uz_kanal,callback_data="kanal")
uz_admin_button = types.InlineKeyboardButton(text=uz_admin,callback_data="admin")
uz_keyboard_choice.add(uz_reg_button,uz_kanal_button,uz_admin_button)
ru_keyboard_choice = types.InlineKeyboardMarkup(row_width=2, )
ru_reg_button = types.InlineKeyboardButton(text=ru_reg,callback_data="reg")
ru_kanal_button = types.InlineKeyboardButton(text=ru_kanal,callback_data="kanal")
ru_admin_button = types.InlineKeyboardButton(text=ru_admin,callback_data="admin")
ru_keyboard_choice.add(ru_reg_button,ru_kanal_button,ru_admin_button)
uz_fanlar_keyboard = types.InlineKeyboardMarkup(row_width=1)
for i in uz_fanlar:
    a= types.InlineKeyboardButton(text=i,callback_data=f"{i}")
    uz_fanlar_keyboard.add(a)
ru_fanlar_keyboard = types.InlineKeyboardMarkup(row_width=1)
for i in ru_fanlar:
    a= types.InlineKeyboardButton(text=i,callback_data=f"{uz_fanlar[ru_fanlar.index(i)]}")
    ru_fanlar_keyboard.add(a)
uz_telefon = types.ReplyKeyboardMarkup()
uz_telefon.add(types.KeyboardButton(text="Jo'natish",request_contact=True))
ru_telefon = types.ReplyKeyboardMarkup()
ru_telefon.add(types.KeyboardButton(text="Отправить",request_contact=True))
uz_tasdiqlash = types.InlineKeyboardMarkup()
uz_tasdiqlash.add(types.InlineKeyboardButton(text="Tasdiqlash" ,callback_data="tasdiqlash"),types.InlineKeyboardButton(text="Tahrirlash" ,callback_data="tahrirlash"))
ru_tasdiqlash = types.InlineKeyboardMarkup()
ru_tasdiqlash.add(types.InlineKeyboardButton(text="Подтверждение:" ,callback_data="tasdiqlash"),types.InlineKeyboardButton(text="Редактирование" ,callback_data="tahrirlash"))
uz_select_keyboard = types.InlineKeyboardMarkup()
uz_select_keyboard.add(types.InlineKeyboardButton(text="Ism",callback_data="ism"),types.InlineKeyboardButton(text="Familya",callback_data="familya"),types.InlineKeyboardButton(text="Telefon raqam",callback_data="tel"),types.InlineKeyboardButton(text="Fan",callback_data="fan"))
ru_select_keyboard = types.InlineKeyboardMarkup()
ru_select_keyboard.add(types.InlineKeyboardButton(text="Имя",callback_data="ism"),types.InlineKeyboardButton(text="Фамилия",callback_data="familya"),types.InlineKeyboardButton(text="Номер телефон",callback_data="tel"),types.InlineKeyboardButton(text="Знание",callback_data="fan"))
