import time
from connection import *


def start_session(uid):
    '''
        Description: start a session for the user with a new unique session number 
        Args:
            uid: user id
        Return: 
            sno: a unique new session number for that user
    '''
    #get data to insert into the database
    current_date = time.strftime("%H:%M:%S %Y-%m-%d")
    sno = generate_sno(uid)
    
    #end_date is NULL
    cursor.execute("""INSERT INTO sessions (uid, sno, start) VALUES (?,?,?);""",(uid, sno, current_date))

    connection.commit()
    return sno
    
def generate_sno(uid):
    '''
        Description: generate a new session number for a user
        Args:
            uid: user id
        Return:
            sno: a unique new session number for that user
    '''
    cursor.execute("""SELECT MAX(sno) FROM sessions WHERE sessions.uid = ?;""", (uid,))
    result =  cursor.fetchone()
    if result == (None,):
        return 1
    return result[0]+1

def check_duplicates(keywords):
    '''
        Description: check if keywords contain duplicates
        Args:
            keywords: a text containing the keyword (input by the user)
        Return:
            bool: True if there's duplicates, False otherwise
    '''
    keywords_list = keywords.split()
    if len(keywords_list) != len(set(keywords_list)):
        return True
    return False

def search_songs(keywords):
    '''
        Description: search songs based on the keywords
        Args: 
            keywords: a text containing the keyword (input by the user)
        Return:
            songs_list: a list of songs order by the number of time keywords appear
    '''

    cursor.execute(
                """
                SELECT sid, title, duration, count_keywords(title, ?)
                FROM songs 
                WHERE count_keywords(title, ?) != 0
                ORDER BY count_keywords(title, ?) DESC;
                """, (keywords,keywords,keywords))
    songs_list = cursor.fetchall()
    return songs_list

def search_playlists(keywords):
    '''
        Description: search playlist based on the keywords
        Args: 
            keywords: a text containing the keyword (input by the user)
        Return:
            playlists_list: a list of playlist order by the number of time keywords appear
    '''

    cursor.execute(
                """
                SELECT p.pid, p.title, SUM(s.duration), count_keywords(p.title, ?)
                FROM playlists p 
                LEFT OUTER JOIN  plinclude pl using (pid) 
                LEFT OUTER JOIN songs s using (sid)
                WHERE count_keywords(p.title, ?) != 0
                GROUP BY p.pid
                ORDER BY count_keywords(p.title, ?) DESC;
                """, (keywords, keywords, keywords))
    playlists_list = cursor.fetchall()
    print(playlists_list)
    return playlists_list

def search_artist(keywords):
    '''
        Description: search artists based on the keywords
        Args: 
            keywords: a text containing the keyword (input by the user)
        Return:
            artist_list: a list of artists, their name, nationality, number of songs order by the number of time keywords appear
    '''

    cursor.execute(
                """
                    SELECT a.aid, a.name, a.nationality, IFNULL(COUNT(DISTINCT sid),0)
                    FROM artists a LEFT OUTER JOIN perform p USING (aid) LEFT OUTER JOIN songs s USING (sid)
                    GROUP BY a.aid
                    HAVING larger(count_keywords(a.name, ?), count_keywords(IFNULL(s.title, ""), ?)) != 0
                    ORDER BY larger(count_keywords(a.name, ?), count_keywords(IFNULL(s.title, ""), ?)) DESC;
                """,(keywords, keywords, keywords, keywords))
    artists_list = cursor.fetchall()
    return artists_list

def search(keywords):
    '''
        Description: merge the results of search artist and search playlist
        Args: 
            keywords: a text containing the keyword (input by the user)
        Return:
            result: the merged result
    '''
    pl_list = search_playlists(keywords)
    songs_list = search_songs(keywords)

    # merge sort
    i,j = 0,0
    result = []
    while i < len(pl_list) and j < len(songs_list):
        if pl_list[i][3] < songs_list[j][3]:
            result.append(list(songs_list[j]) + ["s"])
            j += 1
        else:
            result.append(list(pl_list[i]) + ["pl"])
            i += 1
    
    while i < len(pl_list):
        result.append(list(pl_list[i]) + ["pl"])
        i += 1
    
    while j < len(songs_list):
        result.append(list(songs_list[j]) + ["s"])
        j += 1
    
    return result

def getsong_playlist(pid):
    '''
        Description: get song from playlists
        Args:
            pid: playlist id
        Return: 
            songs_list: list of songs in the playlist including id, title, duration
    '''
    cursor.execute(
                """
                SELECT s.sid, s.title, s.duration
                FROM plinclude pl, songs s
                WHERE pl.pid = ?
                AND pl.sid = s.sid;
                """,(pid,))
    songs_list = cursor.fetchall()
    return songs_list

