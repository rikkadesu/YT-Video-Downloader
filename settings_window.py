import json
import sys
import tkinter as tk
import os.path
from tkinter import filedialog, messagebox

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


class SettingsInterface:
    def __init__(self, parent_window):
        """This class configures and populates the toplevel window.
           top is the toplevel containing window."""

        self.parent_window = parent_window
        self.settings_window = tk.Toplevel(self.parent_window)
        self.settings_window.geometry("485x159+651+368")
        self.settings_window.minsize(120, 1)
        self.settings_window.maxsize(1924, 1061)
        self.settings_window.resizable(True,  True)
        self.settings_window.title("Settings")
        self.settings_window.configure(background="#d9d9d9")

        self.dl_path_label = tk.Label(self.settings_window)
        self.dl_path_label.place(relx=0.021, rely=0.126, height=29, width=459)
        self.dl_path_label.configure(anchor='w')
        self.dl_path_label.configure(background="#d9d9d9")
        self.dl_path_label.configure(compound='left')
        self.dl_path_label.configure(disabledforeground="#a3a3a3")
        self.dl_path_label.configure(font="-family {Comic Sans MS} -size 14 -weight bold")
        self.dl_path_label.configure(foreground="#000000")
        self.dl_path_label.configure(text='''Download path: (Leave blank to use default path)''')

        self.dl_path_entry = tk.Entry(self.settings_window)
        self.dl_path_entry.place(relx=0.021, rely=0.377, height=34, relwidth=0.874)
        self.dl_path_entry.configure(background="white")
        self.dl_path_entry.configure(disabledforeground="#a3a3a3")
        self.dl_path_entry.configure(font="-family {Comic Sans MS} -size 10")
        self.dl_path_entry.configure(foreground="#000000")
        self.dl_path_entry.configure(insertbackground="black")

        self.file_pick_button = tk.Button(self.settings_window)
        self.file_pick_button.place(relx=0.909, rely=0.377, height=34, width=37)
        self.file_pick_button.configure(activebackground="beige")
        self.file_pick_button.configure(activeforeground="black")
        self.file_pick_button.configure(background="#d9d9d9")
        self.file_pick_button.configure(command=self.open_directory_picker)
        self.file_pick_button.configure(compound='left')
        self.file_pick_button.configure(cursor='hand2')
        self.file_pick_button.configure(disabledforeground="#a3a3a3")
        self.file_pick_button.configure(font="-family {Comic Sans MS} -size 9")
        self.file_pick_button.configure(foreground="#000000")
        self.file_pick_button.configure(highlightbackground="#d9d9d9")
        self.file_pick_button.configure(highlightcolor="black")
        self.file_pick_button.configure(pady="0")
        self.file_pick_button.configure(text='''Pick''')

        self.save_button = tk.Button(self.settings_window)
        self.save_button.place(relx=0.41, rely=0.692, height=34, width=77)
        self.save_button.configure(activebackground="#b5b5b5")
        self.save_button.configure(activeforeground="black")
        self.save_button.configure(background="#d9d9d9")
        self.save_button.configure(command=self.save_settings)
        self.save_button.configure(compound='left')
        self.save_button.configure(cursor='hand2')
        self.save_button.configure(disabledforeground="#a3a3a3")
        self.save_button.configure(font="-family {Comic Sans MS} -size 14")
        self.save_button.configure(foreground="#000000")
        self.save_button.configure(highlightbackground="#d9d9d9")
        self.save_button.configure(highlightcolor="black")
        self.save_button.configure(pady="0")
        self.save_button.configure(text='''Save''')

        self.get_current_directory()

    def open_directory_picker(self):
        directory = filedialog.askdirectory(title="Choose where to save...")
        if directory:
            self.dl_path_entry.delete(0, tk.END)
            self.dl_path_entry.insert(0, f"{directory}/")

    def get_current_directory(self):
        with open("settings.json", "r") as js_file:
            settings = json.load(js_file)
            self.dl_path_entry.delete(0, tk.END)
            self.dl_path_entry.insert(0, settings["directory"])

    def save_settings(self):
        directory = self.dl_path_entry.get()[::-1]
        if directory and directory[0] != "/":
            directory = f"{self.dl_path_entry.get()}/"
        else:
            directory = self.dl_path_entry.get()

        with open("settings.json", "w") as js_file:
            settings = {
                "directory": directory
            }
            json.dump(settings, js_file)

        messagebox.showinfo("Success", "Settings saved successfully!")


if __name__ == '__main__':
    window = tk.Tk()
    SettingsInterface(window)
    window.mainloop()
