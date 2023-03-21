from aiogram import Bot, types
from aiogram.dispatcher import Dispatcher
from aiogram.utils import executor
from datetime import date

from config import TOKEN,spravka,greeting,admins,admin_id,master_id
from config import vopros1,vopros2,vopros3,vopros4,vopros5,vopros6,vopros7
from keyboard import kb_1_start,kb_2_start, q1_kb,btnreg,buttons,q2_kb,adm_btn,btn_back
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
class zapis(StatesGroup):
    v1_answer = State()
    v2_answer = State()
    v3_answer = State()
    v4_answer = State()
    data = State()
    time = State()

    contact = State()
    complete =State()
    admin = State()
    menu = State()

    banhammer1 = State()
    banhammer2 = State()
    ban_complete = State()

    

#команда старт
@dp.message_handler(commands=['start'])
async def process_start_command(message: types.Message):
    await message.answer(greeting, reply_markup=buttons)
#меню
@dp.callback_query_handler(state=zapis.menu)
async def call_zapis(call: types.CallbackQuery,state: FSMContext):
    await bot.send_message(text="Меню",reply_markup=buttons, chat_id=call.from_user.id)
    await state.set_state(None)

#вывод справки
@dp.callback_query_handler(text='info')
async def call_spravka(callback: types.CallbackQuery):
    await callback.message.answer(spravka)

#---------------------

#запись на точку

@dp.callback_query_handler(text='zapis_test', state=None)
async def call_zapis(call: types.CallbackQuery,state: FSMContext):
    await bot.send_message(text="Тогда заполни простую форму!",reply_markup=btnreg, chat_id=call.from_user.id)
    await state.set_state(zapis.v1_answer)

@dp.callback_query_handler(state=zapis.v1_answer)
async def q1(message: types.Message,state: FSMContext):
    await bot.send_message(text=vopros1,chat_id=message.from_user.id)
    await state.set_state(zapis.contact)
    

@dp.message_handler(state=zapis.contact)
async def contact(message: types.Message,state: FSMContext):
    await bot.send_message(text=vopros2, chat_id=message.from_user.id)
    await state.update_data(imya=message.text) 
    await state.set_state(zapis.v2_answer)
   

@dp.message_handler(state=zapis.v2_answer)
async def q2(message: types.Message,state: FSMContext):
    await bot.send_message(text=vopros3,reply_markup=q1_kb,chat_id=message.from_user.id)
    await state.update_data(cont=message.text)
    await state.set_state(zapis.v3_answer)

@dp.callback_query_handler(state=zapis.v3_answer)
async def q3(callback: types.CallbackQuery,state: FSMContext):
    await bot.send_message(text=vopros4,reply_markup=q2_kb, chat_id=callback.from_user.id)
    await state.update_data(kol_vo=callback.data)
    await state.set_state(zapis.v4_answer)
    

@dp.callback_query_handler(state=zapis.v4_answer) 
async def q4(callback: types.CallbackQuery,state: FSMContext):
    await bot.send_message(text=vopros5,reply_markup=q2_kb, chat_id=callback.from_user.id)
    await state.update_data(q1_answ=callback.data)
    await state.set_state(zapis.data)
    

@dp.callback_query_handler(state=zapis.data)
async def q5(callback: types.CallbackQuery,state: FSMContext):
    await bot.send_message(text=vopros6,reply_markup=await kb_1_start(), chat_id=callback.from_user.id)
    await state.update_data(q2_answ=callback.data)
    await state.set_state(zapis.time)
    

@dp.callback_query_handler(state=zapis.time)   
async def q6(callback: types.CallbackQuery,state: FSMContext):
    day_r=callback.data
    await state.update_data(datezap=callback.data)
    await bot.send_message(text=vopros7,reply_markup=await kb_2_start(day_r), chat_id=callback.from_user.id)
    await state.set_state(zapis.complete)
    
@dp.callback_query_handler(state=zapis.complete)
async def success(callback: types.CallbackQuery,state: FSMContext):
    await state.update_data(vremya=callback.data)
    data = await state.get_data()
    dater=data['datezap'].split(',')  
    adder = User(data['imya'],data['kol_vo'],data['q1_answ'],data['q2_answ'],date(2022,int(dater[0]),int(dater[1])),data['vremya'],data['cont'],callback.from_user.id)
    banchecker = DBB.check_ban(callback.from_user.id)
    if banchecker == True & data['vremya'] != 'error' &  data['datezap'] != 'error':
        await bot.send_message(text="Ошибка или вы забаненны.Нажмите,чтобы выйти",reply_markup=btn_back, chat_id=callback.from_user.id)
    else:
        await bot.send_message(text="Успешно!Нажмите,чтобы выйти",reply_markup=btn_back, chat_id=callback.from_user.id)
        await DBW.add_user(adder)

        printer = "У вас новая запись!\n" + \
            '👤Название' + ' - ' + str(data['imya']) + '\n' + '👥Количество участников' + ' - ' + str(data['kol_vo']) + '\n'+ '🎸Вопрос 1' + ' - ' + str(data['q1_answ']) + '\n'+ '🥁Вопрос 2' + ' - ' + str(data['q2_answ']) + '\n'+ '🗓День' + ' - ' + str(date(2022,int(dater[0]),int(dater[1]))) + '\n'+ '⏰Время и Зал' + ' - ' + str(data['vremya']) + '\n' + '📞Номер телефона' + ' - ' + str(data['cont']) + '\n'+ '🔓Айди телеграм' + ' - ' + str(callback.from_user.id)
        
        await bot.send_message(text=printer,chat_id=master_id)
    
    await state.set_state(None)
    await state.set_state(zapis.menu)
    


