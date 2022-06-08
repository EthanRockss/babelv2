import sqlite3

def createSetTable(dbPath:str="Cogs/Cogs.db"):
    con = sqlite3.connect(dbPath)
    cur = con.cursor()
    cur.execute('''CREATE TABLE IF NOT EXISTS setting (name, value, UNIQUE(name, value))''')
    con.commit()
    con.close()  

def addSetting(cogName:str, setName:str, setValue:any, dbPath:str="Cogs/Cogs.db"):
    con = sqlite3.connect(dbPath)
    cur = con.cursor()
    cur.execute('''INSERT OR IGNORE INTO setting(cog, name, value) VALUES(?,?,?)''', (cogName, setName, setValue))
    con.commit()
    con.close()

def updateSetting(cogName:str, setName:str, setValue:any, dbPath:str="Cogs/Cogs.db"):
    con = sqlite3.connect(dbPath)
    cur = con.cursor()
    cur.execute('''UPDATE setting SET value=? WHERE name=? AND cog=?''', (setValue, setName, cogName))
    con.commit()
    con.close()

def fetchSetting(cogName:str, setName:str, dbPath:str="Cogs/Cogs.db"):
    con = sqlite3.connect(dbPath)
    cur = con.cursor()
    value = cur.execute('''SELECT value FROM setting WHERE name=? AND cog=?''',(setName, cogName))
    con.close()
    return value