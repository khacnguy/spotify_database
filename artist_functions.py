from connection import *
from tkinter import messagebox

def check_new_song(aid_list, title, duration):
    '''
        Description: Check if the new song already exists
        Arguments: 
            aid_list: aid and the additional artists
            title, duration: title and duration of the song (unique)
        Return:

    '''
    for aid in aid_list:
        print(aid)
        cursor.execute('''SELECT * 
                        FROM songs, perform 
                        WHERE title = ? AND duration = ? AND aid = ? AND songs.sid = perform.sid;
                        ''',(title,duration,aid))
        result = cursor.fetchone()
        print(result)
        if result is not None:
            return False
    return True
    
def add_song(aid, title, duration, additional_aid):
    '''
        Description: add the new song for all artists listed
        Arguments:
            aid: main artist
            additional_aid: additional artists
            title, duration: title and duration of the song (unique)
    '''
    sid = generate_sid()
    if additional_aid != '':
        additional_aid = additional_aid.split(",")

        # check adding user as the using user
        if aid in additional_aid:
            return False

        # check if additional IDs are in the database
        cursor.execute("SELECT aid FROM artists;")
        aids_list = []
        for id in cursor.fetchall():
            aids_list.append(id[0])
        print(aids_list)
        for id in additional_aid:
            if id not in aids_list:
                return False

        aid_list = additional_aid + [aid]
    else: aid_list = [aid]
    data = [[x,sid] for x in aid_list]
    if check_new_song(aid_list,title,duration):
        cursor.execute("INSERT INTO songs VALUES (?,?,?)",(sid, title, duration))
        cursor.executemany("INSERT INTO perform VALUES (?,?);",data)
    else:
        return False
    connection.commit()
    return True

def generate_sid():
    '''
        Description: generate a new sid for the song
        Arguments: 
            None
        Return: 
            sid: new sid
    '''
    cursor.execute("SELECT MAX(sid) FROM songs;")
    sid = cursor.fetchone()[0] + 1
    return sid

def topFans(artist_id):
    '''
        Description: find top fans
        Arguments:
            artist_id: artist id
        Return:
            top_users: the list of top
    '''
    # find the top 3 users who listen to their songs the longest time
    cursor.execute(''' 
                    SELECT listen.uid, users.name
                    FROM listen, perform, songs, users
                    WHERE listen.sid = songs.sid 
                          AND users.uid = listen.uid
                          AND perform.sid = songs.sid 
                          AND perform.aid = ?
                    GROUP BY listen.uid
                    ORDER BY SUM(listen.cnt*songs.duration) DESC
                    LIMIT 3;
                    ''', (artist_id,)                    
                   )
    top_users = cursor.fetchall()
    return top_users

def topPLs(artist_id):
    '''
        Description: find top 3 playlists
        Arguments: 
            artist_id: artist id
        Return: 
            None
    '''
    cursor.execute(''' 
                    SELECT plinclude.pid, playlists.title
                    FROM plinclude, perform, playlists
                    WHERE plinclude.sid = perform.sid
                          AND playlists.pid = plinclude.pid
                          AND perform.aid = ?
                    GROUP BY plinclude.pid
                    ORDER BY COUNT(*) DESC
                    LIMIT 3;
                    ''', (artist_id,)                       
                   )
    top_pls = cursor.fetchall()

            
    return top_pls



