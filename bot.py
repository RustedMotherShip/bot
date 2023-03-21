from aiogram import Bot, types
from aiogram.dispatcher import Dispatcher
from aiogram.utils import executor
from datetime import date
from datetime import datetime

from config import TOKEN,spravka,greeting,admins,admin_id,master_id
from config import vopros1,vopros2,vopros3,vopros4,vopros5,vopros6,vopros7
from keyboard import kb1,kb2,kb3,kb6,kb7,menu_selector,rec_start,KeyBoard,day_s,back_kb
from db import DBWorker,User
from bandb import DBBan,UserBan

from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.contrib.fsm_storage.memory import MemoryStorage

from aiogram.types import InlineKeyboardButton

storage=MemoryStorage()
bot = Bot(token=TOKEN)
dp = Dispatcher(bot, storage=storage)
DBW=DBWorker()
DBB=DBBan()
class SS(StatesGroup):
    v1_answer = State()
    v2_answer = State()
    v3_answer = State()
    v4_answer = State()
    v5_answer = State()
    v6_answer = State()
    v7_answer = State()

    complete =State()
    admin = State()
    menu = State()

    banhammer1 = State()
    banhammer2 = State()
    ban_complete = State()

ck = KeyBoard()

#команда старт
@dp.message_handler(commands=['start'])
async def start_command(message: types.Message):
    await message.answer(greeting,reply_markup=await menu_selector(ck))

#меню
@dp.callback_query_handler(state=SS.menu)
async def record_call(call: types.CallbackQuery,state: FSMContext):
    await bot.send_message(text="Меню",reply_markup=await menu_selector(ck), chat_id=call.from_user.id)
    await state.set_state(None)

#вывод справки
@dp.callback_query_handler(text='info')
async def call_spravka(call: types.CallbackQuery):
    await bot.send_message(text=spravka,chat_id=call.from_user.id)

#контакты
@dp.callback_query_handler(text='admins')
async def call_spravka(call: types.CallbackQuery):
    await bot.send_message(text=admins,chat_id=call.from_user.id)
#---------------------
'''
     if ck.checker = True:
         await state.set_state(SS.)
     else:
'''
#запись на точку

@dp.callback_query_handler(text='record', state=None)
async def record_start(call: types.CallbackQuery,state: FSMContext):
    print(call.data)
    if await ck.checker(call.data) == True:
        await bot.send_message(text="Тогда заполни простую форму!",reply_markup=await rec_start(ck), chat_id=call.from_user.id)
        await state.set_state(SS.v1_answer)

@dp.callback_query_handler(state=SS.v1_answer)
async def q1(call: types.CallbackQuery,state: FSMContext):
    print(call.data)
    if await ck.checker(call.data) == True:
        await bot.send_message(text=vopros1,reply_markup=await kb1(ck),chat_id=call.from_user.id)
        await state.set_state(SS.v2_answer)

@dp.callback_query_handler(state=SS.v2_answer)
async def q2(call: types.CallbackQuery,state: FSMContext):
    print(call.data)
    if await ck.checker(call.data) == True:
        await state.update_data(rec_day=call.data)
        await bot.send_message(text=vopros2,reply_markup=await kb2(ck), chat_id=call.from_user.id)
        await state.set_state(SS.v3_answer)

@dp.callback_query_handler(state=SS.v3_answer)
async def q3(call: types.CallbackQuery,state: FSMContext):
    print(call.data)
    if await ck.checker(call.data) == True:
        await state.update_data(kol_vo=call.data)
        data = await state.get_data()
        await bot.send_message(text=vopros3,reply_markup=await kb3(ck,data['rec_day'],call.data), chat_id=call.from_user.id)
        await state.set_state(SS.v4_answer)

@dp.callback_query_handler(state=SS.v4_answer)
async def q4(call: types.CallbackQuery,state: FSMContext):
    print(call.data)
    if await ck.checker(call.data) == True:
        await state.update_data(vremya=call.data)
        await bot.send_message(text=vopros4, chat_id=call.from_user.id)
        await state.set_state(SS.v5_answer)

@dp.message_handler(state=SS.v5_answer)
async def q5(message: types.Message,state: FSMContext):
    await state.update_data(cont=message.text)
    await bot.send_message(text=vopros5, chat_id=message.from_user.id) 
    await state.set_state(SS.v6_answer)

@dp.message_handler(state=SS.v6_answer)
async def q6(message: types.Message,state: FSMContext):
        await state.update_data(name=message.text)
        await bot.send_message(text=vopros6,reply_markup=await kb6(ck), chat_id=message.from_user.id) 
        await state.set_state(SS.v7_answer)

@dp.callback_query_handler(state=SS.v7_answer)
async def q7(call: types.CallbackQuery,state: FSMContext):
    if await ck.checker(call.data) == True:
        await state.update_data(q1_answ=call.data)
        await bot.send_message(text=vopros7,reply_markup=await kb7(ck), chat_id=call.from_user.id)
        await state.set_state(SS.complete)

@dp.callback_query_handler(state=SS.complete)
async def success(call: types.CallbackQuery,state: FSMContext):
    if await ck.checker(call.data) == True:
        await state.update_data(q2_answ=call.data)
        data = await state.get_data()
        dater=data['rec_day'].split('.')  
        adder = User(data['name'],data['kol_vo'],data['q1_answ'],data['q2_answ'],date(datetime.now().year,int(dater[1]),int(dater[0])),data['vremya'],data['cont'],call.from_user.id)
        banchecker = DBB.check_ban(call.from_user.id)
        print(banchecker)
        print(data['vremya'])
        print(data['rec_day'])
        if (banchecker == True) or (data['vremya'] == 'error') or (data['rec_day'] == 'error'):
            await bot.send_message(text="Ошибка или вы забаненны.Нажмите,чтобы выйти",reply_markup=await back_kb(ck), chat_id=call.from_user.id)
        else:
            await bot.send_message(text="Успешно!Нажмите,чтобы выйти",reply_markup=await back_kb(ck), chat_id=call.from_user.id)
            await DBW.add_user(adder)

            printer = "У вас новая запись!\n" + \
            '👤Название' + ' - ' + str(data['name']) + '\n' + '👥Количество участников' + ' - ' + str(data['kol_vo']) + '\n'+ '🎸Вопрос 1' + ' - ' + str(data['q1_answ']) + '\n'+ '🥁Вопрос 2' + ' - ' + str(data['q2_answ']) + '\n'+ '🗓День' + ' - ' + str(date(datetime.now().year,int(dater[1]),int(dater[0]))) + '\n'+ '⏰Время и Зал' + ' - ' + str(data['vremya']) + '\n' + '📞Номер телефона' + ' - ' + str(data['cont']) + '\n'+ '🔓Айди телеграм' + ' - ' + str(call.from_user.id)
            
            await bot.send_message(text=printer,chat_id=master_id)
        
        await state.set_state(None)
        await state.set_state(SS.menu)




if __name__ == '__main__':  
    executor.start_polling(dp)