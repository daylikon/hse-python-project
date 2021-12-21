from tkinter import Tk, Label, Button, Listbox, Scrollbar, Frame, Text
import tkinter as tki
import tkinter.ttk as ttk
import pandas as pd
import webbrowser
from database_csl import opendb, savedb, saveasdb, createdb
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt
import tkinter as tk
from math import nan
global db

def reference():
    """
    Функция создания окна справки 
    Входные параметры: нет
    Возвращаемые параметры: нет
    Автор: Нигматуллин Николай
    """
    webbrowser.open_new("https://docs.google.com/document/d/1zTwk0MAbT2lQ6tAyasB94XARHzYeTEEf/edit")   

def dbcontroller(event, mainwindow):
    """
    Функция обработки действий с Базой Данных
    Входные параметры: event - действие с БД (new,open,saveas)
    Возвращаемые параметры: нет
    Автор: Угодников Андрей
    """
    global db
    global proj
    global desc
    global location
    global path
    global path1
    global path2
    global path3
    if(event == "open"):
        proj, path1 = opendb("proj.csv")
        if(proj is not None):
            print(proj)
            desc, path2 = opendb("desc.csv")
            if(desc is not None):
                location, path3 = opendb("location.csv")
                if(location is not None):
                    createmainwin()
    if(event == "new"):
        proj,desc,location = createdb()
        createmainwin()
        global newdb
        newdb = True
        
    if(event == "saveas"):
        path = saveasdb(db)
        ext=str(path1).split('.')[-1]
        if(ext=="csv"):
            proj.to_csv(path1, index=False)
        elif(ext=="xls" or ext=="xlsx"):
            proj.to_excel(path1, index=False)
        ext=str(path2).split('.')[-1]
        if(ext=="csv"):
            desc.to_csv(path2, index=False)
        elif(ext=="xls" or ext=="xlsx"):
            desc.to_excel(path2, index=False)
        if path != None:
            mainwindow.title(str(path).split('/')[-1] + " - Анализ проектов Kickstarter")
def histogramm(array1, array2, num1, num2):
    
    """
    Построение Столбчатой диаграммы
    Входные параметры: array1, array2 - массивы строк, num1, num2 - int
    Возвращаемые параметры: нет
    Автор: Нигматуллин Николай
    """
    global db
    print(array1[num1])
    st=''
    j=0
    num2=1
    if (num2==1): 
        def hd():
            num3=combobox.current()
            hist.destroy()
            ar1=['']*1000
            ar2=[0]*1000
            ar3=[0]*1000
            if (num3==1) or (num3==0):
                j=0
                for i in range(len(db.index+1)):
                    if (j==0):
                        ar1[0]=db.loc[i, array1[num1]]
                        ar2[0]+=round(float(db.loc[i, array2[num2]]),2)
                        ar3[0]+=1
                        j+=1
                    else:
                        q=0
                        for t in range(j):
                            if ar1[t]==db.loc[i, array1[num1]]:
                                ar2[t]+=round(float(db.loc[i, array2[num2]]),2)
                                ar3[t]+=1
                                q=1
                        if q==0:
                            ar1[j]=db.loc[i, array1[num1]]
                            ar2[j]+=round(float(db.loc[i, array2[num2]]),2)
                            ar3[j]+=1
                            j+=1
                        
                if num3==0:
                    print(ar3)
                    st='Средние сборы'
                    for t in range(j):
                        ar2[t]=round((ar2[t]/ar3[t]),2)
                else:
                    st='Общие сборы'
            else:
                if (num3==2):
                    j=0
                    st='Максимальные сборы'
                    for i in range(len(db.index+1)):
                        print(db.loc[i, array1[num1]])
                        print(db.loc[i, array2[num2]])
                        if (j==0):
                            ar1[0]=db.loc[i, array1[num1]]
                            ar2[0]+=round(float(db.loc[i, array2[num2]]),2)
                            j+=1      
                        else:
                            q=0
                            for t in range(j):
                                if ar1[t]==db.loc[i, array1[num1]]:
                                    ar2[t]=max(ar2[t],round(float(db.loc[i, array2[num2]]),2))
                                    q=1
                                if q==0:
                                    ar1[j]=db.loc[i, array1[num1]]
                                    ar2[j]=round(float(db.loc[i, array2[num2]]),2)
                                    j+=1
                else:
                    j=0
                    st='Минимальные сборы'
                    for i in range(len(db.index+1)):
                        print(db.loc[i, array1[num1]])
                        print(db.loc[i, array2[num2]])
                        if (j==0):
                            ar1[0]=db.loc[i, array1[num1]]
                            ar2[0]+=round(float(db.loc[i, array2[num2]]),2)
                            j+=1      
                        else:
                            q=0
                            for t in range(j):
                                if ar1[t]==db.loc[i, array1[num1]]:
                                    ar2[t]=min(ar2[t],round(float(db.loc[i, array2[num2]]),2))
                                    q=1
                            if q==0:
                                ar1[j]=db.loc[i, array1[num1]]
                                ar2[j]=round(float(db.loc[i, array2[num2]]),2)
                                j+=1
            root=Tk()
            figure1 = plt.Figure(figsize=(6,5), dpi=100)
            ax1 = figure1.add_subplot(111)
            bar1 = FigureCanvasTkAgg(figure1, root)
            bar1.get_tk_widget().pack(side=tk.LEFT, fill=tk.BOTH)
            ax1.bar(ar1,ar2)
            ax1.set_title(st)
            figure1.show()
        hist=Tk()
        hist.title("Гистограмма")
        hist.geometry("300x400")
        combobox = ttk.Combobox(hist, width = 38, state="readonly", values=['Среднее', 'Общие сборы', 'Максимум', 'Минимум'])
        combobox.place(relx=0.1, rely=0.3, relheight=0.2, relwidth=0.8)
        combobox.current(0)
        lbl=Label(hist, text="Выберите параметр", font=('Times', 20), anchor='n')
        lbl.place(relx=0, rely=0, relheight=0.2, relwidth=1)
        btn=Button(hist, text='Продолжить', font=('Times', 20), bd=4, relief="raised", command= hd)
        btn.place(relx=0.1,rely=0.8, relheight=0.15, relwidth=0.8)
        hist.mainloop()
    
