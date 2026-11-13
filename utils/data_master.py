import getpass, os, sys
from models.exception import Batal

def input_rahasia(prompt):
    if not sys.stdin.isatty(): return getpass.getpass(prompt)
    print(prompt, end="", flush=True)
    karakter = []
    if os.name == "nt":
        import msvcrt
        while True:
            k = msvcrt.getwch()
            if k in ("\r", "\n"): print(); break
            if k == "\003": raise KeyboardInterrupt
            if k in ("\b", "\x7f"):
                if karakter:
                    karakter.pop(); print("\b \b", end="", flush=True)
            elif k in ("\x00", "\xe0"): msvcrt.getwch()
            else:
                karakter.append(k); print("*", end="", flush=True)
    else:
        import termios, tty
        fd = sys.stdin.fileno()
        pengaturan = termios.tcgetattr(fd)
        try:
            tty.setraw(fd)
            while True:
                k = sys.stdin.read(1)
                if k in ("\r", "\n"): print("\r"); break
                if k == "\x03": raise KeyboardInterrupt
                if k in ("\x7f", "\b"):
                    if karakter:
                        karakter.pop(); print("\b \b", end="", flush=True)
                else:
                    karakter.append(k); print("*", end="", flush=True)
        finally:
            termios.tcsetattr(fd, termios.TCSADRAIN, pengaturan)
    return "".join(karakter)

def tanya(prompt, validasi=None, rahasia=False):
    while True:
        teks = (input_rahasia(prompt) if rahasia else input(prompt)).strip()
        if teks == "0": raise Batal()
        try:
            return validasi(teks) if validasi else teks
        except ValueError as e:
            print(f"[ERROR] {e}")