import math
import tkinter as tk
from tkinter import ttk
import login_functions
import user_functions
import artist_functions
from connection import *
from tkinter import messagebox

global sno
global uid # either uid or aid, depending on the user logging in
uid = ''
sno = ''

class Spotime(tk.Tk):
    def __init__(self, *args, **kwargs):
        """
        Description: initialize
        Arguments: 
            None
        Return:
            None
        """
        tk.Tk.__init__(self, *args, **kwargs)
        container = tk.Frame(self)
        container.pack(side = "top", fill = "both", expand = True)
        container.grid_rowconfigure(0, weight = 1)
        container.grid_columnconfigure(0, weight = 1)
        self.frames = {}
        for F in [LogIn, User, Artist, UserOrArtist, Register, Song, Playlist, Artist_Shown]:

            frame = F(container, self)

            self.frames[F] = frame
            frame.grid(row = 0, column = 0, sticky ="nsew")

        self.show_frame(LogIn)
        self.geometry("1300x800")
        self.title("Spotime")
        self.protocol("WM_DELETE_WINDOW", self.on_closing)

	# to display the current frame passed as
	# parameter
    def show_frame(self, cont):
        """
        Description: change between frames
        Arguments:
            cont: frame to change to
        Return:
            None
        """
        frame = self.frames[cont]
        frame.update()
        frame.tkraise()

    def show_song(self, sid):
        """
        Description: change to frame songs 
        Arguments:
            sid: song id
        Return:
            None
        """
        frame = self.frames[Song]
        frame.sid = sid
        frame.update()
        frame.tkraise()

    def show_playlist(self, pid):
        """
        Description: change frame to playlist
        Arguments:  
            pid: playlist id
        Return:
            None
        """
        frame = self.frames[Playlist]
        frame.pid = pid
        frame.update()
        frame.tkraise()

    def show_artist(self,aid):
        """
        Description: show frame profile of an artists
        Arguments: 
            aid: artist id
        Return:
            None
        """
        frame = self.frames[Artist_Shown]
        frame.aid = aid
        frame.update()
        frame.tkraise()

    def on_closing(self):
        """
        Description:
            Handle close window events
        Arguments:
            None
        Return:
            None
        """
        global sno
        user = user_functions.end_session(uid,sno)
        self.destroy()

# log in screen
class LogIn(tk.Frame):
    def __init__(self, parent, controller):
        """
        Description: Initialize
        Arguments:
            parent: parent of log in frame
            controller: to swap between frames
        Return:
            None
        """
        self.controller = controller
        self.entries = []

        tk.Frame.__init__(self, parent)
        login_label = ttk.Label(self, text ="Log in")
        login_label.grid(row = 0, column = 2, padx = 10, pady = 10)

        id_label = ttk.Label(self, text = "id:")
        id_label.grid(row = 1, column = 1)
        id_entry = ttk.Entry(self)
        id_entry.grid(row = 1, column = 2)
        self.entries.append(id_entry)

        pw_label = ttk.Label(self, text = "pw:")
        pw_label.grid(row = 2, column = 1)
        pw_entry = ttk.Entry(self, show="*")
        pw_entry.grid(row = 2, column = 2)
        self.entries.append(pw_entry)

        login_btn = ttk.Button(self, text ="Log in", command = lambda: self.logincheck(id_entry.get(), pw_entry.get()))
        login_btn.grid(row = 3, column = 1)
        register_btn = ttk.Button(self, text ="Register", command = lambda: controller.show_frame(Register))
        register_btn.grid(row = 4, column = 1)

    def logincheck(self, user_id, input_pwd):
        """
        Description: Check if user_id match input_pwd
        Arguments:
            user_id: user id input by the user
            input_pwd: password input by the user
        Return:
            None
        """
        if user_id == '' or input_pwd == '':
            messagebox.showinfo("Alert","Empty id or passwords")
            return 
        result = login_functions.check_pw(user_id, input_pwd)
        global uid
        uid = user_id
        if result[0] is True and result[1] is True:
            self.controller.show_frame(UserOrArtist)
        elif result[0] is True:
            self.controller.show_frame(User)
        elif result[1] is True:
            self.controller.show_frame(Artist)
        else: 
            #wrong password, raise messagebox
            messagebox.showinfo("Alert","Invalid username or password")

    def update(self):
        """
        Description: update frame
        Arguments:
            None
        Return:
            None
        """
        for entry in self.entries:
            entry.delete(0,len(entry.get()))