def histogramm_win():
    
    """
    Окно выбора параметров столбчатой диаграммы
    Входные параметры: нет
    Возвращаемые параметры: нет
    Автор: Нигматуллин Николай
    """
    global db
    def hd ():
       num1=combobox1.current()
       num2=2
       global db
       histogramm(array1,array2, num1,num2)
    hist_win=Tk()
    hist_win.title("Гистограмма")
    hist_win.geometry("600x400")
    combobox1 = ttk.Combobox(hist_win, width = 38, state="readonly", values=['main_category', 'country'])
    combobox1.place(relx=0.1, rely=0.3, relheight=0.2, relwidth=0.8)
    combobox1.current(0)
    array1=['main_category', 'country' ]
    array2=['status', 'usd_pledged']
    lbl=Label(hist_win, text="Выберите параметр", font=('Times', 20), anchor='n')
    lbl.place(relx=0, rely=0, relheight=0.2, relwidth=1)
    btn=Button(hist_win, text='Построить', font=('Times', 20), bd=4, relief="raised", command= hd)
    btn.place(relx=0.1,rely=0.8, relheight=0.15, relwidth=0.8)

def pie(array1,num1):
    
    """
    Построение круговой диаграммы
    Входные параметры: array1 - массив строк, num1 - int
    Возвращаемые параметры: нет
    Автор: Нигматуллин Николай
    """
    global db
    print(array1[num1])
    st=''
    j=0
    ar2=[0]*1000
    ar1=['']*1000
    if (num1==3): 
        def hd():
            global db
            num3=combobox1.current()
            num2=combobox2.current()
            hist.destroy()
            ar1=['']*1000
            ar2=[0]*1000
            ar3=[0]*1000
            if (num3==1) or (num3==0):
                j=0
                for i in range(len(db.index+1)):
                    if (j==0):
                        ar1[0]=db.loc[i, array2[num2]]
                        ar2[0]+=round(float(db.loc[i, array1[num1]]),2)
                        ar3[0]+=1
                        j+=1
                    else:
                        q=0
                        for t in range(j):
                            if ar1[t]==db.loc[i, array2[num2]]:
                                ar2[t]+=round(float(db.loc[i, array1[num1]]),2)
                                ar3[t]+=1
                                q=1
                        if q==0:
                            ar1[j]=db.loc[i, array2[num2]]
                            ar2[j]+=round(float(db.loc[i, array1[num1]]),2)
                            ar3[j]+=1
                            j+=1
                        
                if num3==0:
                    print(ar3)
                    for t in range(j):
                        ar2[t]=round((ar2[t]/ar3[t]),2)
 
            else:
                if (num3==2):
                    j=0
                    for i in range(len(db.index+1)):
                        print(db.loc[i, array1[num1]])
                        print(db.loc[i, array2[num2]])
                        if (j==0):
                            ar1[0]=db.loc[i, array2[num2]]
                            ar2[0]+=round(float(db.loc[i, array1[num1]]),2)
                            j+=1      
                        else:
                            q=0
                            for t in range(j):
                                if ar1[t]==db.loc[i, array2[num2]]:
                                    ar2[t]=max(ar2[t],round(float(db.loc[i, array2[num2]]),2))
                                    q=1
                                if q==0:
                                    ar1[j]=db.loc[i, array2[num2]]
                                    ar2[j]=round(float(db.loc[i, array1[num1]]),2)
                                    j+=1
                else:
                    j=0
                    for i in range(len(db.index+1)):
                        print(db.loc[i, array1[num1]])
                        print(db.loc[i, array2[num2]])
                        if (j==0):
                            ar1[0]=db.loc[i, array2[num2]]
                            ar2[0]+=round(float(db.loc[i, array1[num1]]),2)
                            j+=1      
                        else:
                            q=0
                            for t in range(j):
                                if ar1[t]==db.loc[i, array2[num2]]:
                                    ar2[t]=min(ar2[t],round(float(db.loc[i, array1[num1]]),2))
                                    q=1
                            if q==0:
                                ar1[j]=db.loc[i, array2[num2]]
                                ar2[j]=round(float(db.loc[i, array1[num1]]),2)
                                j+=1
        hist=Tk()
        hist.title("Круговая диаграмма")
        hist.geometry("600x400")
        combobox1 = ttk.Combobox(hist, width = 38, state="readonly", values=['Среднее', 'Общие сборы', 'Максимум', 'Минимум'])
        combobox1.place(relx=0.1, rely=0.3, relheight=0.2, relwidth=0.35)
        combobox1.current(0)
        combobox2 = ttk.Combobox(hist, width = 38, state="readonly", values=['main_category', 'country'])
        combobox2.place(relx=0.45, rely=0.3, relheight=0.2, relwidth=0.35)
        combobox2.current(0)
        array2=['main_category', 'country']
        lbl=Label(hist, text="Выберите параметр", font=('Times', 20), anchor='n')
        lbl.place(relx=0, rely=0, relheight=0.2, relwidth=1)
        btn=Button(hist, text='Продолжить', font=('Times', 20), bd=4, relief="raised", command= hd)
        btn.place(relx=0.1,rely=0.8, relheight=0.15, relwidth=0.8)
        hist.mainloop()
    else:
        if num1==2:
            ar2=[0]*2
            ar1=['successful', 'failed']
            for i in range(len(db.index())+1):
                if(db.loc[i, array1[num1]]=='failed'):
                   ar2[1]+=1
                else:
                    ar2[0]+=1
        else:
            ar2=[0]*1000
            ar1=['']*1000
            j=0
            for i in range(len(db.index+1)):
                if (j==0):
                    ar1[0]=db.loc[i, array1[num1]]
                    ar2[0]+=1
                    j+=1
                else:
                    q=0
                    for t in range(j):
                        if ar1[t]==db.loc[i, array1[num1]]:
                            ar2[t]+=1
                            q=1
                    if q==0:
                        ar1[j]=db.loc[i, array1[num1]]
                        ar2[j]+=1
                        j+=1
                  
    root=Tk()
    figure1 = plt.Figure(figsize=(6,5), dpi=100)
    ax1 = figure1.add_subplot(111)
    bar1 = FigureCanvasTkAgg(figure1, root)
    bar1.get_tk_widget().pack(side=tk.LEFT, fill=tk.BOTH)
    ax1.pie(ar2,labels=ar1)
    ax1.xticks(rotation=90)
    ax1.set_title(st)
    figure1.show()
        
