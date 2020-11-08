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

# App State
app_state = {

}


# App Constants
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
# Color Palette and GUI Constants
PRIMARY_BG = "#1a1a1a"
PRIMARY_FG = "#c2c2c2"
HOVER_BTN_BG = "#333333"
HOVER_BTN_FG = "white"
ACTIVE_FG = "#4cc3f1"
LRG_FONT = 12
SML_FONT = 9


# GUI
window = tk.Tk()
window.title("Student Management System")
# Center App
screen_width = window.winfo_screenwidth()
screen_height = window.winfo_screenheight()
window.geometry(
    f"{WIN_WIDTH}x{WIN_HEIGHT}+{(screen_width // 2) - (WIN_WIDTH // 2)}+{(screen_height // 2) - (WIN_HEIGHT // 2)}")
window.resizable(False, False)

# MENU
# ttk themed styles have inconsistent look on different OSs, therefore style attr.s are declared inline
sidebar = tk.Frame(window, bg=PRIMARY_BG, height=WIN_HEIGHT, width=150)
sidebar.grid(row=0, column=0)
sidebar.grid_propagate(False)
sidebar.grid_columnconfigure(0, weight=1)


# BUTTONS
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
            relief="flat",
            font=LRG_FONT,
            **kw)
        self.bind("<Enter>", lambda event: self.config(
            background=HOVER_BTN_BG,
            foreground=ACTIVE_FG)
        )
        self.bind("<Leave>", lambda event: self.config(
            background=PRIMARY_BG,
            foreground=PRIMARY_FG)
        )


for index, btn_name in enumerate(BUTTONS[:-1]):
    btn = MainButton(sidebar, text=btn_name)
    btn.grid(row=index, column=0)

exit_btn = MainButton(sidebar, text=BUTTONS[-1])
exit_btn.grid(row=len(BUTTONS), column=0, sticky="s")
sidebar.grid_rowconfigure(len(BUTTONS), weight=1)


# DATA DISPLAY
display = tk.Frame(
    window,
    height=WIN_HEIGHT,
    width=1050,
    background=PRIMARY_FG)
display.grid(row=0, column=1)
display.grid_propagate(False)

# CAPTURE
capture = tk.Frame(display, height=20, width=1050)
capture.grid(row=0, column=0)
capture.grid_propagate(False)

for index, c_name in enumerate(CAPTION_NAMES):
    cap = tk.Label(
        capture,
        text=c_name,
        background="#bbbbbb",
        relief="ridge",
        borderwidth=1,
        width=30)
    cap.grid(row=0, column=index)
    cap.grid_propagate(False)
    capture.grid_columnconfigure(index, weight=1)

# TABLE
table_container = tk.Frame(display, height=400, width=1050)
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

# FOOTER
footer = tk.Frame(display, height=32, width=1050, bg=PRIMARY_BG)
footer.grid(row=2, column=0)
footer.grid_propagate(False)


window.mainloop()