class Register(tk.Frame):
    def __init__(self, parent, controller):
        """
        Description: Initialize frame
        Arguments:
            parent: parent of register frame
            controller: to swap between frames
        Return:
            None
        """
        self.controller = controller
        self.entries = []
        tk.Frame.__init__(self,parent)

        uid_label = ttk.Label(self, text = 'uid')
        uid_label.grid(row = 0, column = 0)
        uid_entry = ttk.Entry(self)
        uid_entry.grid(row = 0, column = 1)
        self.entries.append(uid_entry)

        name_label = ttk.Label(self, text = 'name')
        name_label.grid(row = 1, column = 0)
        name_entry = ttk.Entry(self)
        name_entry.grid(row = 1, column = 1)
        self.entries.append(name_entry)
        
        pwd_label = ttk.Label(self, text = 'pwd')
        pwd_label.grid(row = 2, column = 0)
        pwd_entry = ttk.Entry(self, show = "*")
        pwd_entry.grid(row = 2, column = 1)
        self.entries.append(pwd_entry)

        register_btn = ttk.Button(self, text = "Register", command = lambda: self.register(uid_entry.get(), name_entry.get(), pwd_entry.get()))
        register_btn.grid(row = 3, column = 0)
        logout_btn = ttk.Button(self, text ="Back to Log In Page", command = lambda : controller.show_frame(LogIn))
        logout_btn.grid(row = 4, column = 1, padx = 10, pady = 10)

    def update(self):
        """
        Description: update frame
        Arguments:
            None
        Return:
            None
        """
        for entry in self.entries:
            entry.delete(0,len(entry.get()))

    def register(self, uid, name, pwd):
        """
        Description: register the user
        Arguments:
            uid: user_id
            name: name of the user
            pwd: wanted password
        Return:
        """
        if uid == '' or name == '' or pwd == '':
            messagebox.showinfo("Alert","Empty id, name or passwords")
            return 
        result = login_functions.register(uid, name, pwd)
        if result is True:
            messagebox.showinfo("Alert","Registered succesfully")
            self.controller.show_frame(LogIn)
        else:
            #raise message
            messagebox.showinfo("Alert","Invalid UID")
        return

