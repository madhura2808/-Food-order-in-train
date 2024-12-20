import sqlite3


def create_connection():
    con = sqlite3.connect('instance/database.db')
    cur = con.cursor()
    return con, cur


def createtable():
    con, cur = create_connection()
    cur.execute("create table if not exists shopinfo(id integer primary key autoincrement, name text(30), username text(30), shop_name text(30), address text(50))")
    con.commit()
    
def removecolumn():
    con, cur = create_connection()
    cur.execute("delete from access WHERE id=2")
    con.commit()    

def droptable(tablename):
    con, cur = create_connection()
    cur.execute(f"drop table {tablename}")
    con.commit()

def actions():
    con, cur = create_connection()
    # droptable('shopinfo')
    createtable()
    # removecolumn()

    con.close()

actions()