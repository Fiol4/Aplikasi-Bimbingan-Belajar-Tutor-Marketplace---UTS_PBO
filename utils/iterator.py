from .data_master import tanya
from .generator import v_dalam

def baris_sesi(s, user):
    lawan = s.tutor if user is s.siswa else s.siswa
    return f"{s} | {lawan.getRole()}: {lawan.nama}"

def pilih_sesi(daftar, user, judul, kosong):
    if not daftar:
        print(f"[INFO] {kosong}")
        return None
    print(f"\n--- {judul} ---")
    for s in daftar: print("  " + baris_sesi(s, user))
    return tanya("Masukkan ID Sesi (0 = batal): ", v_dalam({s.idSesi: s for s in daftar}, "ID sesi tidak ada di daftar!"))