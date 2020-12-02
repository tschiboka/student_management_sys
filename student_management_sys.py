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


import math
import csv
import tkinter as tk
from tkinter import messagebox

# ---------------------------- Get Students From CSV ---------------------------


def getCSVTable(path):
    with open(path, newline='') as csvfile:
        table = []
        buffer = csv.DictReader(csvfile)
        for row in buffer:
            table.append({
                "f_name": row["f_name"],
                "l_name": row["l_name"],
                "phone": row["phone"],
                "subjects": row["subjects"],
                "dob": row["dob"],
                "email": row["email"]})
    return table


students = getCSVTable("students.csv")

# ---------------------------------- App State ---------------------------------
# -       menu_open: the currently opened dialog eg: menu_open = "Search"      -
# -        update: elements that needs rerendering eg: update = ["list"]       -
# ------------------------------------------------------------------------------


state = {
    "menu_open": None,
    "update": [],
    "total_pages": 1,
    "curr_page": 1,
    "selected": [],
    "filtered": None,
}


# ---------------------------------- Constants ---------------------------------
WIN_WIDTH = 1200
WIN_HEIGHT = 450
TABLE_ROWS = 10
BUTTONS = ["Search", "Filter", "Sort", "New",
           "Modify", "Insert", "Delete", "Selection", "Exit"]
CAPTION_NAMES = ["First Name", "Last Name",
                 "Phone", "Subjects", "DOB", "Email", " "]
SUBJECTS = {
    "MA": "Maths",
    "CH": "Chemistry",
    "BI": "Biology",
    "IT": "IT",
    "PH": "Physics",
    "GE": "Geology",
    "EN": "English",
    "FL": "Foreign Language",
    "HI": "History",
    "PR": "Programming"}

# ----------------------- Color Palette and GUI constants ----------------------
PRIMARY_BG = "#1a1a1a"
PRIMARY_FG = "#c2c2c2"
HOVER_BTN_BG = "#333333"
HOVER_BTN_FG = "white"
ACTIVE_FG = "#4cc3f1"
SELECTED_BG = "#95EAC1"

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
            background="#252525",
            foreground=PRIMARY_FG,
            activebackground=HOVER_BTN_BG,
            activeforeground=ACTIVE_FG,
            borderwidth=1,
            relief=tk.RIDGE,
            font=MID_FONT,
            justify=tk.CENTER,
            anchor=tk.CENTER,
            cursor="hand2",
            ** kw)

        self.bind("<Enter>", lambda event: self.config(
            background=HOVER_BTN_BG,
            foreground="white")
        )

        self.bind("<Leave>", lambda event: self.config(
            background="#252525",
            foreground=PRIMARY_FG)
        )


# ---------------------------- Close Button Class -----------------------------


class CloseButton(tk.Button):
    def __init__(self, master, **kw):
        tk.Button.__init__(
            self,
            master=master,
            width=3,
            background="#252525",
            foreground="#FF1439",
            activebackground=HOVER_BTN_BG,
            activeforeground="#FF1439",
            borderwidth=1,
            relief=tk.RIDGE,
            font=14,
            text=u"\u00D7",
            justify=tk.CENTER,
            anchor=tk.CENTER,
            cursor="hand2",
            ** kw)

        self.bind("<Enter>", lambda event: self.config(
            background=HOVER_BTN_BG)
        )

        self.bind("<Leave>", lambda event: self.config(
            background="#252525")
        )


# ----------------------------- Dialog Input Class -----------------------------


class DialogInput(tk.Entry):
    def __init__(self, master, **kw):
        tk.Entry.__init__(
            self,
            master=master,
            background="#ddd",
            foreground=PRIMARY_BG,
            font=MID_FONT,
            relief=tk.FLAT,
            justify=tk.LEFT,
            ** kw)


# ----------------------------- Dialog Label Class -----------------------------


class DialogLabel(tk.Label):
    def __init__(self, master, **kw):
        tk.Label.__init__(
            self,
            master=master,
            background=PRIMARY_BG,
            foreground=PRIMARY_FG,
            font=MID_FONT,
            justify=tk.CENTER,
            anchor=tk.CENTER,
            ** kw)