def piechart_win():
    """
    Окно выбора параметров для построения круговой диаграммы
    Входные параметры: нет
    Возвращаемые параметры: нет
    Автор: Нигматуллин Николай
    """
    global db
    def hd ():
       num1=combobox1.current()
       num2=2
       pie(array1, num1)
    hist_win=Tk()
    hist_win.title("Круговая диаграмма")
    hist_win.geometry("600x400")
    combobox1 = ttk.Combobox(hist_win, width = 38, state="readonly", values=['main_category', 'country','status','usd_pledged'])
    combobox1.place(relx=0.1, rely=0.3, relheight=0.2, relwidth=0.8)
    combobox1.current(0)
    array1=['main_category', 'country','status','usd_pledged']
    array2=['status', 'usd_pledged']
    lbl=Label(hist_win, text="Выберите параметр", font=('Times', 20), anchor='n')
    lbl.place(relx=0, rely=0, relheight=0.2, relwidth=1)
    btn=Button(hist_win, text='Построить', font=('Times', 20), bd=4, relief="raised", command= hd)
    btn.place(relx=0.1,rely=0.8, relheight=0.15, relwidth=0.8)

def base_stat():
    """
    Вывод базовой статистики по странам
    Входные параметры: нет
    Возвращаемые параметры: нет
    Автор: Нигматуллин Николай
    """
    global bd
    stat_window=Tk()
    stat_window.title("Базовая статистика по сборам")
    stat_window.geometry('480x240+0+0')
    df=db
    if (len(db.index)%2==0):
        med=round(db.loc[(len(db.index)/2), 'usd_pledged'],2)
    else:
        med=round(db.loc[((len(db.index)+1)/2), 'usd_pledged'],2)
    print(med)
    sall=0
    for i in range(len(db.index)):
        sall+=float(db.loc[i, 'usd_pledged'])
    sall=round(sall, 2)
    print (sall)
    srall=round(sall/len(db.index), 2)
    print (srall)
    mx=0
    mn=1.7976931348623157e+308
    mx = df.loc[:, 'usd_pledged'].dropna().max()
    for i in range(len(db.index)):
        if (float(db.loc[i, 'usd_pledged'])!=0):
            mn = min(df.loc[i, 'usd_pledged'], mn)
    lbl=Label(stat_window, text="Базовая статистика по сборам\nМаксимальные сборы: "+str(mx)+"$\nМинимальные сборы: "+ str(mn)+ "$\nСреднее значение: "+str(srall)+"$\nОбщие сборы: "+str(sall)+"$\nМедианна: "+str(med)+"$", font=('Times', 20), anchor='n', bg='#C0C0C0')
    lbl.place(relx=0, rely=0, relheight=1, relwidth=1)
    stat_window.mainloop()
def start_window():
    """
    Функция создания стартового окна пользовательского интерфейса 
    Входные параметры: нет
    Возвращаемые параметры: нет
    Автор: Нигматуллин Николай
    """
    global db
    global path
    path = None
    global newdb
    newdb = False
    global window
    window = Tk()
    window.title("Анализ проектов Kickstarter")
    window.geometry('1280x720+0+0')
    frame = Frame(window, bg='#C0C0C0')
    frame.place(relheight=1, relwidth=1)
    lbl=Label(window, text="Анализ проектов Kickstarter", font=('Times', 40), anchor='n', bg='#C0C0C0')
    lbl.place(relx=0.25, rely=0.2, relheight=0.2, relwidth=0.5)
    btn = Button(window, text="Справка", font=('Times', 20), bd=4, relief="raised", command=reference)
    btn.place(relx = 0.75, rely=0.5, relheight=0.2, relwidth=0.2)
    btn = Button(window, text="Создать базу данных", font=('Times', 20), bd=4, relief="raised", command=lambda: dbcontroller("new", None))
    btn.place(relx = 0.41, rely=0.5, relheight=0.2, relwidth=0.2)
    btn = Button(window, text="Загрузить базу данных", font=('Times', 20), bd=4, relief="raised", command=lambda: dbcontroller("open", None))
    btn.place(relx = 0.05, rely=0.5, relheight=0.2, relwidth=0.21)
    window.mainloop()
    
def close_main(mainwindow):
    """
    Закрытие главного окна
    Входные параметры: mainwindow - окно Tk()
    Выходные параметры: нет
    Автор: Нигматуллин Николай
    """
    mainwindow.destroy()
    start_window()
    
def cur_tree():
    """
    Функция вывода текущего TreeView
    Входные параметры: нет
    Выходные параметры: tree - переменная текущего TreeView
    Автор: Овчинникова Анастасия
    """
    global note
    global tree1, tree2, tree3, tree4
    id_tree = note.index("current")
    tree=tree1
    if(id_tree==1):
        tree=tree2
    if(id_tree==2):
        tree=tree3
    if(id_tree==3):
        tree=tree4
    return tree

def ins_or_edit(tree,db,code,row_value):
    """
    Функция вставки/редактирования поля
    Входные параметры: tree - текущее TreeView, db - DataFrame текущей таблицы, code - код действия (0-вставка, 1-редактирование), row_value - величины для вставки
    Выходные параметры: нет
    Автор: Овчинникова Анастасия
    """
    global projdb
    global descdb
    global locationdb
    if (code==0):
        db.loc[0] = row_value
        tree.insert('', 0, text=row_value[0], values=row_value[1:])
    else:
        db.loc[code]=row_value
        item=tree.selection()[0]
        tree.delete(item)
        tree.insert('', 0, text=row_value[0], values=row_value[1:])
        
def ins_loc(code,row_value):
    """
    Функция вставки/редактирования поля в таблицу локаций
    Входные параметры: code - код действия (0-вставка, 1-редактирование), row_value - величины для вставки
    Выходные параметры: нет
    Автор: Овчинникова Анастасия
    """
    global projdb
    global descdb
    global locationdb
    flag=False
    for i in range(len(locationdb)-1):
        if((locationdb.iloc[i]['city'] == row_value[1])&(locationdb.iloc[i]['state'] == row_value[2])&(locationdb.iloc[i]['country'] == row_value[3])):
            flag=True
    if (not flag):
        ins_or_edit(tree3,locationdb,code,row_value)
    
