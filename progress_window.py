import sys
import tkinter as tk
import tkinter.ttk as ttk
import os.path
import time
from tkinter import messagebox

from pytube import Stream, YouTube, request

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


class ProgressInterface:
    def __init__(self, **kwargs):
        self.stream: Stream = kwargs['stream']
        self.video: YouTube = kwargs['video']
        self.parent_window = kwargs['parent_window']
        self.download_directory = kwargs['directory']

        self.start_time = None
        self.paused = self.cancelled = False

        self.progress_window = tk.Toplevel(self.parent_window)
        self.progress_window.geometry("463x174+699+394")
        self.progress_window.minsize(120, 1)
        self.progress_window.maxsize(4324, 1061)
        self.progress_window.resizable(True, True)
        self.progress_window.title(f"{self.stream.title} - Download Progress")
        self.progress_window.configure(background="#d9d9d9")

        self.video_title_label = tk.Label(self.progress_window)
        self.video_title_label.place(relx=0.022, rely=0.063, height=38, width=444)
        self.video_title_label.configure(anchor='nw')
        self.video_title_label.configure(background="#d9d9d9")
        self.video_title_label.configure(compound='left')
        self.video_title_label.configure(disabledforeground="#a3a3a3")
        self.video_title_label.configure(font="-family {Comic Sans MS} -size 12")
        self.video_title_label.configure(foreground="#000000")
        self.video_title_label.configure(text=f"{self.stream.title}.{self.stream.subtype}")
        self.video_title_label.configure(wraplength="444")

        _style_code()

        self.percent_progress_progressbar = ttk.Progressbar(self.progress_window)
        self.percent_progress_progressbar.place(relx=0.022, rely=0.374, relwidth=0.957, relheight=0.0, height=21)
        self.percent_progress_progressbar.configure(length="440")

        self.progress_info_label = tk.Label(self.progress_window)
        self.progress_info_label.place(relx=0.022, rely=0.557, height=20, width=444)
        self.progress_info_label.configure(anchor='w')
        self.progress_info_label.configure(background="#d9d9d9")
        self.progress_info_label.configure(compound='left')
        self.progress_info_label.configure(disabledforeground="#a3a3a3")
        self.progress_info_label.configure(font="-family {Comic Sans MS} -size 12")
        self.progress_info_label.configure(foreground="#000000")
        self.progress_info_label.configure(text='''Completed: 0%   Estimated: 0 seconds''')

        self.cancel_button = tk.Button(self.progress_window)
        self.cancel_button.place(relx=0.799, rely=0.753, height=24, width=77)
        self.cancel_button.configure(activebackground="beige")
        self.cancel_button.configure(activeforeground="black")
        self.cancel_button.configure(background="#d9d9d9")
        self.cancel_button.configure(command=self.toggle_cancel)
        self.cancel_button.configure(compound='left')
        self.cancel_button.configure(cursor='hand2')
        self.cancel_button.configure(disabledforeground="#a3a3a3")
        self.cancel_button.configure(font="-family {Comic Sans MS} -size 10")
        self.cancel_button.configure(foreground="#000000")
        self.cancel_button.configure(highlightbackground="#d9d9d9")
        self.cancel_button.configure(highlightcolor="black")
        self.cancel_button.configure(pady="0")
        self.cancel_button.configure(text='''Cancel''')

        self.pause_button = tk.Button(self.progress_window)
        self.pause_button.place(relx=0.626, rely=0.753, height=24, width=77)
        self.pause_button.configure(activebackground="beige")
        self.pause_button.configure(activeforeground="black")
        self.pause_button.configure(background="#d9d9d9")
        self.pause_button.configure(command=self.toggle_pause)
        self.pause_button.configure(compound='left')
        self.pause_button.configure(cursor='hand2')
        self.pause_button.configure(disabledforeground="#a3a3a3")
        self.pause_button.configure(font="-family {Comic Sans MS} -size 10")
        self.pause_button.configure(foreground="#000000")
        self.pause_button.configure(highlightbackground="#d9d9d9")
        self.pause_button.configure(highlightcolor="black")
        self.pause_button.configure(pady="0")
        self.pause_button.configure(text='''Pause''')

        self.done_button = tk.Button(self.progress_window)
        self.done_button.place(relx=0.028, rely=0.753, height=24, width=77)
        self.done_button.configure(activebackground="beige")
        self.done_button.configure(activeforeground="black")
        self.done_button.configure(background="#d9d9d9")
        self.done_button.configure(command=lambda: self.progress_window.destroy())
        self.done_button.configure(compound='left')
        self.done_button.configure(cursor="hand2")
        self.done_button.configure(disabledforeground="#a3a3a3")
        self.done_button.configure(font="-family {Comic Sans MS} -size 10")
        self.done_button.configure(foreground="#000000")
        self.done_button.configure(highlightbackground="#d9d9d9")
        self.done_button.configure(highlightcolor="black")
        self.done_button.configure(pady="0")
        self.done_button.configure(state="disabled")
        self.done_button.configure(text='''Done''')

        self.start_download_()

    # def progress_callback(self, stream, chunk, bytes_remaining):
    #     total_size = stream.filesize
    #     bytes_downloaded = total_size - bytes_remaining
    #     percent_completed = round(bytes_downloaded / total_size * 100, 2)
    #
    #     self.percent_progress_progressbar['value'] = percent_completed
    #     self.percent_progress_progressbar.update()
    #
    #     elapsed_time = time.time() - self.start_time
    #     download_rate = bytes_downloaded / elapsed_time
    #     estimated_time_remaining = round(bytes_remaining / download_rate)
    #
    #     self.progress_info_label.configure(text=f"Completed: {percent_completed}%   Estimated: "
    #                                             f"{estimated_time_remaining} seconds")

    # def start_download(self):
    #     self.video.register_on_progress_callback(self.progress_callback)
    #     self.start_time = time.time()
    #     self.stream.download()

    def start_download_(self):
        if not self.start_time:
            self.start_time = time.time()

        def callback():
            percent_completed = round(downloaded / total_size * 100, 2)
            self.percent_progress_progressbar['value'] = percent_completed
            self.percent_progress_progressbar.update()

            elapsed_time = time.time() - self.start_time
            download_rate = downloaded / elapsed_time
            estimated_time_remaining = round((total_size - downloaded) / download_rate)

            self.progress_info_label.configure(text=f"Completed: {percent_completed}%   Estimated: "
                                                    f"{estimated_time_remaining} seconds")

        total_size = self.stream.filesize
        try:
            with open(f"{self.download_directory}{self.stream.title}.{self.stream.subtype}", "wb") as video:
                vid_chunk = request.stream(self.stream.url)
                downloaded = 0
                while True:
                    if self.cancelled:
                        self.progress_window.destroy()
                        break
                    if self.paused:
                        self.video_title_label.configure(text=f"{self.stream.title}.{self.stream.subtype} (Paused)")
                        self.pause_button.configure(text="Resume")
                        time.sleep(1.5)
                        continue
                    chunk = next(vid_chunk, None)
                    self.video_title_label.configure(text=f"{self.stream.title}.{self.stream.subtype}")
                    self.pause_button.configure(text="Pause")
                    if chunk:
                        video.write(chunk)
                        downloaded += len(chunk)

                        callback()
                    else:
                        self.pause_button['state'] = 'disabled'
                        self.cancel_button['state'] = 'disabled'
                        self.done_button['state'] = 'normal'
                        break

            if self.cancelled:
                filename = f"{self.download_directory}{self.stream.title}.{self.stream.subtype}"
                try:
                    os.remove(filename)
                    print(f"File '{filename}' deleted successfully.")
                except FileNotFoundError:
                    print(f"File '{filename}' not found.")
                except Exception as e:
                    print(f"An error occurred: {e}")

        except Exception as e:
            messagebox.showwarning("Unhandled error", "An unhandled error has happened.\n"
                                                      f"Error info: {str(e).capitalize()}")
            self.progress_window.destroy()

    def toggle_pause(self):
        if not self.paused:
            self.video_title_label.configure(text=f"{self.stream.title}.{self.stream.subtype} (Pausing)")
            self.paused = True
            print("Pausing")
        else:
            self.paused = False
            print("Resumed")

    def toggle_cancel(self):
        self.cancelled = True
        self.video_title_label.configure(text=f"{self.stream.title}.{self.stream.subtype} (Cancelling)")
        print("Cancelled")


if __name__ == '__main__':
    ProgressInterface()
