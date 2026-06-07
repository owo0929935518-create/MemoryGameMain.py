import tkinter as tk
from pathlib import Path
from PIL import Image, ImageTk


class Card(tk.Button):
    _images_loaded = False
    _front_images = {}
    _back_image = None
    _matched_image = None
    _image_size = (100, 140)

    @classmethod
    def _find_image_folder(cls):
        script_dir = Path(__file__).resolve().parent
        candidates = [
            script_dir / "poker_images",
            script_dir.parent / "poker_images",
            Path.cwd() / "poker_images",
        ]
        for candidate in candidates:
            if candidate.is_dir():
                return candidate
        raise FileNotFoundError(
            "找不到 poker_images 資料夾，請將 poker_images 放在程式目錄或父目錄中。"
        )

    @classmethod
    def _value_to_index(cls, value):
        if value == "A":
            return 1
        if value == "J":
            return 11
        if value == "Q":
            return 12
        if value == "K":
            return 13
        return int(value)

    @classmethod
    def _load_image(cls, image_path, master):
        image = Image.open(image_path)
        image = image.resize(cls._image_size, Image.LANCZOS)
        return ImageTk.PhotoImage(image, master=master)

    @classmethod
    def _load_blank_image(cls, master):
        blank = Image.new("RGBA", cls._image_size, (240, 240, 240, 255))
        return ImageTk.PhotoImage(blank, master=master)

    @classmethod
    def load_images(cls, master):
        if cls._images_loaded:
            return

        image_folder = cls._find_image_folder()
        cls._back_image = cls._load_image(image_folder / "pokerbk.jpg", master)
        cls._matched_image = cls._load_blank_image(master)

        for value in ["A", "2", "3", "4", "5", "6", "7", "8", "9", "10", "J", "Q", "K"]:
            index = cls._value_to_index(value)
            image_path = image_folder / f"poker{index}.jpg"
            if image_path.exists():
                cls._front_images[value] = cls._load_image(image_path, master)

        cls._images_loaded = True

    def __init__(self,
                 master,
                 value,
                 game,
                 **kwargs):

        if not Card._images_loaded:
            Card.load_images(master)

        super().__init__(
            master,
            image=Card._back_image,
            command=self.click_card,
            **kwargs
        )

        self.value = value
        self.game = game
        self.is_flipped = False
        self.is_matched = False
        self.front_image = Card._front_images.get(value)

        self.show_back()

    def show_back(self):
        if not self.is_matched:
            self.config(
                image=Card._back_image,
                state="normal",
                text=""
            )
            self.is_flipped = False

    def show_front(self):
        if self.front_image is not None:
            self.config(
                image=self.front_image,
                text=""
            )
        else:
            self.config(
                image="",
                text=self.value
            )
        self.is_flipped = True

    def clear_card(self):
        self.config(
            image=Card._matched_image,
            state="disabled",
            text=""
        )
        self.is_matched = True

    def click_card(self):
        self.game.select_card(self)
