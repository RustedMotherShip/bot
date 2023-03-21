class zapis(StatesGroup):
    number = State()
    data = State()
    time = State()
    name = State()
    q1 = State()
    q2 = State()
    contact = State()
    complete = State()

@dp.callback_query_handler(state=zapis.data)
async def number(callback: types.CallbackQuery,state: FSMContext):
    













@dp.callback_query_handler(state=zapis.data)
async def data(callback: types.CallbackQuery,state: FSMContext):
    await bot.edit_message_text(text=vopros6,reply_markup=await kb_1_start(), message_id=callback.message.message_id, chat_id=callback.from_user.id)
    await state.set_state(zapis.time)


@dp.callback_query_handler(state=zapis.time)   
async def time(callback: types.CallbackQuery,state: FSMContext):
    await bot.delete_message(chat_id=callback.from_user.id, message_id=callback.message.message_id)
    day_r=callback.data
    await state.update_data(datezap=callback.data)
    await bot.send_message(text=vopros7,reply_markup=await kb_2_start(day_r), chat_id=callback.from_user.id)
    await state.set_state(zapis.v1_answer)

@dp.callback_query_handler(state=zapis.v1_answer)
async def name_rs(callback: types.CallbackQuery,state: FSMContext):
    await bot.delete_message(chat_id=callback.from_user.id, message_id=callback.message.message_id)
    await bot.send_message(text=vopros1,chat_id=callback.from_user.id)
    await state.update_data(vremya=callback.data)
    await state.set_state(zapis.contact)
    

@dp.message_handler(state=zapis.contact)
async def contact(message: types.Message,state: FSMContext):
    await bot.delete_message(chat_id=message.from_user.id, message_id=message.message_id)
    await bot.send_message(text=vopros2, chat_id=message.from_user.id)
    global q_id
    q_id = message.message_id
    print(q_id)
    await state.update_data(imya=message.text) 
    await state.set_state(zapis.v2_answer)
   

@dp.message_handler(state=zapis.v2_answer)
async def kolvo_rs(message: types.Message,state: FSMContext):
    print(message.message_id)
    await bot.delete_message(chat_id=message.from_user.id, message_id=message.message_id)
    await bot.delete_message(chat_id=message.from_user.id, message_id=message.q_id)
    await bot.send_message(text=vopros3,reply_markup=q1_kb,chat_id=message.from_user.id)
    await state.update_data(cont=message.text)
    await state.set_state(zapis.v3_answer)

@dp.callback_query_handler(state=zapis.v3_answer)
async def q1(callback: types.CallbackQuery,state: FSMContext):
    await bot.delete_message(chat_id=callback.from_user.id, message_id=callback.message.message_id)
    await bot.send_message(text=vopros4,reply_markup=q2_kb, chat_id=callback.from_user.id)
    await state.update_data(kol_vo=callback.data)
    await state.set_state(zapis.v4_answer)
    

@dp.callback_query_handler(state=zapis.v4_answer) 
async def q2(callback: types.CallbackQuery,state: FSMContext):
    await bot.delete_message(chat_id=callback.from_user.id, message_id=callback.message.message_id)
    await bot.send_message(text=vopros5,reply_markup=q2_kb, chat_id=callback.from_user.id)
    await state.update_data(q1_answ=callback.data)
    await state.set_state(zapis.complete)
    


    

    
@dp.callback_query_handler(state=zapis.complete)
async def success(callback: types.CallbackQuery,state: FSMContext):
    await bot.delete_message(chat_id=callback.from_user.id, message_id=callback.message.message_id)
    await state.update_data(q2_answ=callback.data)
    data = await state.get_data()
    dater=data['datezap'].split(',')  
    adder = User(data['imya'],data['kol_vo'],data['q1_answ'],data['q2_answ'],date(2022,int(dater[0]),int(dater[1])),data['vremya'],data['cont'],callback.from_user.id)
    banchecker = DBB.check_ban(callback.from_user.id)
    if banchecker == True or str(data['vremya']) == 'error' or  str(data['datezap']) == 'error':
        await bot.send_message(text="Ошибка или вы забаненны.Нажмите,чтобы выйти",reply_markup=btn_back, chat_id=callback.from_user.id)
    else:
        await bot.send_message(text="Успешно!Нажмите,чтобы выйти",reply_markup=btn_back, chat_id=callback.from_user.id)
        await DBW.add_user(adder)

        printer = "У вас новая запись!\n" + \
            '👤Название' + ' - ' + str(data['imya']) + '\n' + '👥Количество участников' + ' - ' + str(data['kol_vo']) + '\n'+ '🎸Вопрос 1' + ' - ' + str(data['q1_answ']) + '\n'+ '🥁Вопрос 2' + ' - ' + str(data['q2_answ']) + '\n'+ '🗓День' + ' - ' + str(date(2022,int(dater[0]),int(dater[1]))) + '\n'+ '⏰Время и Зал' + ' - ' + str(data['vremya']) + '\n' + '📞Номер телефона' + ' - ' + str(data['cont']) + '\n'+ '🔓Айди телеграм' + ' - ' + str(callback.from_user.id)
        
        await bot.send_message(text=printer,chat_id=master_id)
    
    await state.set_state(None)
    await state.set_state(zapis.menu)
    