# ------------------------------- Main Functions -------------------------------
# -                             Rendering Dialogs                              -
# ------------------------------------------------------------------------------


# ------------------------------- Search by Phone  -----------------------------
def submit_search(prop, value, dialog):
    global students
    input_value = value.get()

    searched_student = list(filter(
        lambda student: str.upper(student[prop]) == str.upper(input_value), students))
    if len(searched_student):
        students = searched_student
    else:
        messagebox.showinfo("Error", f"No Students with name\n{input_value}")

    state["update"].append("table")
    setDialog(None)
    dialog.destroy()

# ------------------------------ Search Dialog Box -----------------------------


def renderSearchDialog():
    # Search dialog container
    search_frame = tk.Frame(
        window,
        width=400,
        background=PRIMARY_BG)
    search_frame.place(bordermode=tk.INSIDE, x=150, y=0)
    search_frame.grid_columnconfigure(0, minsize=370)

    # Search dialog header
    search_header_frame = tk.Frame(
        search_frame, width=370, background=PRIMARY_BG)
    search_header_frame.grid(row=0, column=0)

    search_header_label = DialogLabel(
        search_header_frame, text="Search student by")
    search_header_label.grid(row=0, column=0, padx=10)

    search_close_btn = CloseButton(
        search_frame, command=lambda: search_frame.destroy())
    search_close_btn.grid(row=0, column=1)

    # Search dialog frame
    search_form_frame = tk.Frame(
        search_frame, width=400, background=PRIMARY_BG)
    search_form_frame.grid(row=1, column=0, padx=15, pady=5)
    search_form_frame.grid_columnconfigure(0, minsize=200)
    search_form_frame.grid_columnconfigure(1, minsize=200)

    phone_value = tk.StringVar()
    # Search dialog phone num input
    search_form_phone_input = DialogInput(
        search_form_frame, textvariable=phone_value)
    search_form_phone_input.grid(row=0, column=0)

    # Search dialog phone num label
    search_form_phone_btn = DialogButton(
        search_form_frame, text="Phone",
        command=lambda: submit_search("phone", phone_value, search_frame))
    search_form_phone_btn.grid(row=0, column=1, sticky=tk.NSEW, pady=5)

    email_value = tk.StringVar()
    # Search dialog email input
    search_form_email_input = DialogInput(
        search_form_frame, textvariable=email_value)
    search_form_email_input.grid(row=1, column=0, pady=5)

    # Search dialog email label
    search_form_email_btn = DialogButton(
        search_form_frame, text="Email",
        command=lambda: submit_search("email", email_value, search_frame)
    )
    search_form_email_btn.grid(row=1, column=1, sticky=tk.NSEW, pady=5)


# --------------------------- Filter Submit Function --------------------------
def submitFilter(filter_by_values, dialog):
    # Extracting Values from Filter Dialogbox
    f_name = filter_by_values[0].get()
    l_name = filter_by_values[1].get()
    day = filter_by_values[2].get()
    month = filter_by_values[3].get()
    year = filter_by_values[4].get()

    def getSubjects(i, val):
        abbrs = ["MA", "CH", "BI", "IT", "PH", "GE", "EN", "FL", "HI", "PR"]
        if val:
            return abbrs[i]

    subjects_inp = list(map(lambda el: el.get(), filter_by_values[5]))
    subjects = list(map(lambda x: getSubjects(
        x[0], x[1]), enumerate(subjects_inp)))
    subjects = list(filter(lambda x: x, subjects))

    # Validating inputs (basic validation)
    if day and (not day.isdigit() or int(day) > 31 or int(day) < 1 and float(day) % 1 != 0):
        messagebox.showinfo(
            "Input Error", "Day must be an integer between 1 and 31")

    if month and (not month.isdigit() or int(month) > 12 or int(month) < 1 and float(month) % 1 != 0):
        messagebox.showinfo(
            "Input Error", "Day must be an integer between 1 and 12")

    if year and (not year.isdigit() or int(year) > 99 or int(year) < 1 and float(year) % 1 != 0):
        messagebox.showinfo(
            "Input Error", "Year must be an integer between 1 and 12")

    # Filter students

    def filter_function(student):
        if f_name and str.upper(f_name) == str.upper(student["f_name"]):
            return True

        if l_name and str.upper(l_name) == str.upper(student["l_name"]):
            return True

        [s_day, s_month, s_year] = student["dob"].split(".")
        # if day, month and year is given it needs to match all
        if day and month and year:
            if (int(s_day) == int(day) and int(s_month) == int(month) and int(s_year) == int(year)):
                return True
        else:
            if day and int(s_day) == int(day):
                return True
            if month and int(s_month) == int(month):
                return True
            if year and int(s_year) == int(year):
                return True

        if len(subjects):
            student_subjects = [student["subjects"][i:i + 2]
                                for i in range(0, len(student["subjects"]), 2)]
            subject_matches = set(subjects) - \
                (set(subjects) - set(student_subjects))
            if len(subject_matches):
                return True
        return False

    global students
    oldlength = len(students)
    filtered_students = list(filter(filter_function, students))

    if len(filtered_students):
        students = filtered_students
        state["update"].append("table")
        state["update"].append("footer")
        state["selected"] = []
        state["filtered"] = [len(students), oldlength]
        print(state["filtered"])
        dialog.destroy()
    else:
        messagebox.showinfo(
            "Warning", "Filtering has no result!")