#user screen
class User(tk.Frame):
    def __init__(self, parent, controller):
        """
        Description: initialize frame
        Arguments:
            parent: parent of user frame
            controller: to swap between frames
        Return:
            None
        """
        tk.Frame.__init__(self,parent)
        self.controller = controller
        self.s_page = 1
        self.a_page = 1
        self.s_btn_list = {}
        self.a_btn_list = {}
        self.entries = []
        self.result = []
        self.a_result = []

        self.label = ttk.Label(self, text = '')
        self.label.grid(row = 0, column = 4, padx = 10, pady = 10)
        logout_btn = ttk.Button(self, text ="Log out", command = lambda : self.logOut())
        logout_btn.grid(row = 1, column = 1, padx = 10, pady = 10)
        start_btn = ttk.Button(self, text = "Start session", command = lambda : self.start_session())
        start_btn.grid(row = 2, column = 1)
        end_btn = ttk.Button(self, text = "End session", command = lambda: self.end_session())
        end_btn.grid(row = 2, column = 2)

        # search for song or playlists
        s_search_entry = ttk.Entry(self)
        s_search_entry.grid(row = 3, column = 1)
        self.entries.append(s_search_entry)
        s_search_btn = ttk.Button(self, text = "search for songs or playlists", command = lambda: self.s_search(s_search_entry.get()))
        s_search_btn.grid(row = 3, column = 2)

        direct_label1 = ttk.Label(self, text = "Go to page:")
        direct_label1.grid(row = 11, column = 0)

        page_entry1 = ttk.Entry(self)
        page_entry1.grid(row = 11, column = 1)
        self.entries.append(page_entry1)

        go_btn1 = ttk.Button(self, text = "go", command = lambda: self.s_newpage(page_entry1.get()))
        go_btn1.grid(row = 11, column = 2)

        self.pos_label1 = ttk.Label(self, text = "currently in page " + str(self.s_page))
        self.pos_label1.grid(row = 12, column = 0)

        # search for artistss
        a_search_entry = ttk.Entry(self)
        a_search_entry.grid(row = 13, column = 1)
        self.entries.append(a_search_entry)
        a_search_btn = ttk.Button(self, text = "search for artists", command = lambda: self.a_search(a_search_entry.get()))
        a_search_btn.grid(row = 13, column = 2)

        direct_label2 = ttk.Label(self, text = "Go to page:")
        direct_label2.grid(row = 19, column = 0)

        page_entry2 = ttk.Entry(self)
        page_entry2.grid(row = 19, column = 1)
        self.entries.append(page_entry2)

        go_btn2 = ttk.Button(self, text = "go", command = lambda: self.a_newpage(page_entry2.get()))
        go_btn2.grid(row = 19, column = 2)

        self.pos_label2 = ttk.Label(self, text = "Search to see results")
        self.pos_label2.grid(row = 20, column = 0)
    
    def logOut(self):
        """
        Description: Log out, return to Log In screen 
        Arguments:
            None
        Return:
            None
        """
        global sno
        user_functions.end_session(uid,sno)
        self.controller.show_frame(LogIn)
    
    def start_session(self):
        """
        Description: start new session
        Arguments:
            None
        Return:
            None
        """
        global sno
        sno = user_functions.start_session(uid)
        messagebox.showinfo("Alert","Session started succesfully")

    def end_session(self):
        """
        Description: end session if existed
        Arguments:
            None
        Return:
            None
        """
        global sno
        if sno == '':
            #raise message box no current session
            messagebox.showinfo("Alert","No running session")
            return
        user_functions.end_session(uid, sno)
        messagebox.showinfo("Alert","Session ended succesfully")
        sno = ''
        return
    
    def s_newpage(self, pageno):
        """
        Description: new page for songs and playlists
        Arguments: 
            pageno: new page number
        Return:
            None
        """
        try:
            self.s_page = int(pageno)
            if self.s_page <= 0 and self.s_page == float(pageno):
                messagebox.showinfo("Alert","You should type in a positive number") 
        except:
            messagebox.showinfo("Alert","You should type in a number")
            return
        if self.s_page > math.ceil(len(self.result)/5):
                messagebox.showinfo("Alert","Enter a valid number")
                return
        self.s_show_results()
    
    def a_newpage(self, pageno):
        """
        Description: new page for artists
        Arguments:
            pageno: new page number
        Return:
            None
        """
        try:
            self.a_page = int(pageno)
            if self.a_page <= 0 and self.a_page == float(pageno):
                messagebox.showinfo("Alert","You should type in a positive number") 
        except:
            messagebox.showinfo("Alert","You should type in a number")
            return
        if self.a_page > math.ceil(len(self.a_result)/5):
            messagebox.showinfo("Alert","Enter a valid number")
            return
        self.a_show_results()

    def s_search(self, keywords):
        """
        Description: search for song and artist
        Arguments: 
            keywords
        Return:
            None
        """
        if user_functions.check_duplicates(keywords):
            messagebox.showinfo("Alert","Duplicate keywords")
        if keywords == '':
            messagebox.showinfo("Alert","Empty keywords")
            return 
        self.result = user_functions.search(keywords)
        self.s_show_results()
        return

    def s_show_results(self):
        """
        Description: show song and artist
        Arguments:
            None
        Return:
            None
        """
        self.pos_label1.config(text = "currently in page " + str(self.s_page))
        for btn in self.s_btn_list.values():
            btn.destroy()
        if self.result == []:
            return
        iteration = 5
        if self.s_page == len(self.result) // 5 +1:
            if len(self.result) % 5 != 0:
                iteration = len(self.result) % 5
        for j in range(iteration):
            i = 5*(int(self.s_page)-1) + j
            if self.result[i][4] == 's':
                s_button = ttk.Button(self, text = "song_id: "+ str(self.result[i][0]) + " title: " + str(self.result[i][1]) + " duration: " + str(self.result[i][2]), command = lambda x=self.result[i][0]: self.controller.show_song(x))
                s_button.grid(row = j+5, column = 1)
                self.s_btn_list[j] = s_button
            else:
                pls_button = ttk.Button(self, text = "playlist_id: "+ str(self.result[i][0]) + " title: " + str(self.result[i][1]) + " duration of all songs: " + str(self.result[i][2]), command = lambda x=self.result[i][0]: self.controller.show_playlist(x))
                pls_button.grid(row = j+5, column = 1)
                self.s_btn_list[j] = pls_button 
    
    def a_search(self, keywords):
        """
        Description: search for artist
        Arguments:
            keywords
        Return:
            None
        """ 
        if user_functions.check_duplicates(keywords):
            messagebox.showinfo("Alert","Duplicate keywords")
        if keywords == '':
            messagebox.showinfo("Alert","Empty keywords")
            return 
        self.a_result = user_functions.search_artist(keywords)
        self.a_show_results()
        return

    def a_show_results(self):
        """
        Description: show artist
        Arguments: 
            None
        Return:
            None
        """
        self.pos_label2.config(text = "currently in page " + str(self.a_page))
        for btn in self.a_btn_list.values():
            btn.destroy()
        if self.a_result == []:
            return
        iteration = 5
        if self.a_page == len(self.a_result) // 5 +1:
            if len(self.a_result) % 5 != 0:
                iteration = len(self.a_result) % 5
        for j in range(iteration):
            i = 5*(int(self.a_page)-1) + j
            a_btn = ttk.Button(self, text = " name: " + str(self.a_result[i][1]) + " nationality: " + str(self.a_result[i][2]) + " Number of songs: " + str(self.a_result[i][3]), command = lambda x=self.a_result[i][0]: self.controller.show_artist(x))
            a_btn.grid(row = j+14, column = 1)
            self.a_btn_list[j] = a_btn 
    
    def update(self):
        """
        Description: update frame
        Arguments:
            None
        Return:
            None
        """
        self.label.config(text = "uid: " + uid)
        for btn in self.a_btn_list.values():
            btn.destroy()
        for btn in self.s_btn_list.values():
            btn.destroy()
        for entry in self.entries:
            entry.delete(0,len(entry.get()))
        self.s_page = 1
        self.a_page = 1
        self.result.clear()
        self.a_result.clear()
        self.pos_label1.config(text = "Search to see results")
        self.pos_label2.config(text = "Search to see results")
 