def Insert_row(code, row_value):
    """
    Функция определения переменных для вставки/редактирования поля
    Входные параметры: code - код действия (0-вставка, 1-редактирование), row_value - величины для вставки
    Выходные параметры: нет
    Автор: Овчинникова Анастасия
    """
    global projdb, descdb, locationdb, data
    global note
    global tree1, tree2, tree3, tree4    
    id_tree = note.index("current")
    if(id_tree==0):
        ins_or_edit(tree1,projdb,code,row_value)
        ins_or_edit(tree2,descdb,code,[row_value[0], nan, nan, nan, nan, nan, nan, nan, nan])
        ins_or_edit(tree4,data,code,[row_value[0],row_value[1],row_value[2],row_value[3],nan,nan,nan,nan,nan,nan,nan,nan,nan,nan])
    if(id_tree==1):
        ins_or_edit(tree2,descdb,code,row_value)
        ins_or_edit(tree1,projdb,code,[row_value[0],nan,nan,nan])
        ins_loc(code,[nan,row_value[5],row_value[6],nan])
        ins_or_edit(tree4,data,code,[row_value[0],nan,nan,nan,row_value[1],row_value[2],row_value[3],row_value[4],row_value[5],row_value[6],row_value[7],row_value[8],nan])
    if(id_tree==2):
        ins_loc(code,row_value)
    if(id_tree==3):
        ins_or_edit(tree4,data,code,row_value)
        ins_or_edit(tree1,projdb,code,[row_value[0],row_value[1],row_value[2],row_value[3]])
        ins_or_edit(tree2,descdb,code,[row_value[0],row_value[4],row_value[5],row_value[6],row_value[7],row_value[8],row_value[9],row_value[10],row_value[11]])
        ins_loc(code,[row_value[12],row_value[8],row_value[9],row_value[13]])

