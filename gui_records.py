import tkinter as tk
from tkinter import messagebox, ttk

from models import PriceRecord, UNITS, CATEGORIES
from storage import save_records
from validation import validate_text, validate_price, validate_date, validate_choice


class RecordsTab:
    def __init__(self, app, notebook):
        self.app = app
        self.frame = ttk.Frame(notebook, padding=12)
        notebook.add(self.frame, text="Price Records")

        self.vars = {
            "record_id": tk.StringVar(),
            "item": tk.StringVar(),
            "bazaar": tk.StringVar(),
            "price": tk.StringVar(),
            "unit": tk.StringVar(value=UNITS[0]),
            "category": tk.StringVar(value=CATEGORIES[0]),
            "date": tk.StringVar(),
        }
        self.search_var = tk.StringVar()

        self._build_form()
        self._build_table()
        self.refresh_table()

    def _build_form(self):
        form = ttk.LabelFrame(self.frame, text="Price record details", padding=10)
        form.pack(fill="x")

        fields = [
            ("Record ID", "record_id", "entry"),
            ("Item", "item", "entry"),
            ("Bazaar", "bazaar", "entry"),
            ("Price (Tk)", "price", "entry"),
            ("Unit", "unit", "unit"),
            ("Category", "category", "category"),
            ("Date (YYYY-MM-DD)", "date", "entry"),
        ]
        for index, (label, key, kind) in enumerate(fields):
            row, col = divmod(index, 4)
            cell = ttk.Frame(form)
            cell.grid(row=row, column=col, sticky="ew", padx=5, pady=5)
            ttk.Label(cell, text=label).pack(anchor="w")
            if kind == "unit":
                widget = ttk.Combobox(cell, textvariable=self.vars[key], values=UNITS,
                                      state="readonly", width=18)
            elif kind == "category":
                widget = ttk.Combobox(cell, textvariable=self.vars[key], values=CATEGORIES,
                                      state="readonly", width=18)
            else:
                widget = ttk.Entry(cell, textvariable=self.vars[key], width=21)
            widget.pack(fill="x")
            cell.columnconfigure(0, weight=1)
            form.columnconfigure(col, weight=1)

        actions = ttk.Frame(self.frame)
        actions.pack(fill="x", pady=(8, 10))
        ttk.Button(actions, text="Add Record", command=self.add_record).pack(side="left", padx=(0, 6))
        ttk.Button(actions, text="Update Selected", command=self.update_record).pack(side="left", padx=6)
        ttk.Button(actions, text="Delete Selected", command=self.delete_record).pack(side="left", padx=6)
        ttk.Button(actions, text="Clear Form", command=self.clear_form).pack(side="left", padx=6)

    def _build_table(self):
        search = ttk.Frame(self.frame)
        search.pack(fill="x", pady=(0, 8))
        ttk.Label(search, text="Search item or bazaar:").pack(side="left")
        search_entry = ttk.Entry(search, textvariable=self.search_var, width=32)
        search_entry.pack(side="left", padx=8)
        search_entry.bind("<Return>", lambda _event: self.search_records())
        ttk.Button(search, text="Search", command=self.search_records).pack(side="left")
        ttk.Button(search, text="Show All", command=self.refresh_table).pack(side="left", padx=6)

        columns = ("record_id", "item", "bazaar", "price", "unit", "category", "date")
        headings = {
            "record_id": "Record ID", "item": "Item", "bazaar": "Bazaar",
            "price": "Price (Tk)", "unit": "Unit", "category": "Category", "date": "Date",
        }
        widths = {"record_id": 95, "item": 150, "bazaar": 150, "price": 100,
                  "unit": 75, "category": 110, "date": 110}

        table_frame = ttk.Frame(self.frame)
        table_frame.pack(fill="both", expand=True)
        self.table = ttk.Treeview(table_frame, columns=columns, show="headings", height=14)
        for column in columns:
            self.table.heading(column, text=headings[column])
            self.table.column(column, width=widths[column], anchor="w")
        y_scroll = ttk.Scrollbar(table_frame, orient="vertical", command=self.table.yview)
        x_scroll = ttk.Scrollbar(table_frame, orient="horizontal", command=self.table.xview)
        self.table.configure(yscrollcommand=y_scroll.set, xscrollcommand=x_scroll.set)
        self.table.grid(row=0, column=0, sticky="nsew")
        y_scroll.grid(row=0, column=1, sticky="ns")
        x_scroll.grid(row=1, column=0, sticky="ew")
        table_frame.rowconfigure(0, weight=1)
        table_frame.columnconfigure(0, weight=1)
        self.table.bind("<<TreeviewSelect>>", self._load_selected_into_form)

    def _form_values(self):
        return {key: variable.get().strip() for key, variable in self.vars.items()}

    def _selected_record_id(self):
        selected = self.table.selection()
        if not selected:
            messagebox.showinfo("Select a record", "Please select a record from the table first.")
            return None
        return self.table.item(selected[0], "values")[0]

    def _save_and_refresh(self, message):
        if not save_records(self.app.manager.records, "data/prices.json"):
            messagebox.showerror("Save failed", "The record changed in memory, but could not be saved to data/prices.json.")
            return
        self.refresh_table()
        self.app.say(message)

    def add_record(self):
        values = self._form_values()
        try:
            record = PriceRecord(
                validate_text(values["record_id"], "Record ID"),
                validate_text(values["item"], "Item"),
                validate_text(values["bazaar"], "Bazaar"),
                validate_price(values["price"]),
                validate_choice(values["unit"], UNITS, "Unit"),
                validate_choice(values["category"], CATEGORIES, "Category"),
                validate_date(values["date"]),
            )
            self.app.manager.add_record(record)
        except (ValueError, TypeError) as error:
            messagebox.showerror("Invalid record", str(error))
            return
        self._save_and_refresh(f"Added price record {record.record_id}.")
        self.clear_form()

    def update_record(self):
        record_id = self._selected_record_id()
        if record_id is None:
            return
        values = self._form_values()
        try:
            updated = self.app.manager.update_record(
                record_id,
                item=values["item"], bazaar=values["bazaar"],
                price=values["price"], unit=values["unit"],
                category=values["category"], date=values["date"],
            )
        except (ValueError, TypeError) as error:
            messagebox.showerror("Invalid update", str(error))
            return
        if updated is None:
            messagebox.showerror("Not found", f"Record {record_id} no longer exists.")
            return
        self._save_and_refresh(f"Updated price record {record_id}.")

    def delete_record(self):
        record_id = self._selected_record_id()
        if record_id is None:
            return
        if not messagebox.askyesno("Confirm delete", f"Delete record {record_id}?"):
            return
        deleted = self.app.manager.delete_record(record_id)
        if deleted is None:
            messagebox.showerror("Not found", f"Record {record_id} no longer exists.")
            return
        self._save_and_refresh(f"Deleted price record {record_id}.")
        self.clear_form()

    def search_records(self):
        keyword = self.search_var.get().strip()
        records = self.app.manager.search_records(keyword) if keyword else self.app.manager.records
        self._fill_table(records)
        self.app.say(f"Found {len(records)} matching price records.")

    def refresh_table(self):
        self.search_var.set("")
        self._fill_table(self.app.manager.records)

    def _fill_table(self, records):
        for row in self.table.get_children():
            self.table.delete(row)
        for record in records:
            self.table.insert("", "end", values=(
                record.record_id, record.item, record.bazaar,
                f"{record.price:.2f}", record.unit, record.category, record.date,
            ))

    def _load_selected_into_form(self, _event=None):
        selected = self.table.selection()
        if not selected:
            return
        values = self.table.item(selected[0], "values")
        for key, value in zip(self.vars, values):
            self.vars[key].set(value)

    def clear_form(self):
        for key, variable in self.vars.items():
            variable.set(UNITS[0] if key == "unit" else CATEGORIES[0] if key == "category" else "")
        self.table.selection_remove(self.table.selection())
