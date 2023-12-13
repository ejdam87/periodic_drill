import tkinter as tk
import tkinter.ttk as ttk
import json
import random
from functools import partial

# --- Group name mapping
GROUP_NAMES = {
    1: "I.A",
    2: "II.A",
    3: "III.B",
    4: "IV.B",
    5: "V.B",
    6: "VI.B",
    7: "VII.B",
    8: "VIII.B",
    9: "VIII.B",
    10: "VIII.B",
    11: "I.B",
    12: "II.B",
    13: "III.A",
    14: "IV.A",
    15: "V.A",
    16: "VI.A",
    17: "VII.A",
    18: "VIII.A"
}
# ---

# --- GUI constants
INITIAL_WIDTH = 1000
INITIAL_HEIGHT = 600

SUCCESS_COLOR = "#00FF00"
FAIL_COLOR = "#FF0000"
BG_COLOR = "#000000"

TEXT_COLOR = "#FFFFFF"

FONT = ("Helvetica", 10)
HELP_FONT = ("Helvetica", 12)
ACTIVE_FONT = ("Helvetica", 14)
# ---

def load_table(path: str) -> list[str, str, int, int]:
    """
    Funtion to load all neccessary chemical data
    """

    res = []

    with open(path, encoding="utf8") as f:
        table = json.load(f)
        
        for elem in table["order"]:

            if table[elem]["symbol"] == "Uue":
                continue

            res.append( (table[elem]["name"], table[elem]["symbol"],
                         table[elem]["period"], table[elem]["group"], table[elem]["number"]) )

    return res


