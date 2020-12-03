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


import re
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


def reloadTable():
    global students
    students = getCSVTable("students.csv")
    state["update"].append("table")
    state["update"].append("footer")
    state["filtered"] = None
    state["selected"] = []
    state["sortedby"] = False
    state["sort_asc"] = True


def tableIntoCSVFile(path):
    with open(path, 'w', newline='') as csvfile:
        fieldnames = ['f_name', 'l_name', "phone", "subjects", "dob", "email"]
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()

        for student in students:
            writer.writerow(student)


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
    "sortedby": False,
    "sort_asc": True,
}


# ---------------------------------- Constants ---------------------------------
WIN_WIDTH = 1200
WIN_HEIGHT = 450
TABLE_ROWS = 10
BUTTONS = ["New", "Modify", "Delete", "Filter",
           "Search", "Sort",  "Selection", "Exit"]
CAPTION_NAMES = ["First Name", "Last Name",
                 "Phone", "Subjects", "DOB", "Email", " "]
SUBJECTS = {
    "BI": "Biology",
    "CH": "Chemistry",
    "EN": "English",
    "FL": "Foreign Language",
    "GE": "Geography",
    "HI": "History",
    "IT": "IT",
    "MA": "Maths",
    "PH": "Physics",
    "PR": "Programming"}

# ----------------------- Color Palette and GUI constants ----------------------
PRIMARY_BG = "#1a1a1a"
PRIMARY_FG = "#c2c2c2"
HOVER_BTN_BG = "#333333"
HOVER_BTN_FG = "white"
ACTIVE_FG = "#4cc3f1"
ROW_BG_LIGHT = "#2a2a2a"
ROW_BG_DARK = "#333"
SELECTED_BG = "#95EAC1"
MONOSPACE = ("Courier", 9)

LRG_FONT = 12
MID_FONT = 10
SML_FONT = 9

# -------------------------------- Global Frames -------------------------------
new_frame = None
modify_frame = None
delete_frame = None
filter_frame = None
search_frame = None
sort_frame = None
selection_frame = None

# --------------------------- Component Declarations ---------------------------
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
            font=(None, MID_FONT),
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
            font=(None, LRG_FONT),
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
            font=(None, MID_FONT),
            relief=tk.FLAT,
            ** kw)


# ----------------------------- Dialog Label Class -----------------------------


