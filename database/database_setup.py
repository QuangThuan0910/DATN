from peewee import *
import pymysql

# Kết nối đến cơ sở dữ liệu MySQL trên máy chủ
db = MySQLDatabase(
    'datn',  # Tên cơ sở dữ liệu
    user='root',  # Tên người dùng MySQL
    password='',  # Mật khẩu MySQL
    host='localhost',  # Địa chỉ IP hoặc tên miền của máy chủ MySQL
    port=3306  # Cổng mặc định của MySQL là 3306
)

class User(Model):
    id = AutoField()  # Khóa chính tự động tăng
    email = CharField(unique=True)
    username = CharField(unique=True)
    password = CharField()
    # verification_code = CharField(null=True)

    class Meta:
        database = db  # Mô hình này sử dụng cơ sở dữ liệu đã kết nối

# Tạo bảng nếu chưa tồn tại
def create_tables():
    with db:
        db.create_tables([User])

# Hàm thêm người dùng ví dụ
def add_user(email, username, password):
    try:
        user = User.create(email=email, username=username, password=password)
        print(f"Người dùng {username} đã được thêm thành công.")
    except IntegrityError as e:
        print(f"Lỗi: {e}")

# Hàm lấy thông tin người dùng ví dụ
def get_user(username):
    try:
        user = User.get(User.username == username)
        return user
    except DoesNotExist:
        print("Lỗi: Người dùng không tồn tại.")
        return None

def get_email(email):
    try:
        email = User.get(User.email == email)
        return email
    except DoesNotExist:
        print("Lỗi: Email không tồn tại.")
        return None

if __name__ == "__main__":
    # Tạo bảng
    create_tables()
    # Ví dụ sử dụng
    add_user('test@example.com', 'testuser', 'password123')
    user = get_user('testuser')
    if user:
        print(f"Người dùng lấy được: {user.username}, {user.email}")
