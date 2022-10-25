import tkinter as tk
from tkinter import ttk
from tkcalendar import *
from tkinter import messagebox as msg
import datetime as dt
import pickle


# This function takes last element as pivot, places
# the pivot element at its correct position in sorted
# array, and places all smaller (smaller than pivot)
# to left of pivot and all greater elements to right
# of pivot

def partition(arr, low, high, big):
    i = (low - 1)
    pivot = arr[high]

    for j in range(low, high):
        if arr[j] <= pivot:
            i = i + 1
            arr[i], arr[j], big[i], big[j] = arr[j], arr[i], big[j], big[i]
    arr[i + 1], arr[high], big[i + 1], big[high] = arr[high], arr[i + 1], big[high], big[i + 1]
    return (i + 1)
# The main function that implements QuickSort
# arr[] --> Array to be sorted,
# low --> Starting index,
# high --> Ending index
# Function to do Quick sort
def quickSort(arr, low, high, big):
    if len(arr) == 1:
        return arr
    if low < high:
        pi = partition(arr, low, high, big)
        quickSort(arr, low, pi - 1, big)
        quickSort(arr, pi + 1, high, big)


class Window(tk.Tk):

    def __init__(self):
        tk.Tk.__init__(self)
        self.geometry("1920x1080")
        self.state(newstate='zoomed')
        self.title("Author's Organisation System")
        self.configure(background="yellow")

        self._frame = None
        self.switch_frame(Start)

    def switch_frame(self, frame_class):
        """Destroys current frame and replaces it with a new one."""
        new_frame = frame_class(self)
        if self._frame is not None:
            self._frame.destroy()
        self._frame = new_frame
        self._frame.pack(expand=True, fill="both")


class Start(tk.Frame):
    def __init__(self, parent, **kw):
        # self.bg = ImageTk.PhotoImage(file = r"C:\Users\neels\Pictures\Backgrounds\zero two.jpg")
        # lbl_bg = tk.Label(self, bg="white")
        # lbl_bg.place(x=0,y=0,rewidth=1,reheight=2)
        tk.Frame.__init__(self, parent, bg="blue")
        self.parent = parent

        try:
            f = open("author login.dat", "rb")

            f.close()

        except FileNotFoundError:
            f = open("author login.dat", "wb")
            L = []
            pickle.dump(L, f)
            f.close()
        self.start_widgets()

    def start_widgets(self):
        welcome_message = tk.Label(self, text="Welcome to the\n Author's Organisation System!",
                                   background="crimson", font=("Times New Roman", 25))
        welcome_message.place(x=450, y=50)

        login_button = tk.Button(self, text="Login (Existing Author)", command=lambda: self.parent.switch_frame(Login))
        login_button.place(x=500, y=225, width=300, height=50)

        register_button = tk.Button(self, text="Register (New Author)",
                                    command=lambda: self.parent.switch_frame(Register))
        register_button.place(x=500, y=300, width=300, height=50)

        remove_button = tk.Button(self, text="Delete Account", command=lambda: self.parent.switch_frame(Remove))
        remove_button.place(x=500, y=375, width=300, height=50)

        quit_button = tk.Button(self, text="Quit", command=self.parent.destroy)
        quit_button.place(x=500, y=450, width=300, height=50)