def add_field(code):
    """
    Функция создания окна для ввода данных
    Входные параметры: code - код действия (0-вставка, 1-редактирование)
    Выходные параметры: нет
    Автор: Овчинникова Анастасия
    """
    global note
    id_tree = note.index("current")
    field = Tk()
    field.title('Добавить проект')
    field.resizable(False, False)
    if(id_tree==0):
        field.geometry('320x290+500+50')
        label_description = Label(field, text='ID')
        label_description.place(x=30, y=50)
        label_select = Label(field, text='Название')
        label_select.place(x=30, y=80)
        label_main = Label(field, text='Главная категория')
        label_main.place(x=30, y=110)
        label_sub = Label(field, text='Побочная категория')
        label_sub.place(x=30, y=140)
        
        field.entry_id = ttk.Entry(field)
        field.entry_id.place(x=150, y=50)
        field.entry_name = ttk.Entry(field)
        field.entry_name.place(x=150, y=80)
        field.combobox_main = ttk.Combobox(field, values=[u'art', u'comics', u'technology', u'film & video', u'food', u'games', u'music', u'publishing'])
        field.combobox_main.current(0)
        field.combobox_main.place(x=150, y=110)
        field.entry_cat = ttk.Entry(field)
        field.entry_cat.place(x=150, y=140)
        
        btn_ok = ttk.Button(field, text='Добавить')
        btn_ok.place(x=220, y=245)
        btn_ok.bind('<Button-1>', lambda event: Insert_row(code,[field.entry_id.get(),
                                                                 field.entry_name.get(), field.combobox_main.get(), field.entry_cat.get()]))
    if(id_tree==1):
        field.geometry('320x350+500+50')
        label_description = Label(field, text='ID')
        label_description.place(x=30, y=50)
        label_date_start = Label(field, text='Дата запуска*')
        label_date_start.place(x=30, y=80)
        label_date_finish = Label(field, text='Дата окончания*')
        label_date_finish.place(x=30, y=110)
        label_dur = Label(field, text='Кол-во дней:')
        label_dur.place(x=30, y=140)
        label_goal = Label(field, text='Цель сбора')
        label_goal.place(x=30, y=170)
        label_city = Label(field, text='Город')
        label_city.place(x=30, y=200)
        label_state = Label(field, text='Штат/область')
        label_state.place(x=30, y=230)
        label_sum = Label(field, text='Собранная сумма')
        label_sum.place(x=30, y=260)
        label_insert_date = Label(field, text='*Ввод даты в формате ГГГГ-ММ-ДД')
        label_insert_date.place(x=10, y=280)
        
        field.entry_id = ttk.Entry(field)
        field.entry_id.place(x=150, y=50)
        field.entry_date_start = ttk.Entry(field)
        field.entry_date_start.place(x=150, y=80)
        field.entry_date_finish = ttk.Entry(field)
        field.entry_date_finish.place(x=150, y=110)
        field.entry_dur = ttk.Entry(field)
        field.entry_dur.place(x=150, y=140)
        field.entry_goal = ttk.Entry(field)
        field.entry_goal.place(x=150, y=170)
        field.entry_city = ttk.Entry(field)
        field.entry_city.place(x=150, y=200)
        field.entry_state = ttk.Entry(field)
        field.entry_state.place(x=150, y=230)
        field.entry_sum = ttk.Entry(field)
        field.entry_sum.place(x=150, y=260)
        
        btn_ok = ttk.Button(field, text='Добавить')
        btn_ok.place(x=220, y=305)
        btn_ok.bind('<Button-1>', lambda event: Insert_row(code,[field.entry_id.get(), field.entry_date_start.get(), field.entry_date_finish.get(), 
                                                                 field.entry_dur.get(), field.entry_goal.get(), field.entry_city.get(), field.entry_state.get(),
                                                                 'successful' if (field.entry_sum.get()>=field.entry_goal.get()) else 'failed', field.entry_sum.get()]))
    if(id_tree==2):
        field.geometry('320x230+500+50')
        label_val = Label(field, text='Валюта')
        label_val.place(x=30, y=50)
        label_city = Label(field, text='Город')
        label_city.place(x=30, y=80)
        label_state = Label(field, text='Штат/область')
        label_state.place(x=30, y=110)
        label_coun = Label(field, text='Страна')
        label_coun.place(x=30, y=140)
        
        field.combobox_val = ttk.Combobox(field, values=[u'EUR', u'USD', u'RUS'])
        field.combobox_val.current(0)
        field.combobox_val.place(x=150, y=50)
        field.entry_city = ttk.Entry(field)
        field.entry_city.place(x=150, y=80)
        field.entry_state = ttk.Entry(field)
        field.entry_state.place(x=150, y=110)
        field.entry_country = ttk.Entry(field)
        field.entry_country.place(x=150, y=140)
        
        btn_ok = ttk.Button(field, text='Добавить')
        btn_ok.place(x=220, y=185)
        btn_ok.bind('<Button-1>', lambda event: Insert_row(code,[field.combobox_val.get(),field.entry_city.get(), 
                                                                 field.entry_state.get(), field.entry_country.get()]))
    if(id_tree==3):
        field.geometry('320x500+500+50')
        label_description = Label(field, text='ID')
        label_description.place(x=30, y=50)
        label_select = Label(field, text='Название')
        label_select.place(x=30, y=80)
        label_val = Label(field, text='Валюта')
        label_val.place(x=30, y=110)
        label_main = Label(field, text='Главная категория')
        label_main.place(x=30, y=140)
        label_sub = Label(field, text='Побочная категория')
        label_sub.place(x=30, y=170)
        label_date_start = Label(field, text='Дата запуска*')
        label_date_start.place(x=30, y=200)
        label_date_finish = Label(field, text='Дата окончания*')
        label_date_finish.place(x=30, y=230)
        label_dur = Label(field, text='Кол-во дней:')
        label_dur.place(x=30, y=260)
        label_goal = Label(field, text='Цель сбора')
        label_goal.place(x=30, y=290)
        label_city = Label(field, text='Город')
        label_city.place(x=30, y=320)
        label_state = Label(field, text='Штат/область')
        label_state.place(x=30, y=350)
        label_coun = Label(field, text='Страна')
        label_coun.place(x=30, y=380)
        label_sum = Label(field, text='Собранная сумма')
        label_sum.place(x=30, y=410)
        label_insert_date = Label(field, text='*Ввод даты в формате ГГГГ-ММ-ДД')
        label_insert_date.place(x=10, y=430)
        
        field.entry_id = ttk.Entry(field)
        field.entry_id.place(x=150, y=50)
        field.entry_name = ttk.Entry(field)
        field.entry_name.place(x=150, y=80)
        field.combobox_val = ttk.Combobox(field, values=[u'EUR', u'USD', u'RUS'])
        field.combobox_val.current(0)
        field.combobox_val.place(x=150, y=110)
        field.combobox_main = ttk.Combobox(field, values=[u'art', u'comics', u'technology', u'film & video', u'food', u'games', u'music', u'publishing'])
        field.combobox_main.current(0)
        field.combobox_main.place(x=150, y=140)
        field.entry_cat = ttk.Entry(field)
        field.entry_cat.place(x=150, y=170)
        field.entry_date_start = ttk.Entry(field)
        field.entry_date_start.place(x=150, y=200)
        field.entry_date_finish = ttk.Entry(field)
        field.entry_date_finish.place(x=150, y=230)
        field.entry_dur = ttk.Entry(field)
        field.entry_dur.place(x=150, y=260)
        field.entry_goal = ttk.Entry(field)
        field.entry_goal.place(x=150, y=290)
        field.entry_city = ttk.Entry(field)
        field.entry_city.place(x=150, y=320)
        field.entry_state = ttk.Entry(field)
        field.entry_state.place(x=150, y=350)
        field.entry_country = ttk.Entry(field)
        field.entry_country.place(x=150, y=380)
        field.entry_sum = ttk.Entry(field)
        field.entry_sum.place(x=150, y=410)
        
        btn_ok = ttk.Button(field, text='Добавить')
        btn_ok.place(x=220, y=455)
        btn_ok.bind('<Button-1>', lambda event: Insert_row(code,[field.entry_id.get(), field.entry_name.get(),field.combobox_main.get(),field.entry_cat.get(),
                  field.entry_date_start.get(), field.entry_date_finish.get(),field.entry_dur.get(), 
                field.entry_goal.get(), field.entry_city.get(), field.entry_state.get(),
                'successful' if (field.entry_sum.get()>=field.entry_goal.get()) else 'failed', field.entry_sum.get(), field.combobox_val.get(), field.entry_country.get()]))

def delete_field():
    """
    Функция удаления поля из текущей таблицы
    Входные параметры: нет
    Выходные параметры: нет
    Автор: Овчинникова Анастасия
    """
    global projdb, descdb, locationdb, data
    global note
    global tree1, tree2, tree3, tree4    
    id_tree = note.index("current")
    if(id_tree==0):
        item=tree1.selection()[0]
        tree1.config(height=len(tree1.get_children()))
        for i in range(len(projdb)-1):
            if (projdb.iloc[i]['id'] == tree1.item(item, 'text')):
                projdb = projdb.drop([i]).reset_index(drop=True)
        tree1.delete(item)
        tree1.config(height=len(tree1.get_children()))
        
    if(id_tree==1):
        item=tree2.selection()[0]
        tree2.config(height=len(tree2.get_children()))
        for i in range(len(descdb)-1):
            if (descdb.iloc[i]['id'] == tree2.item(item, 'text')):
                descdb = descdb.drop([i]).reset_index(drop=True)
        tree2.delete(item)
        tree2.config(height=len(tree2.get_children()))
        
    if(id_tree==2):
        item=tree3.selection()[0]
        for i in range(len(locationdb)-1):
            if ((locationdb.iloc[i]['city'] == tree3.item(item, 'values')[0])&(locationdb.iloc[i]['state'] == tree3.item(item, 'values')[1])&(locationdb.iloc[i]['country'] == tree3.item(item, 'values')[2])):
                locationdb = locationdb.drop([i]).reset_index(drop=True) 
        tree3.delete(item)
        tree3.config(height=len(tree3.get_children()))
        tree3.config(height=len(tree3.get_children()))
                
    if(id_tree==3):
        item=tree4.selection()[0]
        for i in range(len(data)-1):
            if (data.iloc[i]['id'] == tree4.item(item, 'text')):
                data = data.drop([i]).reset_index(drop=True)
        for i in range(len(locationdb)-1):
            if ((locationdb.iloc[i]['city'] == tree4.item(item, 'values')[8])&(locationdb.iloc[i]['state'] == tree4.item(item, 'values')[9])&(locationdb.iloc[i]['country'] == tree4.item(item, 'values')[10])):
                locationdb = locationdb.drop([i]).reset_index(drop=True)
                break
        tree3.delete(tree3.identify_row(i))
        tree4.delete(item)
        tree4.config(height=len(tree4.get_children()))
    
