import sqlite3
import time
import hashlib
import tkinter as tk

global connection, cursor
connection = None
cursor = None

def connect(path):
    '''
        Description: Connect to the database
        Args:
            path: path to the database
        Return: None
    '''
    global connection, cursor

    connection = sqlite3.connect(path)
    cursor = connection.cursor()
    cursor.execute(' PRAGMA forteign_keys=ON; ')
    create_count_keywords()
    create_larger()
    connection.commit()
    return

def create_count_keywords():
    connection.create_function('count_keywords',2, count_keywords)
    return

def count_keywords(text, keywords):
    '''
        Description: find the number of time keywords appear in text
        Args:
            text: the songs name or playlists name
        Return:
            cnt: the number of times keywords appear in text
    '''
    keywords = keywords.split()
    text = text.upper()
    cnt = 0
    for keyword in keywords:
        if keyword.upper() in text:
            cnt += 1
    return cnt

def create_larger():
    connection.create_function('larger', 2, larger)
def larger(a,b):
    try:
        if a >= int(b):
            return a
        else:
            return int(b)
    except: 
        print("cant compare")
#path = "../spotime.db"
# "../test.db"
print(count_keywords("Retro Music", "retro"))
path = input("Enter the path of the database: ")
connect(path)