class Login(Start):
    def __init__(self, parent, **kw):
        tk.Frame.__init__(self, parent, bg="blue")

        self.parent = parent

        f = open("author login.dat", "rb")
        userdata = pickle.load(f)
        f.close()
        self.users = []
        for i in range(0, int(len(userdata)), 2):
            self.users.append(userdata[i])

        self.login_widgets()

    def login_widgets(self):
        login_frame = tk.Frame(self, relief="sunken", bd=4, bg="crimson")
        login_frame.place(x=400, y=100, width=500, height=500)

        tk.Label(login_frame, text="Login", font=("times new roman", 25)).place(x=100, y=50, width=300, height=50)
        name = tk.Label(login_frame, text="Enter your username:", font=("times new roman", 15))
        name.place(x=25, y=150)

        self.username = ttk.Combobox(login_frame, state="normal", values=self.users, font=("times new roman", 15))
        self.username.place(x=225, y=150)

        pwd = tk.Label(login_frame, text="Enter your password:", font=("times new roman", 15))
        pwd.place(x=25, y=200)
        password = tk.Entry(login_frame, relief='groove', font=("times new roman", 15), show="*")
        password.place(x=225, y=200)

        confirm_login = tk.Button(login_frame, text="Confirm Login",
                                  command=lambda: self.verify_login(self.username.get(), password.get()),
                                  font=("times new roman", 15))
        confirm_login.place(x=100, y=250, width=300, height=50)

        back_button = tk.Button(login_frame, text="Back", command=lambda: self.parent.switch_frame(Start),
                                font=("times new roman", 15))
        back_button.place(x=100, y=350, width=300, height=50)

    def verify_login(self, name1, password1):

        f = open("author login.dat", "rb")  # Open the file where all logins are stored
        found = False
        userdata = pickle.load(f)  # load file data
        f.close()
        for i in range(len(userdata)):  # search the file data for inputted username and password
            if name1 == userdata[i] and password1 == userdata[i + 1]:
                found = True
                break
        if found == True:
            msg.showinfo("Login Complete", "Login Successful!")
            try:
                g = open("login logger.txt", "a")  # check if file already present and accessible
                g.write("\n" + name1)
                g.close()
            except FileNotFoundError:
                g = open("login logger.txt", "w")  # creates new logger file if file not already found
                g.write("\n" + name1)  # writes most recent login onto file which becomes a stack when parsed
                g.close()
            self.parent.switch_frame(Main)

        elif found == False:
            msg.showerror("Invalid Login", "Account does not exist \n Please create an account")
            self.parent.switch_frame(Start)


class Remove(Start):
    def __init__(self, parent, **kw):
        tk.Frame.__init__(self, parent, bg="blue")
        self.parent = parent

        f = open("author login.dat", "rb")
        userdata = pickle.load(f)
        f.close()
        self.users = []
        for i in range(0, int(len(userdata)), 2):
            self.users.append(userdata[i])
        self.remove_widgets()

    def remove_widgets(self):
        remove_frame = tk.Frame(self, relief="sunken", bd=4, bg="crimson")
        remove_frame.place(x=400, y=100, width=500, height=500)

        tk.Label(remove_frame, text="Delete Account", font=("times new roman", 25)).place(x=100, y=50, width=300,
                                                                                          height=50)
        name = tk.Label(remove_frame, text="Enter your username:", font=("times new roman", 15))
        name.place(x=25, y=150)

        username = ttk.Combobox(remove_frame, values=self.users, state="readonly", font=("Times New Roman", 15))
        username.place(x=225, y=150)

        pwd = tk.Label(remove_frame, text="Enter your password:", font=("times new roman", 15))
        pwd.place(x=25, y=200)
        password = tk.Entry(remove_frame, relief='groove', font=("times new roman", 15), show="*")
        password.place(x=225, y=200)

        confirm_remove = tk.Button(remove_frame, text="Remove User",
                                   command=lambda: self.remove_user(username.get(), password.get()),
                                   font=("times new roman", 15))
        confirm_remove.place(x=100, y=250, width=300, height=50)

        back_button = tk.Button(remove_frame, text="Back", command=lambda: self.parent.switch_frame(Start),
                                font=("times new roman", 15))
        back_button.place(x=100, y=350, width=300, height=50)

    def remove_user(self, name1, password1):
        f = open("author login.dat", "rb")
        userdata = pickle.load(f)
        f.close()
        found = False
        for i in range(0, len(userdata), 2):
            if name1 == userdata[i] and password1 == userdata[i + 1]:
                found = True
                userdata.pop(i + 1)
                userdata.pop(i)

                f = open("author login.dat", "wb")
                pickle.dump(userdata, f)
                f.close()
                msg.showinfo("Successful Removal", "User has been removed")
                self.parent.switch_frame(Start)
                break

        if found == False:
            msg.showerror("Incorrect Password or Account", "Account does not exist \n Cannot be deleted")
            self.parent.switch_frame(Start)


