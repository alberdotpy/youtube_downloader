import sqlite3
from datetime import datetime


def update_db(author, title, elapsed):
    conn = sqlite3.connect('YoutubeVideos.db')
    c = conn.cursor()
    c.execute('''
    CREATE TABLE IF NOT EXISTS videos (
    author text,
    title text,
    date text,
    elapsed text
    )
    ''')
    c.execute('INSERT INTO videos VALUES (?, ?, ?, ?)',
              (str(author), str(title), str(datetime.now()), str(elapsed)))
    conn.commit()
    conn.close()


def query_table():
    conn = sqlite3.connect('YoutubeVideos.db')
    c = conn.cursor()
    c.execute(''' SELECT * from videos''')
    result = c.fetchall()
    print(result)
    return result

dt = query_table()
print(dt[0][0])
