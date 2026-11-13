"""Smart Basket screen: build a shopping basket, find the cheapest bazaar for
each item, and rank the bazaars by what the whole basket costs there."""

from tkinter import messagebox, ttk

import analysis
from models import ITEMS, Basket
from ui import COLORS, FONT, fill_table, make_button, make_table, selected_value
from validation import check_quantity

# Dictionaries: table column -> width in pixels
LIST_COLUMNS = {"Item": 220, "Quantity": 90, "Unit": 70}
ESTIMATE_COLUMNS = {
    "Item": 190,
    "Qty": 60,
    "Cheapest at": 210,
    "Cost there (Tk)": 130,
    "At average (Tk)": 130,
}


class BasketTab:
    def __init__(self, app, notebook):
        self.app = app  # the main app: gives us app.manager and app.say()
        self.basket = Basket()
        self.frame = ttk.Frame(notebook, padding=14)
        notebook.add(self.frame, text="Smart Basket")
        self.build_form()
        self.list_table = make_table(self.frame, LIST_COLUMNS, height=4)
        self.build_buttons()
        self.estimate_table = make_table(self.frame, ESTIMATE_COLUMNS, height=4)
        self.result_label = ttk.Label(
            self.frame,
            text="Add items to the basket, then click Estimate cost.",
            justify="left",
            font=(FONT, 12, "bold"),
            wraplength=1000,
        )
        self.result_label.pack(anchor="w", pady=(10, 0))

    # ---------- building the screen ----------

    def build_form(self):
        form = ttk.Frame(self.frame, style="Card.TFrame", padding=12)
        form.pack(fill="x")

        ttk.Label(form, text="Item", style="CardBold.TLabel").grid(row=0, column=0, sticky="w")
        ttk.Label(form, text="Quantity", style="CardBold.TLabel").grid(
            row=0, column=1, sticky="w", padx=8
        )
        self.item_box = ttk.Combobox(
            form, values=tuple(ITEMS), state="readonly", width=24, font=(FONT, 12)
        )
        self.item_box.set(tuple(ITEMS)[0])
        self.item_box.grid(row=1, column=0, pady=(4, 0), sticky="w")
        self.quantity_entry = ttk.Entry(form, width=8, font=(FONT, 12))
        self.quantity_entry.insert(0, "1")
        self.quantity_entry.grid(row=1, column=1, padx=8, pady=(4, 0), sticky="w")
        self.quantity_entry.bind("<Return>", self.add_to_basket)
        make_button(form, "+ Add to basket", "Green", self.add_to_basket).grid(
            row=1, column=2, pady=(4, 0), sticky="w"
        )

    def build_buttons(self):
        buttons = ttk.Frame(self.frame, padding=(0, 10, 0, 0))
        buttons.pack(fill="x")
        actions = (
            ("Estimate cost", "Blue", self.estimate),
            ("Remove item", "Red", self.remove_from_basket),
            ("Clear basket", "Grey", self.clear_basket),
        )
        for text, color, command in actions:
            make_button(buttons, text, color, command).pack(side="left", padx=(0, 8))

    # ---------- the basket ----------

    def show_basket(self):
        rows = []
        for item, quantity in self.basket.items.items():
            rows.append((item, f"{quantity:g}", ITEMS[item]))
        fill_table(self.list_table, rows)
        fill_table(self.estimate_table, [])
        self.result_label.config(
            text="Click Estimate cost to see the totals.", foreground=COLORS["text"]
        )

    def add_to_basket(self, event=None):
        item = self.item_box.get()
        try:
            quantity = check_quantity(self.quantity_entry.get())
        except ValueError as error:
            messagebox.showerror("Please check", str(error))
            return
        already_listed = item in self.basket.items
        self.basket.add(item, quantity)
        self.show_basket()
        if already_listed:
            self.app.say(f"Changed {item} to {quantity:g} {ITEMS[item]}.")
        else:
            self.app.say(f"Added {quantity:g} {ITEMS[item]} of {item} to the basket.")

    def remove_from_basket(self):
        item = selected_value(self.list_table)
        if item is None:
            messagebox.showinfo("Pick a row", "Click an item in the basket first.")
            return
        self.basket.remove(item)
        self.show_basket()
        self.app.say(f"Removed {item} from the basket.")

    def clear_basket(self):
        self.basket.clear()
        self.show_basket()
        self.app.say("Basket cleared.")

    # ---------- the estimate ----------

    def estimate(self):
        if not self.basket.items:
            messagebox.showinfo("Smart basket", "Add at least one item first.")
            return

        result = analysis.shopping_estimate(self.app.manager, self.basket.items)
        rows = []
        for line in result["lines"]:
            rows.append(
                (
                    line["item"],
                    f"{line['quantity']:g}",
                    line["market"],
                    f"{line['cheapest_cost']:,.2f}",
                    f"{line['average_cost']:,.2f}",
                )
            )
        fill_table(self.estimate_table, rows)

        lines = [
            f"Each item at its cheapest bazaar: {result['total_cheapest']:,.2f} Tk "
            f"(at average prices {result['total_average']:,.2f} Tk, "
            f"so you save {result['saving']:,.2f} Tk)."
        ]

        # Most people buy everything in one place, so rank the bazaars by the whole basket
        market_totals = analysis.cost_by_market(self.app.manager, self.basket.items)
        if market_totals:
            lines.append("Whole basket at one bazaar, cheapest first:")
            ranking = sorted(market_totals.items(), key=lambda pair: pair[1])
            for rank, (market, total) in enumerate(ranking, start=1):
                lines.append(f"{rank}. {market}: {total:,.2f} Tk")
        if result["missing"]:
            lines.append("No prices yet for: " + ", ".join(result["missing"]) + ".")

        self.result_label.config(text="\n".join(lines), foreground=COLORS["primary"])
        self.app.say(f"Estimated {len(self.basket.items)} items.")
