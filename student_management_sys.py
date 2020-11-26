# ------------------------- Student Management system --------------------------
# -                        Developed by: Tivadar Debnar                        -
# -                                                                            -
# -         Implementing Event driven paradigm; by listening app state.        -
# -           Function Paradigm: events calling main functionalities           -
# -             Object Oriented Paradigm: creating MainButton class            -
# ------------------------------------------------------------------------------


# ------------------------------ Imports and State -----------------------------
# -                                Defaults state                              -
# -                          Defining global constants                         -
# ------------------------------------------------------------------------------


import tkinter as tk

# Student List
students = [
    ["Susan", "Taylor", "07474999335", ["MA", "CH", "GE", "EN"],
        "09-12-84", "taylor.susan@gmail.com"],
    ["Jim", "Costner", "07472889335", ["BI", "PH", "IT", "EN"],
        "08-06-72", "j.costner@gmail.com"],
    ["Susan", "Taylor", "07474999335", ["MA", "CH", "GE", "EN"],
     "09-12-84", "taylor.susan@gmail.com"],
    ["Jim", "Costner", "07472889335", ["BI", "PH", "IT", "EN"],
        "08-06-72", "j.costner@gmail.com"],
    ["Susan", "Taylor", "07474999335", ["MA", "CH", "GE", "EN"],
        "09-12-84", "taylor.susan@gmail.com"],
    ["Jim", "Costner", "07472889335", ["BI", "PH", "IT", "EN"],
        "08-06-72", "j.costner@gmail.com"],
    ["Susan", "Taylor", "07474999335", ["MA", "CH", "GE", "EN"],
        "09-12-84", "taylor.susan@gmail.com"],
    ["Jim", "Costner", "07472889335", ["BI", "PH", "IT", "EN"],
        "08-06-72", "j.costner@gmail.com"],
    ["Susan", "Taylor", "07474999335", ["MA", "CH", "GE", "EN"],
        "09-12-84", "taylor.susan@gmail.com"],
    ["Jim", "Costner", "07472889335", ["BI", "PH", "IT", "EN"],
        "08-06-72", "j.costner@gmail.com"],
    ["Susan", "Taylor", "07474999335", ["MA", "CH", "GE", "EN"],
        "09-12-84", "taylor.susan@gmail.com"],
    ["Jim", "Costner", "07472889335", ["BI", "PH", "IT", "EN"],
        "08-06-72", "j.costner@gmail.com"],
    ["Susan", "Taylor", "07474999335", ["MA", "CH", "GE", "EN"],
        "09-12-84", "taylor.susan@gmail.com"],
    ["Jim", "Costner", "07472889335", ["BI", "PH", "IT", "EN"],
        "08-06-72", "j.costner@gmail.com"],
    ["Susan", "Taylor", "07474999335", ["MA", "CH", "GE", "EN"],
        "09-12-84", "taylor.susan@gmail.com"],
    ["Jim", "Costner", "07472889335", ["BI", "PH", "IT", "EN"],
        "08-06-72", "j.costner@gmail.com"],
    ["Susan", "Taylor", "07474999335", ["MA", "CH", "GE", "EN"],
        "09-12-84", "taylor.susan@gmail.com"],
    ["Jim", "Costner", "07472889335", ["BI", "PH", "IT", "EN"],
        "08-06-72", "j.costner@gmail.com"],
    ["Susan", "Taylor", "07474999335", ["MA", "CH", "GE", "EN"],
        "09-12-84", "taylor.susan@gmail.com"],
    ["Jim", "Costner", "07472889335", ["BI", "PH", "IT", "EN"],
        "08-06-72", "j.costner@gmail.com"],
]

# ---------------------------------- App State ---------------------------------
# -       menu_open: the currently opened dialog eg: menu_open = "Search"      -
# -        update: elements that needs rerendering eg: update = ["list"]       -
# ------------------------------------------------------------------------------


state = {
    "menu_open": None,
    "update": []
}

# ---------------------------------- Constants ---------------------------------
WIN_WIDTH = 1200
WIN_HEIGHT = 450
TABLE_ROWS = 10
BUTTONS = ["Search", "Filter", "Sort", "New",
           "Modify", "Insert", "Delete", "Exit"]
CAPTION_NAMES = ["First Name", "Second Name",
                 "Phone", "Subjects", "DOB", "Email"]
SUBJECTS = {
    "MA": "Maths",
    "CH": "Chemistry",
    "BI": "Biology",
    "IT": "IT",
    "PH": "Physics",
    "GE": "Geology",
    "EN": "English",
    "FL": "Foreign Language",
    "HI": "History"}

