import win32con
import ctypes
import ctypes.wintypes

class CsGoCommunicator:

    class COPYDATASTRUCT(ctypes.Structure):
        _fields_ = [
            ('dwData', ctypes.wintypes.LPARAM),
            ('cbData', ctypes.wintypes.DWORD),
            ('lpData', ctypes.c_char_p)
        ]

    def __init__(self, message_type):
        self.message_type = message_type

    def SendMessage(self, s):
        """ Send WM_COPYDATA to the cs go process """
        message = f"{self.message_type} {s}"

        FindWindow = ctypes.windll.user32.FindWindowW
        hwnd = FindWindow(None, 'Counter-Strike: Global Offensive')
        cds = self.COPYDATASTRUCT()
        cds.dwData = 0
        bytestring_to_send = message.encode()
        cds.cbData = ctypes.sizeof(ctypes.create_string_buffer(bytestring_to_send))
        cds.lpData = ctypes.c_char_p(bytestring_to_send)

        SendMessage = ctypes.windll.user32.SendMessageW
        SendMessage(hwnd, win32con.WM_COPYDATA, 0, ctypes.byref(cds))