class DialogLabel(tk.Label):
    def __init__(self, master, **kw):
        tk.Label.__init__(
            self,
            master=master,
            background=PRIMARY_BG,
            foreground=PRIMARY_FG,
            font=(None, MID_FONT),
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
    global search_frame
    # Search dialog container
    search_frame = tk.Frame(
        window,
        width=400,
        background=PRIMARY_BG)
    search_frame.place(bordermode=tk.INSIDE, x=150, y=111)
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
        abbrs = ["BI", "CH", "EN", "FL", "GE", "HI", "IT", "MA", "PH", "PR"]
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
    global filter_frame
    # Filter Dialog Container
    filter_frame = tk.Frame(
        window,
        width=400,
        background=PRIMARY_BG)
    filter_frame.place(bordermode=tk.INSIDE, x=150, y=0)
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
        filter_subj_label.grid(row=index, column=0, sticky=tk.W)

        filter_subj_btn = tk.Checkbutton(
            filter_subject_frame,
            variable=check_vars[index],
            background=PRIMARY_BG,
            foreground=ACTIVE_FG,
            activebackground=PRIMARY_BG)
        filter_subj_btn.grid(row=index, column=1, sticky=tk.E)

    # Filter Dialog Submit Button
    filter_by_values = [f_name_var, l_name_var,
                        day_var, month_var, year_var, check_vars]
    filter_submit_btn = DialogButton(
        filter_body_frame,
        text="Filter",
        command=lambda: submitFilter(filter_by_values, filter_frame))
    filter_submit_btn.grid(row=4, column=0)


# ---------------------------- Sort Method Function ---------------------------
def sortMethod(method, dialog):
    global students
    if method == "f_name" or method == "l_name":
        state["sortedby"] = method
        state["sort_asc"] = True
        sorted_students = sorted(students, key=lambda x: x[method])

    if method == "reverse":
        sorted_students = students[::-1]
        state["sort_asc"] = False if state["sort_asc"] == True else True

    print(state["sortedby"], state["sort_asc"])
    students = sorted_students
    state["update"].append("table")
    state["update"].append("footer")
    state["selected"] = []

    dialog.destroy()


# ------------------------------ Sort Dialog Box ------------------------------
def renderSortDialog():
    global sort_frame
    # Sort Dialog Frame
    sort_frame = tk.Frame(window, width=400, background=PRIMARY_BG)
    sort_frame.place(bordermode=tk.INSIDE, x=150, y=138)
    sort_frame.propagate(False)

    # Sort Header
    sort_header = tk.Frame(sort_frame)
    sort_header.grid(row=0, column=0)
    sort_header.grid_columnconfigure(0, minsize=400)

    # Sort Header Label
    sort_header_label = DialogLabel(
        sort_header, text="Sort Students by")
    sort_header_label.grid(row=0, column=0, sticky=tk.NSEW)

    # Sort Close Button
    sort_close_btn = CloseButton(
        sort_header,
        command=lambda: sort_frame.destroy())
    sort_close_btn.grid(row=0, column=1)

    # Sort Options Frame
    sort_options_frame = tk.Frame(
        sort_frame,
        background=PRIMARY_BG,
        width=400,
        pady=10)
    sort_options_frame.grid(row=1, column=0)

    # Sort by First Name Button
    sort_all_btn = DialogButton(
        sort_options_frame,
        text="First Name",
        width=14,
        command=lambda: sortMethod("f_name", sort_frame))
    sort_all_btn.grid(row=0, column=0, padx=5)

    # Sort by Last Name Button
    desort_all_btn = DialogButton(
        sort_options_frame,
        text="Last Name",
        width=14,
        command=lambda: sortMethod("l_name", sort_frame))
    desort_all_btn.grid(row=0, column=1, padx=5)

    # Reverse Sort Button
    sort_inverse_btn = DialogButton(
        sort_options_frame,
        text="Reverse",
        width=14,
        command=lambda: sortMethod("reverse", sort_frame))
    sort_inverse_btn.grid(row=0, column=2, padx=5)


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
    global selection_frame
    # Select Dialog Frame
    selection_frame = tk.Frame(window, width=400, background=PRIMARY_BG)
    selection_frame.place(bordermode=tk.INSIDE, x=150, y=167)
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


# -------------------------- Submit New Student Function -------------------------
def submitStudent(student_inputs, check_btn_flags, dialog, method, selected_index):
    global students
    # Extract inputs and checkbox values
    [f_name, l_name, phone, email, day, month, year] = map(
        lambda inp: inp.get(), student_inputs)

    abbrs = ["BI", "HI", "CH", "IT", "EN", "MA", "FL", "PH", "GE", "PR"]

    subjects = list(filter(
        lambda abbr: bool(abbr),
        list(map(
            lambda inp: abbrs[inp[0]] if inp[1].get() else None,
            enumerate(check_btn_flags)))
    ))

    # Validate Inputs

    def msg(message):
        title = "New Record Input Warning"
        messagebox.showinfo(title, message)

    if not len(f_name):
        return msg("First name is missing!")

    if not f_name.isalpha() or not l_name.isalpha():
        return msg("Name can only contain letters!")

    if not phone.isdigit():
        return msg("Invalid phone number!")

    if len(phone) < 8:
        return msg("Phone number has to be at least 8 digit long!")

    if not len(l_name):
        return msg("Last name is missing!")

    if not re.match(r"[^@]+@[^@]+\.[^@]+", email):
        return msg("Invalid email address!")

    if not len(day) or not day.isdigit() or int(day) > 31 or int(day) < 1 or float(day) % 1 != 0:
        return msg("Invalid day input!")

    if not len(month) or not month.isdigit() or int(month) > 12 or int(month) < 1 or float(month) % 1 != 0:
        return msg("Invalid month input!")

    if not len(year) or not year.isdigit() or int(year) > 99 or int(year) < 0 or float(year) % 1 != 0:
        return msg("Invalid year input!")

    if len(subjects) != 4:
        return msg("Exactly 4 subjects must be selected!")

    def padZeros(num):
        return "0" + str(int(num)) if int(num) < 10 else num

    new_student = {
        "f_name": f_name,
        "l_name": l_name,
        "phone": phone,
        "subjects": "".join(subjects),
        "dob": f"{padZeros(day)}.{padZeros(month)}.{padZeros(year)}",
        "email": email
    }

    if method == "new":
        students.append(new_student)

    if method == "modify":
        students[selected_index] = new_student

    tableIntoCSVFile("students.csv")
    getCSVTable("students.csv")
    reloadTable()
    dialog.destroy()


# -------------------------------- New Dialog Box --------------------------------
def renderNewDialog(method):
    global new_frame

    if (method == "modify"):
        if not len(state["selected"]):
            messagebox.showinfo(
                "Select Student",
                "You need to select a student that you want to modify.\nYou can select a student by clicking the checkbox\nat the end of student details. ['\u25A3'] ['\u25A1']")
            return
        if len(state["selected"]) > 1:
            messagebox.showinfo("Selection Warning",
                                "You have too many items selected!")
            return

    # New Dialog Container
    new_frame = tk.Frame(
        window,
        width=400,
        background=PRIMARY_BG)
    new_frame.place(bordermode=tk.INSIDE, x=150, y=0)

    # New Dialog Header
    new_header_frame = tk.Frame(
        new_frame, background=PRIMARY_BG)
    new_header_frame.grid(row=0, column=0)
    new_header_frame.grid_columnconfigure(0, minsize=370)

    header_text = "Create " if method == "new" else "Modify "

    new_header_label = DialogLabel(
        new_header_frame, text=f"{header_text} Student Record")
    new_header_label.grid(row=0, column=0)

    # New Dialog Close Button
    new_close_btn = CloseButton(
        new_header_frame, command=lambda: new_frame.destroy())
    new_close_btn.grid(row=0, column=1, sticky=tk.E)

    # New Dialog Separator 1
    new_separator_1 = tk.Frame(new_header_frame, bg="#444", height=1)
    new_separator_1.grid(row=1, column=0, sticky=tk.EW,
                         columnspan=2, pady=(0, 2))

    # New Dialog Body
    new_body = tk.Frame(new_frame, background=PRIMARY_BG)
    new_body.grid(row=1, column=0)
    new_body.grid_columnconfigure(0, minsize=200)
    new_body.grid_columnconfigure(1, minsize=200)
    new_body.grid_rowconfigure(0, minsize=30)
    new_body.grid_rowconfigure(1, minsize=30)
    new_body.grid_rowconfigure(3, minsize=30)
    new_body.grid_rowconfigure(4, minsize=30)
    new_body.grid_rowconfigure(6, minsize=30)
    new_body.grid_rowconfigure(8, minsize=30)
    new_body.grid_rowconfigure(9, minsize=30)
    new_body.grid_rowconfigure(10, minsize=30)
    new_body.grid_rowconfigure(11, minsize=30)
    new_body.grid_rowconfigure(12, minsize=30)
    new_body.grid_rowconfigure(13, minsize=30)
    new_body.grid_rowconfigure(15, minsize=30)

    # New Dialog First Name Label
    new_f_name_label = DialogLabel(
        new_body, text="First Name")
    new_f_name_label.grid(row=-0, column=0, sticky=tk.W)

    # New Dialog First Name Input
    f_name_var = tk.StringVar()
    new_f_name_input = DialogInput(new_body, textvariable=f_name_var)
    new_f_name_input.grid(row=0, column=1, sticky=tk.EW, padx=(0, 4))

    # New Dialog Last Name Label
    new_l_name_label = DialogLabel(
        new_body, text="Last Name")
    new_l_name_label.grid(row=1, column=0, sticky=tk.W)

    # New Dialog Last Name Input
    l_name_var = tk.StringVar()
    new_l_name_input = DialogInput(new_body, textvariable=l_name_var)
    new_l_name_input.grid(row=1, column=1, sticky=tk.EW, padx=(0, 4))

    # New Dialog Separator 2
    new_separator_2 = tk.Frame(new_body, bg="#444", height=1)
    new_separator_2.grid(row=2, column=0, sticky=tk.EW,
                         columnspan=2, pady=2)

    # New Dialog Phone Number Label
    new_phone_label = DialogLabel(
        new_body, text="Phone Number")
    new_phone_label.grid(row=3, column=0, sticky=tk.W)

    # New Dialog Phone Number Input
    phone_var = tk.StringVar()
    new_phone_input = DialogInput(new_body, textvariable=phone_var)
    new_phone_input.grid(row=3, column=1, sticky=tk.EW, padx=(0, 4))

    # New Dialog Email Label
    new_email_label = DialogLabel(
        new_body, text="Email")
    new_email_label.grid(row=4, column=0, sticky=tk.W)

    # New Dialog Email Input
    email_var = tk.StringVar()
    new_email_input = DialogInput(new_body, textvariable=email_var)
    new_email_input.grid(row=4, column=1, sticky=tk.EW, padx=(0, 4))

    # New Dialog Separator 3
    new_separator_3 = tk.Frame(new_body, bg="#444", height=1)
    new_separator_3.grid(row=5, column=0, sticky=tk.EW,
                         columnspan=2, pady=(2, 4))

    # New Dialog DOB  Label
    new_dob_label = DialogLabel(
        new_body, text="Date of Birth")
    new_dob_label.grid(row=6, column=0, sticky=tk.W)

    # New Dialog DOB Input Frame
    new_dob_input_frame = tk.Frame(new_body, background=PRIMARY_BG)
    new_dob_input_frame.grid(row=6, column=1, sticky=tk.E)
    new_dob_input_frame.grid_columnconfigure(0, minsize=67, weight=1)
    new_dob_input_frame.grid_columnconfigure(1, minsize=66, weight=1)
    new_dob_input_frame.grid_columnconfigure(2, minsize=67, weight=1)

    # New Dialog DOB Day Input
    day_var = tk.StringVar()
    new_dob_day_input = DialogInput(
        new_dob_input_frame, width=2, justify=tk.CENTER, textvariable=day_var)
    new_dob_day_input.grid(row=0, column=0, sticky=tk.EW, padx=(0, 4))

    # New Dialog DOB Month Input
    month_var = tk.StringVar()
    new_dob_month_input = DialogInput(
        new_dob_input_frame, width=2, justify=tk.CENTER, textvariable=month_var)
    new_dob_month_input.grid(row=0, column=1, sticky=tk.EW, padx=4)

    # New Dialog DOB Year Input
    year_var = tk.StringVar()
    new_dob_year_input = DialogInput(
        new_dob_input_frame, width=2, justify=tk.CENTER, textvariable=year_var)
    new_dob_year_input.grid(row=0, column=2, sticky=tk.EW, padx=4)

    # New Dialog Separator 4
    new_separator_4 = tk.Frame(new_body, bg="#444", height=1)
    new_separator_4.grid(row=7, column=0, sticky=tk.EW,
                         columnspan=2, pady=(4, 2))

    # New Dialog Subjects Label
    new_subjects_label = DialogLabel(
        new_body, text="Select 4 Subjects")
    new_subjects_label.grid(row=8, column=0, sticky=tk.W)

    check_vars = list(map(lambda x: tk.IntVar(), range(10)))

    # New Dialog Subject Row 0 Col 0 SUBJECT 0
    new_subject_r0_c0 = tk.Frame(new_body, width=200, background=PRIMARY_BG)
    new_subject_r0_c0.grid(row=9, column=0)
    new_subject_r0_c0.grid_columnconfigure(0, minsize=170)
    new_subject_r0_c0.grid_columnconfigure(1, minsize=30)
    new_subject_0_label = DialogLabel(new_subject_r0_c0, text="[BI] Biology")
    new_subject_0_label.grid(row=0, column=0, sticky=tk.W)
    new_subject_0_check = tk.Checkbutton(
        new_subject_r0_c0,  variable=check_vars[0],
        background=PRIMARY_BG, foreground=ACTIVE_FG, activebackground=PRIMARY_BG)
    new_subject_0_check.grid(row=0, column=1, sticky=tk.E)

    # New Dialog Subject Row 0 Col 1 SUBJECT 1
    new_subject_r0_c1 = tk.Frame(new_body, width=200, background=PRIMARY_BG)
    new_subject_r0_c1.grid(row=9, column=1)
    new_subject_r0_c1.grid_columnconfigure(0, minsize=170)
    new_subject_r0_c1.grid_columnconfigure(1, minsize=30)
    new_subject_1_label = DialogLabel(new_subject_r0_c1, text="[HI] History")
    new_subject_1_label.grid(row=0, column=0, sticky=tk.W)
    new_subject_1_check = tk.Checkbutton(
        new_subject_r0_c1, variable=check_vars[1],
        background=PRIMARY_BG, foreground=ACTIVE_FG, activebackground=PRIMARY_BG)
    new_subject_1_check.grid(row=0, column=1, sticky=tk.E)

    # New Dialog Subject Row 1 Col 0 SUBJECT 2
    new_subject_r1_c0 = tk.Frame(new_body, width=200, background=PRIMARY_BG)
    new_subject_r1_c0.grid(row=10, column=0)
    new_subject_r1_c0.grid_columnconfigure(0, minsize=170)
    new_subject_r1_c0.grid_columnconfigure(1, minsize=30)
    new_subject_2_label = DialogLabel(new_subject_r1_c0, text="[CH] Chemistry")
    new_subject_2_label.grid(row=0, column=0, sticky=tk.W)
    new_subject_2_check = tk.Checkbutton(
        new_subject_r1_c0, variable=check_vars[2],
        background=PRIMARY_BG, foreground=ACTIVE_FG, activebackground=PRIMARY_BG)
    new_subject_2_check.grid(row=0, column=1, sticky=tk.E)

    # New Dialog Subject Row 1 Col 1 SUBJECT 3
    new_subject_r1_c1 = tk.Frame(new_body, width=200, background=PRIMARY_BG)
    new_subject_r1_c1.grid(row=10, column=1)
    new_subject_r1_c1.grid_columnconfigure(0, minsize=170)
    new_subject_r1_c1.grid_columnconfigure(1, minsize=30)
    new_subject_3_label = DialogLabel(
        new_subject_r1_c1, text="[IT] Information Techonlogy")
    new_subject_3_label.grid(row=0, column=0, sticky=tk.W)
    new_subject_3_check = tk.Checkbutton(
        new_subject_r1_c1, variable=check_vars[3],
        background=PRIMARY_BG, foreground=ACTIVE_FG, activebackground=PRIMARY_BG)
    new_subject_3_check.grid(row=0, column=1, sticky=tk.E)

    # New Dialog Subject Row 2 Col 0 SUBJECT 4
    new_subject_r2_c0 = tk.Frame(new_body, width=200, background=PRIMARY_BG)
    new_subject_r2_c0.grid(row=11, column=0)
    new_subject_r2_c0.grid_columnconfigure(0, minsize=170)
    new_subject_r2_c0.grid_columnconfigure(1, minsize=30)
    new_subject_4_label = DialogLabel(new_subject_r2_c0, text="[EN] English")
    new_subject_4_label.grid(row=0, column=0, sticky=tk.W)
    new_subject_4_check = tk.Checkbutton(
        new_subject_r2_c0, variable=check_vars[4],
        background=PRIMARY_BG, foreground=ACTIVE_FG, activebackground=PRIMARY_BG)
    new_subject_4_check.grid(row=0, column=1, sticky=tk.E)

    # New Dialog Subject Row 2 Col 1 SUBJECT 5
    new_subject_r2_c1 = tk.Frame(new_body, width=200, background=PRIMARY_BG)
    new_subject_r2_c1.grid(row=11, column=1)
    new_subject_r2_c1.grid_columnconfigure(0, minsize=170)
    new_subject_r2_c1.grid_columnconfigure(1, minsize=30)
    new_subject_5_label = DialogLabel(
        new_subject_r2_c1, text="[MA] Maths")
    new_subject_5_label.grid(row=0, column=0, sticky=tk.W)
    new_subject_5_check = tk.Checkbutton(
        new_subject_r2_c1, variable=check_vars[5],
        background=PRIMARY_BG, foreground=ACTIVE_FG, activebackground=PRIMARY_BG)
    new_subject_5_check.grid(row=0, column=1, sticky=tk.E)

    # New Dialog Subject Row 3 Col 0 SUBJECT 6
    new_subject_r3_c0 = tk.Frame(new_body, width=200, background=PRIMARY_BG)
    new_subject_r3_c0.grid(row=12, column=0)
    new_subject_r3_c0.grid_columnconfigure(0, minsize=170)
    new_subject_r3_c0.grid_columnconfigure(1, minsize=30)
    new_subject_6_label = DialogLabel(
        new_subject_r3_c0, text="[FL] Foreign Language")
    new_subject_6_label.grid(row=0, column=0, sticky=tk.W)
    new_subject_6_check = tk.Checkbutton(
        new_subject_r3_c0, variable=check_vars[6],
        background=PRIMARY_BG, foreground=ACTIVE_FG, activebackground=PRIMARY_BG)
    new_subject_6_check.grid(row=0, column=1, sticky=tk.E)

    # New Dialog Subject Row 3 Col 1 SUBJECT 7
    new_subject_r3_c1 = tk.Frame(new_body, width=200, background=PRIMARY_BG)
    new_subject_r3_c1.grid(row=12, column=1)
    new_subject_r3_c1.grid_columnconfigure(0, minsize=170)
    new_subject_r3_c1.grid_columnconfigure(1, minsize=30)
    new_subject_7_label = DialogLabel(
        new_subject_r3_c1, text="[PH] Physics")
    new_subject_7_label.grid(row=0, column=0, sticky=tk.W)
    new_subject_7_check = tk.Checkbutton(
        new_subject_r3_c1, variable=check_vars[7],
        background=PRIMARY_BG, foreground=ACTIVE_FG, activebackground=PRIMARY_BG)
    new_subject_7_check.grid(row=0, column=1, sticky=tk.E)

    # New Dialog Subject Row 3 Col 0 SUBJECT 8
    new_subject_r4_c0 = tk.Frame(new_body, width=200, background=PRIMARY_BG)
    new_subject_r4_c0.grid(row=13, column=0)
    new_subject_r4_c0.grid_columnconfigure(0, minsize=170)
    new_subject_r4_c0.grid_columnconfigure(1, minsize=30)
    new_subject_8_label = DialogLabel(
        new_subject_r4_c0, text="[GE] Geography")
    new_subject_8_label.grid(row=0, column=0, sticky=tk.W)
    new_subject_8_check = tk.Checkbutton(
        new_subject_r4_c0, variable=check_vars[8],
        background=PRIMARY_BG, foreground=ACTIVE_FG, activebackground=PRIMARY_BG)
    new_subject_8_check.grid(row=0, column=1, sticky=tk.E)

    # New Dialog Subject Row 3 Col 1 SUBJECT 9
    new_subject_r4_c1 = tk.Frame(new_body, width=200, background=PRIMARY_BG)
    new_subject_r4_c1.grid(row=13, column=1)
    new_subject_r4_c1.grid_columnconfigure(0, minsize=170)
    new_subject_r4_c1.grid_columnconfigure(1, minsize=30)
    new_subject_9_label = DialogLabel(
        new_subject_r4_c1, text="[PR] Programming")
    new_subject_9_label.grid(row=0, column=0, sticky=tk.W)
    new_subject_9_check = tk.Checkbutton(
        new_subject_r4_c1, variable=check_vars[9],
        background=PRIMARY_BG, foreground=ACTIVE_FG, activebackground=PRIMARY_BG)
    new_subject_9_check.grid(row=0, column=1, sticky=tk.E)

    # New Dialog Separator 5
    new_separator_4 = tk.Frame(new_body, bg="#444", height=1)
    new_separator_4.grid(row=14, column=0, sticky=tk.EW,
                         columnspan=2, pady=(4, 2))

    # New Dialog Submit Button
    new_dialog_vars = [f_name_var, l_name_var, phone_var,
                       email_var, day_var, month_var, year_var]

    # We need to pass state[selected] as an argument for submitStudent function
    # Because user can select other elements while submitting, consequently
    # changing the index of the student being under modification

    def getSelected():
        try:
            return state["selected"][0]
        except IndexError:
            return None

    new_submit = DialogButton(
        new_body, text="Submit", width=10,
        command=lambda: submitStudent(
            new_dialog_vars, check_vars, new_frame, method, getSelected()))
    new_submit.grid(row=15, column=0, columnspan=2)

    # New Dialog Separator 6
    new_separator_4 = tk.Frame(new_body, bg="#444", height=1)
    new_separator_4.grid(row=16, column=0, sticky=tk.EW,
                         columnspan=2, pady=(4, 2))

    if method == "modify":
        student = students[state["selected"][0]]

        # Set Default Values of Inputs
        new_f_name_input.insert(tk.END, student["f_name"])
        new_l_name_input.insert(tk.END, student["l_name"])
        new_phone_input.insert(tk.END, student["phone"])
        new_email_input.insert(tk.END, student["email"])

        [day, month, year] = student["dob"].split(".")

        new_dob_day_input.insert(tk.END, int(day))  # get rid of zeros like 09
        new_dob_month_input.insert(tk.END, int(month))
        new_dob_year_input.insert(tk.END, int(year))

        # Check Subjects
        subjects = student["subjects"]
        subs = [subjects[i: i + 2] for i in range(0, len(subjects), 2)]

        if "BI" in subs:
            new_subject_0_check.select()

        if "HI" in subs:
            new_subject_1_check.select()

        if "CH" in subs:
            new_subject_2_check.select()

        if "IT" in subs:
            new_subject_3_check.select()

        if "EN" in subs:
            new_subject_4_check.select()

        if "MA" in subs:
            new_subject_5_check.select()

        if "FL" in subs:
            new_subject_6_check.select()

        if "PH" in subs:
            new_subject_7_check.select()

        if "GE" in subs:
            new_subject_8_check.select()

        if "PR" in subs:
            new_subject_9_check.select()


def renderDeleteMsg():
    global students

    if not len(state["selected"]):
        tk.messagebox.showinfo(
            "Delete",
            "You need to select a student that you want to delete.\nYou can select a student by clicking the checkbox\nat the end of student details. ['\u25A3'] ['\u25A1']")
        return

    result = tk.messagebox.askquestion(
        "Delete Warning",
        f"You have selected {len(state['selected'])} item(s) to delete! Delete item(s)?",
        icon='warning')
    if result == 'no':
        return
    else:
        for index in state["selected"]:

            del students[index]

            state["curr_page"] = 1  # if page is out of range

            tableIntoCSVFile("students.csv")
            getCSVTable("students.csv")

            reloadTable()


def createDialog(dialog_name):
    if dialog_name == "Search":
        renderSearchDialog()

    if dialog_name == "Filter":
        renderFilterDialog()

    if dialog_name == "Selection":
        renderSelectionDialog()

    if dialog_name == "Sort":
        renderSortDialog()

    if dialog_name == "New":
        renderNewDialog("new")

    if dialog_name == "Modify":
        renderNewDialog("modify")  # Reuse renderNewDialog function

    if dialog_name == "Delete":
        renderDeleteMsg()

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


sidebar = tk.Frame(
    window,
    bg=PRIMARY_BG, height=WIN_HEIGHT,
    width=150, name="sidebar")
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
    window, name="display",
    height=WIN_HEIGHT,
    width=1050, background=PRIMARY_BG)
