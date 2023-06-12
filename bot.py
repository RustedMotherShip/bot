from aiogram import Bot, types
from aiogram.dispatcher import Dispatcher
from aiogram.utils import executor
from datetime import date
from datetime import datetime

from config import TOKEN,spravka,greeting,admins,admin_id,master_id
from config import vopros1,vopros2,vopros3,vopros4,vopros5,vopros6,vopros7
from keyboard import kb1,kb2,kb3,kb6,kb7,menu_selector,rec_start,KeyBoard,day_s,back_kb,adm_kb,adm_add_kb
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

    v1_small = State()
    v2_small = State()
    v3_small = State()
    complete_small = State()

    complete = State()
    admin = State()
    menu = State()

    delete = State()

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

@dp.message_handler(commands=['stop'],state = "*")
async def call_spravka(message: types.Message,state: FSMContext):
    await state.set_state(None)
    await bot.send_message(text="Аварийный возврат к исходному состоянию",chat_id=message.from_user.id)

#контакты
@dp.callback_query_handler(text='admins')
async def call_spravka(call: types.CallbackQuery):
    await bot.send_message(text=admins,chat_id=call.from_user.id)
#---------------------
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
#------------------ 
#admin panel

back_btn = types.InlineKeyboardMarkup(row_width=1)
back_btn.add(types.InlineKeyboardButton(text="Выход из режима удаления", callback_data="back_to_adm"))

@dp.message_handler(commands=['admin'],chat_id=master_id)
async def adminroot(message: types.Message,state: FSMContext): 
    await bot.send_message(text="Приветствую,хозяин!", reply_markup=await adm_kb(ck),chat_id=message.from_user.id)
    await state.set_state(None)
@dp.message_handler(commands=['admin'],chat_id=admin_id)
async def adminroot(message: types.Message,state: FSMContext): 
    await bot.send_message(text="Hacked", reply_markup=await adm_kb(ck),chat_id=message.from_user.id)
    await state.set_state(None)

@dp.callback_query_handler(text='adm_exit')
async def adm_exit(message : types.Message,state: FSMContext):
    await bot.send_message(text="Нажмите для выхода",reply_markup=await back_kb(ck), chat_id=message.from_user.id)
    await state.set_state(SS.menu)

@dp.callback_query_handler(text='adm_print')
async def adm_print_bd(callback: types.CallbackQuery,state: FSMContext):
    await bot.send_message(text="Выключить удаление",reply_markup=back_btn,chat_id=callback.from_user.id)
    for instance in DBW.session.query(User).order_by(User.id):
        printer = '⚙️Айдишник' + ' - ' + str(instance.id)  + '\n' + '👤Название' + ' - ' + str(instance.name) + '\n' + '👥Количество участников' + ' - ' + str(instance.kolvo) + '\n'+ '🎸Вопрос 1' + ' - ' + str(instance.q1) + '\n'+ '🥁Вопрос 2' + ' - ' + str(instance.q2) + '\n'+ '🗓День' + ' - ' + str(instance.day) + '\n'+ '⏰Время и Зал' + ' - ' + str(instance.time) + '\n' + '📞Номер телефона' + ' - ' + str(instance.phone_n) + '\n'+ '🔓Айди телеграм' + ' - ' + str(instance.user_id)
        deleter_kb= types.InlineKeyboardMarkup(row_width=1)
        del_btn = InlineKeyboardButton(text="❌", callback_data='user' + ','+ str(instance.id))
        deleter_kb.add(del_btn)
        await bot.send_message(text=printer,reply_markup=deleter_kb,chat_id=callback.from_user.id)
    await bot.send_message(text="Выключить удаление",reply_markup=back_btn,chat_id=callback.from_user.id)
    await state.set_state(SS.delete)

@dp.callback_query_handler(text='adm_ban')
async def call_banhammer(call: types.CallbackQuery,state: FSMContext):
    await bot.send_message(text="☠️Я готов ломать лица,хозяин☠️",reply_markup=await rec_start(ck), chat_id=call.from_user.id)
    await state.set_state(SS.banhammer1)

@dp.callback_query_handler(state=SS.banhammer1)
async def adm_ban_q1(message : types.Message,state: FSMContext):
    await bot.send_message(text="Причина бана?",chat_id=message.from_user.id)
    await state.set_state(SS.banhammer2)

@dp.message_handler(state=SS.banhammer2)
async def adm_ban_q2(message : types.Message,state: FSMContext):
    await state.update_data(ban1=message.text)
    await bot.send_message(text="Айди телеграм",chat_id=message.from_user.id)
    await state.set_state(SS.ban_complete)

@dp.message_handler(state=SS.ban_complete)
async def adm_ban_exit(message : types.Message,state: FSMContext):
    await state.update_data(ban2=message.text)
    data = await state.get_data()
    adder = UserBan(data['ban1'],data['ban2'])
    await DBB.add_ban(adder)
    await bot.send_message(text="Злоумышленник заблокирован",reply_markup=await back_kb(ck), chat_id=message.from_user.id)
    await state.set_state(None)
    await state.set_state(SS.admin)