# ----------------------------- Filter Dialog Box -----------------------------


def renderFilterDialog():
    # Filter Dialog Container
    filter_frame = tk.Frame(
        window,
        width=400,
        background=PRIMARY_BG)
    filter_frame.place(bordermode=tk.INSIDE, x=150, y=27)
    filter_frame.grid_columnconfigure(0, minsize=400)

    # Filter Dialog Header
    filter_header_frame = tk.Frame(
        filter_frame, background=PRIMARY_BG)
    filter_header_frame.grid(row=0, column=0)

    filter_header_label = DialogLabel(
        filter_header_frame, text="Filter students by")
    filter_header_label.grid(row=0, column=0, padx=10)

    # Filter Dialog Close Button
    filter_close_btn = CloseButton(
        filter_frame, command=lambda: filter_frame.destroy())
    filter_close_btn.grid(row=0, column=1)

    # Filter Dialog Body
    filter_body_frame = tk.Frame(filter_frame, background=PRIMARY_BG)
    filter_body_frame.grid(row=1, column=0, sticky=tk.NSEW)
    filter_body_frame.grid_columnconfigure(0, minsize=400)

    # Filter Dialog First Name
    filter_f_name_frame = tk.Frame(
        filter_body_frame, background=PRIMARY_BG)
    filter_f_name_frame.grid(row=0, column=0)

    filter_f_name_label = tk.Label(
        filter_f_name_frame,
        text="First Name",
        background=PRIMARY_BG,
        foreground=PRIMARY_FG,
        width=28,
        justify=tk.LEFT,
        anchor=tk.W)
    filter_f_name_label.grid(row=0, column=0, sticky=tk.W)

    f_name_var = tk.StringVar()
    filter_f_name_input = DialogInput(
        filter_f_name_frame, width=20, textvariable=f_name_var)
    filter_f_name_input.grid(row=0, column=1, pady=2)

    # Filter Dialog Last Name
    filter_l_name_frame = tk.Frame(
        filter_body_frame, background=PRIMARY_BG)
    filter_l_name_frame.grid(row=1, column=0)

    filter_l_name_label = tk.Label(
        filter_l_name_frame,
        text="Last Name",
        background=PRIMARY_BG,
        foreground=PRIMARY_FG,
        width=28,
        justify=tk.LEFT,
        anchor=tk.W)
    filter_l_name_label.grid(row=0, column=0)

    l_name_var = tk.StringVar()
    filter_l_name_input = DialogInput(
        filter_l_name_frame, width=20, textvariable=l_name_var)
    filter_l_name_input.grid(row=0, column=1)

    # Filter Dialog Date of Birth
    filter_dob_frame = tk.Frame(
        filter_body_frame, background=PRIMARY_BG)
    filter_dob_frame.grid(row=2, column=0)

    filter_dob_label = tk.Label(
        filter_dob_frame,
        text="Date of Birth [dd,mm,yy]",
        background=PRIMARY_BG,
        foreground=PRIMARY_FG,
        width=28,
        justify=tk.LEFT,
        anchor=tk.W)
    filter_dob_label.grid(row=0, column=0, pady=2)

    # Filter Dialog DOB Day
    day_var = tk.StringVar()
    filter_day_input = DialogInput(
        filter_dob_frame, width=2, textvariable=day_var)
    filter_day_input.grid(row=0, column=1, padx=10, sticky=tk.E)

    # Filter Dialog DOB Month
    month_var = tk.StringVar()
    filter_month_input = DialogInput(
        filter_dob_frame, width=2, textvariable=month_var)
    filter_month_input.grid(row=0, column=2, padx=10, sticky=tk.E)

    # Filter Dialog  DOB Year
    year_var = tk.StringVar()
    filter_year_input = DialogInput(
        filter_dob_frame, width=2, textvariable=year_var)
    filter_year_input.grid(row=0, column=3, padx=10, sticky=tk.E)

    # Filter Dialog Subject Container
    filter_subject_frame = tk.Frame(
        filter_body_frame, background=PRIMARY_BG)
    filter_subject_frame.grid(row=3, column=0)

    check_vars = list(map(lambda x: tk.IntVar(), range(10)))
    # Filter Dialog Subjects
    for index, prop in enumerate(SUBJECTS):
        subject = SUBJECTS[prop]
        txt = f"{subject} [{prop}]"
        filter_subj_label = tk.Label(
            filter_subject_frame,
            text=txt,
            background=PRIMARY_BG,
            foreground=PRIMARY_FG,
            width=50,
            justify=tk.LEFT,
            anchor=tk.W)
        filter_subj_label.grid(row=index, column=0, sticky="W")

        filter_subj_btn = tk.Checkbutton(
            filter_subject_frame,
            variable=check_vars[index],
            background=PRIMARY_BG,
            foreground=ACTIVE_FG,
            activebackground=PRIMARY_BG)
        filter_subj_btn.grid(row=index, column=1, sticky="E")

    # Filter Dialog Submit Button
    filter_by_values = [f_name_var, l_name_var,
                        day_var, month_var, year_var, check_vars]
    filter_submit_btn = DialogButton(
        filter_body_frame,
        text="Filter",
        command=lambda: submitFilter(filter_by_values, filter_frame))
    filter_submit_btn.grid(row=4, column=0)