class Song(tk.Frame):
    def __init__(self, parent, controller, sid = ''):
        """
        Description: initialize frame
        Arguments:
            parent: parent of the song frame
            controller: to swap between frames
            sid: song id
        Return:
            None
        """
        tk.Frame.__init__(self,parent)
        self.controller = controller
        self.sid = sid
        self.page = 1
        self.pl_info_page = 1
        self.artist_info_page = 1
        self.pl_info = []
        self.artist_info = []
        self.user_playlists = []

        self.pls = {}
        self.artist = {}
        self.add_pls = {}
        self.entries = []
        self.labels = []
        self.btns = []

        listen_btn = ttk.Button(self, text = "Listen", command = lambda: self.listen())
        listen_btn.grid(row = 2, column = 2)
        info_btn = ttk.Button(self, text = "See more information", command = lambda: self.show_info())
        info_btn.grid(row = 3, column = 2)
        add_btn = ttk.Button(self, text = "Add to playlist", command = lambda: self.add_to_playlist())
        add_btn.grid(row = 6, column = 2)
        logout_btn = ttk.Button(self, text ="Log out", command = lambda : self.logOut())
        logout_btn.grid(row = 11, column = 3, padx = 10, pady = 10)
        home_button = ttk.Button(self, text ="Home", command = lambda : controller.show_frame(User))
        home_button.grid(row = 11, column = 4, padx = 10, pady = 10)

        self.page_entry1 = ttk.Entry(self)
        self.page_entry1.grid(row = 4, column = 8)
        go_button1 = ttk.Button(self, text = "Go", command = lambda: self.new_page_pl(self.page_entry1.get()))
        go_button1.grid(row = 4, column = 9)
        self.pos_label1 = ttk.Label(self, text = "Currently in page" + str(self.pl_info_page))
        self.pos_label1.grid(row = 4, column = 10)

        self.page_entry2 = ttk.Entry(self)
        self.page_entry2.grid(row = 5, column = 8)
        go_button2 = ttk.Button(self, text = "Go", command = lambda: self.new_page_artist(self.page_entry2.get()))
        go_button2.grid(row = 5, column = 9)
        self.pos_label2 = ttk.Label(self, text = "Currently in page" + str(self.artist_info_page))
        self.pos_label2.grid(row = 5, column = 10)

    def listen(self):
        """
        Description: start listen to the song
        Arguments: 
            None
        Return:
            None
        """
        global sno
        if sno == '':
            sno = user_functions.start_session(uid)
        user_functions.add_song_session(self.sid,uid,sno,1)

    def get_info(self):
        """
        Description: get song info
        Arguments: 
            None
        Return:
            None
        """
        self.song_info, self.artist_info, self.pl_info = user_functions.get_song_information(self.sid)

    def show_info(self):
        """
        Description: show song info
        Arguments:
            None
        Return:
            None
        """
        self.get_info()
        label_info = ttk.Label(self,text = "id: " + str(self.song_info[0]) + " title: " + str(self.song_info[1]) + " duration: " + str(self.song_info[2]))
        label_info.grid(row = 3 ,column = 3)
        self.labels.append(label_info)

        self.pos_label1.config(text = "currently in page " + str(self.pl_info_page))
        self.pos_label2.config(text = "currently in page " + str(self.artist_info_page))

        self.show_playlist_in()
        self.show_artist_p()

    def show_artist_p(self):
        """
        Description: show artists perform the song
        Arguments:
            None
        Return:
            None
        """
        for label in self.artist.values():
            label.destroy()
        if self.artist_info == []:
            return
        iteration = 5
        if self.artist_info_page - 1 == len(self.artist_info) // 5 :
            if len(self.artist_info) % 5 != 0:
                iteration = len(self.artist_info) % 5
        for j in range(iteration):
            i = 5*(self.artist_info_page-1) + j
            label = ttk.Label(self, text = self.artist_info[i][0])
            label.grid(row = 5, column = 2 + j)
            self.artist[j+5] = label

    def new_page_artist(self, pno):
        """
        Description: New page for artist
        Arguments:
            pno: page number
        Return:
            None
        """
        try:
            self.artist_info_page = int(pno)
            if self.artist_info_page <= 0 and self.artist_info_page == float(pno):
                messagebox.showinfo("Alert","You should type in a positive number") 
        except:
            messagebox.showinfo("Alert","You should type a number in")
            return
        if self.artist_info_page > math.ceil(len(self.artist_info)/5):
            messagebox.showinfo("Alert","No more artists")
            return
        self.pos_label2.config(text = "Currently in page" + str(self.artist_info_page))
        self.show_artist_p()

    def show_playlist_in(self):
        """
        Description: show playlist the song is in
        Arguments:
            None
        Return:
            None
        """
        for label in self.pls.values():
            label.destroy()
        if self.pl_info == []:
            return
        iteration = 5
        if self.pl_info_page - 1 == len(self.pl_info) // 5 :
            if len(self.pl_info) % 5 != 0:
                iteration = len(self.pl_info) % 5
        for j in range(iteration):
            i = 5*(self.pl_info_page-1) + j
            label = ttk.Label(self, text = self.pl_info[i][0])
            label.grid(row = 4, column = 2 + j)
            self.pls[j+5] = label

    def new_page_pl(self, pno):
        """
        Description: New page for playlists
        Arguments:
            pno: page number
        Return:
            None
        """
        try:
            self.pl_info_page = int(pno)
            if self.pl_info_page <= 0 and self.pl_info_page == float(pno):
                messagebox.showinfo("Alert","You should type in a positive number") 
        except:
            messagebox.showinfo("Alert","You should type a number in")
            return
        if self.pl_info_page > math.ceil(len(self.pl_info)/5):
            messagebox.showinfo("Alert","No more playlists")
            return
        self.pos_label1.config(text = "Currently in page" + str(self.pl_info_page))
        self.show_playlist_in()
    
    def add_to_playlist(self):
        """
        Description: add song to playlist
        Arguments: 
            None
        Return:
            None
        """
        self.page = 1
        add_new_button = ttk.Button(self, text = "Add to new playlist", command = lambda: self.create_playlist())
        add_new_button.grid(row = 7, column = 2)
        self.btns.append(add_new_button)
        page_entry = ttk.Entry(self)
        page_entry.grid(row = 8, column = 2)
        self.entries.append(page_entry)
        go_button = ttk.Button(self, text = "Go", command = lambda: self.new_page(page_entry.get()))
        go_button.grid(row = 8, column = 3)
        self.pos_label3 = ttk.Label(self, text = "Currently in page" + str(self.page))
        self.pos_label3.grid(row=8,column=4)
        self.labels.append(self.pos_label3)
        self.btns.append(go_button)
        self.get_playlist()
        self.show_results()

    def get_playlist(self):
        """
        Description: get user's playlist
        Arguments: 
            None
        Return:
            None
        """
        self.user_playlists = user_functions.get_playlist(uid)

    def show_results(self):
        """
        Description: show result
        Arguments:
            None
        Return:
            None
        """
        for label in self.add_pls.values():
            label.destroy()
        if self.user_playlists == []: 
            return
        iteration = 5
        if self.page - 1 == len(self.user_playlists) // 5 :
            if len(self.user_playlists) % 5 != 0:
                iteration = len(self.user_playlists) % 5
        for j in range(iteration):
            i = 5*(self.page-1) + j
            button = ttk.Button(self, text = "Title: " + self.user_playlists[i][1], command = lambda x = self.user_playlists[i][0]: self.add_to_existed_playlist(x))
            button.grid(row = 7, column = 3 + i)
            self.add_pls[j] = button

    def new_page(self, pno):
        """
        Description: new page for 
        Arguments: 
            pno: new page number
        Return:
            None
        """
        try:
            self.page = int(pno)
            if self.page <= 0 and self.page == float(pno):
                messagebox.showinfo("Alert","You should type in a positive number") 
        except:
            messagebox.showinfo("Alert","You should type a number in")
            return
        if self.page > math.ceil(len(self.user_playlists)/5):
            messagebox.showinfo("Alert","No more playlists to add to")
            return
        self.pos_label3.config(text = "Currently in page " + str(self.page))
        self.show_results()

    def add_to_existed_playlist(self,pid):
        """
        Description: add the song to an existed playlist if possible
        Arguments:
            pid: playlist id
        Return:
            None
        """
        if user_functions.add_to_existed_playlist(pid,self.sid) == False:
            #raise mesagaebx
            messagebox.showinfo("Title", "Song already exists in the playlist")
            return
        messagebox.showinfo("Alert","Song added")

    def create_playlist(self):
        """
        Description: create new playlist
        Arguments:
            None
        Return:
            None
        """
        title_label = ttk.Label(self, text = "Title of new playlist")
        title_label.grid(row = 9, column = 2)
        self.labels.append(title_label)
        title_entry = ttk.Entry(self) 
        title_entry.grid(row = 9, column = 3)
        self.entries.append(title_entry)
        create_button = ttk.Button(self, text = "Create", command = lambda: self.create_playlist_and_add_song(uid, title_entry.get(), self.sid))
        create_button.grid(row = 9, column = 4)
        self.btns.append(create_button)
    
    def create_playlist_and_add_song(self,uid,title,sid):
        """
        Description: create new playlist and add song
        Arguments:
            uid: uid of user
            title: title of new playlist
            sid: song id to add
        Return:
            None
        """
        if title == '':
            messagebox.showinfo("Alert","Empty title")
            return 
        user_functions.create_playlist_and_add_song(uid, title, sid)
        messagebox.showinfo("Alert","Playlist created and song added")
    
    def logOut(self):
        """
        Description: Log out
        Arguments:
            None
        Return:
            None
        """
        global sno
        user_functions.end_session(uid,sno)
        self.controller.show_frame(LogIn)
    
    def update(self):
        """
        Description: update frame
        Arguments:
            None
        Return:
            None
        """
        for label in self.labels:
            label.destroy()
        for entry in self.entries:
            entry.destroy()
        for btn in self.btns:
            btn.destroy()
        for btn in self.pls.values():
            btn.destroy()
        for label in self.artist.values():
            label.destroy()
        for label in self.add_pls.values():
            label.destroy()
        self.page_entry1.delete(0,len(self.page_entry1.get()))
        self.page_entry2.delete(0,len(self.page_entry2.get()))
        self.pos_label1.config(text = "Press 'See more information' to search")
        self.pos_label2.config(text = "Press 'See more information' to search")
        self.pl_info_page = 1
        self.artist_info_page = 1
        self.page = 1
        self.pl_info = []
        self.artist_info = []
        self.user_playlists = []