display.grid(row=0, column=1)
display.grid_propagate(False)

# ---------------------------------- Caption -----------------------------------

caption = tk.Frame(
    display,
    height=20, width=1050,
    background=PRIMARY_BG, name="caption")
caption.grid(row=0, column=0)
caption.grid_propagate(False)

table_container = tk.Frame(
    display, name="table_container",
    height=400, width=1050,
    background=ROW_BG_DARK)


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

    if len(students):
        # divide list into chunks of 20 items
        chunks = [students[i:i + 20] for i in range(0, len(students), 20)]
        state["total_pages"] = math.ceil(len(students) / 20)

        # display current chunk of data
        list_to_display = chunks[state["curr_page"] - 1]
    else:
        list_to_display = []

    if len(list_to_display):
        for row_index, student in enumerate(list_to_display):

            # Every secound row darker
            background = ROW_BG_LIGHT
            foreground = "white"

            if row_index % 2 == 0:
                background = ROW_BG_DARK

            # Check if student is selected
            tab_index = (state["curr_page"] - 1) * 20 + row_index

            selected = True if tab_index in state["selected"] else False

            if selected:
                background = SELECTED_BG
                foreground = PRIMARY_BG

            row = tk.Frame(
                table_container, name=f"row_{tab_index}",
                width=1050, height=20,
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
                    if index == 3:
                        subjects = [entry[i: i + 2]
                                    for i in range(0, len(entry), 2)]
                        entry = subjects

                    cell = tk.Label(
                        row,
                        width=cell_width[index],
                        background=background,
                        foreground=foreground,
                        text=entry,
                        font=MONOSPACE,
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
            background=ROW_BG_DARK,
            foreground=PRIMARY_FG,
            width=150,
            height=30)
        no_item.grid(row=0, column=0)
        no_item.grid_propagate(False)
        table_container.grid_columnconfigure(0, weight=1)
        table_container.grid_rowconfigure(0, weight=1)


createTable(table_container)


# --------------------------------- Footer -------------------------------------
footer_container = tk.Frame(
    display,
    name="footer_container",
    height=32, width=1050,
    background=PRIMARY_BG)


def createFooter(footer_container):
    footer_container.grid(row=2, column=0)
    footer_container.grid_propagate(False)

# ------------------------------ Sorting Info -----------------------------------
    sort_info_frame = tk.Frame(
        footer_container, width=293, height=32, background=PRIMARY_BG)
    sort_info_frame.grid(row=0, column=0)
    sort_info_frame.grid_columnconfigure(0, minsize=293)

    sort_items = tk.Frame(sort_info_frame, width=239, background=PRIMARY_BG)
    sort_items.grid(row=0, column=0, sticky=tk.NSEW)

    sorted_txt = "Sorted by : "
    asc_txt = "ASC" if state["sort_asc"] else "DESC"

    name_txt = ""
    if state["sortedby"] == "f_name":
        name_txt = "first name"

    if state["sortedby"] == "l_name":
        name_txt = "last name"

    sorted_state = f'  {name_txt} {asc_txt}  '
    sorted_txt += sorted_state if state["sortedby"] else "-"

    sort_label = tk.Label(
        sort_items,
        text=sorted_txt,
        background=PRIMARY_BG,
        foreground=PRIMARY_FG,
        anchor=tk.E)
    sort_label.grid(row=0, column=0)
    sort_label.propagate(False)

    if state["sortedby"]:
        sort_clear_btn = DialogButton(
            sort_items, text="Clear Sorting",
            command=reloadTable)
        sort_clear_btn.grid(row=0, column=1)


# ------------------------------- Filter Info -----------------------------------
    filter_info_frame = tk.Frame(
        footer_container, width=293, height=32, background=PRIMARY_BG)
    filter_info_frame.grid(row=0, column=1)
    filter_info_frame.grid_columnconfigure(0, minsize=293)

    filter_items = tk.Frame(
        filter_info_frame, width=239, background=PRIMARY_BG)
    filter_items.grid(row=0, column=0, sticky=tk.NSEW)

    [fil, tot_fil] = state["filtered"] or [0, 0]
    filter_text = f"Filtered: [ {fil} | {tot_fil} ]"
    filter_label = tk.Label(
        filter_items,
        text=filter_text,
        background=PRIMARY_BG,
        foreground=PRIMARY_FG,
        anchor=tk.W)
    filter_label.grid(row=0, column=0, sticky=tk.NSEW)
    filter_label.propagate(False)

    if state["filtered"]:
        filter_clear_btn = DialogButton(
            filter_items, text="Clear Filter",
            command=reloadTable)
        filter_clear_btn.grid(row=0, column=1)

# ----------------------------- Selection Info ----------------------------------
    selection_info_frame = tk.Frame(
        footer_container, width=293, height=32)
    selection_info_frame.grid(row=0, column=2)
    selection_info_frame.propagate(False)
    selection_info_frame.grid_columnconfigure(0, minsize=293)

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
    pagination_frame.grid(row=0, column=3)
    pagination_frame.grid_rowconfigure(0, minsize=32)
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
    # close open dialogs

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
        dialogs = [new_frame, modify_frame, delete_frame,
                   filter_frame, search_frame, sort_frame, selection_frame]
        for dialog in dialogs:
            if dialog:
                dialog.destroy()

        createDialog(state["menu_open"])

    window.after(100, listeningState)


listeningState()


def setDialog(new_state):
    state["menu_open"] = new_state
    state["update"].append("table")


window.mainloop()
