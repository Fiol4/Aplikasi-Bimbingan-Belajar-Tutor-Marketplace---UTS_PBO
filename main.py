from models import PengelolaAplikasi, Batal, BimbelError, rp
from services import *
from utils import tanya, v_email

def jalankan_menu(judul, opsi):
    while True:
        print(f"\n=== {judul} ===")
        for k, (label, _) in opsi.items(): print(f"{k}. {label}")
        print("0. Logout")
        pilihan = input("Pilih menu: ").strip()
        if pilihan == "0": return
        if pilihan not in opsi:
            print("[ERROR] Pilihan tidak valid."); continue
        try:
            opsi[pilihan][1]()
        except Batal: print("[INFO] Dibatalkan.")
        except (BimbelError, ValueError) as e: print(f"[GAGAL] {e}")

def menu_siswa(app, siswa):
    jalankan_menu(f"MENU SISWA (Halo, {siswa.nama})", {
        "1": ("Cari & Booking Tutor", lambda: siswa_booking(app, siswa)),
        "2": ("Bayar Sesi (Wallet)", lambda: siswa_bayar(app, siswa)),
        "3": ("Isi Saldo", lambda: siswa_isi_saldo(app, siswa)),
        "4": ("Riwayat Booking", lambda: lihat_riwayat(siswa)),
        "5": ("Profil Saya", lambda: print(siswa.ringkasan())),
    })

def menu_tutor(app, tutor):
    jalankan_menu(f"MENU TUTOR (Halo, {tutor.nama})", {
        "1": ("Atur Jadwal Ketersediaan", lambda: tutor_jadwal(app, tutor)),
        "2": ("Setujui / Tolak Booking", lambda: tutor_persetujuan(app, tutor)),
        "3": ("Mulai Sesi", lambda: tutor_mulai(app, tutor)),
        "4": ("Selesaikan Sesi & Catat Materi", lambda: tutor_selesai(app, tutor)),
        "5": ("Riwayat Mengajar", lambda: lihat_riwayat(tutor)),
        "6": ("Profil Saya", lambda: print(tutor.ringkasan())),
    })

MENU_PER_ROLE = {"Siswa": menu_siswa, "Tutor": menu_tutor}

def login(app):
    print("\n--- LOGIN (ketik 0 untuk kembali) ---")
    while True:
        email = tanya("Email: ", v_email)
        password = tanya("Password: ", rahasia=True)
        user = app.login(email, password)
        if user: break
        print("[ERROR] Email/password salah, atau akun belum terdaftar. Silakan Registrasi dulu bila belum punya akun.")
    print(f"\n[SUKSES] Selamat datang, {user.nama} ({user.getRole()})!")
    try:
        MENU_PER_ROLE[user.getRole()](app, user)
    finally:
        app.logout()
        print("[INFO] Logout berhasil.")

def main():
    try:
        app = PengelolaAplikasi()
    except RuntimeError as e:
        print(f"[FATAL] {e}"); return
        
    try:
        while True:
            print("\n" + "=" * 45 + "\n" + "BIMBEL ONLINE - MENU AWAL".center(45) + "\n" + "=" * 45)
            print("1. Registrasi Akun\n2. Login\n3. Lupa Password\n0. Keluar")
            pilihan = input("Pilih menu: ").strip()
            if pilihan == "0": break
            try:
                if pilihan == "1": registrasi(app)
                elif pilihan == "2": login(app)
                elif pilihan == "3": lupa_password(app)
                else: print("[ERROR] Pilihan tidak valid.")
            except Batal: print("[INFO] Dibatalkan.")
            except (BimbelError, ValueError) as e: print(f"[GAGAL] {e}")
    except (KeyboardInterrupt, EOFError):
        print("\n[INFO] Program dihentikan.")
        
    app.simpan()
    print("Terima kasih!")

if __name__ == "__main__":
    main()