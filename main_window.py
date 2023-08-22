import sys
import tkinter as tk
import tkinter.ttk as ttk
import os.path
from tkinter import messagebox

import json
from pytube import YouTube, exceptions
import threading
import http.client

from tooltip import ToolTip
from download_window import LoadStreams
from settings_window import SettingsInterface

_script = sys.argv[0]
_location = os.path.dirname(_script)

_bgcolor = '#d9d9d9'  # X11 color: 'gray85'
_fgcolor = '#000000'  # X11 color: 'black'
_compcolor = 'gray40'  # X11 color: #666666
_ana1color = '#c3c3c3'  # Closest X11 color: 'gray76'
_ana2color = 'beige'  # X11 color: #f5f5dc
_tabfg1 = 'black'
_tabfg2 = 'black'
_tabbg1 = 'grey75'
_tabbg2 = 'grey89'
_bgmode = 'light'

_style_code_ran = 0


def _style_code():
    global _style_code_ran
    if _style_code_ran:
        return
    style = ttk.Style()
    if sys.platform == "win32":
        style.theme_use('winnative')
    style.configure('.', background=_bgcolor)
    style.configure('.', foreground=_fgcolor)
    style.configure('.', font='TkDefaultFont')
    style.map('.', background=[('selected', _compcolor), ('active', _ana2color)])
    if _bgmode == 'dark':
        style.map('.', foreground=[('selected', 'white'), ('active', 'white')])
    else:
        style.map('.', foreground=[('selected', 'black'), ('active', 'black')])
    _style_code_ran = 1