class Register(Start):
    def __init__(self, parent, **kw):
        tk.Frame.__init__(self, parent, bg="blue")
        self.parent = parent
        self.register_widgets()

    def register_widgets(self):
        register_frame = tk.Frame(self, relief="sunken", bd=4, background="crimson")
        register_frame.place(x=400, y=100, width=500, height=500)
        tk.Label(register_frame, text="Register", font=("times new roman", 25)).place(x=100, y=50, width=300, height=50)

        new_username = tk.Label(register_frame, text="Enter your username:", font=("times new roman", 15))
        new_username.place(x=25, y=150)
        new_name = tk.Entry(register_frame, relief='sunken', font=("times new roman", 15))
        new_name.place(x=225, y=150)

        new_password = tk.Label(register_frame, text="Enter your password:", font=("times new roman", 15))
        new_password.place(x=25, y=200)
        new_pwd = tk.Entry(register_frame, relief='sunken', font=("times new roman", 15), show="*")
        new_pwd.place(x=225, y=200)

        verify_password = tk.Label(register_frame, text="Re-enter password:", font=("times new roman", 15))
        verify_password.place(x=25, y=250)
        verify_pwd = tk.Entry(register_frame, relief='sunken', font=("times new roman", 15), show="*")
        verify_pwd.place(x=225, y=250)

        confirm_reg = tk.Button(register_frame, font=("times new roman", 15), text="Create",
                                command=lambda: self.verify_reg(new_name.get(), new_pwd.get(), verify_pwd.get()))
        confirm_reg.place(x=100, y=300, width=300, height=50)

        back_button = tk.Button(register_frame, font=("times new roman", 15), text="Back",
                                command=lambda: self.parent.switch_frame(Start))
        back_button.place(x=100, y=400, width=300, height=50)

    def verify_reg(self, name, pwd1, pwd2):
        if len(name) == 0 or len(pwd1) == 0 or len(pwd2) == 0:
            msg.showerror("No Input", "Please input values")
        elif pwd1 != pwd2:
            msg.showwarning('Invalid Entry', 'Passwords do not match!')
        else:
            alreadyexists = False
            f = open("author login.dat", "rb")
            userdata = pickle.load(f)
            f.close()
            for i in range(len(userdata)):
                if userdata[i] == name:  #:
                    alreadyexists = True
                    break
            if alreadyexists == True:
                msg.showwarning("User already exists!", "Duplicate registration not allowed")
            elif alreadyexists == False:
                userdata.append(name)
                userdata.append(pwd1)
                msg.showinfo("Account Created", "Successful Registration")
                f = open("author login.dat", "wb")
                pickle.dump(userdata, f)
                f.close()
                self.parent.switch_frame(Start)


class Main(Login):
    def __init__(self, parent, **kw):
        tk.Frame.__init__(self, parent, bg="blue")
        Login.__init__(self, parent)
        self.parent = parent

        g = open("login logger.txt", "r")
        self.login_list = g.read().split("\n")
        print(self.username)
        g.close()

        self.main_widgets()

    def main_widgets(self):
        home_frame = tk.Frame(self, relief="sunken", bd=4, bg="crimson")
        home_frame.place(x=200, y=100, width=900, height=500)
        label_homepage = tk.Label(home_frame, text='Welcome ' + self.login_list[-1] + '!', font=("times new roman", 25))
        label_homepage.place(x=300, y=50, width=300, height=50)

        manage_readers = tk.Button(home_frame, text="Manage Readers", font=("times new roman", 25),
                                   command=lambda: self.parent.switch_frame(ManageReader))
        manage_readers.place(x=150, y=150, width=250, height=100)

        manage_events = tk.Button(home_frame, text="Manage Events", font=("times new roman", 25),
                                  command=lambda: self.parent.switch_frame(ManageEvent))
        manage_events.place(x=550, y=150, width=250, height=100)

        time_label = tk.Label(home_frame, text=dt.datetime.today().strftime('%d %b %Y'), font=("times new roman", 25))
        time_label.place(x=300, y=300, width=300, height=50)

        back_button = tk.Button(home_frame, text="Logout", font=("times new roman", 25),
                                command=lambda: self.parent.switch_frame(Login))
        back_button.place(x=300, y=400, width=300, height=50)


