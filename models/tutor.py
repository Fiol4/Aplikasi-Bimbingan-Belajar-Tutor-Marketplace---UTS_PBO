from datetime import datetime
from .user import User, rp
from .exception import JadwalBentrokError

class Tutor(User):
    def __init__(self, id_user, nama, email, password, noHp, daftar_mapel, level):
        super().__init__(id_user, nama, email, password, noHp)
        self.daftar_mapel = daftar_mapel
        self.level = level
        self.jadwal = []

    def getRole(self): return "Tutor"

    def ringkasan(self):
        mapel = ", ".join(f"{m} ({rp(t)}/jam)" for m, t in self.daftar_mapel.items())
        return f"[Tutor] {self.id} | {self.nama} | Level {self.level} | HP {self.noHp} | Saldo {rp(self.saldo)}\n        Mapel: {mapel}"

    def get_tarif(self, mapel) -> int: return self.daftar_mapel[mapel]

    def set_jadwal(self, mulai, selesai) -> None:
        if mulai <= datetime.now(): raise ValueError("Jadwal harus berada di masa depan!")
        if selesai <= mulai: raise ValueError("Jam selesai harus lebih besar dari jam mulai!")
        for m, s in self.jadwal:
            if mulai < s and selesai > m:
                raise JadwalBentrokError(f"Jadwal bertabrakan dengan jadwal {m:%Y-%m-%d %H:%M}-{s:%H:%M}!")
        self.jadwal.append((mulai, selesai))
        self.jadwal.sort()

    def jadwal_mendatang(self): return [(m, s) for m, s in self.jadwal if s > datetime.now()]

    def cek_ketersediaan(self, mulai, selesai) -> bool:
        dalam_jadwal = any(m <= mulai and selesai <= s for m, s in self.jadwal)
        return dalam_jadwal and not self.ada_bentrok(mulai, selesai)