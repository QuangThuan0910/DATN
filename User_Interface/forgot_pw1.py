from tkinter import *
from PIL import ImageTk
from tkinter import messagebox
import forgot_pw2
from database.database_setup import User
import random
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import smtplib


def generate_verification_code():
    return str(random.randint(100000, 999999))

def send_verification_email(to_email, verification_code):
    from_email = 'your_email@example.com'  # Replace with your email
    from_password = 'your_email_password'  # Replace with your email password

    subject = 'Your Verification Code'
    body = f'Your verification code is {verification_code}'

    msg = MIMEMultipart()
    msg['From'] = from_email
    msg['To'] = to_email
    msg['Subject'] = subject

    msg.attach(MIMEText(body, 'plain'))

    try:
        server = smtplib.SMTP('smtp.example.com', 587)  # Replace with your SMTP server and port
        server.starttls()
        server.login(from_email, from_password)
        text = msg.as_string()
        server.sendmail(from_email, to_email, text)
        server.quit()
        print('Email sent successfully')
    except Exception as e:
        print(f'Failed to send email: {e}')

def submit_email():
    email = email_entry.get()
    if email:
        code = generate_verification_code()
        try:
            user = User.get(User.email == email)
            user.verification_code = code
            user.save()
            send_verification_email(email, code)
            messagebox.showinfo('Success', 'Verification code sent to your email.')
        except User.DoesNotExist:
            messagebox.showerror('Error', 'Email not found.')
    else:
        messagebox.showerror('Error', 'Please enter an email address.')

def forgot_password1():
    global forgot_pw1_window, bgImage
    forgot_pw1_window = Tk()
    forgot_pw1_window.geometry('990x600+50+50')
    forgot_pw1_window.resizable(False, False)
    forgot_pw1_window.title('Forgot Password')
    bgImage = ImageTk.PhotoImage(file='bg.jpg')

    bgLabel = Label(forgot_pw1_window, image=bgImage)
    bgLabel.place(x=0, y=0)

    heading = Label(forgot_pw1_window, text='FORGOT PASSWORD', font=('open Sans',16,'bold'),fg = 'brown1',bg='white')
    heading.place(x=580, y=110)

    email_label = Label(forgot_pw1_window ,text = 'Email',font=('open Sans',10,'bold'),fg = 'brown1',bg='white')
    email_label.place(x=565, y=150)
    global email_entry
    email_entry = Entry(forgot_pw1_window, width=30,font=('open Sans',10,'bold'), bg ='brown1',fg='white')
    email_entry.place(x=580, y=200)

    send_code_button = Button(forgot_pw1_window ,text="Send Code", font=('Open Sans', 16, 'bold'), fg='white', bg='brown1',
                             activeforeground='white', activebackground='brown1', cursor='hand2', bd=0, width=19,
                             command=send_code)
    send_code_button.place(x=580, y=250)

    forgot_pw1_window.mainloop()


def send_code():
    # Placeholder for code to send the verification code to the email
    messagebox.showinfo("Info", "Verification code sent to your email.")
    forgot_pw1_window.destroy()
    forgot_pw2.forgot_password2()