# ----------------------- Color Palette and GUI constants ----------------------
PRIMARY_BG = "#1a1a1a"
PRIMARY_FG = "#c2c2c2"
HOVER_BTN_BG = "#333333"
HOVER_BTN_FG = "white"
ACTIVE_FG = "#4cc3f1"

LRG_FONT = 12
MID_FONT = 10
SML_FONT = 9

# --------------------------- Component Declarations ----------------------------
# -                  for custom widget settings like hover                     -
# -                as Tkinter has no such built in functionality               -
# ------------------------------------------------------------------------------

# ---------------------------- Main Button Class -------------------------------


class MainButton(tk.Button):
    def __init__(self, master, **kw):
        tk.Button.__init__(
            self,
            master=master,
            background=PRIMARY_BG,
            foreground=PRIMARY_FG,
            width=100,
            borderwidth=0,
            activebackground=HOVER_BTN_BG,
            activeforeground=ACTIVE_FG,
            relief=tk.FLAT,
            font=LRG_FONT,
            cursor="hand2",
            ** kw)

        self.bind("<Enter>", lambda event: self.config(
            background=HOVER_BTN_BG,
            foreground=ACTIVE_FG)
        )

        self.bind("<Leave>", lambda event: self.config(
            background=PRIMARY_BG,
            foreground=PRIMARY_FG)
        )

# ---------------------------- Dialog Button Class -----------------------------


class DialogButton(tk.Button):
    def __init__(self, master, **kw):
        tk.Button.__init__(
            self,
            master=master,
            background=PRIMARY_BG,
            foreground=PRIMARY_FG,
            activebackground=HOVER_BTN_BG,
            activeforeground=ACTIVE_FG,
            borderwidth=2,
            relief=tk.RIDGE,
            highlightbackground="red",
            highlightcolor="red",
            font=MID_FONT,
            cursor="hand2",
            ** kw)

        self.bind("<Enter>", lambda event: self.config(
            background=HOVER_BTN_BG,
            foreground="white")
        )

        self.bind("<Leave>", lambda event: self.config(
            background=PRIMARY_BG,
            foreground=PRIMARY_FG)
        )


# ------------------------------- Main Functions -------------------------------
# -                             Rendering Dialogs                              -
# ------------------------------------------------------------------------------


def createDialog(dialog_name):
    print(dialog_name)
    if (dialog_name == "Search"):
        # Search dialog container
        search_frame = tk.Frame(
            window,
            width=400,
            background=PRIMARY_BG)
        search_frame.place(
            bordermode=tk.INSIDE,
            x=150,
            y=0)
        search_frame.grid_columnconfigure(0, minsize=400)

        # Search dialog header
        search_header_label = tk.Label(
            search_frame,
            background=PRIMARY_BG,
            foreground=PRIMARY_FG,
            text="Search student by",
            font=MID_FONT,
            justify=tk.CENTER,
            anchor=tk.CENTER)
        search_header_label.grid(row=0, column=0)

        # Search dialog frame
        search_form_frame = tk.Frame(
            search_frame,
            width=400,
            background=PRIMARY_BG)
        search_form_frame.grid(row=1, column=0)
        search_form_frame.grid_columnconfigure(0, minsize=200)
        search_form_frame.grid_columnconfigure(1, minsize=200)

        # Search dialog phone num input
        search_form_phone_input = tk.Entry(
            search_form_frame,
            background="#bbbbbb",
            foreground=PRIMARY_BG,
            font=MID_FONT,
            relief=tk.FLAT,
            justify=tk.CENTER)
        search_form_phone_input.grid(row=0, column=0)

        # Serach dialog phone num label
        search_form_phone_btn = DialogButton(
            search_form_frame,
            text="Phone",
            justify=tk.CENTER,
            anchor=tk.CENTER)
        search_form_phone_btn.grid(row=0, column=1, sticky=tk.NSEW)

        # Serach dialog email input
        search_form_email_input = tk.Entry(
            search_form_frame,
            background="#bbbbbb",
            foreground=PRIMARY_BG,
            font=MID_FONT,
            relief=tk.FLAT,
            justify=tk.CENTER)
        search_form_email_input.grid(row=1, column=0)

        # Serach dialog email label
        search_form_email_btn = DialogButton(
            search_form_frame,
            text="Email",
            justify=tk.CENTER,
            anchor=tk.CENTER)
        search_form_email_btn.grid(row=1, column=1, sticky=tk.NSEW)

    state["menu_open"] = None  # ---- Reset state so listener does not re-paint


