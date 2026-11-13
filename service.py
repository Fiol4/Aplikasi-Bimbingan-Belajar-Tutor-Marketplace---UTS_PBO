from models import Siswa, Tutor, rp
from models.constants import MAPEL, MIN_TARIF, MIN_PASSWORD
from utils import tanya, v_dalam, v_angka, v_nama, v_hp, v_email, v_password, v_level, pilih_mapel, baris_sesi

def registrasi(app):
    print("\n--- REGISTRASI AKUN (ketik 0 kapan saja untuk batal) ---")
    print("1. Siswa\n2. Tutor")
    peran = tanya("Daftar sebagai (1/2): ", v_dalam({"1": "Siswa", "2": "Tutor"}, "Pilih 1 atau 2!"))

    def hp_baru(t):
        t = v_hp(t)
        if any(u.noHp == t for u in app.semua_user()): raise ValueError("Nomor HP sudah terdaftar!")
        return t

    def email_baru(t):
        t = v_email(t)
        if any(u.email == t for u in app.semua_user()): raise ValueError("Email sudah terdaftar!")
        return t

    nama = tanya("Nama: ", v_nama)
    hp = tanya("No HP: ", hp_baru)
    email = tanya("Email: ", email_baru)
    while True:
        password = tanya(f"Password (min {MIN_PASSWORD} karakter, wajib huruf, angka, dan simbol): ", v_password, rahasia=True)
        if password == tanya("Konfirmasi Password: ", rahasia=True): break
        print("[ERROR] Konfirmasi password tidak cocok, ulangi.")

    if peran == "Siswa":
        jenjang = tanya("Jenjang (SD/SMP/SMA): ", v_level())
        user = Siswa(app.id_baru("S", app.daftar_siswa), nama, email, password, hp, jenjang)
    else:
        level = tanya("Level mengajar (SD/SMP/SMA): ", v_level())
        mapel_tarif = {}
        while True:
            mapel = pilih_mapel(kecuali=mapel_tarif)
            mapel_tarif[mapel] = tanya(f"Tarif per jam {mapel} (Rp, min {MIN_TARIF}): ", v_angka(MIN_TARIF))
            if len(mapel_tarif) == len(MAPEL): break
            if not tanya("Tambah mapel lain? (1=Ya, 2=Tidak): ", v_dalam({"1": True, "2": False}, "Pilih 1 atau 2!")): break
        user = Tutor(app.id_baru("T", app.daftar_tutor), nama, email, password, hp, mapel_tarif, level)

    app.tambah_user(user)
    print(f"[SUKSES] {user.getRole()} {nama} terdaftar. ID: {user.id}. Silakan login.")

def lupa_password(app):
    print("\n--- RESET PASSWORD (ketik 0 untuk kembali) ---")
    email = tanya("Email terdaftar: ", v_email)
    no_hp = tanya("Nomor HP terdaftar: ", v_hp)

    user = next((u for u in app.semua_user() if u.email == email and u.noHp == no_hp), None)
    if not user:
        print("[ERROR] Email atau nomor HP tidak cocok dengan akun terdaftar.")
        return

    while True:
        password = tanya(f"Password baru (min {MIN_PASSWORD} karakter, wajib huruf, angka, dan simbol): ", v_password, rahasia=True)
        konfirmasi = tanya("Konfirmasi password baru: ", rahasia=True)
        if password == konfirmasi: break
        print("[ERROR] Konfirmasi password tidak cocok, silakan ulangi.")

    salt_lama, hash_lama = user._salt, user._password_hash
    user.ganti_password(password)
    if not app.simpan():
        user._salt, user._password_hash = salt_lama, hash_lama
        print("[GAGAL] Password tidak diubah karena data gagal disimpan.")
        return
    print("[SUKSES] Password berhasil diubah. Silakan login dengan password baru.")

def lihat_riwayat(user):
    if not user.riwayat_sesi:
        print("[INFO] Belum ada sesi.")
        return
    print("\n--- RIWAYAT SESI ---")
    for s in user.riwayat_sesi: print("  " + baris_sesi(s, user))