class Window(tk.Tk):

    def __init__(self, *args) -> None:
        super().__init__(*args)
        self.geometry(f"{INITIAL_WIDTH}x{INITIAL_HEIGHT}")
        self.title("Periodic table drill")
        self.configure(background=BG_COLOR)
        self.table = load_table("table.json")

        self.base_elements = []
        self.round_elements = []

        self.buttons = {}
        self.missed_buttons = []

        self.active_element = tk.StringVar()
        self.active_element.set("??")
        self.win_phrase = tk.StringVar()

        self.table_shown = True

        for i in range(20):
            self.grid_columnconfigure(i, weight=1)
        for i in range(20):
            self.grid_rowconfigure(i, weight=1)

        y_padding = 2
        x_padding = 1

        ## [period, group] labels
        ## ---
        for period in range(1, 8):
            tk.Label(self,
                     text=f"{period}",
                     font=FONT,
                     fg=TEXT_COLOR,
                     bg=BG_COLOR).grid(row=period + y_padding, column=1)

        ## lanthanoids, actinoids
        tk.Label(self, text="", fg=TEXT_COLOR, bg=BG_COLOR).grid(row=9 + y_padding, column=1)

        tk.Label(self,
                 text=f"{6}",
                 font=FONT,
                 fg=TEXT_COLOR,
                 bg=BG_COLOR).grid(row=10 + y_padding, column=1)
        tk.Label(self,
                 text=f"{7}",
                 font=FONT,
                 fg=TEXT_COLOR,
                 bg=BG_COLOR).grid(row=11 + y_padding, column=1)

        for group in range(1, 19):
            tk.Label(self,
                     text=f"{group}",
                     font=FONT,
                     fg=TEXT_COLOR,
                     bg=BG_COLOR).grid(row=1, column=group + x_padding)
            tk.Label(self,
                     text=GROUP_NAMES[group],
                     font=FONT,
                     fg=TEXT_COLOR,
                     bg=BG_COLOR).grid(row=2, column=group + x_padding)
        ## ---

        ## --- periodic table layout setting
        for name, symbol, period, group, number in self.table:

            self.base_elements.append(symbol)
            button = tk.Button(self, text=symbol, font=FONT, bg=BG_COLOR, fg=TEXT_COLOR, width=5, height=2)
            x = -1
            y = -1

            actinium_number = 89
            lantanium_number = 57

            ## actionids and lanthanoids
            if period in (6, 7) and group == 3:
                delimiter = lantanium_number if period == 6 else actinium_number
                x = number - delimiter + x_padding + 4
                y = period + y_padding + 4
                button.grid(row=y, column=x, padx=2, pady=2)
            else:
                x = group + x_padding
                y = period + y_padding
                button.grid(row=y, column=x, padx=2, pady=2)

            button.configure(command=partial(self.fill, x, y))
            self.buttons[(x, y)] = (button, symbol)

        tk.Label(self,
            text="Active:",
            font=HELP_FONT,
            fg=TEXT_COLOR,
            bg=BG_COLOR).grid(row=4,
                              column=7,
                              columnspan=1)
        tk.Label(self,
            textvariable=self.active_element,
            font=ACTIVE_FONT,
            borderwidth=1,
            relief="solid",
            fg=TEXT_COLOR,
            bg=BG_COLOR).grid(row=4,
                              column=9,
                              rowspan=1,
                              columnspan=1,
                              sticky=tk.W+tk.E+tk.N+tk.S)

        tk.Label(self,
                 textvariable=self.win_phrase,
                 font=HELP_FONT,
                 fg=TEXT_COLOR,
                 bg=BG_COLOR).grid(row=5,
                                   column=8,
                                   columnspan=3)

        ttk.Separator(self, orient="horizontal").grid(column=1,
                                                      row=11 + y_padding + 1,
                                                      columnspan=20,
                                                      pady=10,
                                                      sticky=tk.W+tk.E)


        self.show_button = tk.Button(self,
                                     text="Hide\ntable",
                                     command=self.show_hide,
                                     font=FONT,
                                     fg=TEXT_COLOR,
                                     bg=BG_COLOR)

        self.show_button.grid(row=11 + y_padding + 2,
                              column=2,
                              columnspan=1,
                              rowspan=1,
                              sticky=tk.W+tk.E+tk.N+tk.S,
                              pady=10)

        tk.Button(self,
                  text="Restart",
                  command=self.restart,
                  font=ACTIVE_FONT,
                  fg=TEXT_COLOR,
                  bg=BG_COLOR).grid(row=11 + y_padding + 2,
                                      column=5,
                                      sticky=tk.W+tk.E+tk.N+tk.S,
                                      columnspan=3,
                                      rowspan=1,
                                      pady=10)
        tk.Button(self,
                  text="Start",
                  command=self.start,
                  font=ACTIVE_FONT,
                  fg=TEXT_COLOR,
                  bg=BG_COLOR).grid(row=11 + y_padding + 2,
                                      column=9,
                                      sticky=tk.W+tk.E+tk.N+tk.S,
                                      columnspan=3,
                                      rowspan=1,
                                      pady=10)
        tk.Button(self,
                  text="Reveal",
                  command=self.reveal,
                  font=ACTIVE_FONT,
                  fg=TEXT_COLOR,
                  bg=BG_COLOR).grid(row=11 + y_padding + 2,
                                    column=13,
                                    sticky=tk.W+tk.E+tk.N+tk.S,
                                    columnspan=3,
                                    rowspan=1,
                                    pady=10)
        ## ---

    ## recolor red cells
    def recolor_missed(self) -> None:
        for button in self.missed_buttons:
            button.configure(bg=BG_COLOR)
        self.missed_buttons = []

    ## choosing next element to guess
    def next_active(self) -> None:
        if len(self.round_elements) == 0:
            self.active_element.set("??")
            self.win_phrase.set("Great job Pipi!!!")
            return

        random.shuffle(self.round_elements)
        self.active_element.set(self.round_elements.pop())

    ## functionality of periodic table buttons
    def fill(self, x: int, y: int) -> None:
        button, symbol = self.buttons[(x, y)]
        if self.active_element.get() == symbol:
            button.configure(bg=SUCCESS_COLOR, text=symbol)
            self.next_active()
            self.recolor_missed()

        ## We did not select alredy solved button
        elif button.cget("bg") != SUCCESS_COLOR:
            button.configure(bg=FAIL_COLOR)
            self.missed_buttons.append(button)

    ## --- Button functionality
    def show_hide(self, initial=False) -> None:
        # initial - during the first hiding (also during the restart) remove green/red colors
        self.show_button.configure(text="Hide\ntable" if self.table_shown else "Show\ntable")
        for button, symbol in self.buttons.values():
            color = BG_COLOR if initial else button.cget("bg")
            to_fill = "" if self.table_shown else symbol
            button.configure(text=to_fill, bg=color)
        self.table_shown = not self.table_shown

    def start(self) -> None:

        self.win_phrase.set("")
        # initialize active element
        self.round_elements = self.base_elements[:]

        # hide elements
        self.show_hide(initial=True)

        if self.table_shown:
            self.show_hide()

        self.next_active()

    def restart(self) -> None:
        self.start()

    def reveal(self) -> None:
        for button, symbol in self.buttons.values():
            if self.active_element.get() == symbol:
                button.invoke()
                break
    ## ---