# ---------------------------- Selection Functions ----------------------------


def selectionMethod(method):
    if method == "all":
        updatedSelection = list(range(len(students)))
    if method == "none":
        updatedSelection = []
    if method == "inverse":
        all_elements = list(range(len(students)))
        updatedSelection = list(filter(
            lambda ind: ind not in state["selected"], all_elements))

    state["selected"] = updatedSelection
    state["update"].append("table")
    state["update"].append("footer")


# ---------------------------- Selection Dialog Box ---------------------------


def renderSelectionDialog():
    # Select Dialog Frame
    selection_frame = tk.Frame(window, width=400, background=PRIMARY_BG)
    selection_frame.place(bordermode=tk.INSIDE, x=150, y=195)
    selection_frame.propagate(False)

    # Select Header
    selection_header = tk.Frame(selection_frame)
    selection_header.grid(row=0, column=0)
    selection_header.grid_columnconfigure(0, minsize=400)

    # Select Header Label
    selection_header_label = DialogLabel(
        selection_header, text="Manage Selection")
    selection_header_label.grid(row=0, column=0, sticky=tk.NSEW)

    # Select Close Button
    selection_close_btn = CloseButton(
        selection_header,
        command=lambda: selection_frame.destroy())
    selection_close_btn.grid(row=0, column=1)

    # Select Options Frame
    selection_options_frame = tk.Frame(
        selection_frame,
        background=PRIMARY_BG,
        width=400,
        pady=10)
    selection_options_frame.grid(row=1, column=0)

    # Select All Button
    select_all_btn = DialogButton(
        selection_options_frame,
        text="Select All",
        width=14,
        command=lambda: selectionMethod("all"))
    select_all_btn.grid(row=0, column=0, padx=5)

    # Deselect All Button
    deselect_all_btn = DialogButton(
        selection_options_frame,
        text="Deselect All",
        width=14,
        command=lambda: selectionMethod("none"))
    deselect_all_btn.grid(row=0, column=1, padx=5)

    # Inverse Selection Button
    select_inverse_btn = DialogButton(
        selection_options_frame,
        text="Inverse Selection",
        width=14,
        command=lambda: selectionMethod("inverse"))
    select_inverse_btn.grid(row=0, column=2, padx=5)


