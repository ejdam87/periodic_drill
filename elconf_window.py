import tkinter as tk

class ElconfWindow(tk.Toplevel):

    def __init__(self, *args):
        super().__init__(*args)

    def configure(self, symbol: str, correct_answer: str) -> None:
        self.correct = correct_answer

        tk.Label(self, text="Electron configuration").grid(row=1, column=1)
        tk.Label(self, text=symbol).grid(row=2, column=1)
        self.user_input = tk.Entry(self)
        self.user_input.grid(row=3, column=1)
        tk.Button(self, text="Submit", command=self.check_answer).grid(row=4, column=1)

    def check_answer(self) -> None:
        user = self.user_input.get()
        if user.lower().replace(" ", "") == self.correct:
            pass
        else:
            pass
