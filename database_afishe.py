import sqlite3 as sql
import os
import pandas as pd

DATABASE = '/home/tehnokrat/PythonProjects/db.sqlite'

if not os.path.exists(DATABASE):
    con = sql.connect(DATABASE)
    cur = con.cursor()
    cur.execute('CREATE TABLE posters (source, picture_url, text, status)')
    cur.execute('CREATE TABLE groups (group_id, domain, last_post_id, post_text, photo_attachments_url, is_published)')
    cur.close()
    con.close()


def get_poster(poster_id=None):
    con = sql.connect(DATABASE)
    cur = con.cursor()
    info = list(cur.execute("SELECT * FROM posters"))[-1]
    cur.close()
    con.close()
    return info


def set_poster(source="VK", picture_url=None, text="#афиша", status="new"):
    con = sql.connect(DATABASE)
    cur = con.cursor()
    df = pd.DataFrame([[source, picture_url, text, status]],
                      columns=['source', 'picture_url', 'text', 'status'])
    print(df)
    df.to_sql('posters', con, if_exists='append', index=False)
    con.commit()
    cur.close()
    con.close()


def get_groups(group_id=None):
    con = sql.connect(DATABASE)
    cur = con.cursor()
    existance = bool(cur.execute("SELECT * FROM groups").fetchall())
    if existance:
        if group_id:
            info = list(cur.execute(f"SELECT * FROM groups WHERE group_id = {group_id}").fetchall())
            cur.close()
            con.close()
            return info
        else:
            info = list(cur.execute("SELECT * FROM groups").fetchall())
            cur.close()
            con.close()
            return info
    else:
        return existance


def set_group(group_id: int, domain: str, last_post_id: int = None, post_text=None, photo_attachments_url=None, is_published=False):
    con = sql.connect(DATABASE)
    cur = con.cursor()
    existence = cur.execute('SELECT * FROM groups WHERE group_id = {}'.format(group_id)).fetchall()
    if not existence:
        df = pd.DataFrame([[group_id, domain, last_post_id, post_text, photo_attachments_url, is_published]],
                          columns=['group_id', 'domain', 'last_post_id', 'post_text', 'photo_attachments_url', 'is_published'])
        print(df)
        df.to_sql('groups', con, if_exists='append', index=False)
    else:
        print("initializing")
        sql_update = """UPDATE groups SET last_post_id=?, post_text=?, photo_attachments_url=?, is_published=? WHERE group_id=?"""
        data = (last_post_id, post_text, photo_attachments_url, is_published, group_id)
        cur.execute(sql_update, data)
    con.commit()
    cur.close()
    con.close()