class ManageReader(Main):
    def __init__(self, parent, **kw):
        tk.Frame.__init__(self, parent, bg="blue")
        self.parent = parent
        self.reader_widgets()

    # ======READER ENTRY=====================#
    def reader_widgets(self):
        addreaderframe = tk.Frame(self, relief="sunken", bg="crimson", bd=4)
        addreaderframe.place(x=50, y=50, width=400, height=600)

        tk.Label(addreaderframe, text="Add Reader", font=("Times New Roman", 25), bg="crimson").place(x=100, y=25)

        tk.Label(addreaderframe, text="Name:", font=("Times New Roman", 15), bg="crimson").place(x=25, y=100)
        self.reader_name = tk.StringVar()
        self.reader_name = tk.Entry(addreaderframe, relief="sunken", font=("Times New Roman", 15))
        self.reader_name.place(x=150, y=100)

        age_groups = ["Toddlers", "Children", "Teens", "Young Adults", "Adults"]
        tk.Label(addreaderframe, text="Age:", font=("Times New Roman", 15), bg="crimson").place(x=25, y=150)
        self.reader_age = tk.Entry(addreaderframe, relief="sunken", font=("Times New Roman", 15))
        self.reader_age.place(x=150, y=150)

        tk.Label(addreaderframe, text="Gender", font=("Times New Roman", 15), bg="crimson").place(x=25, y=200)
        self.reader_gender = ttk.Combobox(addreaderframe, font=("Times New Roman", 15),
                                          values=["M", "F", "Other", "Prefer Not to say"])
        self.reader_gender.place(x=150, y=200)

        books = ["Midnight Years", "Superzero 1", "Superzero 2", "Superzero 3", "Uncool", "When the world went dark"]
        tk.Label(addreaderframe, text="Favourite Book:", font=("Times New Roman", 15), bg="crimson").place(x=25, y=250)
        self.reader_favbook = ttk.Combobox(addreaderframe, values=books, state="normal", font=("Times New Roman", 15))
        self.reader_favbook.place(x=150, y=250)

        tk.Label(addreaderframe, text="Reader Email:", font=("times new roman", 15), bg="crimson").place(x=25, y=300)
        self.reader_email = tk.Entry(addreaderframe, relief="sunken", font=("Times New Roman", 15))
        self.reader_email.place(x=150, y=300)

        addreader = tk.Button(addreaderframe, text="Add Reader Profile", font=("Times New Roman", 15),
                              command=self.add_reader)
        addreader.place(x=50, y=350, width=300, height=50)

        updatereader = tk.Button(addreaderframe, text="Update Reader Profile", font=("Times New Roman", 15),
                                 command=self.update_reader)
        updatereader.place(x=50, y=425, width=300, height=50)

        back_button = tk.Button(addreaderframe, text="Back", command=lambda: self.parent.switch_frame(Main))
        back_button.place(x=50, y=500, width=300, height=50)

        # ============READER LIST FRAME============#
        readerlistframe = tk.Frame(self, relief="sunken", bg="crimson", bd=4)
        readerlistframe.place(x=500, y=50, width=700, height=600)

        self.readerlist = ttk.Treeview(readerlistframe, columns=(1, 2, 3, 4, 5, 6), show="headings")
        self.readerlist.column(1, width=15)
        self.readerlist.heading(1, text="ID")
        self.readerlist.column(2, width=75)
        self.readerlist.heading(2, text="Name")
        self.readerlist.column(3, width=15)
        self.readerlist.heading(3, text="Age")
        self.readerlist.column(4, width=100)
        self.readerlist.heading(4, text="Gender")
        self.readerlist.column(5, width=150)
        self.readerlist.heading(5, text="Favourite book")
        self.readerlist.column(6, width=125)
        self.readerlist.heading(6, text="Email")
        self.readerlist.place(x=25, y=25, width=650, height=350)

        searchreaderbutton = tk.Button(readerlistframe, text="Search",
                                       command=lambda: self.parent.switch_frame(SearchReader))
        searchreaderbutton.place(x=350, y=450, width=300, height=50)

        tk.Label(readerlistframe, text="Sort By:", font=("times new roman", 15), bg="crimson").place(x=350, y=525,
                                                                                                     width=75,
                                                                                                     height=50)

        self.sortreaderby = ttk.Combobox(readerlistframe, values=["Name", "Age", "Gender", "FavBook"], state="readonly")
        self.sortreaderby.place(x=440, y=525, width=65, height=50)

        sortreaderbutton = tk.Button(readerlistframe, text="Sort", command=self.sort_reader)
        sortreaderbutton.place(x=525, y=525, width=125, height=50)

        deletereader = tk.Button(readerlistframe, text="Delete Reader", command=self.delete_reader)
        deletereader.place(x=25, y=450, width=300, height=50)

        edit_button = tk.Button(readerlistframe, text="Edit Reader", command=self.edit_reader)
        edit_button.place(x=25, y=525, width=300, height=50)

        try:  # Check to see if bin file has been created
            f = open("reader list.dat", "rb")
            data = pickle.load(f)  # binary file storage allows me to load 2D array without parsing
            f.close()

            count = 0
            for rec in data:  # 2D array values are then placed into the table which is displayed
                self.readerlist.insert('', index='end', iid=count,
                                       values=rec)
                count += 1

        except FileNotFoundError:  # bin file created if not found
            f = open("reader list.dat", "wb")
            D = []
            pickle.dump(D, f)
            f.close()

    def sort_reader(self):
        sorter = self.sortreaderby.get().lower()

        f = open("reader list.dat", "rb")
        readerdata = pickle.load(f)
        f.close()
        if sorter == "age":
            arr = [rec[2] for rec in readerdata]
            n = len(arr)
            quickSort(arr, 0, n - 1, readerdata)

        if sorter == "name":
            arr = [rec[1] for rec in readerdata]
            n = len(arr)
            quickSort(arr, 0, n - 1, readerdata)

        if sorter == "gender":
            arr = [rec[3] for rec in readerdata]
            n = len(arr)
            quickSort(arr, 0, n - 1, readerdata)

        if sorter == "favbook":
            arr = [rec[4] for rec in readerdata]
            n = len(arr)
            quickSort(arr, 0, n - 1, readerdata)

        f = open("reader list.dat", "wb")
        pickle.dump(readerdata, f)
        f.close()

        self.parent.switch_frame(ManageReader)

    def edit_reader(self):
        x = self.readerlist.selection()
        y = self.readerlist.item(x)


        self.reader_name.insert(0, (y["values"])[1])
        self.reader_age.insert(0, (y["values"])[2])
        self.reader_gender.insert(0, (y["values"])[3])
        self.reader_favbook.insert(0, y["values"][4])
        self.reader_email.insert(0, (y["values"])[5])

    def delete_reader(self):  # Deletes selected reader in the table
        for selected_item in self.readerlist.selection():
            item = self.readerlist.item(selected_item)
            readerrecord = item["values"][0]
            f = open("reader list.dat", "rb")  # opens the file in which table contents are loaded from
            readerdata = pickle.load(f)

            f.close()

            for rec in readerdata:

                if rec[0] == readerrecord:  # checks if selected reader is present in file data
                    readerdata.pop(readerdata.index(rec))
                    break

            h = open("reader list.dat", "wb")  # clears old contents of file
            pickle.dump(readerdata, h)  # contents are dumped back into file from 2D array
            h.close()
            self.parent.switch_frame(ManageReader)  # refresh page to display new file contents in table

    def add_reader(self):  # adds reader record to 2D array stored in binary file
        g = open("reader list.dat", "rb")
        readerdata = pickle.load(g)  # picks up the 2D array

        g.close()
        try:
            readerdata.append(["r" + str(1 + len(readerdata)),  # adds the record to the 2D array
                               self.reader_name.get().strip(),
                               int(self.reader_age.get().strip()),
                               self.reader_gender.get().strip(),
                               self.reader_favbook.get().strip(),
                               self.reader_email.get().strip()])

            h = open("reader list.dat", "wb")
            pickle.dump(readerdata, h)  # 2D array is re-written onto binary file
            h.close()

            self.parent.switch_frame(ManageReader)
        except ValueError:
            msg.showerror("Invalid Input", "Please input valid data")

    def update_reader(self):
        f = open("reader list.dat", "rb")
        readerdata = pickle.load(f)

        f.close()

        x = self.readerlist.selection()
        y = self.readerlist.item(x)

        for rec in readerdata:
            if rec[0] == y["values"][0]:
                readerdata[readerdata.index(rec)] = [rec[0],
                                                     self.reader_name.get().strip(),
                                                     int(self.reader_age.get().strip()),
                                                     self.reader_gender.get().strip(),
                                                     self.reader_favbook.get().strip(),
                                                     self.reader_email.get().strip()]
                break

        g = open("reader list.dat", "wb")
        pickle.dump(readerdata, g)
        g.close()

        self.parent.switch_frame(ManageReader)