class Playlist(tk.Frame):
    def __init__(self, parent, controller, pid = ''):
        """
        Description: initialize frame
        Arguments: 
            pid: playlist id
        Return:
            None
        """
        tk.Frame.__init__(self,parent)
        self.pid = pid
        self.controller = controller
        self.btn_list  = {}
        self.entries = []
        self.page = 1
        self.result = []

        direct_label = ttk.Label(self, text = "Go to page:")
        direct_label.grid(row = 6, column = 0)
        page_entry = ttk.Entry(self)
        page_entry.grid(row = 6, column = 1)
        self.entries.append(page_entry)
        go_button = ttk.Button(self, text = "go", command = lambda: self.newpage(page_entry.get()))
        go_button.grid(row = 6, column = 2)
        self.pos_label = ttk.Label(self, text = "currently in page " + str(self.page))
        self.pos_label.grid(row = 7, column = 0)

        logout_btn = ttk.Button(self, text ="Log out", command = lambda : self.logOut())
        logout_btn.grid(row = 8, column = 2, padx = 10, pady = 10)
        home_button = ttk.Button(self, text ="Home", command = lambda : controller.show_frame(User))
        home_button.grid(row = 8, column = 3, padx = 10, pady = 10)

    def newpage(self, pageno):
        """
        Description: new page
        Arguments:
            pageno: new page
        Return:
            None
        """
        try:
            self.page = int(pageno)
            if self.page <= 0 and self.page == float(pageno):
                messagebox.showinfo("Alert","You should type in a positive number") 
        except:
            messagebox.showinfo("Alert","You should type in a number")
            return
        if self.page > math.ceil(len(self.result)/5):
            messagebox.showinfo("Alert","No more songs")
            self.page = 1
            return
        self.pos_label.config(text = "currently in page " + str(self.page))
        self.show_results()

    def get_songs(self):
        """
        Description: get songs in the playlist
        Arguments: 
            None
        Return:
            None
        """
        self.result = user_functions.getsong_playlist(self.pid)
    
    def show_results(self):
        """
        Description: show results
        Arguments:
            None
        Return:
            None
        """
        for btn in self.btn_list.values():
            btn.destroy()
        if self.result == []:
            return
        iteration = 5
        if self.page - 1 == len(self.result) // 5 :
            if len(self.result) % 5 != 0:
                iteration = len(self.result) % 5
        for j in range(iteration):
            i = 5*(int(self.page)-1) + j
            song_btn = ttk.Button(self, text = "song: "+ str(self.result[i][0]) + " title: " + str(self.result[i][1]) + " duration: " + str(self.result[i][2]), command = lambda x = self.result[i][0]: self.controller.show_song(x))
            song_btn.grid(row = 5, column = j)
            self.btn_list[j] = song_btn
        
    def logOut(self):
        """
        Description: log out
        Arguments:
            None
        Return:
            None
        """
        global sno
        user_functions.end_session(uid,sno)
        self.controller.show_frame(LogIn)

    def update(self):
        """
        Description: update frame
        Arguments:
            None
        Return:
            None
        """
        for entry in self.entries:
            entry.delete(0,len(entry.get()))
        for btn in self.btn_list.values():
            btn.destroy()
        self.page = 1
        self.pos_label.config(text="Currently in page 1")
        self.get_songs()
        self.show_results()

