import math, re
from datetime import datetime, date
from models.constants import MIN_PASSWORD, LEVEL
from .data_master import tanya

def v_dalam(pilihan, pesan):
    def cek(t):
        if t.upper() not in pilihan: raise ValueError(pesan)
        return pilihan[t.upper()]
    return cek

def v_angka(minimal, maksimal=None, tipe=int):
    def cek(t):
        try:
            n = tipe(t)
        except ValueError:
            raise ValueError("Input harus berupa angka" + (" bulat!" if tipe is int else " (desimal pakai titik, contoh 1.5)!")) from None
        if not math.isfinite(n) or n < minimal or (maksimal is not None and n > maksimal):
            raise ValueError(f"Angka harus antara {minimal:g} dan {maksimal:g}!" if maksimal is not None else f"Angka minimal {minimal:g}!")
        return n
    return cek

def v_nama(t):
    if not re.fullmatch(r"[A-Za-z][A-Za-z .']*", t): raise ValueError("Nama hanya boleh huruf dan spasi, diawali huruf!")
    return t.title()

def v_hp(t):
    if not re.fullmatch(r"[0-9]{10,15}", t): raise ValueError("Nomor HP harus 10-15 digit angka!")
    return t

def v_email(t):
    if not re.fullmatch(r"[\w.+-]+@[\w-]+(\.[\w-]+)+", t): raise ValueError("Format email tidak valid!")
    return t.lower()

def v_password(t):
    if len(t) < MIN_PASSWORD: raise ValueError(f"Password minimal {MIN_PASSWORD} karakter!")
    if any(k.isspace() for k in t): raise ValueError("Password tidak boleh mengandung spasi!")
    if not any(k.isalpha() for k in t): raise ValueError("Password harus memiliki minimal 1 huruf!")
    if not any(k.isdigit() for k in t): raise ValueError("Password harus memiliki minimal 1 angka!")
    if not any(not k.isalnum() for k in t): raise ValueError("Password harus memiliki minimal 1 simbol, contoh !, @, atau #!")
    return t

def v_level(default=None):
    def cek(t):
        t = (t or default or "").upper()
        if t not in LEVEL: raise ValueError("Level harus SD, SMP, atau SMA!")
        return t
    return cek

def v_tidak_kosong(t):
    if not t: raise ValueError("Tidak boleh kosong!")
    return t

def v_tanggal(t):
    try:
        d = datetime.strptime(t, "%Y-%m-%d").date()
    except ValueError:
        raise ValueError("Gunakan format YYYY-MM-DD!") from None
    if d < date.today(): raise ValueError("Tanggal tidak boleh di masa lalu!")
    return d

def v_jam(t):
    try:
        return datetime.strptime(t, "%H:%M").time()
    except ValueError:
        raise ValueError("Gunakan format HH:MM (contoh 09:30)!") from None

def v_waktu(t):
    try:
        dt = datetime.strptime(t, "%Y-%m-%d %H:%M")
    except ValueError:
        raise ValueError("Gunakan format YYYY-MM-DD HH:MM!") from None
    if dt <= datetime.now(): raise ValueError("Waktu harus berada di masa depan!")
    return dt

def pilih_mapel(kecuali=()):
    from models.constants import MAPEL
    pilihan = {str(i): m for i, m in enumerate(MAPEL, 1) if m not in kecuali}
    print("\nPilihan Mapel:")
    for k, m in pilihan.items(): print(f"  {k}. {m}")
    return tanya("Pilih nomor mapel (0 = batal): ", v_dalam(pilihan, "Nomor tidak valid!"))