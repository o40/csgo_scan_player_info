import os
import time

class Tailer:

    def Tail(path):
        with open(path, "r", encoding="utf-8") as f:
            f.seek(0, os.SEEK_END)
            while True:
                try:
                   line = f.readline()
                except Exception as e:
                   print(e)
                   pass
                if not line:
                   time.sleep(0.5)
                   continue
                yield line