class Artist_Shown(tk.Frame):
    def __init__(self, parent, controller, aid = ''):
        """
        Description: initialize frame
        Arguments:
            parent: parent of artist frame
            controller: to swap between frames
            aid: artist id
        Return:
        """
        tk.Frame.__init__(self, parent)
        self.btn_list = {}
        self.page = 1
        self.controller = controller
        self.aid = aid
        self.entries = []
        self.result = []

        direct_label = ttk.Label(self, text = "Go to page:")
        direct_label.grid(row = 2, column = 0)
        page_entry = ttk.Entry(self)
        page_entry.grid(row = 2, column = 1)
        self.entries.append(page_entry)
        go_button = ttk.Button(self, text = "go", command = lambda: self.newpage(page_entry.get()))
        go_button.grid(row = 2, column = 2)
        self.pos_label = ttk.Label(self, text = "currently in page " + str(self.page))
        self.pos_label.grid(row = 3, column = 0)

        logout_btn = ttk.Button(self, text ="Log out", command = lambda : self.logOut())
        logout_btn.grid(row = 10, column = 2, padx = 10, pady = 10)
        home_button = ttk.Button(self, text ="Home", command = lambda : controller.show_frame(User))
        home_button.grid(row = 10, column = 3, padx = 10, pady = 10)

    def newpage(self, pageno):
        """
        Description: new page
        Arguments:
            pageno: new page number
        Return:
            None
        """
        try:
            self.page = int(pageno)
            if self.page <= 0 and self.page == float(pageno):
                messagebox.showinfo("Alert","You should type in a positive number") 
        except:
            messagebox.showinfo("Alert","You should type in a number")
            return
        if self.page > math.ceil(len(self.result)/5):
            messagebox.showinfo("Alert","No more songs")
            self.page = 1
            return
        self.pos_label.config(text = "currently in page " + str(self.page))
        self.show_results_artists()

    def get_songs_artists(self):
        """
        Description: get song performed by the artist
        Arguments: 
            None
        Return:
            None
        """
        self.result = user_functions.getsong_artist(self.aid)

    def show_results_artists(self):
        """
        Description: show result 
        Arguments:
            None
        Return:
            None
        """
        for btn in self.btn_list.values():
            btn.destroy()
        if self.result == []: 
            return
        iteration = 5
        if self.page == len(self.result) // 5 +1:
            if len(self.result) % 5 != 0:
                iteration = len(self.result) % 5
        for j in range(iteration):
            i = 5*(int(self.page)-1) + j
            s_button = ttk.Button(self, text = "song: "+ str(self.result[i][0]) + " title: " + str(self.result[i][1]) + " duration: " + str(self.result[i][2]), command = lambda x = self.result[i][0]: self.controller.show_song(x))
            s_button.grid(row = 4 + j, column = 1)
            self.btn_list[j] = s_button

    def logOut(self):
        """
        Description: log out
        Arguments: 
            None
        Return:
            None
        """
        global sno
        user_functions.end_session(uid,sno)
        self.controller.show_frame(LogIn)

    def update(self):
        """
        Description: update frame
        Arguments:
            None
        Return:
            None
        """
        for entry in self.entries:
            entry.delete(0,len(entry.get()))
        for btn in self.btn_list.values():
            btn.destroy()
        self.page = 1
        self.pos_label.config(text="currently in page 1")
        self.get_songs_artists()
        self.show_results_artists()

