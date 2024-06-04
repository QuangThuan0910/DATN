from tkinter import *
from tkinter import messagebox
from PIL import Image, ImageTk
from database.database_setup import User
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
import yfinance as yf
from datetime import datetime
from googletrans import Translator
import os
from keras.models import load_model
import pandas as pd

from pythonProject.functions_test import load_stock_data
# Import các hàm cần thiết
from pythonProject.testmodel import predict_future_days, prepare_data, plot_predictions


def hide_password(entry, button, show_image, hide_image):
    entry.config(show='*')
    button.config(image=show_image, command=lambda: show_password(entry, button, show_image, hide_image))

def show_password(entry, button, show_image, hide_image):
    entry.config(show='')
    button.config(image=hide_image, command=lambda: hide_password(entry, button, show_image, hide_image))


def resize_image(image_path, percent):
    image = Image.open(image_path)
    width, height = image.size
    new_width = int(width * percent / 100)
    new_height = int(height * percent / 100)
    resized_image = image.resize((new_width, new_height))
    return ImageTk.PhotoImage(resized_image)

# Hàm xử lý đổi mật khẩu
def change_password(user):
    change_pw_window = Toplevel()
    change_pw_window.geometry('400x300+50+50')
    change_pw_window.resizable(False, False)
    change_pw_window.title('Đổi Mật Khẩu')

    Label(change_pw_window, text="Mật khẩu cũ:", font=('Open Sans', 12)).pack(pady=10)
    old_password_entry = Entry(change_pw_window, width=30, font=('Open Sans', 12), show='*')
    old_password_entry.pack()

    Label(change_pw_window, text="Mật khẩu mới:", font=('Open Sans', 12)).pack(pady=10)
    new_password_entry = Entry(change_pw_window, width=30, font=('Open Sans', 12), show='*')
    new_password_entry.pack()

    Label(change_pw_window, text="Xác nhận mật khẩu mới:", font=('Open Sans', 12)).pack(pady=10)
    confirm_password_entry = Entry(change_pw_window, width=30, font=('Open Sans', 12), show='*')
    confirm_password_entry.pack()

    closeye = 'closeye.png'
    openeye = 'openeye.png'
    closeye = resize_image(closeye, 75)
    openeye = resize_image(openeye, 75)

    eyeButton1 = Button(change_pw_window, image=closeye, bd=0, bg='white', activebackground='white', cursor='hand2',
                        command=lambda: show_password(old_password_entry, eyeButton1, closeye, openeye))
    eyeButton1.place(x=315, y=45)

    eyeButton2 = Button(change_pw_window, image=closeye, bd=0, bg='white', activebackground='white', cursor='hand2',
                        command=lambda: show_password(new_password_entry, eyeButton2, closeye, openeye))
    eyeButton2.place(x=315, y=112)

    eyeButton3 = Button(change_pw_window, image=closeye, bd=0, bg='white', activebackground='white', cursor='hand2',
                        command=lambda: show_password(confirm_password_entry, eyeButton2, closeye, openeye))
    eyeButton3.place(x=315, y=177)

    def update_password():
        old_password = old_password_entry.get()
        new_password = new_password_entry.get()
        confirm_password = confirm_password_entry.get()

        if old_password == user.password:
            if new_password == confirm_password:
                user.password = new_password
                user.save()
                messagebox.showinfo('Thành công', 'Mật khẩu đã được thay đổi.')
                change_pw_window.destroy()
            else:
                messagebox.showerror('Lỗi', 'Mật khẩu mới không khớp.')
        else:
            messagebox.showerror('Lỗi', 'Mật khẩu cũ không đúng.')

    Button(change_pw_window, text="Đổi Mật Khẩu", font=('Open Sans', 12, 'bold'),
            command=update_password).pack(pady=20)

def logout(main_window):
    main_window.destroy()
    import signin
    signin.signin()


def show_menu(menu_frame):
    if menu_frame.winfo_ismapped():
        menu_frame.place_forget()
    else:
        menu_frame.place(x=770, y=80)


def toggle_info(info_frame, user):
    if info_frame.winfo_ismapped():
        info_frame.place_forget()
    else:
        info_frame.place(x=430, y=60)
        # Clear previous content if any
        for widget in info_frame.winfo_children():
            widget.destroy()
        info_frame.config(highlightbackground="black", highlightthickness=2)
        Label(info_frame, text=f"Tài khoản: {user.username}", font=('Open Sans', 14), bg='white').pack(
            pady=5)
        Label(info_frame, text=f"Email: {user.email}", font=('Open Sans', 14), bg='white').pack(pady=5)

