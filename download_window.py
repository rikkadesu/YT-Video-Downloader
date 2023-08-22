import sys
import threading
import tkinter as tk
from tkinter import messagebox
import tkinter.ttk as ttk
import os.path
import json

import pytube
from pytube import YouTube, Stream
from progress_window import ProgressInterface

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


class DownloadInterface:
    def __init__(self, **kwargs):
        """This class configures and populates the toplevel window.
           top is the toplevel containing window."""

        self.parent_window = kwargs['parent_window']
        self.download_window = tk.Toplevel(self.parent_window)

        self.download_directory = None
        self.selected_mode = kwargs['selected_mode']
        self.video = kwargs['video']
        self.streams = kwargs['streams']
        self.stream_list = kwargs['stream_list']

        self.download_window.geometry("600x600+570+205")
        self.download_window.minsize(120, 1)
        self.download_window.maxsize(4324, 1061)
        self.download_window.resizable(True, True)
        self.download_window.title(f"{self.video.title} - Complete Requirements")
        self.download_window.configure(background="#d9d9d9")

        self.download_heading = tk.Label(self.download_window)
        self.download_heading.place(relx=0.067, rely=0.083, height=111, width=524)
        self.download_heading.configure(anchor='w')
        self.download_heading.configure(background="#d9d9d9")
        self.download_heading.configure(compound='left')
        self.download_heading.configure(disabledforeground="#a3a3a3")
        self.download_heading.configure(font="-family {MV Boli} -size 36 -weight bold")
        self.download_heading.configure(foreground="#000000")
        self.download_heading.configure(text='''YT Video Downloader''')

        self.title_label = tk.Label(self.download_window)
        self.title_label.place(relx=0.083, rely=0.267, height=71, width=504)
        self.title_label.configure(anchor='n')
        self.title_label.configure(background="#d9d9d9")
        self.title_label.configure(compound='left')
        self.title_label.configure(disabledforeground="#a3a3a3")
        self.title_label.configure(font="-family {Comic Sans MS} -size 14")
        self.title_label.configure(foreground="#000000")
        self.title_label.configure(text=f"{self.video.title}")
        self.title_label.configure(wraplength="504")

        self.creator_label = tk.Label(self.download_window)
        self.creator_label.place(relx=0.083, rely=0.35, height=71, width=504)
        self.creator_label.configure(anchor='n')
        self.creator_label.configure(background="#d9d9d9")
        self.creator_label.configure(compound='left')
        self.creator_label.configure(disabledforeground="#a3a3a3")
        self.creator_label.configure(font="-family {Comic Sans MS} -size 12")
        self.creator_label.configure(foreground="#000000")
        self.creator_label.configure(text=f"{self.video.author}")

        self.resolution_label = tk.Label(self.download_window)
        self.resolution_label.place(relx=0.017, rely=0.433, height=41, width=284)
        self.resolution_label.configure(anchor='e')
        self.resolution_label.configure(background="#d9d9d9")
        self.resolution_label.configure(compound='left')
        self.resolution_label.configure(disabledforeground="#a3a3a3")
        self.resolution_label.configure(font="-family {Comic Sans MS} -size 14 -weight bold")
        self.resolution_label.configure(foreground="#000000")
        resolution_label = "Select resolution | file type:" if self.selected_mode == "normal" else \
            "Select bitrate | file type:"
        self.resolution_label.configure(text=resolution_label)

        _style_code()

        self.comboboxSelected = tk.StringVar()

        self.resolution_combobox = ttk.Combobox(self.download_window)
        self.resolution_combobox.place(relx=0.5, rely=0.45, relheight=0.045, relwidth=0.338)
        self.resolution_combobox.configure(textvariable=self.comboboxSelected)
        self.resolution_combobox.configure(takefocus="")
        self.resolution_combobox.configure(cursor="hand2")
        self.resolution_combobox.set("Please select a stream.")
        self.resolution_combobox.configure(state="readonly")
        self.resolution_combobox.bind("<<ComboboxSelected>>", lambda e: self.selected_item_combobox())

        self.size_label = tk.Label(self.download_window)
        self.size_label.place(relx=0.017, rely=0.498, height=41, width=284)
        self.size_label.configure(anchor='e')
        self.size_label.configure(background="#d9d9d9")
        self.size_label.configure(compound='left')
        self.size_label.configure(disabledforeground="#a3a3a3")
        self.size_label.configure(font="-family {Comic Sans MS} -size 14 -weight bold")
        self.size_label.configure(foreground="#000000")
        self.size_label.configure(text='''File size:''')

        self.size_value_label = tk.Label(self.download_window)
        self.size_value_label.place(relx=0.495, rely=0.51, height=31, width=204)
        self.size_value_label.configure(anchor='w')
        self.size_value_label.configure(background="#d9d9d9")
        self.size_value_label.configure(compound='left')
        self.size_value_label.configure(disabledforeground="#a3a3a3")
        self.size_value_label.configure(font="-family {Comic Sans MS} -size 14")
        self.size_value_label.configure(foreground="#000000")
        self.size_value_label.configure(text='''-''')

        self.dev_name = tk.Label(self.download_window)
        self.dev_name.place(relx=0.0, rely=0.967, height=21, width=174)
        self.dev_name.configure(anchor='w')
        self.dev_name.configure(background="#d9d9d9")
        self.dev_name.configure(compound='left')
        self.dev_name.configure(disabledforeground="#a3a3a3")
        self.dev_name.configure(foreground="#000000")
        self.dev_name.configure(text='''rikkadesu ©2023''')

        self.download_button = tk.Button(self.download_window)
        self.download_button.place(relx=0.393, rely=0.783, height=44, width=127)
        self.download_button.configure(activebackground="beige")
        self.download_button.configure(activeforeground="black")
        self.download_button.configure(background="#d9d9d9")
        self.download_button.configure(borderwidth="3")
        self.download_button.configure(compound='left')
        self.download_button.configure(cursor="hand2")
        self.download_button.configure(disabledforeground="#a3a3a3")
        self.download_button.configure(font="-family {Comic Sans MS} -size 14 -weight bold")
        self.download_button.configure(foreground="#000000")
        self.download_button.configure(highlightbackground="#d9d9d9")
        self.download_button.configure(highlightcolor="black")
        self.download_button.configure(pady="0")
        self.download_button.configure(text='''Download''')
        self.download_button.configure(command=self.start_download)

        self.bitrate_label = tk.Label(self.download_window)
        self.bitrate_label.place(relx=0.017, rely=0.567, height=41, width=284)
        self.bitrate_label.configure(anchor='e')
        self.bitrate_label.configure(background="#d9d9d9")
        self.bitrate_label.configure(compound='left')
        self.bitrate_label.configure(disabledforeground="#a3a3a3")
        self.bitrate_label.configure(font="-family {Comic Sans MS} -size 14 -weight bold")
        self.bitrate_label.configure(foreground="#000000")
        self.bitrate_label.configure(text='''Bitrate:''')

        self.bitrate_value_label = tk.Label(self.download_window)
        self.bitrate_value_label.place(relx=0.495, rely=0.577, height=31, width=204)
        self.bitrate_value_label.configure(anchor='w')
        self.bitrate_value_label.configure(background="#d9d9d9")
        self.bitrate_value_label.configure(compound='left')
        self.bitrate_value_label.configure(disabledforeground="#a3a3a3")
        self.bitrate_value_label.configure(font="-family {Comic Sans MS} -size 14")
        self.bitrate_value_label.configure(foreground="#000000")
        self.bitrate_value_label.configure(text='''-''')

        self.initialize_stream_list()
        self.get_download_directory()

    def get_download_directory(self):
        with open("settings.json", "r") as js_file:
            settings = json.load(js_file)
            self.download_directory = settings['directory']

    def selected_item_combobox(self):
        self.download_window.focus()
        current_stream_index = self.resolution_combobox.current()
        current_stream = self.streams[current_stream_index]
        self.size_value_label.configure(text=f"{current_stream.filesize_mb} MB")
        self.bitrate_value_label.configure(text=f"{int(current_stream.bitrate / 1_000)}kbps")

    def initialize_stream_list(self):
        self.resolution_combobox['values'] = self.stream_list

    def start_download(self):
        if self.resolution_combobox.get() == "Please select a stream.":
            messagebox.showinfo("Incomplete Requirements", "Please select a stream :D")
            return
        continue_download = True

        current_stream_index = self.resolution_combobox.current()
        current_stream: Stream = self.streams[current_stream_index]

        def download():
            self.download_window.destroy()
            ProgressInterface(stream=current_stream, video=self.video, parent_window=self.parent_window,
                              directory=self.download_directory)

        if os.path.exists(f"{self.download_directory}{current_stream.title}.{current_stream.subtype}"):
            continue_download = messagebox.askyesno("Existing copy", "File is already existing, continue and overwrite?")
            if continue_download:
                filename = f"{self.download_directory}{current_stream.title}.{current_stream.subtype}"
                try:
                    os.remove(filename)
                    print(f"File '{filename}' deleted successfully.")
                except FileNotFoundError:
                    print(f"File '{filename}' not found.")
                except Exception as e:
                    print(f"An error occurred: {e}")

        if continue_download:
            print(f"Directory: {self.download_directory}{current_stream.title}.{current_stream.subtype}")
            thread = threading.Thread(target=download)
            thread.start()
        else:
            self.download_window.destroy()


