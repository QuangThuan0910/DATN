from tkinter import *
from PIL import ImageTk
from tkinter import messagebox
import signin
from database.database_setup import User

def hide_password(entry, button, show_image, hide_image):
    entry.config(show='*')
    button.config(image=show_image, command=lambda: show_password(entry, button, show_image, hide_image))

def show_password(entry, button, show_image, hide_image):
    entry.config(show='')
    button.config(image=hide_image, command=lambda: hide_password(entry, button, show_image, hide_image))

def forgot_password2():
    global forgot_pw2_window, bgImage
    forgot_pw2_window = Tk()
    forgot_pw2_window.geometry('990x600+50+50')
    forgot_pw2_window.resizable(False, False)
    forgot_pw2_window.title('Forgot Password')
    bgImage = ImageTk.PhotoImage(file='bg.jpg')

    bgLabel = Label(forgot_pw2_window, image=bgImage)
    bgLabel.place(x=0, y=0)

    heading = Label(forgot_pw2_window, text='FORGOT PASSWORD', font=('open Sans', 16, 'bold'), fg='brown1', bg='white')
    heading.place(x=580, y=110)

    code_label = Label(forgot_pw2_window, text = 'Enter your verification code:',font=('open Sans',10,'bold'),fg = 'brown1',bg='white')
    code_label.place(x=580, y=166)
    global code_entry
    code_entry = Entry(forgot_pw2_window, width=30,font=('open Sans',10,'bold'), bg ='brown1',fg='white')
    code_entry.place(x=580, y=194)

    new_password_label = Label(forgot_pw2_window, text="Enter new password:", font=('open Sans',10,'bold'),fg = 'brown1',bg='white')
    new_password_label.place(x=580, y=252)

    global new_password_entry
    new_password_entry = Entry(forgot_pw2_window, width=30,font=('open Sans',10,'bold'), bg ='brown1',fg='white', show='*')
    new_password_entry.place(x=580, y=286)

    confirm_password_label = Label(forgot_pw2_window, text="Confirm new password:", font=('open Sans',10,'bold'),fg = 'brown1',bg='white')
    confirm_password_label.place(x=580, y=348)

    global confirm_password_entry
    confirm_password_entry = Entry(forgot_pw2_window, width=30,font=('open Sans',10,'bold'), bg ='brown1',fg='white', show='*')
    confirm_password_entry.place(x=580, y=380)

    closeye = PhotoImage(file='closeye.png')
    openeye = PhotoImage(file='openeye.png')

    eyeButton1 = Button(forgot_pw2_window, image=closeye, bd=0, bg='white', activebackground='white', cursor='hand2',
                        command=lambda: show_password(new_password_entry, eyeButton1, closeye, openeye))
    eyeButton1.place(x=796, y=283)

    eyeButton2 = Button(forgot_pw2_window, image=closeye, bd=0, bg='white', activebackground='white', cursor='hand2',
                        command=lambda: show_password(confirm_password_entry, eyeButton2, closeye, openeye))
    eyeButton2.place(x=796, y=377)

    submit_button = Button(forgot_pw2_window, text="Submit", font=('Open Sans', 14, 'bold'), fg='white', bg='brown1',
                           activeforeground='white', activebackground='brown1', cursor='hand2', bd=0, width=19, command=reset_password)
    submit_button.place(x=580, y=450)

    forgot_pw2_window.mainloop()

def reset_password():
    code = code_entry.get()
    new_password = new_password_entry.get()
    confirm_password = confirm_password_entry.get()

    if new_password != confirm_password:
        messagebox.showerror('Error', 'Passwords do not match.')
        return

    try:
        user = User.get(User.email == email)
        if user.verification_code == code:
            user.password = new_password  # Ensure to hash the password in a real application
            user.verification_code = None
            user.save()
            messagebox.showinfo('Success', 'Password has been reset.')
        else:
            messagebox.showerror('Error', 'Invalid verification code.')
    except User.DoesNotExist:
        messagebox.showerror('Error', 'Email not found.')
