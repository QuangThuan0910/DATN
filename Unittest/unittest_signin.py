import unittest
from unittest.mock import patch, MagicMock
from User_Interface import signin


class TestSignIn(unittest.TestCase):

    @patch('signin.Tk')
    @patch('signin.ImageTk.PhotoImage')
    @patch('signin.PhotoImage')
    def test_signin_window(self, MockPhotoImage, MockImageTk, MockTk):
        mock_tk = MockTk.return_value
        signin.signin()
        self.assertTrue(mock_tk.mainloop.called)

    @patch('signin.get_user')
    @patch('signin.messagebox.showinfo')
    @patch.object(signin, 'usernameEntry', create=True)
    @patch.object(signin, 'passwordEntry', create=True)
    def test_login_user_success(self, mock_usernameEntry, mock_passwordEntry, mock_showinfo, mock_get_user):
        mock_get_user.return_value = MagicMock(password="thuan123")
        mock_usernameEntry.get.return_value = 'testuser'
        mock_passwordEntry.get.return_value = 'thuan123'

        signin.login_user()

        mock_showinfo.assert_called_once_with("Success", "Login successful!")

    @patch('signin.get_user')
    @patch('signin.messagebox.showerror')
    @patch.object(signin, 'usernameEntry', create=True)
    @patch.object(signin, 'passwordEntry', create=True)
    def test_login_user_fail(self, mock_usernameEntry, mock_passwordEntry, mock_showerror, mock_get_user):
        mock_get_user.return_value = MagicMock(password="thuan123")
        mock_usernameEntry.get.return_value = 'testuser'
        mock_passwordEntry.get.return_value = 'thuan123'

        signin.login_user()

        mock_showerror.assert_called_once_with("Error", "Tài khoản không tồn tại hoặc mật khẩu không đúng")

    @patch('signin.Toplevel')
    @patch('signin.ImageTk.PhotoImage')
    @patch('signin.PhotoImage')
    @patch.object(signin, 'login_window', create=True)
    def test_crate_window(self, mock_login_window, MockPhotoImage, MockImageTk, MockToplevel):
        mock_toplevel = MockToplevel.return_value
        signin.crate()
        self.assertTrue(mock_toplevel.mainloop.called)

    @patch('signin.forgot_pw1.forgot_password1')
    @patch.object(signin, 'login_window', create=True)
    def test_show_forgot_password1(self, mock_login_window, mock_forgot_password1):
        mock_login_window.destroy = MagicMock()

        signin.show_forgot_password1()

        mock_login_window.destroy.assert_called_once()
        mock_forgot_password1.assert_called_once()

    def test_hide_password(self):
        mock_entry = MagicMock()
        mock_button = MagicMock()
        mock_show_image = MagicMock()
        mock_hide_image = MagicMock()

        signin.hide_password(mock_entry, mock_button, mock_show_image, mock_hide_image)
        mock_entry.config.assert_called_once_with(show='*')
        mock_button.config.assert_called_once()

    def test_show_password(self):
        mock_entry = MagicMock()
        mock_button = MagicMock()
        mock_show_image = MagicMock()
        mock_hide_image = MagicMock()

        signin.show_password(mock_entry, mock_button, mock_show_image, mock_hide_image)
        mock_entry.config.assert_called_once_with(show='')
        mock_button.config.assert_called_once()


if __name__ == '__main__':
    unittest.main()
