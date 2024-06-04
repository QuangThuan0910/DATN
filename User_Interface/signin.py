from tkinter import *
from PIL import ImageTk, Image
from tkinter import messagebox
import forgot_pw1
from database.database_setup import User, add_user, get_user, get_email  # Import mô hình User và các hàm cơ sở dữ liệu
from page1 import page1  # Đảm bảo rằng bạn nhập hàm page1 đúng cách
import re


# Hàm xử lý quên mật khẩu
def show_forgot_password1():
    login_window.destroy()
    forgot_pw1.forgot_password1()


# Chức năng đăng nhập hiện tại
def username_enter(event):
    if usernameEntry.get() == 'Username':
        usernameEntry.delete(0, END)

def password_enter(event):
    if passwordEntry.get() == 'Password':
        passwordEntry.delete(0, END)

def hide():
    passwordEntry.config(show='*')
    eyeButton.config(image=closeye, command=show)


def show():
    passwordEntry.config(show='')
    eyeButton.config(image=openeye, command=hide)

def hide_password(entry, button, show_image, hide_image):
    entry.config(show='*')
    button.config(image=show_image, command=lambda: show_password(entry, button, show_image, hide_image))

def show_password(entry, button, show_image, hide_image):
    entry.config(show='')
    button.config(image=hide_image, command=lambda: hide_password(entry, button, show_image, hide_image))

def crate():
    # Mở cửa sổ đăng ký
    register_window = Toplevel(login_window)
    register_window.geometry('990x600+50+50')
    register_window.resizable(False, False)
    register_window.title('Đăng Ký Tài Khoản')

    bg_image = ImageTk.PhotoImage(Image.open("bg.jpg"))
    canvas = Canvas(register_window, width=990, height=600)
    canvas.pack(fill="both", expand=True)
    canvas.create_image(0, 0, image=bg_image, anchor="nw")

    heading = Label(register_window, text='CREATE ACCOUNT', font=('open Sans', 16, 'bold'), fg='brown1', bg='white')
    heading.place(x=590, y=110)

    email_label = Label(register_window, text='Email', font=('open Sans', 10, 'bold'), fg='brown1', bg='white')
    email_label.place(x=570, y=150)
    email_entry = Entry(register_window, width=30, font=('open Sans', 10, 'bold'), bg='brown1', fg='white')
    email_entry.place(x=570, y=185)

    username_label = Label(register_window, text='Username', font=('open Sans', 10, 'bold'), fg='brown1', bg='white')
    username_label.place(x=570, y=220)
    username_entry = Entry(register_window, width=30, font=('open Sans', 10, 'bold'), bg='brown1', fg='white')
    username_entry.place(x=570, y=255)

    password_label = Label(register_window, text='Password', font=('open Sans', 10, 'bold'), fg='brown1', bg='white')
    password_label.place(x=570, y=295)

    password_entry = Entry(register_window, width=30, font=('open Sans', 10, 'bold'), bg='brown1', fg='white', show='*')
    password_entry.place(x=570, y=325)

    confirm_password_label = Label(register_window, text='Confirm Password', font=('open Sans', 10, 'bold'),
                                   fg='brown1', bg='white')
    confirm_password_label.place(x=570, y=365)

    confirm_password_entry = Entry(register_window, width=30, font=('open Sans', 10, 'bold'), bg='brown1', fg='white',
                                   show='*')
    confirm_password_entry.place(x=570, y=395)

    closeye = PhotoImage(file='closeye.png')
    openeye = PhotoImage(file='openeye.png')

    eyeButton1 = Button(register_window, image=closeye, bd=0, bg='white', activebackground='white', cursor='hand2',
                        command=lambda: show_password(password_entry, eyeButton1, closeye, openeye))
    eyeButton1.place(x=783, y=322)

    eyeButton2 = Button(register_window, image=closeye, bd=0, bg='white', activebackground='white', cursor='hand2',
                        command=lambda: show_password(confirm_password_entry, eyeButton2, closeye, openeye))
    eyeButton2.place(x=783, y=392)

    def register_user():
        email = email_entry.get()
        username = username_entry.get()
        password = password_entry.get()
        confirm_password = confirm_password_entry.get()

        if email == '' or username == '' or password == '':
            messagebox.showerror('Error', 'Vui lòng điền đầy đủ thông tin.')
            return
        if get_user(username):
            messagebox.showerror('Error', 'Tài khoản đã tồn tại. Vui lòng chọn tài khoản khác.')
            return
        if get_email(email):
            messagebox.showerror('Error', 'Email đã được sử dụng. Vui lòng chọn email khác.')
            return
        if password != confirm_password:
            messagebox.showerror("Error", "Passwords do not match. Please try again.")
            return
        else:
            add_user(username, password, email)
            messagebox.showinfo('Success', 'Đăng ký thành công')
            register_window.destroy()

    register_button = Button(register_window, text="Đăng Ký", font=('Open Sans', 16, 'bold'), fg='white', bg='brown1',
                             activeforeground='white', activebackground='brown1', cursor='hand2', bd=0, width=19,
                             command=register_user)
    register_button.place(x=570, y=450)
    register_window.mainloop()