#artist screen
class Artist(tk.Frame):
    def __init__(self, parent, controller):
        """
        Description: initialize frame
        Arguments:
            parent: parent of the artist frame
            controller: to swap between frames
        Return:
            None
        """
        tk.Frame.__init__(self, parent)
        self.entries = []
        self.labels = []

        self.label = ttk.Label(self, text = '')
        self.label.grid(row = 0, column = 4, padx = 10, pady = 10)

        logout_btn = ttk.Button(self, text ="Log out", command = lambda : controller.show_frame(LogIn))
        logout_btn.grid(row = 1, column = 1, padx = 10, pady = 10)
        
        title_label = ttk.Label(self, text = 'Title')
        title_label.grid(row = 2, column = 0)
        title_entry = ttk.Entry(self)
        title_entry.grid(row = 2, column = 1)
        self.entries.append(title_entry)

        dur_label = ttk.Label(self, text = 'Duration')
        dur_label.grid(row = 3, column = 0)
        dur_entry = ttk.Entry(self)
        dur_entry.grid(row = 3, column = 1)
        self.entries.append(dur_entry)

        aa_label = ttk.Label(self, text = 'Additional Artist IDs')
        aa_label.grid(row = 4, column = 0)
        aa_entry = ttk.Entry(self)
        aa_entry.grid(row = 4, column = 1)
        self.entries.append(aa_entry)

        noti_label = ttk.Label(self, text = '(separated by comma - no space)') 
        noti_label.grid(row=5,column=0)

        button2 = ttk.Button(self, text = "Add song", command = lambda: self.add_song(title_entry.get(),dur_entry.get(),aa_entry.get()))
        button2.grid(row = 6, column = 1)

        topfans_btn = ttk.Button(self, text = "Find top 3 fans and top 3 playlists", command = lambda: [self.find_topfans(uid),self.find_toppls(uid)])
        topfans_btn.grid(row = 7, column = 0)

    def find_topfans(self,artist_id):
        """
        Description: find top fans
        Arguments:
            None
        Return:
            None
        """
        results = artist_functions.topFans(artist_id)
        fans_label = ttk.Label(self, text = "Top Fans: ")
        self.labels.append(fans_label)
        fans_label.grid(row = 8, column = 0)
        for i in range (len(results)):
            f_label = ttk.Label(self, text = " uid: " + results[i][0] + " name: " + results[i][1])
            f_label.grid(row = 8, column = i + 1)
            self.labels.append(f_label)

    def find_toppls(self,artist_id):
        """
        Description: find top playlists
        Arguments:
            artist_id
        Return:
            None
        """
        results = artist_functions.topPLs(artist_id)
        pls_label = ttk.Label(self, text = "Top Playlists: ")
        self.labels.append(pls_label)
        pls_label.grid(row = 9, column = 0)
        for i in range (len(results)):
            pl_label = ttk.Label(self, text = " pid: " + str(results[i][0]) + " title: " + results[i][1])
            pl_label.grid(row = 9, column = i + 1)
            self.labels.append(pl_label)
            
    def add_song(self, title, duration, additional_aids):
        """
        Description: add new song
        Arguments:
            title
            duration
            additional_aids
        Return:
            None
        """
        if title == '' or duration == '':
            messagebox.showinfo("Alert","Empty title or duration")
            return
        try:
            check_duration = int(duration)
        except:
            messagebox.showinfo("Alert","Duration must be a number")
            return
        if not artist_functions.add_song(uid,title,duration,additional_aids):
            messagebox.showinfo("Alert","Song already performed or additional artist not exist or YOUR id is being inputted") 
            return
        messagebox.showinfo("Alert","Song added")
        for entry in self.entries:
            entry.delete(0,len(entry.get()))

    def update(self):
        """
        Description: update frame
        Arguments:
            None
        Return:
            None
        """
        print("fadsfdffdsafds")
        self.label.config(text = "aid: " + uid)
        for label in self.labels:
            label.destroy()

class UserOrArtist(tk.Frame):
    def __init__(self, parent, controller):
        """
        Description: initialize frame
        Arguments:
            parent: parent of the frame
            controller: to swap between frames
        Return:
        """
        tk.Frame.__init__(self,parent)
        self.controller = controller
        choose_label = ttk.Label(self, text = "Choose user or artist")
        choose_label.grid(row = 0, column = 4)
        user_btn = ttk.Button(self, text = "User", command = lambda: controller.show_frame(User))
        user_btn.grid(row = 1, column = 4)
        a_btn = ttk.Button(self, text = "Artist", command = lambda: controller.show_frame(Artist))
        a_btn.grid(row = 2, column = 4)
        logout_btn = ttk.Button(self, text ="Log out", command = lambda : controller.show_frame(LogIn))
        logout_btn.grid(row = 3, column = 4, padx = 10, pady = 10)



    
