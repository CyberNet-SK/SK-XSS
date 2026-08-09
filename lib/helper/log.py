'''
SK XSS - Log Module
Developer: Sheikh Sabbir
Version: 1.0 Final
'''
from datetime import datetime

# ============ Color Codes ============
W = "\033[93m"
G = "\033[92m"
R = "\033[91m"
B = "\033[94m"
C = "\033[96m"
Y = "\033[93m"
N = "\033[0m"
P = "\033[95m"
M = "\033[1;35m"
# ===================================

class Log:

    @classmethod
    def info(self, text):
        print("[" + Y + datetime.now().strftime("%H:%M:%S") + N + "] [" + G + "INFO" + N + "] " + text)

    @classmethod
    def warning(self, text):
        print("[" + Y + datetime.now().strftime("%H:%M:%S") + N + "] [" + Y + "WARNING" + N + "] " + text)

    @classmethod
    def high(self, text):
        print("[" + Y + datetime.now().strftime("%H:%M:%S") + N + "] [" + R + "CRITICAL" + N + "] " + text)

    @classmethod
    def error(self, text):
        print("[" + Y + datetime.now().strftime("%H:%M:%S") + N + "] [" + R + "ERROR" + N + "] " + text)

    @classmethod
    def success(self, text):
        print("[" + Y + datetime.now().strftime("%H:%M:%S") + N + "] [" + G + "SUCCESS" + N + "] " + text)

    @classmethod
    def debug(self, text):
        print("[" + Y + datetime.now().strftime("%H:%M:%S") + N + "] [" + C + "DEBUG" + N + "] " + text)