class LoadStreams:
    def __init__(self, parent_window, video: pytube.YouTube, selected_mode):

        self.parent_window = parent_window
        self.loading_window = tk.Toplevel(self.parent_window)
        self.loading_window.overrideredirect(True)

        self.loading_window.geometry("305x90+703+472")
        self.loading_window.minsize(120, 1)
        self.loading_window.maxsize(4324, 1061)
        self.loading_window.resizable(True, True)
        self.loading_window.title("Loading")
        self.loading_window.configure(background="#d9d9d9")

        self.selected_mode = selected_mode
        self.video = video
        self.streams = None
        self.stream_list = []

        self.loading_header = tk.Label(self.loading_window)
        self.loading_header.place(relx=0.0, rely=0.0, height=91, width=304)
        self.loading_header.configure(background="#d9d9d9")
        self.loading_header.configure(compound='left')
        self.loading_header.configure(disabledforeground="#a3a3a3")
        self.loading_header.configure(font="-family {Comic Sans MS} -size 36 -weight bold")
        self.loading_header.configure(foreground="#000000")
        self.loading_header.configure(text='''Please wait''')

        self.start_dl()

    def load_stream_list(self):
        if self.selected_mode == "normal":
            self.streams = self.video.streams.filter(progressive=True, only_audio=False)
        elif self.selected_mode == "audio_only":
            self.streams = self.video.streams.filter(progressive=False, only_audio=True)

        if self.selected_mode == "normal":
            for streams in self.streams:
                self.stream_list.append(f"{streams.resolution}, {streams.subtype}")
        elif self.selected_mode == "audio_only":
            for streams in self.streams:
                self.stream_list.append(f"{int(streams.bitrate / 1_000)}kbps, {streams.subtype}")

    def start_dl(self):
        self.load_stream_list()
        dl_window = DownloadInterface(parent_window=self.parent_window, video=self.video, selected_mode=self.selected_mode,
                                      streams=self.streams, stream_list=self.stream_list)
        self.loading_window.withdraw()
        dl_window.download_window.wait_window()
        self.loading_window.destroy()
        self.parent_window.deiconify()


if __name__ == '__main__':
    window = tk.Tk()
    LoadStreams(window, YouTube('https://youtu.be/y2XArpEcygc'), "normal")
    window.mainloop()