def page1(user):
    main_window = Tk()
    main_window.geometry('990x600+50+50')
    main_window.resizable(False, False)
    main_window.title('DỰ ĐOÁN CHỨNG KHOÁN')

    # Tạo frame cố định cho các ô nhập và hình ảnh người dùng
    fixed_frame = Frame(main_window, bg='#f0f0f0')
    fixed_frame.place(x=0, y=0, width=920, height=80)

    # Load hình ảnh người dùng và thêm vào fixed_frame
    user_img_path = 'nguoidung.png'
    if os.path.exists(user_img_path):
        user_img = Image.open(user_img_path)
        user_img = user_img.resize((40, 40))
        user_img_tk = ImageTk.PhotoImage(user_img)
        user_img_label = Label(fixed_frame, image=user_img_tk, cursor="hand2")
        user_img_label.pack(side=RIGHT, padx=10, pady=10)
        user_img_label.bind("<Button-1>", lambda e: show_menu(menu_frame))
    else:
        print(f"User image {user_img_path} not found.")

    # Thêm các ô nhập vào fixed_frame
    Label(fixed_frame, text="Nhập mã chứng khoán:", font=('open Sans', 12), bg='#f0f0f0').pack(side=LEFT,
                                                                                                              padx=10,
                                                                                                              pady=10)
    stock_code_entry = Entry(fixed_frame, width=20, font=('open Sans', 12))
    stock_code_entry.pack(side=LEFT, padx=10, pady=10)

    Label(fixed_frame, text="Nhập số năm dữ liệu:", font=('open Sans', 12), bg='#f0f0f0').pack(side=LEFT,
                                                                                                              padx=10,
                                                                                                              pady=10)
    years_entry = Entry(fixed_frame, width=10, font=('open Sans', 12))
    years_entry.pack(side=LEFT, padx=10, pady=10)

    enter_button = Button(fixed_frame, text="Enter", font=('Open Sans', 12, 'bold'),
                          command=lambda: handle_stock_code(frame, stock_code_entry, years_entry))
    enter_button.pack(side=LEFT, padx=10, pady=10)

    # Create a canvas and a scrollbar
    canvas = Canvas(main_window, bg='#f0f0f0')
    scrollbar = Scrollbar(main_window, orient=VERTICAL, command=canvas.yview)
    canvas.configure(yscrollcommand=scrollbar.set)

    # Pack canvas and scrollbar
    scrollbar.pack(side=RIGHT, fill=Y)
    canvas.pack(side=LEFT, fill=BOTH, expand=True, pady=(80, 0))

    # Create a frame inside the canvas
    frame = Frame(canvas, bg='#f0f0f0')
    canvas.create_window((0, 0), window=frame, anchor='nw')

    # Ensure the canvas scrolls with the mouse wheel
    def on_mouse_wheel(event):
        canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")

    canvas.bind_all("<MouseWheel>", on_mouse_wheel)

    # Tạo Frame cho bảng chọn các chức năng
    menu_frame = Frame(main_window, bg='white')
    menu_frame.place_forget()  # Ẩn frame khi chưa được click

    # Tạo Frame cho thông tin tài khoản
    info_frame = Frame(main_window, bg='white')
    info_frame.place_forget()  # Ẩn frame khi chưa được click

    # Thêm nút vào menu_frame
    Button(menu_frame, text="Thông tin tài khoản", font=('Open Sans', 12, 'bold'), width=20,
           command=lambda: toggle_info(info_frame, user)).pack(pady=5)

    Button(menu_frame, text="Đổi Mật Khẩu", font=('Open Sans', 12, 'bold'), width=20,
           command=lambda: change_password(user)).pack(pady=5)

    Button(menu_frame, text="Đăng Xuất", font=('Open Sans', 12, 'bold'), width=20,
           command=lambda: logout(main_window)).pack(pady=5)

    # Frame cho thông tin chứng khoán
    stock_info_frame = Frame(frame, bg='#f0f0f0')
    stock_info_frame.pack()

    translator = Translator()

    def handle_stock_code(frame, stock_code_entry, years_entry):
        stock_code = stock_code_entry.get()
        years = int(years_entry.get())
        end = datetime.now()
        start = datetime(end.year - years, end.month, end.day)
        data = yf.Ticker(stock_code).history(start=start, end=end)
        google_data = yf.download(stock_code, start, end)
        ticker = yf.Ticker(stock_code)
        info = ticker.info

        if not data.empty:
            for widget in stock_info_frame.winfo_children():
                widget.destroy()

            company_name = translator.translate(info.get('longName', 'N/A'), src='en', dest='vi').text
            sector = translator.translate(info.get('sector', 'N/A'), src='en', dest='vi').text
            industry = translator.translate(info.get('industry', 'N/A'), src='en', dest='vi').text
            employees = info.get('fullTimeEmployees', 'N/A')
            description = translator.translate(info.get('longBusinessSummary', 'N/A'), src='en', dest='vi').text

            Message(stock_info_frame, text=f"Tên công ty: {company_name}", font=('open Sans', 12), bg='#f0f0f0',
                    width=800).pack()
            Message(stock_info_frame, text=f"Ngành: {sector}", font=('open Sans', 12), bg='#f0f0f0', width=800).pack()
            Message(stock_info_frame, text=f"Ngành nghề: {industry}", font=('open Sans', 12), bg='#f0f0f0',
                    width=800).pack()
            Message(stock_info_frame, text=f"Số lượng nhân viên: {employees}", font=('open Sans', 12), bg='#f0f0f0',
                    width=800).pack()
            Message(stock_info_frame, text=f"Mô tả công ty: {description}", font=('open Sans', 12), bg='#f0f0f0',
                    width=800).pack()

            selected_data = google_data[['Open', 'High', 'Low', 'Close', 'Adj Close', 'Volume']]
            data_str = selected_data.to_string()
            data_text_frame = Frame(stock_info_frame)
            data_text_frame.pack(pady=20)
            data_scroll_y = Scrollbar(data_text_frame, orient=VERTICAL)
            data_scroll_x = Scrollbar(data_text_frame, orient=HORIZONTAL)
            data_text = Text(data_text_frame, wrap='none', height=20, yscrollcommand=data_scroll_y.set,
                             xscrollcommand=data_scroll_x.set)
            data_scroll_y.config(command=data_text.yview)
            data_scroll_x.config(command=data_text.xview)
            data_text.insert(END, data_str)
            data_scroll_y.pack(side=RIGHT, fill=Y)
            data_scroll_x.pack(side=BOTTOM, fill=X)
            data_text.pack(side=LEFT, fill=BOTH, expand=True)

            last_close = data['Close'].iloc[-1]
            Message(stock_info_frame, text=f"Mã: {stock_code}, Giá đóng cửa mới nhất: {last_close:.2f}",
                    font=('open Sans', 12), bg='#f0f0f0', width=800).pack()

            fig = Figure(figsize=(10, 5), dpi=100)
            fig.suptitle('Lịch sử giá đóng của của ' + stock_code)
            plot = fig.add_subplot(111)
            plot.plot(data.index, data['Close'], label="Giá đóng cửa")
            plot.legend()
            canvas_chart = FigureCanvasTkAgg(fig, master=stock_info_frame)
            canvas_chart.draw()
            canvas_chart.get_tk_widget().pack()

            stock_data = load_stock_data(stock_code, start, end)
            new_df, last_60days_sc, scaler = prepare_data(stock_data)
            model = load_model('D:/DATN/pythonProject/Latest_stock_price_model.h5')
            predicted_prices = predict_future_days(model, scaler, last_60days_sc, days_to_predict=7)
            Message(stock_info_frame, text=f"Dự đoán giá đóng của điều chỉnh của mã  {stock_code} sau 7 ngày là: {predicted_prices}",
                font=('open Sans', 12), bg='#f0f0f0', width=800).pack()
            last_date = new_df.index[-1]
            predicted_dates = pd.date_range(last_date, periods=8, inclusive='right')
            predicted_df = pd.DataFrame(predicted_prices, index=predicted_dates, columns=['Adj Close'])
            combined_df = pd.concat([new_df, predicted_df])
            fig = Figure(figsize=(10, 5), dpi=100)
            fig.suptitle('Lịch sử giá đóng cửa và dự đoán của ' + stock_code)
            plot = fig.add_subplot(111)
            plot.plot(data.index, data['Close'], label="Giá đóng cửa", color='blue')
            plot.plot(predicted_df.index, predicted_df['Adj Close'], label="Giá dự đoán", color='red')
            plot.legend()
            canvas_chart = FigureCanvasTkAgg(fig, master=stock_info_frame)
            canvas_chart.draw()
            canvas_chart.get_tk_widget().pack()

        else:
            messagebox.showerror('Error', 'No data found for the specified stock code.')

    # Update the scrollregion of the canvas
    def configure_canvas(event):
        canvas.configure(scrollregion=canvas.bbox("all"))

    frame.bind("<Configure>", configure_canvas)
    main_window.mainloop()

if __name__ == "__main__":
    # Ví dụ người dùng để kiểm tra
    user = User(email='test@example.com', username='testuser', password='password123')
    page1(user)