class SearchReader(ManageReader):
    def __init__(self, parent, **kw):
        tk.Frame.__init__(self, parent, bg="blue")
        self.parent = parent
        self.search_widgets()

    def search_widgets(self):
        self.searchframe = tk.Frame(self, relief="sunken", bg="crimson", bd=4)
        self.searchframe.place(x=25, y=25, width=1225, height=650)
        searchframe = self.searchframe
        tk.Label(text="Search Readers", font=("times new roman", 35), bg="crimson").place(x=500, y=50)

        tk.Label(searchframe, text="Search By:", font=("times new roman", 15), bg="crimson").place(x=25, y=100,
                                                                                                   width=150, height=50)
        self.searchreaderby = ttk.Combobox(searchframe, values=["Name", "Age", "Gender", "Favourite Book", "ID"],
                                           state="readonly")
        self.searchreaderby.place(x=200, y=100, width=200, height=50)

        self.searchreaderlist = ttk.Treeview(searchframe, columns=(1, 2, 3, 4, 5, 6), show="headings")
        self.searchreaderlist.column(1, width=50)
        self.searchreaderlist.heading(1, text="id")
        self.searchreaderlist.column(2, width=100)
        self.searchreaderlist.heading(2, text="Name")
        self.searchreaderlist.column(3, width=50)
        self.searchreaderlist.heading(3, text="Age")
        self.searchreaderlist.column(4, width=50)
        self.searchreaderlist.heading(4, text="Gender")
        self.searchreaderlist.column(6, width=150)
        self.searchreaderlist.heading(6, text="Favourite Book")
        self.searchreaderlist.column(5, width=150)
        self.searchreaderlist.heading(5, text="Email")
        self.searchreaderlist.place(x=500, y=100, width=700, height=450)

        tk.Label(self.searchframe, text="Age:", font=("Times New Roman", 15), bg="crimson").place(x=25, y=175)
        self.searchreader_agelow = tk.Entry(self.searchframe, relief="sunken", font=("Times New Roman", 15))
        self.searchreader_agelow.place(x=150, y=175, width=50)

        tk.Label(self.searchframe, text="to", font=("times new roman", 15), bg="crimson").place(x=225, y=175, width=25)
        self.searchreader_agehigh = tk.Entry(self.searchframe, relief="sunken", font=("Times New Roman", 15))
        self.searchreader_agehigh.place(x=275, y=175, width=50)

        tk.Label(self.searchframe, text="Name:", font=("Times New Roman", 15), bg="crimson").place(x=25, y=250)
        self.searchreader_name = tk.StringVar()
        self.searchreader_name = tk.Entry(self.searchframe, relief="sunken", font=("Times New Roman", 15))
        self.searchreader_name.place(x=150, y=250)

        tk.Label(self.searchframe, text="Gender", font=("Times New Roman", 15), bg="crimson").place(x=25, y=325)
        self.searchreader_gender = ttk.Combobox(self.searchframe, font=("Times New Roman", 15),
                                                values=["M", "F", "Other", "Prefer Not to say"])
        self.searchreader_gender.place(x=150, y=325)

        books = ["Midnight Years", "Superzero 1", "Superzero 2", "Superzero 3", "Uncool", "When the world went dark"]
        tk.Label(self.searchframe, text="Favourite Book", font=("times new roman", 15), bg="crimson").place(x=25, y=385)
        self.searchreader_favbook = ttk.Combobox(self.searchframe, values=books, font=("Times New Roman", 15))
        self.searchreader_favbook.place(x=150, y=385)

        search_button = tk.Button(searchframe, text="Search", font=("times new roman", 15), command=self.searchreader)
        search_button.place(x=75, y=450, width=300, height=50)

        back_button = tk.Button(searchframe, text="Back", font=("times new roman", 15),
                                command=lambda: self.parent.switch_frame(ManageReader))
        back_button.place(x=75, y=525, width=300, height=50)

    def searchreader(self):

        for i in self.searchreaderlist.get_children():
            self.searchreaderlist.delete(i)

        f = open("reader list.dat", "rb")
        readerdata = pickle.load(f)

        f.close()
        count = 0

        try:
            if self.searchreaderby.get().lower() == "age":

                for rec in readerdata:
                    self.searchreader_name.delete(0, 'end')
                    self.searchreader_gender.delete(0, 'end')
                    self.searchreader_favbook.delete(0, 'end')
                    if int(self.searchreader_agelow.get()) <= rec[2] and int(self.searchreader_agehigh.get()) >= rec[2]:
                        self.searchreaderlist.insert('', index='end', iid=count,
                                                     values=(readerdata[readerdata.index(rec)]))
                    count = count + 1

            if self.searchreaderby.get().lower() == "name":
                self.searchreader_agelow.delete(0, 'end')
                self.searchreader_agehigh.delete(0, 'end')
                self.searchreader_gender.delete(0, 'end')
                self.searchreader_favbook.delete(0, 'end')
                for rec in readerdata:
                    if self.searchreader_name.get() == rec[1]:
                        self.searchreaderlist.insert('', index='end', iid=count,
                                                     values=rec)
                    count = count + 1

            if self.searchreaderby.get().lower() == "gender":
                self.searchreader_agelow.delete(0, 'end')
                self.searchreader_agehigh.delete(0, 'end')
                self.searchreader_name.delete(0, 'end')
                self.searchreader_favbook.delete(0, 'end')
                for rec in readerdata:
                    if self.searchreader_gender.get() == rec[3]:
                        self.searchreaderlist.insert('', index='end', iid=count,
                                                     values=rec)
                    count = count + 1

            if self.searchreaderby.get().lower() == "favourite book":
                self.searchreader_agelow.delete(0, 'end')
                self.searchreader_agehigh.delete(0, 'end')
                self.searchreader_name.delete(0, 'end')

                for rec in readerdata:
                    if self.searchreader_favbook.get() == rec[4]:
                        self.searchreaderlist.insert('', index='end', iid=count,
                                                     values=rec)
                    count = count + 1
        except ValueError:
            msg.showerror("Unable to search", "Please enter valid search values")