# ------------------------------ RENDER GUI WINDOW -----------------------------
# -                   Create mainloop, render main menu and table              -
# -                             Invoke stateListener                           -
# ------------------------------------------------------------------------------


window = tk.Tk()
window.title("Student Management System")
# Center App
screen_width = window.winfo_screenwidth()
screen_height = window.winfo_screenheight()
window.geometry(
    f"{WIN_WIDTH}x{WIN_HEIGHT}+{(screen_width // 2) - (WIN_WIDTH // 2)}+{(screen_height // 2) - (WIN_HEIGHT // 2)}")
# ------------ will not develop responsive design
window.resizable(False, False)


# ----------------------------------- Sidebar ----------------------------------
# -            ttk themed styles have inconsistent look on different OSs       -
# -                   therefore style attr-s are declared inline               -
# ------------------------------------------------------------------------------


sidebar = tk.Frame(window, bg=PRIMARY_BG, height=WIN_HEIGHT, width=150)
sidebar.grid(row=0, column=0)
sidebar.grid_propagate(False)
sidebar.grid_columnconfigure(0, weight=1)


# -------------------------------- Main Buttons --------------------------------

for index, btn_name in enumerate(BUTTONS[:-1]):
    btn = MainButton(
        sidebar,
        text=btn_name,
        command=lambda new_state=btn_name: setState(new_state))
    btn.grid(row=index, column=0)

# -------------------------------- Exit Button ---------------------------------

exit_btn = MainButton(sidebar, text=BUTTONS[-1], command=window.destroy)
exit_btn.grid(row=len(BUTTONS), column=0, sticky="s")

sidebar.grid_rowconfigure(len(BUTTONS), weight=1)


# -------------------------------- Data Display --------------------------------

display = tk.Frame(
    window,
    height=WIN_HEIGHT,
    width=1050,
    background=PRIMARY_FG)
display.grid(row=0, column=1)
display.grid_propagate(False)

# ---------------------------------- Caption -----------------------------------

caption = tk.Frame(display, height=20, width=1050)
caption.grid(row=0, column=0)
caption.grid_propagate(False)

table_container = tk.Frame(display, height=400, width=1050)


# -------------------------------- Table Creation ------------------------------
# -                   Student table has its own create function.               -
# -       If student data is modified, table is destroyed and recreated        -
# ------------------------------------------------------------------------------

def createTable(table_container):
    for index, c_name in enumerate(CAPTION_NAMES):
        cap = tk.Label(
            caption,
            text=c_name,
            background="#bbbbbb",
            relief="ridge",
            borderwidth=1,
            width=30)
        cap.grid(row=0, column=index)
        cap.grid_propagate(False)
        caption.grid_columnconfigure(index, weight=1)

# -------------------------------- Student List --------------------------------

    table_container.grid(row=1, column=0)
    table_container.grid_propagate(False)
    table_container.grid_columnconfigure(0, weight=0)
    table_container.grid_rowconfigure(0, weight=0)

    list_to_display = students

    if len(list_to_display):
        for row_index, student in enumerate(students):
            row = tk.Frame(table_container, width=1050, height=20)

            for index, entry in enumerate(student):
                col = tk.Label(
                    row,
                    text=entry,
                    relief="sunken",
                    borderwidth=1,
                    width=30)
                col.grid(row=0, column=index)
                col.grid_propagate(False)
                row.grid_columnconfigure(index, weight=1)

            row.grid(row=row_index, column=0)
            row.grid_propagate(False)
            table_container.grid_columnconfigure(index, weight=1)
    else:
        no_item = tk.Label(
            table_container,
            text="No Item Found!",
            width=150,
            height=30)
        no_item.grid(row=0, column=0)
        no_item.grid_propagate(False)
        table_container.grid_columnconfigure(0, weight=1)
        table_container.grid_rowconfigure(0, weight=1)

    def listeningState():
        if "table" in state["update"]:
            state["update"].remove("table")
            table_container.destroy()
            updated_table_container = tk.Frame(display, height=400, width=1050)
            createTable(updated_table_container)

        if (state["menu_open"]):
            createDialog(state["menu_open"])

        window.after(100, listeningState)

    listeningState()


createTable(table_container)


# --------------------------------- Footer -------------------------------------
footer = tk.Frame(display, height=32, width=1050, bg=PRIMARY_BG)
footer.grid(row=2, column=0)
footer.grid_propagate(False)


def setState(new_state):
    state["menu_open"] = new_state
    state["update"].append("table")


window.mainloop()
