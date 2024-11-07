import tkinter as tk

# --- local imports
from gui_const import *


class ElconfWindow(tk.Toplevel):

    def __init__(self, *args):
        super().__init__(*args)
        self.geometry(f"{ELCONF_WIDTH}x{ELCONF_HEIGHT}")
        self.title("Electron configuration")
        self.iconbitmap("icon.ico")

    def configure_quiz(self, symbol: str, correct_answer: str) -> None:
        self.correct = correct_answer
        self.status = tk.StringVar()
        self.columnconfigure(1, weight=5)

        tk.Label(self,
                 text="Electron configuration",
                 bg=BG_COLOR,
                 fg=TEXT_COLOR,
                 font=ACTIVE_FONT).grid(row=1, column=1)

        tk.Label(self,
                 text=symbol,
                 bg=BG_COLOR,
                 font=HELP_FONT,
                 fg=TEXT_COLOR).grid(row=2, column=1)

        self.user_input = tk.Entry(self,
                                   bg=BG_COLOR,
                                   fg=TEXT_COLOR,
                                   font=HELP_FONT,
                                   insertbackground=TEXT_COLOR)

        self.user_input.grid(row=3, column=1, sticky=tk.W + tk.E, pady=10)

        tk.Button(self,
                  text="Submit",
                  bg=BG_COLOR,
                  fg=TEXT_COLOR,
                  font=HELP_FONT,
                  command=self.check_answer).grid(row=4, column=1)

        tk.Label(self,
                 textvariable=self.status,
                 bg=BG_COLOR,
                 fg=TEXT_COLOR,
                 font=HELP_FONT).grid(row=5, column=1, pady=10)

        tk.Button(self,
                  text="Show",
                  bg=BG_COLOR,
                  fg=TEXT_COLOR,
                  font=HELP_FONT,
                  command=self.show_answer).grid(row=6, column=1)

    # --- Button functionality
    def check_answer(self) -> None:
        user = self.user_input.get()
        if user.lower().replace(" ", "") == self.correct.replace(" ", ""):
            self.destroy()
        else:
            self.status.set("Wrong cici")

    def show_answer(self) -> None:
        self.user_input.delete(0, tk.END)
        self.user_input.insert(0, self.correct)
