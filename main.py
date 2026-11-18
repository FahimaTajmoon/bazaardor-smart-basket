import tkinter as tk
from tkinter import ttk

from manager import BazaarManager
from storage import load_records
from gui_records import RecordsTab
from gui_basket import BasketTab
from theme import apply_theme


class BazaarDorApp:
    def __init__(self, root):
        self.root = root
        self.root.title("BazaarDor - Smart Basket")
        self.root.geometry("1150x720")
        self.root.minsize(850, 560)
        apply_theme(self.root)

        records = load_records("data/prices.json")
        self.manager = BazaarManager(records)

        self.tabs = ttk.Notebook(self.root)
        self.tabs.pack(fill="both", expand=True, padx=10, pady=(10, 4))

        self.records_tab = RecordsTab(self, self.tabs)

        self.basket_tab = BasketTab(self, self.tabs)

        self.status_label = ttk.Label(
            self.root,
            text="BazaarDor is ready.",
            anchor="w",
            relief="sunken",
            padding=(8, 5),
        )
        self.status_label.pack(side="bottom", fill="x")

    def say(self, text):
        self.status_label.config(text=str(text))


if __name__ == "__main__":
    root = tk.Tk()
    app = BazaarDorApp(root)
    root.mainloop()