def createmainwin():
    """
    Отображение главного окна
    Входные параметры: нет
    Возвращаемые параметры: нет
    Автор: Овчинникова Анастасия
    """
    global proj
    global desc
    global location
    global projdb
    global descdb
    global locationdb
    global path
    global path1
    global path2
    global path3
    global indexpos
    global db
    window.destroy()
    mainwindow = tki.Tk()
    mainwindow.title("Анализ проектов Kickstarter")
    mainwindow.geometry("1280x720+300+100")
    mainwindow.resizable(True, True)
    
    # Меню
    menubar = tki.Menu(mainwindow)
    mainwindow.config(menu=menubar)
    fileMenu=tki.Menu(menubar)
    fileMenu.add_command(label="Открыть другую БД", command= lambda: close_main(mainwindow))
    fileMenu.add_command(label="Сохранить как", command=lambda: dbcontroller("saveas", mainwindow))
    menubar.add_cascade(label="Файл", menu=fileMenu)
    editMenu=tki.Menu(menubar)
    editMenu.add_command(label="Добавить поле", command=lambda: add_field(0))
    editMenu.add_command(label="Редактировать поле", command=lambda: add_field(1))
    editMenu.add_command(label="Удалить поле", command=lambda: delete_field())
    menubar.add_cascade(label="Редактирование", menu=editMenu)
    anmenu=tki.Menu(menubar)
    anmenu.add_command(label="Базовая статистика", command=base_stat)
    anmenu.add_command(label="Круговая диаграмма", command=piechart_win)
    anmenu.add_command(label="Гистограмма", command=histogramm_win)
    menubar.add_cascade(label="Анализ", menu=anmenu)
    appMenu=tki.Menu(menubar)
    appMenu.add_command(label="Рук-во пользователя", command=reference)
    appMenu.add_command(label="Закрыть", command= lambda: close_main(mainwindow))
    menubar.add_cascade(label="Приложение", menu=appMenu)        
    # Конец меню
    indexpos=0
    db=proj.merge(desc, how='outer')
    db=db.merge(location).sort_values(by='id').reset_index(drop=True)
    projdb = pd.DataFrame({"id":(), "name":(), "main_category":(), "sub_category":()})
    projdb = pd.concat([projdb, proj.loc[0:19]], ignore_index=True)
    descdb = pd.DataFrame({"id":(), "launched_at":(), "deadline":(), "duration":(), "goal_usd":(), "city":(), "state":(), "status":(), "usd_pledged":()})
    descdb = pd.concat([descdb, desc.loc[0:19]], ignore_index=True)
    locationdb = pd.DataFrame({"currency":(), "city":(), "state":(), "country":()})
    locationdb = pd.concat([locationdb, location.loc[0:19]], ignore_index=True)
    data = pd.DataFrame({"id":(), "name":(), "main_category":(), "sub_category":(), "launched_at":(), "deadline":(), "duration":(), "goal_usd":(), "city":(), "state":(), "status":(), "usd_pledged":(), "currency":(), "country":()})
    data = pd.concat([data, db.loc[0:19]], ignore_index=True)
    print("Data table")
    
    toolbar = tki.Frame(bg='#d7d8e0')
    toolbar.pack(side=tki.TOP, fill=tki.X)
    btn2 = tki.Button(toolbar, text='Закрыть', command= lambda: close_main(mainwindow), bg='#d7d8e0', bd=0)   
    btn4 = tki.Button(toolbar, text='Сохранить как..', command = lambda: dbcontroller("saveas", mainwindow))
    btn2.pack(side=tki.LEFT, fill=tki.X)
    btn4.pack(side=tki.TOP, fill=tki.X)
    # Notebook
    global note
    note = ttk.Notebook(mainwindow)

    tab1 = Frame(note)
    tab2 = Frame(note)
    tab3 = Frame(note)
    tab4 = Frame(note)

    note.add(tab1, text = "Проекты")
    note.add(tab2, text = "Описание проекта")
    note.add(tab3, text = "Локации")
    note.add(tab4, text = "Полная таблица")
    
    global tree1
    global tree2
    global tree3
    global tree4
    # TreeView
    treeframe4 = tki.Frame(tab4, bg='#ff6347')
    treeframe4.pack(expand=True)
    tree4 = ttk.Treeview(treeframe4, columns=data[1:])
    vsb_4 = tki.Scrollbar(treeframe4, orient="vertical", command=tree4.yview)
    vsb2_4 = tki.Scrollbar(treeframe4, orient="horizontal", command=tree4.xview)
    tree4.configure(yscrollcommand=vsb_4.set, xscrollcommand=vsb2_4.set)
    vsb_4.pack(side="right", fill="y")
    vsb2_4.pack(side="bottom", fill=tki.X)  
    tree4.pack()
    
    treeframe3 = tki.Frame(tab3, bg='#ff6347')
    treeframe3.pack(expand=True)
    tree3 = ttk.Treeview(treeframe3, columns=data[1:])
    vsb_3 = tki.Scrollbar(treeframe3, orient="vertical", command=tree3.yview)
    vsb2_3 = tki.Scrollbar(treeframe3, orient="horizontal", command=tree3.xview)
    tree3.configure(yscrollcommand=vsb_3.set, xscrollcommand=vsb2_3.set)
    vsb_3.pack(side="right", fill="y")
    vsb2_3.pack(side="bottom", fill=tki.X)  
    tree3.pack()
    
    treeframe2 = tki.Frame(tab2, bg='#ff6347')
    treeframe2.pack(expand=True)
    tree2 = ttk.Treeview(treeframe2, columns=data[1:])
    vsb_2 = tki.Scrollbar(treeframe2, orient="vertical", command=tree2.yview)
    vsb2_2 = tki.Scrollbar(treeframe2, orient="horizontal", command=tree2.xview)
    tree2.configure(yscrollcommand=vsb_2.set, xscrollcommand=vsb2_2.set)
    vsb_2.pack(side="right", fill="y")
    vsb2_2.pack(side="bottom", fill=tki.X)  
    tree2.pack()
    
    treeframe1 = tki.Frame(tab1, bg='#ff6347')
    treeframe1.pack(expand=True)
    tree1 = ttk.Treeview(treeframe1, columns=data[1:])
    vsb_1 = tki.Scrollbar(treeframe1, orient="vertical", command=tree1.yview)
    vsb2_1 = tki.Scrollbar(treeframe1, orient="horizontal", command=tree1.xview)
    tree1.configure(yscrollcommand=vsb_1.set, xscrollcommand=vsb2_1.set)
    vsb_1.pack(side="right", fill="y")
    vsb2_1.pack(side="bottom", fill=tki.X)  
    tree1.pack()
    # Notebook
    note.pack()
    # Нижнее меню
    bottommenu = tki.Frame(tab4)
    bottommenu.pack(expand=True)
    toleftbtn = tki.Button(bottommenu, text='<<', command= lambda: turnleftdb(mainwindow, tree4, page))
    torightbtn = tki.Button(bottommenu, text='>>', command= lambda: turnrightdb(mainwindow, tree4, page))
    page1label = tki.Label(bottommenu, text='Страница')
    if(int(len(db.index))%20==0):
        page2label = tki.Label(bottommenu, text=' из ' + str(int(len(db.index)/20)))
    else:
        page2label = tki.Label(bottommenu, text=' из ' + str(int(len(db.index)/20+1)))
    page = tki.StringVar()
    page.set(indexpos+1)
    page.trace("w", lambda name, index, mode, page=page: changepage(page, mainwindow, tree4))
    pageinput = tki.Entry(bottommenu, width=10, textvariable=page)
    toleftbtn.pack(side=tki.LEFT, fill=tki.X)
    page1label.pack(side=tki.LEFT, fill=tki.X)
    pageinput.pack(side=tki.LEFT, fill=tki.X)
    page2label.pack(side=tki.LEFT, fill=tki.X)
    torightbtn.pack(side=tki.LEFT, fill=tki.X)
    # Нижнее меню 1 вкладка
    bottommenu1 = tki.Frame(tab1)
    bottommenu1.pack(expand=True)
    pagelabel1 = tki.Label(bottommenu1, text='Страница')
    if(int(len(proj.index))%20==0):
        page2label1 = tki.Label(bottommenu1, text=' из ' + str(int(len(proj.index)/20)))
    else:
        page2label1 = tki.Label(bottommenu1, text=' из ' + str(int(len(proj.index)/20+1)))
    page1 = tki.StringVar()
    page1.set(indexpos+1)
    page1.trace("w", lambda name, index, mode, page=page: changepage1(page1, mainwindow, tree1))
    pageinput1 = tki.Entry(bottommenu1, width=10, textvariable=page1)
    pagelabel1.pack(side=tki.LEFT, fill=tki.X)
    pageinput1.pack(side=tki.LEFT, fill=tki.X)
    page2label1.pack(side=tki.LEFT, fill=tki.X)
    # Нижнее меню 2 вкладка
    bottommenu2 = tki.Frame(tab2)
    bottommenu2.pack(expand=True)
    pagelabel2 = tki.Label(bottommenu2, text='Страница')
    if(int(len(desc.index))%20==0):
        page2label2 = tki.Label(bottommenu2, text=' из ' + str(int(len(desc.index)/20)))
    else:
        page2label2 = tki.Label(bottommenu2, text=' из ' + str(int(len(desc.index)/20+1)))
    page2 = tki.StringVar()
    page2.set(indexpos+1)
    page2.trace("w", lambda name, index, mode, page=page: changepage2(page2, mainwindow, tree2))
    pageinput2 = tki.Entry(bottommenu2, width=10, textvariable=page2)
    pagelabel2.pack(side=tki.LEFT, fill=tki.X)
    pageinput2.pack(side=tki.LEFT, fill=tki.X)
    page2label2.pack(side=tki.LEFT, fill=tki.X)
    # Нижнее меню 3 вкладка
    bottommenu3 = tki.Frame(tab3)
    bottommenu3.pack(expand=True)
    pagelabel3 = tki.Label(bottommenu3, text='Страница')
    if(int(len(location.index))%20==0):
        page2label3 = tki.Label(bottommenu3, text=' из ' + str(int(len(location.index)/20)))
    else:
        page2label3 = tki.Label(bottommenu3, text=' из ' + str(int(len(location.index)/20+1)))
    page3 = tki.StringVar()
    page3.set(indexpos+1)
    page3.trace("w", lambda name, index, mode, page=page: changepage3(page3, mainwindow, tree3))
    pageinput3 = tki.Entry(bottommenu3, width=10, textvariable=page3)
    pagelabel3.pack(side=tki.LEFT, fill=tki.X)
    pageinput3.pack(side=tki.LEFT, fill=tki.X)
    page2label3.pack(side=tki.LEFT, fill=tki.X)    
    # RenderTree
    render_tree(data,mainwindow, tree4)
    render_tree(locationdb, mainwindow, tree3)
    render_tree(descdb, mainwindow, tree2)
    render_tree(projdb, mainwindow, tree1)
    mainwindow.mainloop()

