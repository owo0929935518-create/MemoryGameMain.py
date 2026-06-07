import tkinter as tk


class Card(tk.Button):

    def __init__(self,
                 master,
                 value,
                 game,
                 **kwargs):

        super().__init__(
            master,
            width=8,
            height=4,
            font=("Arial", 16),
            command=self.click_card,
            **kwargs
        )

        self.value = value
        self.game = game

        self.is_flipped = False
        self.is_matched = False

        self.show_back()

    def show_back(self):
        if not self.is_matched:
            self.config(
                text="❓",
                state="normal"
            )
            self.is_flipped = False

    def show_front(self):
        self.config(
            text=self.value
        )
        self.is_flipped = True

    def clear_card(self):
        self.config(
            text="",
            state="disabled",
            bg="lightgray"
        )
        self.is_matched = True

    def click_card(self):
        self.game.select_card(self)