class MainInterface:
    def __init__(self):
        self.video = None

        self.main_window = tk.Tk()
        self.main_window.geometry("600x600+629+216")
        self.main_window.minsize(120, 1)
        self.main_window.maxsize(1924, 1061)
        self.main_window.resizable(True, True)
        self.main_window.title("YT Video Downloader")
        self.main_window.configure(background="#d9d9d9")

        self.main_heading = tk.Label(self.main_window)
        self.main_heading.place(relx=0.067, rely=0.083, height=99, width=514)
        self.main_heading.configure(background="#d9d9d9")
        self.main_heading.configure(compound='left')
        self.main_heading.configure(disabledforeground="#a3a3a3")
        self.main_heading.configure(font="-family {MV Boli} -size 36 -weight bold")
        self.main_heading.configure(foreground="#000000")
        self.main_heading.configure(text="YT Video Downloader")
        ToolTip(self.main_heading, "Made with Pytube API ;-)", delay=1.5)

        self.url_entry = tk.Entry(self.main_window)
        self.url_entry.place(relx=0.083, rely=0.4, height=30, relwidth=0.823)
        self.url_entry.configure(background="white")
        self.url_entry.configure(disabledforeground="#a3a3a3")
        self.url_entry.configure(font="-family {Comic Sans MS} -size 10")
        self.url_entry.configure(foreground="#000000")
        self.url_entry.configure(insertbackground="black")

        self.url_label = tk.Label(self.main_window)
        self.url_label.place(relx=0.083, rely=0.333, height=31, width=494)
        self.url_label.configure(background="#d9d9d9")
        self.url_label.configure(compound='left')
        self.url_label.configure(disabledforeground="#a3a3a3")
        self.url_label.configure(font="-family {Comic Sans MS} -size 14 -weight bold")
        self.url_label.configure(foreground="#000000")
        self.url_label.configure(text='''Enter video url here:''')

        self.download_modes_label = tk.Label(self.main_window)
        self.download_modes_label.place(relx=0.087, rely=0.467, height=31, width=494)
        self.download_modes_label.configure(activebackground="#f9f9f9")
        self.download_modes_label.configure(background="#d9d9d9")
        self.download_modes_label.configure(compound='left')
        self.download_modes_label.configure(disabledforeground="#a3a3a3")
        self.download_modes_label.configure(font="-family {Comic Sans MS} -size 16 -weight bold")
        self.download_modes_label.configure(foreground="#000000")
        self.download_modes_label.configure(highlightbackground="#d9d9d9")
        self.download_modes_label.configure(highlightcolor="#ffffff")
        self.download_modes_label.configure(text='''Select download mode:''')

        self.selectedMode = tk.StringVar(value="normal")

        self.normal_radiobutton = tk.Radiobutton(self.main_window)
        self.normal_radiobutton.configure(activebackground="#b5b5b5")
        self.normal_radiobutton.configure(activeforeground="black")
        self.normal_radiobutton.configure(anchor='w')
        self.normal_radiobutton.configure(background="#d9d9d9")
        self.normal_radiobutton.configure(compound='left')
        self.normal_radiobutton.configure(cursor='hand2')
        self.normal_radiobutton.configure(disabledforeground="#a3a3a3")
        self.normal_radiobutton.configure(font="-family {Comic Sans MS} -size 14")
        self.normal_radiobutton.configure(foreground="#000000")
        self.normal_radiobutton.configure(highlightbackground="#d9d9d9")
        self.normal_radiobutton.configure(highlightcolor="black")
        self.normal_radiobutton.configure(justify='left')
        self.normal_radiobutton.configure(selectcolor="#d9d9d9")
        self.normal_radiobutton.configure(text='''Normal''')
        self.normal_radiobutton.configure(value="normal")
        self.normal_radiobutton.configure(variable=self.selectedMode)
        ToolTip(self.normal_radiobutton, "Choose from a selection of video streams to download.", delay=0.35)
        self.normal_radiobutton.place(relx=0.302, rely=0.533, relheight=0.058, relwidth=0.163)

        self.audio_only_radiobutton = tk.Radiobutton(self.main_window)
        self.audio_only_radiobutton.configure(activebackground="#b5b5b5")
        self.audio_only_radiobutton.configure(activeforeground="black")
        self.audio_only_radiobutton.configure(anchor='w')
        self.audio_only_radiobutton.configure(background="#d9d9d9")
        self.audio_only_radiobutton.configure(compound='left')
        self.audio_only_radiobutton.configure(cursor='hand2')
        self.audio_only_radiobutton.configure(disabledforeground="#a3a3a3")
        self.audio_only_radiobutton.configure(font="-family {Comic Sans MS} -size 14")
        self.audio_only_radiobutton.configure(foreground="#000000")
        self.audio_only_radiobutton.configure(highlightbackground="#d9d9d9")
        self.audio_only_radiobutton.configure(highlightcolor="black")
        self.audio_only_radiobutton.configure(justify='left')
        self.audio_only_radiobutton.configure(selectcolor="#d9d9d9")
        self.audio_only_radiobutton.configure(text='''Audio-only''')
        self.audio_only_radiobutton.configure(value='audio_only')
        self.audio_only_radiobutton.configure(variable=self.selectedMode)
        ToolTip(self.audio_only_radiobutton, "Choose from a selection of audio-only streams to download.", delay=0.35)
        self.audio_only_radiobutton.place(relx=0.493, rely=0.533, relheight=0.058, relwidth=0.213)

        self.next_button = tk.Button(self.main_window)
        self.next_button.place(relx=0.417, rely=0.6, height=34, width=97)
        self.next_button.configure(activebackground="#b5b5b5")
        self.next_button.configure(activeforeground="black")
        self.next_button.configure(background="#d9d9d9")
        self.next_button.configure(borderwidth="3")
        self.next_button.configure(compound='left')
        self.next_button.configure(cursor='hand2')
        self.next_button.configure(disabledforeground="#a3a3a3")
        self.next_button.configure(font="-family {Comic Sans MS} -size 14 -weight bold")
        self.next_button.configure(foreground="#000000")
        self.next_button.configure(highlightbackground="#d9d9d9")
        self.next_button.configure(highlightcolor="black")
        self.next_button.configure(pady="0")
        self.next_button.configure(text='''Next''')
        self.next_button.configure(command=self.create_youtube_instance)

        _style_code()

        self.or_label = tk.Label(self.main_window)
        self.or_label.place(relx=0.465, rely=0.673, height=31, width=44)
        self.or_label.configure(background="#d9d9d9")
        self.or_label.configure(compound='left')
        self.or_label.configure(disabledforeground="#a3a3a3")
        self.or_label.configure(font="-family {Comic Sans MS} -size 14")
        self.or_label.configure(foreground="#000000")
        self.or_label.configure(text='''or''')

        self.left_separator = ttk.Separator(self.main_window)
        self.left_separator.place(relx=0.045, rely=0.7, relwidth=0.367)

        self.right_separator = ttk.Separator(self.main_window)
        self.right_separator.place(relx=0.588, rely=0.7, relwidth=0.367)

        self.playlist_mode_button = tk.Button(self.main_window)
        self.playlist_mode_button.place(relx=0.317, rely=0.75, height=34, width=227)
        self.playlist_mode_button.configure(activebackground="#b5b5b5")
        self.playlist_mode_button.configure(activeforeground="black")
        self.playlist_mode_button.configure(background="#d9d9d9")
        self.playlist_mode_button.configure(command=self.use_playlist_mode)
        self.playlist_mode_button.configure(compound='left')
        self.playlist_mode_button.configure(cursor='hand2')
        self.playlist_mode_button.configure(disabledforeground="#a3a3a3")
        self.playlist_mode_button.configure(font="-family {Comic Sans MS} -size 14 -underline 1")
        self.playlist_mode_button.configure(foreground="#000000")
        self.playlist_mode_button.configure(highlightbackground="#d9d9d9")
        self.playlist_mode_button.configure(highlightcolor="black")
        self.playlist_mode_button.configure(overrelief="flat")
        self.playlist_mode_button.configure(pady="0")
        self.playlist_mode_button.configure(relief="flat")
        self.playlist_mode_button.configure(text='''Download a playlist here!''')

        self.settings_button = tk.Button(self.main_window)
        self.settings_button.place(relx=0.917, rely=0.917, height=44, width=47)
        self.settings_button.configure(activebackground="#b5b5b5")
        self.settings_button.configure(activeforeground="black")
        self.settings_button.configure(background="#d9d9d9")
        self.settings_button.configure(command=self.open_settings)
        self.settings_button.configure(compound='left')
        self.settings_button.configure(cursor='hand2')
        self.settings_button.configure(disabledforeground="#a3a3a3")
        self.settings_button.configure(font="-family {Comic Sans MS} -size 9")
        self.settings_button.configure(foreground="#000000")
        self.settings_button.configure(highlightbackground="#d9d9d9")
        self.settings_button.configure(highlightcolor="black")
        self.settings_button.configure(pady="0")
        self.settings_button.configure(text='''Settings''')
        self.settings_button.configure(wraplength="47")

        self.dev_name = tk.Label(self.main_window)
        self.dev_name.place(relx=0.0, rely=0.967, height=21, width=94)
        self.dev_name.configure(anchor='w')
        self.dev_name.configure(background="#d9d9d9")
        self.dev_name.configure(compound='left')
        self.dev_name.configure(disabledforeground="#a3a3a3")
        self.dev_name.configure(foreground="#000000")
        self.dev_name.configure(text='''rikkadesu ©2023''')
        ToolTip(self.dev_name, "hi :3", delay=1)

        self.initialize_directory()
        self.main_window.mainloop()

    def create_youtube_instance(self):
        def proceed_download():
            loading = None
            try:
                loading = LoadStreams(self.main_window, self.video, self.selectedMode.get())
            except http.client.IncompleteRead:
                messagebox.showwarning("Something went wrong...", "Something went wrong and the process were interrupted,"
                                                                  " please try again :)")
                loading.loading_window.destroy()

        try:
            self.video = YouTube(self.url_entry.get())
            thread = threading.Thread(target=proceed_download)
            thread.start()
            self.main_window.withdraw()
        except exceptions.RegexMatchError:
            messagebox.showwarning("Invalid url", "Entered url is not valid. Please check if you provided a "
                                                  "valid youtube video url and try again! :)")

    @staticmethod
    def use_playlist_mode():
        messagebox.showinfo("Playlist Mode", "Still in development. Stay tune for updates!")

    def open_settings(self):
        settings = SettingsInterface(self.main_window)
        self.main_window.withdraw()
        settings.settings_window.wait_window()
        self.main_window.deiconify()

    @staticmethod
    def initialize_directory():
        if not os.path.exists("settings.json"):
            current_directory = {
                "directory": ""
            }
            with open("settings.json", "w") as js_file:
                json.dump(current_directory, js_file)


if __name__ == '__main__':
    MainInterface()
