# -*- coding: utf-8 -*-
"""
database_csl.py
Файл, содержащий функции создания/сохранения/загрузки БД
в формате csv/xls/xlsx
"""

import pandas as pd
import tkinter as tki
from tkinter import filedialog, messagebox

def opendb(dbname):
    """
    Функция открытия Базы Данных из файла
    Входные параметры: bdname - базу, которую надо выбрать
    Возвращаемые параметры: db=pandas.DataFrame
    Автор: Андрей Угодников
    """
    window = tki.Tk()
    window.withdraw()
    try:
        file = filedialog.askopenfile(defaultextension='.csv', filetypes=[('CSV files','*.csv'), ('Excel files', '*.xls*'), ('All files','*.*')]).name
    except AttributeError:
        box = messagebox.askyesno(title="Анализ проектов Kickstarter - Открытие базы данных" + dbname, message="Файл не выбран\nХотите выбрать заново?")
        if box:
            window.destroy()
            opendb(dbname)
        else:
            window.destroy()
            return None, None
    ext=str(file).split('.')[-1]
    if(ext=="csv"):
        database = pd.read_csv(file)
        window.destroy()
        return database, file
    elif(ext=="xls" or ext=="xlsx"):
        excelbox = messagebox.askyesno(title="Анализ проектов Kickstarter - Открытие базы данных", message="Файлы Excel требуют больше времени на открытие.\nВы хотите продолжить?")
        if excelbox:
            database = pd.read_excel(file)
            window.destroy()
            return database, file
        else: 
            window.destroy()
            opendb(dbname)
    else:
        messagebox.showerror(title="Анализ проектов Kickstarter - Открытие базы данных", message="Выбранный файл не поддерживается.\nПоддерживаемые форматы: csv, xls, xlsx")
        window.destroy()
        opendb(dbname)
    window.destroy()

def createdb():
    """
    Функция создания новой Базы Данных (новый датафрейм)
    Входные параметры: нет
    Возвращаемые параметры: pandas.DataFrame - пустые базы данных
    Автор: Андрей Угодников
    """
    projdb = pd.DataFrame({"id":(), "name":(), "main_category":(), "sub_category":()})
    descdb = pd.DataFrame({"id":(), "launched_at":(), "deadline":(), "duration":(), "goal_usd":(), "city":(), "state":(), "status":(), "usd_pledged":()})
    locationdb = pd.DataFrame({"currency":(), "city":(), "state":(), "country":()})
    return projdb, descdb, locationdb

def savedb(db, path):
    """
    Функция сохранения Базы Данных
    Входные параметры: db=pandas.DataFrame, path-string путь до файла
    Возвращаемые параметры: нет
    Автор: Андрей Угодников
    """
    ext=str(path).split('.')[-1]
    if(ext=="csv"):
        db.to_csv(path, index=False)
    elif(ext=="xls" or ext=="xlsx"):
        db.to_excel(path, index=False)

def saveasdb(db):
    """
    Функция "сохранить как" для Базы Данных
    Входные параметры: db=pandas.DataFrame
    Возвращаемые параметры: нет
    Автор: Андрей Угодников
    """
    window = tki.Tk()
    window.withdraw()
    file = filedialog.asksaveasfilename(defaultextension='.csv',filetypes=[('CSV files','*.csv'), ('Excel files', '*.xls*')])
    ext=str(file).split('.')[-1]
    if(ext=="csv"):
        db.to_csv(file, index=False)
        window.destroy()
        return file
    elif(ext=="xls" or ext=="xlsx"):
        db.to_excel(file, index=False)
        window.destroy()
        return file