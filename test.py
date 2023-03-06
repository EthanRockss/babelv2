import sqlite3

con = sqlite3.connect("cogs/cogsettings/utils.db")
cur = con.cursor()
cur.execute('''CREATE TABLE IF NOT EXISTS logchannel (guildid, channelid)''')

cur.execute('''SELECT * FROM logchannel WHERE guildid=?''', (guildid,))
if cur.fetchone() != None:
    cur.execute('''SELECT * FROM logchannel WHERE guildid=?''', (guildid,))
    if cur.fetchone()[1] == channelid:
        print("no need for change")
    else:
        cur.execute('''UPDATE logchannel SET channelid=? WHERE guildid=?''', (channelid, guildid))
        print("updated")
else:
    cur.execute('''INSERT INTO logchannel (guildid, channelid) VALUES (?, ?)''', (guildid, channelid))
    print("created new")
con.commit()
con.close()