class ManageEvent(Main):
    def __init__(self, parent, **kw):
        tk.Frame.__init__(self, parent, bg="blue")
        self.parent = parent
        self.event_widgets()

    # =============EVENT ENTRY =============#
    def event_widgets(self):
        addeventframe = tk.Frame(self, relief="sunken", bg="crimson", bd=4)
        addeventframe.place(x=50, y=50, width=400, height=600)

        tk.Label(addeventframe, text="Add Event", font=("Times New Roman", 25), bg="crimson").place(x=100, y=25)

        tk.Label(addeventframe, text="Event Name:", font=("Times New Roman", 15), bg="crimson").place(x=25, y=100)
        self.event_name = tk.Entry(addeventframe, relief="sunken", font=("Times New Roman", 15))
        self.event_name.place(x=150, y=100)

        self.event_cal = Calendar(addeventframe, selectmode="day", year=2022, month=1, day=12)
        self.event_cal.place(x=75, y=150)

        tk.Label(addeventframe, text="Agenda", font=("Times New Roman", 15), bg="crimson").place(x=25, y=375)
        self.event_agenda = tk.Entry(addeventframe, font=("Times New Roman", 15))
        self.event_agenda.place(x=150, y=375)

        addevent = tk.Button(addeventframe, text="Add Event", font=("Times New Roman", 15),
                             command=self.add_event)
        addevent.place(x=50, y=450, width=300, height=50)

        back_button = tk.Button(addeventframe, text="Back", command=lambda: self.parent.switch_frame(Main))
        back_button.place(x=50, y=525, width=300, height=50)

        # =========EVENT LIST FRAME ===========#

        eventlistframe = tk.Frame(self, relief="sunken", bg="crimson", bd=4)
        eventlistframe.place(x=500, y=50, width=700, height=600)

        self.eventlist = ttk.Treeview(eventlistframe, columns=(1, 2, 3), show="headings")
        self.eventlist.heading(1, text="event name")
        self.eventlist.heading(2, text="date")
        self.eventlist.heading(3, text="agenda")
        self.eventlist.place(x=25, y=25, width=650, height=350)

        updateevent = tk.Button(eventlistframe, text="Update Event Details", font=("Times New Roman", 15),
                                command=self.update_event)
        updateevent.place(x=25, y=425, width=300, height=50)

        deleteevent = tk.Button(eventlistframe, text="Delete Event", font=("times new roman", 15),
                                command=self.delete_event)
        deleteevent.place(x=375, y=425, width=300, height=50)

        edit_button = tk.Button(eventlistframe, text="Edit Event", font=("times new roman", 15),
                                command=self.edit_event)
        edit_button.place(x=25, y=525, width=300, height=50)

        try:
            f = open("event list.dat", "rb")
            eventdata = pickle.load(f)
            f.close()
            print(eventdata)

            count = 0
            for rec in eventdata:
                self.eventlist.insert('', index='end', iid=count,
                                      values=(rec[0], rec[1], rec[2]))
                count += 1

        except FileNotFoundError:
            f = open("event list.dat", "wb")
            eventformat = []
            pickle.dump(eventformat, f)

    def delete_event(self):
        for selected_item in self.eventlist.selection():
            item = self.eventlist.item(selected_item)

            f = open("event list.dat", "rb")

            eventrecord1 = item["values"][0]

            print(eventrecord1)
            eventdata = pickle.load(f)
            f.close()

            for rec in eventdata:

                if rec[0] == eventrecord1:
                    eventdata.pop(eventdata.index(rec))

            h = open("event list.dat", "wb")
            pickle.dump(eventdata, h)
            h.close()
            self.parent.switch_frame(ManageEvent)

    def add_event(self):
        g = open("event list.dat", "rb")
        eventdata = pickle.load(g)
        print(eventdata)
        g.close()

        eventdata.append([self.event_name.get(), self.event_cal.get_date(), self.event_agenda.get()])

        h = open("event list.dat", "wb")
        pickle.dump(eventdata, h)
        h.close()

        self.parent.switch_frame(ManageEvent)

    def edit_event(self):
        x = self.eventlist.selection()
        y = self.eventlist.item(x)
        print(y["values"])

        self.event_name.insert(0, (y["values"])[0])
        self.event_agenda.insert(0, (y["values"])[2])

    def update_event(self):
        f = open("event list.dat", "rb")
        eventdata = pickle.load(f)
        print(eventdata)
        f.close()

        x = self.eventlist.selection()
        y = self.eventlist.item(x)

        for rec in eventdata:
            if rec[0] == y["values"][0]:
                eventdata[eventdata.index(rec)] = [self.event_name.get(), self.event_cal.get_date(),
                                                   self.event_agenda.get()]
                break

        g = open("event list.dat", "wb")
        pickle.dump(eventdata, g)
        g.close()

        self.parent.switch_frame(ManageEvent)


if __name__ == "__main__":
    app = Window()
    app.mainloop()