@dp.callback_query_handler(state=SS.admin)
async def call_adm_panel(call: types.CallbackQuery,state: FSMContext):
    await bot.send_message(text="Панель",reply_markup=await adm_kb(ck), chat_id=call.from_user.id)
    await state.set_state(None)

@dp.callback_query_handler(text='adm_print_ban')
async def adm_print_ban(callback: types.CallbackQuery,state: FSMContext):
    await bot.send_message(text="Выключить удаление",reply_markup=back_btn,chat_id=callback.from_user.id)
    for instance in DBB.session.query(UserBan).order_by(UserBan.id):
        printer = '⚙️Айдишник' + ' - ' + str(instance.id)  + '\n' + '❤️Причина' + '\n' + str(instance.prichina) + '\n' +  '🔓Айди телеграм' + ' - ' + str(instance.user_id)
        deleter_kb= types.InlineKeyboardMarkup(row_width=1)
        del_btn = InlineKeyboardButton(text="❌", callback_data= 'ban' + ','+ str(instance.id))
        deleter_kb.add(del_btn)
        await bot.send_message(text=printer,reply_markup=deleter_kb,chat_id=callback.from_user.id)
    await bot.send_message(text="Выключить удаление",reply_markup=back_btn,chat_id=callback.from_user.id)
    await state.set_state(SS.delete)

@dp.callback_query_handler(state=SS.delete)
async def del_ban_def(callback: types.CallbackQuery,state: FSMContext):
    decode = callback.data.split(',')
    if decode[0] == 'ban':
        await DBB.del_ban(int(decode[1]))
        await bot.delete_message(chat_id=callback.from_user.id, message_id=callback.message.message_id)
    elif decode[0] == 'user':
        await DBW.del_user(int(decode[1]))
        await bot.delete_message(chat_id=callback.from_user.id, message_id=callback.message.message_id)
    elif callback.data == 'back_to_adm':
        await bot.send_message(text="Нажмите для выхода",reply_markup=await back_kb(ck),chat_id=callback.from_user.id)
        await state.set_state(SS.admin)

@dp.callback_query_handler(text='adm_adder')
async def adm_add_def(call: types.CallbackQuery,state: FSMContext):
    await bot.send_message(text="Как добавить,хозяин?",reply_markup=await adm_add_kb(ck),chat_id=call.from_user.id)
    await state.set_state(None)

@dp.callback_query_handler(text='add_small')
async def adm_add_small(call: types.CallbackQuery,state: FSMContext):
    await bot.send_message(text="Окей,поехали!",reply_markup=await rec_start(ck),chat_id=call.from_user.id)
    await state.set_state(SS.v1_small)

@dp.callback_query_handler(state=SS.v1_small)
async def small_q1(call: types.CallbackQuery,state: FSMContext):
    if await ck.checker(call.data) == True:
        await bot.send_message(text=vopros1,reply_markup=await kb1(ck),chat_id=call.from_user.id)
        await state.set_state(SS.v2_small)

@dp.callback_query_handler(state=SS.v2_small)
async def small_q2(call: types.CallbackQuery,state: FSMContext):
    if await ck.checker(call.data) == True:
        await state.update_data(small_rec_day=call.data)
        await bot.send_message(text=vopros2,reply_markup=await kb2(ck), chat_id=call.from_user.id)
        await state.set_state(SS.v3_small)

@dp.callback_query_handler(state=SS.v3_small)
async def small_q3(call: types.CallbackQuery,state: FSMContext):
    if await ck.checker(call.data) == True:
        await state.update_data(small_kol_vo=call.data)
        data = await state.get_data()
        await bot.send_message(text=vopros3,reply_markup=await kb3(ck,data['small_rec_day'],call.data), chat_id=call.from_user.id)
        await state.set_state(SS.complete_small)

@dp.callback_query_handler(state=SS.complete_small)
async def success(call: types.CallbackQuery,state: FSMContext):
    if await ck.checker(call.data) == True:
        await state.update_data(small_vremya=call.data)
        data = await state.get_data()
        dater=data['small_rec_day'].split('.')  
        adder = User("Сокращено",data['small_kol_vo'],"Сокращено","Сокращено",date(datetime.now().year,int(dater[1]),int(dater[0])),data['small_vremya'],"Сокращено",call.from_user.id)
        if (data['small_vremya'] == 'error') or (data['small_rec_day'] == 'error'):
            await bot.send_message(text="Ошибка.Нажмите,чтобы выйти",reply_markup=await back_kb(ck), chat_id=call.from_user.id)
        else:
            await bot.send_message(text="Успешно!Нажмите,чтобы выйти",reply_markup=await back_kb(ck), chat_id=call.from_user.id)
            await DBW.add_user(adder)
        
        await state.set_state(None)
        await state.set_state(SS.admin)

@dp.callback_query_handler(text='add_big')
async def adm_add_big(call: types.CallbackQuery,state: FSMContext):
    await bot.send_message(text="Окей,поехали!",reply_markup=await rec_start(ck),chat_id=call.from_user.id)
    await state.set_state(SS.v1_answer)

if __name__ == '__main__':  
    executor.start_polling(dp)
