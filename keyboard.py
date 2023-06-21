from datetime import date
from datetime import datetime
from aiogram import types
from aiogram.types import InlineKeyboardButton
from aiogram.types import InlineKeyboardMarkup
from db import DBWorker

DBW=DBWorker()
class KeyBoard:

    current_keyboard = InlineKeyboardMarkup()
    list_of={}

    async def clear_keyboard(self):
        self.current_keyboard = InlineKeyboardMarkup()
        self.list_of={}

    async def new_list_of(self,nl):
        self.list_of=nl
        for i in self.list_of:
            btn=InlineKeyboardButton(text=i, callback_data=self.list_of[i])
            self.current_keyboard.insert(btn)

    async def new_width_of(self,w):
        self.current_keyboard = InlineKeyboardMarkup(row_width = w)
        for i in self.list_of:
            btn=InlineKeyboardButton(text=i, callback_data=self.list_of[i])
            self.current_keyboard.insert(btn)

    async def checker(self,clbck):
        chckr=False
        for i in self.list_of:
            if clbck == self.list_of[i]:
                chckr = True
        return chckr
#Заключительная часть руководства
#В параметре num функции number необходимо написать количество уникальных чисел
#для трёх возможных типов записи по дням недели(будние,суббота,воскресение) по инструкции представленной ниже
#
#   if  datetime.weekday(day_r) <= 4: #будние дни
#       if clbck1 == 'Три человека и больше':
#           list_of_times=[1,2,3] #Будние дни, три человека
#       elif clbck1 == 'Два человека':
#           list_of_times=[4,5] #Будние дни, два человека
#       else:
#           list_of_times=[5] #Будние дни, один человек
#
#    В первом типе у нас встреччаются цифры 1,2,3,4,5 слеедовательно значение num равно 5,так как 5 уникальных чисел
#
#   elif datetime.weekday(day_r) == 5: #Суббота
#       if clbck1 == 'Три человека и больше':
#           list_of_times=[2,3] #Субботние дни, три человека
#       elif clbck1 == 'Два человека': #Субботние дни, два человека
#           list_of_times=[1]
#       else:
#           list_of_times=[4] #Субботние дни, один человек
#
#     В втором типе у нас встречаются цифры 1,2,3,4 слеедовательно значение num равно 4,так как 4 уникальных чисел
#
#   else:                             #Воскресение
#       if clbck1 == 'Три человека и больше':
#           list_of_times=[1,2,3,4,5,6] #Воскресные дни, три человека
#       elif clbck1 == 'Два человека':
#        list_of_times=[1,2,3,4] #Воскресные дни, два человека
#       else:
#           list_of_times=[7,8] #Воскресные дни, один человек
#
#    В втором типе у нас встречаются цифры 1,2,3,4,5,6,7,8 слеедовательно значение num равно 8,так как 8 уникальных чисел
#
    async def number(self,d):
        if  d <= 4:       #Будние дни
            num = 13      #<---Укажите значение для num
        elif d <= 5:      #Суббота
            num = 17      #<---Укажите значение для num
        elif d <= 6:      #Воскресение
            num = 17      #<---Укажите значение для num
        return num

kb_date_time_list = {\
1:'Красный 11.00-14.00',\
2:'Красный 12.00-14.00',\
3:'Красный 14.00-17.00',\
4:'Красный 17.00-20.00',\
5:'Красный на 20.00-23.00',\
6:'Красный на 23.00-02.00',\
7:'Белый 11.00-14.00',\
8:'Белый 12.00-14.00',\
9:'Белый 14.00-17.00',\
10:'Белый 17.00-20.00',\
11:'Белый на 20.00-23.00',\
12:'Белый на 23.00-02.00',\
13:'Чёрный 11.00-14.00',\
14:'Чёрный 12.00-14.00',\
15:'Чёрный 14.00-17.00',\
16:'Чёрный 17.00-20.00',\
17:'Чёрный на 20.00-23.00',\
18:'Чёрный на 23.00-02.00',\
19:'Домашний 11.00-14.00',\
20:'Домашний 12.00-14.00',\
21:'Домашний 14.00-17.00',\
22:'Домашний 17.00-20.00',\
23:'Домашний на 20.00-23.00',\
24:'Домашний на 23.00-02.00',\ #Для добавления нового времени и типа зала необходимо добавить строчку
}                              #после последней запятой по следующему образцу: (1:'Значение',\) скобки копировать не нужно,
menu_btn = {\                  #цифра может быть любой,но она должна быть уникальной.После добавления необходимых значений  
'🎸Записаться':'record',\      #нужно добавить номера этих значений в функцию kb3(), там продолжение руководства
'💾Информация':'info',\
'☎️Контакты':'admins',\        
}
#Краткая справка, для изменения текста на кнопках клавиатуры достаточно просто указать любое значение в первых кавычках
#Пример ('🎸Другое значение🎸':'record',\) скобки не нужно указывать, можно вставлять эмодзи
back_btn = {\
'Назад🔙':'back',\
}
reg_btn = {\
'Поехали!':'record_start',\
}
people_btn = {\
'Один человек':'Один человек',\
'Два человека':'Два человека',\
'Три человека и больше':'Три человека и больше',\
}
answer_btn = {\
'Да':'Да',\
'Нет':'Нет',\
}
adm_btn = {\
'Вывод записей':'adm_print',\
'Добавить':'adm_adder',\
'Вывод банов':'adm_print_ban',\
'Забанить':'adm_ban',\
'Выход':'adm_exit',\
}
adm_add = {\
'Добавить полностью':'add_big',\
'Добавить сокращённо':'add_small',\
}
def day_s(h):
    day = int(datetime.now().day)#сегодня 
    o = int(datetime.now().month) #номер месяца  
    month  = {1 : 31, 2: 28, 3: 31, 4: 30, 5: 31, 6: 30, 7:31, 8: 31 , 9: 30, 10: 31, 11: 30, 12: 31 }
    if day + h > month[o]:
        if o + 1 != 13:
            g = str(day + h - month[o]) + "." + str(o + 1)
        else:
            g = str(day + h - month[o]) + str(1) + "."
    else: 
        g = str(day + h) + '.'+ str(o)
    return g 