def createDialog(dialog_name):
    if (dialog_name == "Search"):
        renderSearchDialog()

    if (dialog_name == "Filter"):
        renderFilterDialog()

    if (dialog_name == "Selection"):
        renderSelectionDialog()

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
        command=lambda new_state=btn_name: setDialog(new_state))
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
    cell_width = [35, 35, 20, 20, 20, 35, 7]

    for index, c_name in enumerate(CAPTION_NAMES):
        cap = tk.Label(
            caption,
            width=cell_width[index],
            text=c_name,
            anchor=tk.W,
            background=PRIMARY_BG,
            foreground=PRIMARY_FG)
        cap.grid(row=0, column=index)
        cap.grid_propagate(False)
        caption.grid_columnconfigure(index, weight=1)

# -------------------------------- Student List --------------------------------

    table_container.grid(row=1, column=0)
    table_container.grid_propagate(False)
    table_container.grid_columnconfigure(0, weight=0)
    table_container.grid_rowconfigure(0, weight=0)

    # divide list into chunks of 20 items
    chunks = [students[i:i + 20] for i in range(0, len(students), 20)]
    state["total_pages"] = math.ceil(len(students) / 20)

    # display current chunk of data
    list_to_display = chunks[state["curr_page"] - 1]

    if len(list_to_display):
        for row_index, student in enumerate(list_to_display):

            # Every secound row darker
            background = "#c7c7c7"
            if row_index % 2 == 0:
                background = "#e5e5e5"

            # Check if student is selected
            tab_index = (state["curr_page"] - 1) * 20 + row_index
            selected = True if tab_index in state["selected"] else False
            if selected:
                background = SELECTED_BG

            row = tk.Frame(
                table_container,
                width=1050,
                height=20,
                background=background)

            student_row = [student["f_name"], student["l_name"], student["phone"],
                           student["subjects"], student["dob"], student["email"], "X"]

            # Show Student Information Details Function

            def showStudentInfoDetails(index):
                student = students[index]
                f_name = "First Name    : " + student["f_name"]
                l_name = "Last Name     : " + student["l_name"]
                dob = "Date of Birth : " + student["dob"]
                phone = "Phone Number  : " + student["phone"]
                email = "Email         : " + student["email"]
                sub_s = student["subjects"]

                # split subject strings by 2-s
                subs_abbr = [sub_s[i: i + 2] for i in range(0, len(sub_s), 2)]

                # Assign string from abbriviation
                decor = "\n" + (" " * 16) + u"\u2022 "
                subs = list(map(lambda s: decor + SUBJECTS[s], subs_abbr))
                sub_text = "".join(subs)

                details = f"{f_name}\n{l_name}\n{dob}\n{phone}\n{email}\nSubjects      :{sub_text}"
                messagebox.showinfo("Student Details", details)

            # Iterate cells
            for index, entry in enumerate(student_row):
                # Student record
                if index < 6:
                    cell = tk.Label(
                        row,
                        width=cell_width[index],
                        background=background,
                        text=entry,
                        anchor=tk.W)
                    cell.bind("<Button 1>", lambda event,
                              ind=tab_index: showStudentInfoDetails(ind))
                else:
                    # Toggle Selection
                    def toggleSelect(index):
                        updated_selected = state["selected"]
                        if index in state["selected"]:
                            updated_selected.remove(index)
                        else:
                            updated_selected.append(index)

                        state["update"].append("table")
                        state["update"].append("footer")

                    # Selection Checkbox
                    checkbox_text = u"\u25A3" if selected else u"\u25A1"
                    checkbox_color = SELECTED_BG if selected else PRIMARY_FG

                    cell = tk.Label(
                        row,
                        text=checkbox_text,
                        foreground=checkbox_color,
                        width=cell_width[index],
                        background=PRIMARY_BG)

                    # Bind click event to label using closures
                    cell.bind("<Button-1>",
                              lambda event, ind=tab_index: toggleSelect(ind))

                cell.grid(row=0, column=index)
                cell.grid_propagate(False)
                row.grid_columnconfigure(index, weight=1)

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