def changepage(page, mainwindow, tree):
    """
    Функция смены страниц
    Входные параметры: page - StringVar(), mainwindow - текущее окно, tree - TreeView для вывода
    Выходные параметры: нет
    Автор: Угодников Андрей
    """
    global indexpos
    try:
        p = int(page.get())
    except ValueError:
        p = 0
    else:
        if(p>0 and p<int(len(db.index)/20+2)):
            indexpos=p-1
            data = pd.DataFrame({"id":(), "name":(), "main_category":(), "sub_category":(), "launched_at":(), "deadline":(), "duration":(), "goal_usd":(), "city":(), "state":(), "status":(), "usd_pledged":(), "currency":(), "country":()})
            data = pd.concat([data, db.loc[0+indexpos*20:19+indexpos*20]], ignore_index=True)
            print("Indexpos ", indexpos)
            print("Укорочена")
            render_tree(data, mainwindow, tree)        

def changepage1(page, mainwindow, tree):
    """
    Функция смены страниц
    Входные параметры: page - StringVar(), mainwindow - текущее окно, tree - TreeView для вывода
    Выходные параметры: нет
    Автор: Угодников Андрей
    """
    global indexpos
    try:
        p = int(page.get())
    except ValueError:
        p = 0
    else:
        if(p>0 and p<int(len(db.index)/20+2)):
            indexpos=p-1
            projdb = pd.DataFrame({"id":(), "name":(), "main_category":(), "sub_category":()})
            projdb = pd.concat([projdb, proj.loc[0+indexpos*20:19+indexpos*20]], ignore_index=True)
            print("Indexpos ", indexpos)
            render_tree(projdb, mainwindow, tree)