#----------------------

#контакты
@dp.callback_query_handler(text='admins')
async def call_spravka(callback: types.CallbackQuery):
    await callback.message.answer(admins)

#ADMIN-----------------------


@dp.message_handler(commands=['admin'],chat_id=master_id)
async def adminroot(message: types.Message,state: FSMContext): 
    await bot.send_message(text="Приветствую,хозяин!", reply_markup=adm_btn,chat_id=message.from_user.id)
    await state.set_state(None)
@dp.message_handler(commands=['admin'],chat_id=admin_id)
async def adminroot(message: types.Message,state: FSMContext): 
    await bot.send_message(text="Hacked", reply_markup=adm_btn,chat_id=message.from_user.id)
    await state.set_state(None)

@dp.callback_query_handler(text='adm_exit')
async def adm_exit(message : types.Message,state: FSMContext):
    await bot.send_message(text="Нажмите для выхода",reply_markup=btn_back, chat_id=message.from_user.id)
    await state.set_state(zapis.menu)

@dp.callback_query_handler(text='adm_print')
async def adm_exit(callback: types.CallbackQuery,state: FSMContext):
    for instance in DBW.session.query(User).order_by(User.id):
        printer = '⚙️Айдишник' + ' - ' + str(instance.id)  + '\n' + '👤Название' + ' - ' + str(instance.name) + '\n' + '👥Количество участников' + ' - ' + str(instance.kolvo) + '\n'+ '🎸Вопрос 1' + ' - ' + str(instance.q1) + '\n'+ '🥁Вопрос 2' + ' - ' + str(instance.q2) + '\n'+ '🗓День' + ' - ' + str(instance.day) + '\n'+ '⏰Время и Зал' + ' - ' + str(instance.time) + '\n' + '📞Номер телефона' + ' - ' + str(instance.phone_n) + '\n'+ '🔓Айди телеграм' + ' - ' + str(instance.user_id)
        deleter_kb= types.InlineKeyboardMarkup(row_width=1)
        del_btn = InlineKeyboardButton(text="❌", callback_data='user' + ','+ str(instance.id))
        deleter_kb.add(del_btn)
        await bot.send_message(text=printer,reply_markup=deleter_kb,chat_id=callback.from_user.id)
    await state.set_state(None)

@dp.callback_query_handler(text='adm_ban')
async def call_zapis(call: types.CallbackQuery,state: FSMContext):
    await bot.send_message(text="☠️Я готов ломать лица,хозяин☠️",reply_markup=btnreg, chat_id=call.from_user.id)
    await state.set_state(zapis.banhammer1)

@dp.callback_query_handler(state=zapis.banhammer1)
async def adm_exit(message : types.Message,state: FSMContext):
    await bot.send_message(text="Причина бана?",chat_id=message.from_user.id)
    await state.set_state(zapis.banhammer2)

@dp.message_handler(state=zapis.banhammer2)
async def adm_exit(message : types.Message,state: FSMContext):
    await state.update_data(ban1=message.text)
    await bot.send_message(text="Айди телеграм",chat_id=message.from_user.id)
    await state.set_state(zapis.ban_complete)

@dp.message_handler(state=zapis.ban_complete)
async def adm_exit(message : types.Message,state: FSMContext):
    await state.update_data(ban2=message.text)
    data = await state.get_data()
    adder = UserBan(data['ban1'],data['ban2'])
    await DBB.add_ban(adder)
    await bot.send_message(text="Злоумышленник заблокирован",reply_markup=btn_back, chat_id=message.from_user.id)
    await state.set_state(None)
    await state.set_state(zapis.admin)

@dp.callback_query_handler(state=zapis.admin)
async def call_zapis(call: types.CallbackQuery,state: FSMContext):
    await bot.send_message(text="Панель",reply_markup=adm_btn, chat_id=call.from_user.id)
    await state.set_state(None)

@dp.callback_query_handler(text='adm_print_ban')
async def adm_exit(callback: types.CallbackQuery,state: FSMContext):
    for instance in DBB.session.query(UserBan).order_by(UserBan.id):
        printer = '⚙️Айдишник' + ' - ' + str(instance.id)  + '\n' + '❤️Причина' + '\n' + str(instance.prichina) + '\n' +  '🔓Айди телеграм' + ' - ' + str(instance.user_id)
        deleter_kb= types.InlineKeyboardMarkup(row_width=1)
        del_btn = InlineKeyboardButton(text="❌", callback_data= 'ban' + ','+ str(instance.id))
        deleter_kb.add(del_btn)
        await bot.send_message(text=printer,reply_markup=deleter_kb,chat_id=callback.from_user.id)
    await state.set_state(None)

@dp.callback_query_handler(state=None)
async def del_ban_def(callback: types.CallbackQuery,state: FSMContext):
    decode = callback.data.split(',')
    if decode[0] == 'ban':
        await DBB.del_ban(int(decode[1]))
    elif decode[0] == 'user':
        await DBW.del_user(int(decode[1]))
    else:
        False
    await bot.delete_message(chat_id=callback.from_user.id, message_id=callback.message.message_id)








if __name__ == '__main__':  
    executor.start_polling(dp)