async def menu_selector(ck):
    await ck.clear_keyboard()
    await ck.new_width_of(1)
    await ck.new_list_of(menu_btn)
    return ck.current_keyboard

async def rec_start(ck):
    await ck.clear_keyboard()
    await ck.new_width_of(1)
    await ck.new_list_of(reg_btn)
    return ck.current_keyboard

async def back_kb(ck):
    await ck.clear_keyboard()
    await ck.new_width_of(1)
    await ck.new_list_of(back_btn)
    return ck.current_keyboard

async def kb1(ck):
    kb_date_15 = {}
    for i_d in range(1,16):
        dater = day_s(i_d).split('.')
        r = date(datetime.now().year,int(dater[1]),int(dater[0]))
        data_db=DBW.kb_check_day(day_s(i_d),await ck.number(datetime.weekday(r)))
        if data_db == True:
            kb_date_15["✖️"+day_s(i_d)+"✖️"] = 'error'
        else:
            dater = day_s(i_d).split('.')
            day_r = date(datetime.now().year,int(dater[1]),int(dater[0]))
            if  datetime.weekday(day_r) <= 4:
                kb_date_15["☑️"+day_s(i_d)+"☑️"]= day_s(i_d)
            else:
                kb_date_15["🔘"+day_s(i_d)+"🔘"]= day_s(i_d)
    await ck.clear_keyboard()
    await ck.new_width_of(3)
    await ck.new_list_of(kb_date_15)
    return ck.current_keyboard

async def kb2(ck):
    await ck.clear_keyboard()
    await ck.new_width_of(1)
    await ck.new_list_of(people_btn)
    return ck.current_keyboard
#Продолжение руководства
#Сверяясь со списком kb_date_time_list{}, который был заполнен выше, заполните списки list_of_times[] по указанному шаблону
# kb_date_time_list = {\
# 1:'Значение 1',\
# 2:'Значение 2',\
# 3:'Значение 3'}
#
# list_of_times=[1,2,3] #Будние дни, три человека
#
# У каждого списка есть комментарий за что он отвечает, заполняйте в соответствии.Каждая цифра должна быть разделена запятой, заполняйте цифры в таком порядке
# в каком хотите видеть порядок кнопок
# Продолжение руководства выше в функции number
async def kb3(ck,clbck,clbck1):
    dater = clbck.split('.')
    day_r = date(datetime.now().year,int(dater[1]),int(dater[0]))
    if  datetime.weekday(day_r) <= 4: #будние дни
        if clbck1 == 'Три человека и больше':
            list_of_times=[3,4,5,9,10,11,12,15,16,17,18,23] #Будние дни, три человека
        elif clbck1 == 'Два человека':
            list_of_times=[16,22,23] #Будние дни, два человека
        else:
            list_of_times=[22] #Будние дни, один человек
    elif datetime.weekday(day_r) == 5: #Суббота
        if clbck1 == 'Три человека и больше':
            list_of_times=[1,3,4,5,7,9,10,11,12,13,15,16,17,18,21,22,23] #Субботние дни, три человека
        elif clbck1 == 'Два человека': #Субботние дни, два человека
            list_of_times=[13,15,16,18,21,22,23]
        else:
            list_of_times=[21,22,23] #Субботние дни, один человек
    else:                             #Воскресение
        if clbck1 == 'Три человека и больше':
            list_of_times=[2,3,4,5,8,9,10,11,12,14,15,16,17,18,21,22,23] #Воскресные дни, три человека
        elif clbck1 == 'Два человека':
            list_of_times=[14,15,16,18,21,22,23] #Воскресные дни, два человека
        else:
            list_of_times=[21,22,23] #Воскресные дни, один человек

    current_time={}

    for i in range(len(list_of_times)):
        check=kb_date_time_list[list_of_times[i]]
        time_db = await DBW.kb_check_time(check,clbck)
        if time_db == True:
            current_time["✖️"+kb_date_time_list[list_of_times[i]]+"✖️"] = 'error'
        else:
            current_time[kb_date_time_list[list_of_times[i]]] = kb_date_time_list[list_of_times[i]]

    await ck.clear_keyboard()
    await ck.new_list_of(current_time)
    await ck.new_width_of(1)
    return ck.current_keyboard

async def kb6(ck):
    await ck.clear_keyboard()
    await ck.new_width_of(1)
    await ck.new_list_of(answer_btn)
    return ck.current_keyboard

async def kb7(ck):
    await ck.clear_keyboard()
    await ck.new_width_of(1)
    await ck.new_list_of(answer_btn)
    return ck.current_keyboard

async def adm_kb(ck):
    await ck.clear_keyboard()
    await ck.new_width_of(1)
    await ck.new_list_of(adm_btn)
    return ck.current_keyboard

async def adm_add_kb(ck):
    await ck.clear_keyboard()
    await ck.new_width_of(1)
    await ck.new_list_of(adm_add)
    return ck.current_keyboard
