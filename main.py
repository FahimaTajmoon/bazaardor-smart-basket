"""Main Tkinter application for BazaarDor."""

import tkinter as tk
from tkinter import ttk

from manager import BazaarManager
from storage import load_records
from gui_records import RecordsTab
from gui_basket import BasketTab


class BazaarDorApp:
    def __init__(self, root):
        self.root = root
        self.root.title("BazaarDor - Smart Basket")
        self.root.geometry("1150x720")
        self.root.minsize(850, 560)

        # Load price records from the shared JSON database, then create Arif's manager.
        records = load_records("data/prices.json")
        self.manager = BazaarManager(records)

        # Shared notebook for the application's screens.
        self.tabs = ttk.Notebook(self.root)
        self.tabs.pack(fill="both", expand=True, padx=10, pady=(10, 4))

        # Member 3: price-record form and table.
        self.records_tab = RecordsTab(self, self.tabs)

        # Member 4: Smart Basket screen. BasketTab uses app.manager and app.say().
        self.basket_tab = BasketTab(self, self.tabs)

        # Shared status message area used by both tabs.
        self.status_label = ttk.Label(
            self.root,
            text="BazaarDor is ready.",
            anchor="w",
            relief="sunken",
            padding=(8, 5),
        )
        self.status_label.pack(side="bottom", fill="x")

    def say(self, text):
        """Show a short status message at the bottom of the main window."""
        self.status_label.config(text=str(text))


if __name__ == "__main__":
    root = tk.Tk()
    app = BazaarDorApp(root)
    root.mainloop()