def getsong_artist(aid):
    '''
        Description: get songs performed by artists
        Args:
            aid: artist id
        Return:
            songs_list: list of songs performed by an artist
    '''
    cursor.execute(
                """
                SELECT s.sid, s.title, s.duration
                FROM perform p, songs s
                WHERE p.sid = s.sid
                AND p.aid = ?;
                """, (aid,))
    songs_list = cursor.fetchall()
    return songs_list

def end_session(uid, sno):
    '''
        Description: end the current session of the user
        Args:
            uid: user id
            sno: session number 
        Return: 
            None
    '''
    current_date = time.strftime("%H:%M:%S %Y-%m-%d")
    cursor.execute("""UPDATE sessions SET end = ? WHERE sessions.uid = ? AND sessions.sno = ?;""", (current_date, uid, sno))
    connection.commit()
    return

def get_song_information(sid):
    '''
        Description: get song information
        Args:
            sid: song id
        Return:
            song_info: song information
            artist_info: artist performed that song
            pl_info: playlist the song is in
    '''
    cursor.execute("""SELECT * FROM songs WHERE sid == ?;""", (sid,))
    song_info = cursor.fetchone()

    cursor.execute("""SELECT name FROM artists a, perform p WHERE a.aid = p.aid AND p.sid = ?;""",(sid,))
    artist_info = cursor.fetchall()

    cursor.execute("""SELECT title FROM playlists p, plinclude pl WHERE p.pid = pl.pid AND pl.sid = ?;""",(sid,))
    pl_info = cursor.fetchall()

    connection.commit()

    return song_info, artist_info, pl_info

def get_playlist(uid):
    '''
        Description: get the user_playlist
        Args: 
            uid: user id
            sid: song id
        Return:
            None
    '''
    cursor.execute("""SELECT pid, title FROM playlists p WHERE uid = ?""",(uid,))
    pls = cursor.fetchall() 
    connection.commit()

    return pls

def add_to_existed_playlist(pid,sid):
    '''
        Description: add the song to a playlist
        Arguments:
            pid: playlist id
            sid: song id
        Return: 
            None
    '''
    cursor.execute("SELECT * FROM plinclude WHERE pid = ? AND sid = ?;",(pid,sid))
    if cursor.fetchone() != None:
        return False
    else:
        cursor.execute("""INSERT INTO plinclude(pid, sid, sorder) VALUES (?,?,?);""", (pid, sid, get_new_order(pid)))
    connection.commit()
    return True

def get_new_order(pid):
    '''
        Description: generate a new order number for a new song in the playlist
        Args:
            pid: playlist id
        Return:
            sorder: order of the new song
    '''
    cursor.execute("""SELECT MAX(sorder) FROM plinclude WHERE pid = ?;""", (pid,))
    sorder = cursor.fetchone()[0]
    if sorder is None: 
        return 1
    connection.commit()

    return sorder +1

def add_song_session(sid, uid, sno, cnt):
    '''
        Description: add song to session
        Args: 
            sid: song id
            uid: playlist id
            sno: session number
            cnt: count (1 in this case)
        Return:
            None
    '''
    cursor.execute("""SELECT * FROM listen WHERE sid = ? AND sno = ? AND uid = ?;""",(sid,sno,uid))
    if cursor.fetchone() == None:
        cursor.execute("""INSERT INTO listen(uid, sno, sid, cnt) VALUES (?,?,?,?);""", (uid, sno, sid, cnt))
    else:
        cursor.execute("""UPDATE listen SET cnt = cnt + ? WHERE sid = ? AND sno = ? AND uid = ?;""",(cnt,sid,sno,uid))
     
    connection.commit()

    return


def create_playlist_and_add_song(uid, title, sid):
    '''
        Description: create playlist and add the new song in
        Args:
            uid: user id
            title: playlist title
            sid: song_id
        Return:
            None
    '''
    pid = generate_pid()
    cursor.execute(
                """INSERT INTO playlists (pid, title, uid) VALUES (?,?,?);""", (pid, title, uid))
    cursor.execute("""INSERT INTO plinclude(pid, sid, sorder) VALUES (?,?,?);""", (pid, sid, 1))
    connection.commit()
    return

def generate_pid():
    '''
        Description: generate a new unique playlist id
        Args: 
            None
        Return:
            pid: playlist id
    '''
    cursor.execute(
                """
                SELECT MAX(pid) 
                FROM playlists;
                """)
    pid = cursor.fetchone()[0] + 1
    return pid
