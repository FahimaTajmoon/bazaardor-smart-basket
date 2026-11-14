"""Smart Basket screen: build a shopping basket, find the cheapest bazaar for
each item, and rank the bazaars by what the whole basket costs there."""

from tkinter import messagebox, ttk

import analysis
from models import Basket
from validation import validate_quantity

# Dictionaries: table column -> width in pixels
LIST_COLUMNS = {"Item": 220, "Quantity": 90, "Unit": 70}
ESTIMATE_COLUMNS = {
    "Item": 190,
    "Qty": 60,
    "Cheapest at": 210,
    "Cost there (Tk)": 130,
    "At average (Tk)": 130,
}


def make_table(parent, columns, height):
    """A table (Treeview). columns: dictionary column name -> width."""
    table = ttk.Treeview(parent, columns=tuple(columns), show="headings", height=height)
    for name, width in columns.items():
        table.heading(name, text=name)
        table.column(name, width=width, anchor="w")
    table.pack(fill="x", pady=(10, 0))
    return table


def fill_table(table, rows):
    """Replace all the rows of a table."""
    for row in table.get_children():
        table.delete(row)
    for values in rows:
        table.insert("", "end", values=values)


class BasketTab:
    def __init__(self, app, notebook):
        self.app = app  # the main app: gives us app.manager and app.say()
        self.basket = Basket("My basket")
        self.units = {}  # dictionary: item -> unit, filled from the price records
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
            wraplength=1000,
        )
        self.result_label.pack(anchor="w", pady=(10, 0))

    # ---------- building the screen ----------

    def build_form(self):
        form = ttk.LabelFrame(self.frame, text="Add to basket", padding=12)
        form.pack(fill="x")

        ttk.Label(form, text="Item").grid(row=0, column=0, sticky="w")
        ttk.Label(form, text="Quantity").grid(row=0, column=1, sticky="w", padx=8)
        # postcommand reloads the item list every time it opens, so new items appear
        self.item_box = ttk.Combobox(
            form, state="readonly", width=24, postcommand=self.refresh_items
        )
        self.item_box.grid(row=1, column=0, pady=(4, 0), sticky="w")
        self.refresh_items()
        if self.item_box["values"]:
            self.item_box.current(0)
        self.quantity_entry = ttk.Entry(form, width=8)
        self.quantity_entry.insert(0, "1")
        self.quantity_entry.grid(row=1, column=1, padx=8, pady=(4, 0), sticky="w")
        self.quantity_entry.bind("<Return>", self.add_to_basket)
        ttk.Button(form, text="+ Add to basket", command=self.add_to_basket).grid(
            row=1, column=2, pady=(4, 0), sticky="w"
        )

    def build_buttons(self):
        buttons = ttk.Frame(self.frame, padding=(0, 10, 0, 0))
        buttons.pack(fill="x")
        actions = (
            ("Estimate cost", self.estimate),
            ("Remove item", self.remove_from_basket),
            ("Clear basket", self.clear_basket),
        )
        for text, command in actions:
            ttk.Button(buttons, text=text, command=command).pack(side="left", padx=(0, 8))

    def refresh_items(self):
        records = self.app.manager.records
        items = {record.item for record in records}  # set: each item only once
        self.units = {record.item: record.unit for record in records}
        self.item_box["values"] = sorted(items)

    # ---------- the basket ----------

    def show_basket(self):
        rows = []
        for item, quantity in self.basket.items.items():
            rows.append((item, f"{quantity:g}", self.units.get(item, "")))
        fill_table(self.list_table, rows)
        fill_table(self.estimate_table, [])
        self.result_label.config(text="Click Estimate cost to see the totals.")

    def add_to_basket(self, event=None):
        item = self.item_box.get()
        if item == "":
            messagebox.showinfo("No items", "There are no price records yet. Add some first.")
            return
        try:
            quantity = validate_quantity(self.quantity_entry.get())
        except ValueError as error:
            messagebox.showerror("Please check", str(error))
            return
        self.basket.add_item(item, quantity)  # adds to the quantity if already listed
        self.show_basket()
        total = self.basket.items[item]
        self.app.say(f"Basket now has {total:g} {self.units.get(item, '')} of {item}.")

    def remove_from_basket(self):
        selected = self.list_table.selection()
        if not selected:
            messagebox.showinfo("Pick a row", "Click an item in the basket first.")
            return
        item = self.list_table.item(selected[0], "values")[0]
        self.basket.remove_item(item)
        self.show_basket()
        self.app.say(f"Removed {item} from the basket.")

    def clear_basket(self):
        self.basket.items.clear()
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

        self.result_label.config(text="\n".join(lines))
        self.app.say(f"Estimated {len(self.basket.items)} items.")