def login_user():
    if usernameEntry.get() == '' or passwordEntry.get() == '':
        messagebox.showerror('Error', 'Chưa nhập tài khoản hoặc mật khẩu')
    else:
        user = get_user(usernameEntry.get())
        if user and user.password == passwordEntry.get():
            messagebox.showinfo('Welcome', 'Đăng nhập thành công')
            login_window.destroy()
            page1(user)  # Chuyển sang trang chính sau khi đăng nhập thành công và truyền thông tin người dùng
        else:
            messagebox.showerror('Error', 'Tài khoản không tồn tại hoặc mật khẩu không đúng')


# Giao diện người dùng
def signin():
    global login_window, bgImage, openeye, closeye, eyeButton
    login_window = Tk()
    login_window.geometry('990x600+50+50')
    login_window.resizable(False, False)
    login_window.title('DỰ ĐOÁN CHỨNG KHOÁN')
    bgImage = ImageTk.PhotoImage(file='bg.jpg')

    bgLabel = Label(login_window, image=bgImage)
    bgLabel.place(x=0, y=0)

    heading = Label(login_window, text='USER LOGIN', font=('Microsoft Yahei UI Light', 23, 'bold'), bg='white',
                    fg='brown1')
    heading.place(x=605, y=120)

    global usernameEntry
    usernameEntry = Entry(login_window, width=25, font=('Microsoft Yahei UI Light', 11, 'bold'), bd=0, fg='brown1')
    usernameEntry.place(x=580, y=200)
    usernameEntry.insert(0, 'Username')
    usernameEntry.bind('<FocusIn>', username_enter)

    global passwordEntry
    passwordEntry = Entry(login_window, width=25, font=('Microsoft Yahei UI Light', 11, 'bold'), bd=0, fg='brown1',
                          show='*')
    passwordEntry.place(x=580, y=260)
    passwordEntry.insert(0, 'Password')
    passwordEntry.bind('<FocusIn>', password_enter)

    Frame1 = Frame(login_window, width=250, height=2, bg='brown1')
    Frame1.place(x=580, y=222)

    Frame2 = Frame(login_window, width=250, height=2, bg='brown1')
    Frame2.place(x=580, y=282)

    closeye = PhotoImage(file='closeye.png')
    openeye = PhotoImage(file='openeye.png')
    eyeButton = Button(login_window, image=closeye, bd=0, bg='white', activebackground='white', cursor='hand2',
                       command=show)
    eyeButton.place(x=800, y=255)

    forgetpassword = Button(login_window, text='Forgot Password?', bd=0, bg='white', activebackground='white',
                            cursor='hand2', font=('Microsoft Yahei UI Light', 9, 'bold'), fg='brown1',
                            activeforeground='brown1', command=show_forgot_password1)
    forgetpassword.place(x=715, y=295)

    loginButtonn = Button(login_window, text='LOGIN', font=('Open Sans', 16, 'bold'), fg='white', bg='brown1',
                          activeforeground='white', activebackground='brown1', cursor='hand2', bd=0, width=19,
                          command=login_user)
    loginButtonn.place(x=578, y=355)

    orlable = Label(login_window, text='--------------OR-------------', font=('open Sans', 16), fg='brown1', bg='white')
    orlable.place(x=583, y=400)

    fb_logo = PhotoImage(file='facebook.png')
    fbLabel = Label(login_window, image=fb_logo, bg='white')
    fbLabel.place(x=630, y=450)

    gg_logo = PhotoImage(file='google.png')
    ggLabel = Label(login_window, image=gg_logo, bg='white')
    ggLabel.place(x=690, y=450)

    tw_logo = PhotoImage(file='twitter.png')
    twLabel = Label(login_window, image=tw_logo, bg='white')
    twLabel.place(x=750, y=450)

    sgnlable = Label(login_window, text="Don't have an account?", font=('open Sans', 9, 'bold'), fg='brown1',
                     bg='white')
    sgnlable.place(x=570, y=500)
    newacc = Button(login_window, text='Create account', bd=0, bg='white', activebackground='white', cursor='hand2',
                    font=('open Sans', 9, 'bold'), fg='blue', activeforeground='brown1', command=crate)
    newacc.place(x=700, y=500)

    login_window.mainloop()


if __name__ == "__main__":
    signin()