createTable(table_container)


# --------------------------------- Footer -------------------------------------
footer_container = tk.Frame(
    display, height=32, width=1050, background=PRIMARY_BG)


def createFooter(footer_container):
    footer_container.grid(row=2, column=0)
    footer_container.grid_propagate(False)

# ------------------------------- Filter Info -----------------------------------
    filter_info_frame = tk.Frame(
        footer_container, width=440, height=32, background=PRIMARY_BG)
    filter_info_frame.grid(row=0, column=0)

# ----------------------------- Selection Info ----------------------------------
    selection_info_frame = tk.Frame(
        footer_container, width=440, height=32)
    selection_info_frame.grid(row=0, column=1)
    selection_info_frame.propagate(False)
    selection_info_frame.grid_columnconfigure(0, minsize=440)

    selected_num = len(state["selected"])
    selection_text = f"Selected: [ {selected_num} | {len(students)} ]"
    selection_label = tk.Label(
        selection_info_frame,
        text=selection_text,
        background=PRIMARY_BG,
        foreground=PRIMARY_FG,
        anchor=tk.W)
    selection_label.grid(row=0, column=0, sticky=tk.NSEW)
    selection_label.propagate(False)


# ----------------------------- Pagination Info ---------------------------------


    def paginate(direction):
        if direction == "+" and state["curr_page"] < state["total_pages"]:
            state["curr_page"] = state["curr_page"] + 1

        if direction == "-" and state["curr_page"] > 1:
            state["curr_page"] = state["curr_page"] - 1

        state["update"].append("table")
        state["update"].append("footer")
        footer_container.destroy()

    # Pagination Control
    pagination_frame = tk.Frame(
        footer_container, width=160, height=32, background=PRIMARY_BG)
    pagination_frame.grid(row=0, column=2)
    pagination_frame.grid_propagate(False)

    pagination_label1 = tk.Label(
        pagination_frame, text="Page: ", width=5, background=PRIMARY_BG, foreground=PRIMARY_FG)
    pagination_label1.grid(row=0, column=0)

    pagination_backwards_btn = DialogButton(
        pagination_frame, text="<", width=2, command=lambda: paginate("-"))
    pagination_backwards_btn.grid(row=0, column=1)

    pagination_label2 = tk.Label(
        pagination_frame, text=state["curr_page"], width=3, background=PRIMARY_BG, foreground=ACTIVE_FG)
    pagination_label2.grid(row=0, column=2)

    pagination_forward_btn = DialogButton(
        pagination_frame, text=">", width=2, command=lambda: paginate("+"))
    pagination_forward_btn.grid(row=0, column=3)

    pagination_label3 = tk.Label(
        pagination_frame, text=" of " + str(state["total_pages"]), width=6, background=PRIMARY_BG, foreground=PRIMARY_FG)
    pagination_label3.grid(row=0, column=4)


createFooter(footer_container)

# State Listener


def listeningState():
    if "table" in state["update"]:
        state["update"].remove("table")
        table_container.destroy()
        updated_table_container = tk.Frame(display, height=400, width=1050)
        createTable(updated_table_container)

    if "footer" in state["update"]:
        state["update"].remove("footer")
        footer_container.destroy()
        updated_footer_containter = tk.Frame(
            display, height=32, width=1050, background=PRIMARY_BG)
        createFooter(updated_footer_containter)

    if (state["menu_open"]):
        createDialog(state["menu_open"])

    window.after(100, listeningState)


listeningState()


def setDialog(new_state):
    state["menu_open"] = new_state
    state["update"].append("table")


window.mainloop()
