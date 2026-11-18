"""Colours for the BazaarDor window: one ttk style setup shared by every screen."""

from tkinter import ttk

# All colours in one dictionary, so a colour is changed in one place
COLORS = {
    "background": "#F3F7F1",  # light leafy green page
    "text": "#1E2B22",
    "green": "#1F7A45",  # buttons, headings, selected tab
    "dark_green": "#145A32",  # button and heading when the mouse is on it
    "turmeric": "#F4B400",  # selected table row
    "soft_yellow": "#FFF1C2",  # tabs that are not selected
    "white": "#FFFFFF",
}


def apply_theme(root):
    """Use the 'clam' theme (it accepts colours on every platform) and colour each widget type."""
    c = COLORS
    style = ttk.Style(root)
    style.theme_use("clam")
    root.configure(background=c["background"])

    style.configure(".", background=c["background"], foreground=c["text"])
    style.configure("TFrame", background=c["background"])
    style.configure("TLabel", background=c["background"], foreground=c["text"])
    style.configure("TLabelframe", background=c["background"], bordercolor=c["green"])
    style.configure("TLabelframe.Label", background=c["background"], foreground=c["green"],
                    font=("TkDefaultFont", 12, "bold"))

    style.configure("TButton", background=c["green"], foreground=c["white"],
                    bordercolor=c["dark_green"], focuscolor=c["turmeric"], padding=(10, 3))
    style.map("TButton", background=[("pressed", c["dark_green"]), ("active", c["dark_green"])])

    style.configure("TNotebook", background=c["background"], borderwidth=0)
    style.configure("TNotebook.Tab", background=c["soft_yellow"], foreground=c["text"], padding=(14, 4))
    style.map("TNotebook.Tab", background=[("selected", c["green"])], foreground=[("selected", c["white"])])

    style.configure("Treeview", background=c["white"], fieldbackground=c["white"],
                    foreground=c["text"], rowheight=20)
    style.map("Treeview", background=[("selected", c["turmeric"])], foreground=[("selected", c["text"])])
    style.configure("Treeview.Heading", background=c["green"], foreground=c["white"],
                    font=("TkDefaultFont", 11, "bold"))
    style.map("Treeview.Heading", background=[("active", c["dark_green"])])

    style.configure("TEntry", fieldbackground=c["white"], foreground=c["text"], insertcolor=c["text"])
    style.configure("TCombobox", fieldbackground=c["white"], foreground=c["text"], arrowcolor=c["green"])
    style.map("TCombobox", fieldbackground=[("readonly", c["white"])], foreground=[("readonly", c["text"])])
    # the drop-down list of a Combobox is a plain Tk listbox, coloured through the option database
    root.option_add("*TCombobox*Listbox.background", c["white"])
    root.option_add("*TCombobox*Listbox.foreground", c["text"])
    root.option_add("*TCombobox*Listbox.selectBackground", c["turmeric"])
    root.option_add("*TCombobox*Listbox.selectForeground", c["text"])
