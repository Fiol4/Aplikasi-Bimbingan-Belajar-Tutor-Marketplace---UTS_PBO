import os, pickle
from datetime import datetime, timedelta
from .constants import DB_FILE, DB_VERSI, MAX_DURASI
from .siswa import Siswa
from .tutor import Tutor
from .sesi import Sesi
from .exception import TutorNotAvailableException, JadwalBentrokError

class PengelolaAplikasi:
    def __init__(self):
        self.daftar_siswa = []
        self.daftar_tutor = []
        self.pengguna_aktif = None
        self._muat()

    def _muat(self):
        if not os.path.exists(DB_FILE): return
        try:
            with open(DB_FILE, "rb") as f: data = pickle.load(f)
            if not isinstance(data, dict) or data.get("versi") != DB_VERSI: raise ValueError("versi database tidak cocok")
            siswa, tutor = data.get("siswa"), data.get("tutor")
            if not isinstance(siswa, list) or not isinstance(tutor, list): raise ValueError("isi database tidak valid")
            self.daftar_siswa, self.daftar_tutor = siswa, tutor
        except Exception as e:
            cadangan = DB_FILE + ".bak"
            nomor = 1
            while os.path.exists(cadangan):
                cadangan = DB_FILE + f".bak{nomor}"
                nomor += 1
            try: os.replace(DB_FILE, cadangan)
            except OSError as err:
                raise RuntimeError(f"Database gagal dibaca ({e}) dan tidak bisa dicadangkan ({err}). Program dihentikan agar data lama tidak tertimpa.") from err
            print(f"[INFO] Database tidak kompatibel ({e}). File asli diamankan ke {cadangan}; aplikasi dimulai dengan data kosong.")

    def simpan(self) -> bool:
        tmp = DB_FILE + ".tmp"
        try:
            with open(tmp, "wb") as f:
                pickle.dump({"versi": DB_VERSI, "siswa": self.daftar_siswa, "tutor": self.daftar_tutor}, f)
                f.flush(); os.fsync(f.fileno())
            os.replace(tmp, DB_FILE)
            return True
        except Exception as e:
            try:
                if os.path.exists(tmp): os.remove(tmp)
            except OSError: pass
            print(f"[PERINGATAN] Data gagal disimpan ke file: {e}. Perubahan belum aman tersimpan.")
            return False

    def semua_user(self): return self.daftar_siswa + self.daftar_tutor

    def id_baru(self, prefix, daftar):
        nomor = len(daftar) + 1
        id_terpakai = {u.id for u in daftar}
        while f"{prefix}{nomor:03d}" in id_terpakai: nomor += 1
        return f"{prefix}{nomor:03d}"

    def tambah_user(self, user):
        {"Siswa": self.daftar_siswa, "Tutor": self.daftar_tutor}[user.getRole()].append(user)
        self.simpan()

    def login(self, email, password):
        user = next((u for u in self.semua_user() if u.email == email.lower()), None)
        if user and user.verifikasi_password(password):
            self.pengguna_aktif = user
            return user
        return None

    def logout(self): self.pengguna_aktif = None

    def cari_tutor(self, mapel, level):
        return [t for t in self.daftar_tutor if t.level == level and mapel in t.daftar_mapel]

    def buat_booking(self, siswa, tutor, mapel, waktu, durasi) -> Sesi:
        if mapel not in tutor.daftar_mapel: raise ValueError(f"Tutor {tutor.nama} tidak mengajar {mapel}.")
        if not 0 < durasi <= MAX_DURASI: raise ValueError(f"Durasi harus lebih dari 0 dan maksimal {MAX_DURASI} jam!")
        if waktu <= datetime.now(): raise ValueError("Waktu booking harus berada di masa depan!")
        selesai = waktu + timedelta(hours=durasi)
        if not tutor.cek_ketersediaan(waktu, selesai):
            raise TutorNotAvailableException(f"Tutor {tutor.nama} tidak tersedia pada {waktu:%Y-%m-%d %H:%M} selama {durasi:g} jam (di luar jadwalnya atau sudah dibooking).")
        if siswa.ada_bentrok(waktu, selesai): raise JadwalBentrokError("Anda sudah punya booking lain di jam tersebut!")
        
        id_terpakai = {s.idSesi for u in self.semua_user() for s in u.riwayat_sesi}
        nomor = 1
        while f"SESI-{nomor:03d}" in id_terpakai: nomor += 1
        
        sesi = Sesi(f"SESI-{nomor:03d}", siswa, tutor, mapel, waktu, durasi)
        siswa.riwayat_sesi.append(sesi)
        tutor.riwayat_sesi.append(sesi)
        self.simpan()
        return sesi