def changepage2(page, mainwindow, tree):
    """
    Функция смены страниц
    Входные параметры: page - StringVar(), mainwindow - текущее окно, tree - TreeView для вывода
    Выходные параметры: нет
    Автор: Угодников Андрей
    """
    global indexpos
    try:
        p = int(page.get())
    except ValueError:
        p = 0
    else:
        if(p>0 and p<int(len(db.index)/20+2)):
            indexpos=p-1
            descdb = pd.DataFrame({"id":(), "launched_at":(), "deadline":(), "duration":(), "goal_usd":(), "city":(), "state":(), "status":(), "usd_pledged":()})
            descdb = pd.concat([descdb, desc.loc[0+indexpos*20:19+indexpos*20]], ignore_index=True)
            print("Indexpos ", indexpos)
            render_tree(descdb, mainwindow, tree)

def changepage3(page, mainwindow, tree):
    """
    Функция смены страниц
    Входные параметры: page - StringVar(), mainwindow - текущее окно, tree - TreeView для вывода
    Выходные параметры: нет
    Автор: Угодников Андрей
    """
    global indexpos
    try:
        p = int(page.get())
    except ValueError:
        p = 0
    else:
        if(p>0 and p<int(len(db.index)/20+2)):
            indexpos=p-1
            locationdb = pd.DataFrame({"currency":(), "city":(), "state":(), "country":()})
            locationdb = pd.concat([locationdb, location.loc[0+indexpos*20:19+indexpos*20]], ignore_index=True)
            print("Indexpos ", indexpos)
            render_tree(locationdb, mainwindow, tree)
            
def turnleftdb(mainwindow, tree, page):
    """
    Открыть левую страницу относительно текущей
    Входные параметры: page - StringVar(), mainwindow - текущее окно, tree - TreeView для вывода
    Выходные параметры: нет
    Автор: Угодников Андрей
    """
    global indexpos
    if(indexpos>0):
        indexpos=indexpos-1
        page.set(indexpos+1)
        data = pd.DataFrame({"id":(), "name":(), "main_category":(), "sub_category":(), "launched_at":(), "deadline":(), "duration":(), "goal_usd":(), "city":(), "state":(), "status":(), "usd_pledged":(), "currency":(), "country":()})
        data = pd.concat([data, db.loc[0+indexpos*20:19+indexpos*20]], ignore_index=True)
        print("Indexpos ", indexpos)
        render_tree(data, mainwindow, tree)
        
def turnrightdb(mainwindow, tree, page):
    """
    Открыть правую страницу относительно текущей
    Входные параметры: page - StringVar(), mainwindow - текущее окно, tree - TreeView для вывода
    Выходные параметры: нет
    Автор: Угодников Андрей
    """
    global indexpos
    print("DB Length is ", len(db.index))
    print("Pages ", len(db.index)/20)
    if(indexpos<(len(db.index)/20-1)):
        indexpos=indexpos+1
        page.set(indexpos+1)
        data = pd.DataFrame({"id":(), "name":(), "main_category":(), "sub_category":(), "launched_at":(), "deadline":(), "duration":(), "goal_usd":(), "city":(), "state":(), "status":(), "usd_pledged":(), "currency":(), "country":()})
        data = pd.concat([data, db.loc[0+indexpos*20:19+indexpos*20]], ignore_index=True)   
        print("Indexpos ", indexpos)
        render_tree(data, mainwindow, tree)

def render_tree(data, mainwindow, tree):
    """
    Вывод дерева
    Входные параметры: data - часть БД для вывода (20 строк), mainwindow - текущее окно, tree - TreeView для вывода
    Выходные параметры: нет
    Автор: Угодников Андрей (обработка чисел и исключений), Овчинникова Анастасия (вывод дерева)
    """
    print("Render table")
    mainwindow.update_idletasks()
    tree.delete(*tree.get_children())
    text = data.columns.values
    s = mainwindow.geometry()
    s = s.split('+')
    s = s[0].split('x')
    width_root = int(s[0])
    print(data.columns.values)
    for i, j in enumerate(text):
        tree.column(f"#{i}", width=round(width_root/len(text))) 
        tree.heading(f"#{i}", text=j)
    for i in range(len(data[text[0]])):
        stroka=list(map(lambda x: data[x][i], text[1:]))
        try:
            z=data.columns.values.tolist().index('goal_usd')
        except ValueError:
            z=0
        else:
            stroka[z-1]=round(stroka[z-1],2)
        try:
            z=data.columns.values.tolist().index('usd_pledged')
        except ValueError:
            z=0
        else:
            stroka[z-1]=round(stroka[z-1],2)
        try:
            z=data.columns.values.tolist().index('duration')
        except ValueError:
            z=0
        else:
            stroka[z-1]=int(stroka[z-1])
        try:
            z=data.columns.values.tolist().index('id')
            stroka[z-1]=int(stroka[z-1])
        except ValueError:
            z=0
        if(data.columns[0] == 'id'):
            tree.insert('', 'end', text=int(data[text[0]][i]), values=stroka)
        else:
            tree.insert('', 'end', text=data[text[0]][i], values=stroka)            
    tree.config(height=len(tree.get_children()))

def main():
    start_window()
    
    
if __name__ == '__main__':
    main()