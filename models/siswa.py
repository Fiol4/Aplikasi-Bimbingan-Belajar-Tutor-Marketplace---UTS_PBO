from .user import User, rp
from .constants import APPROVED
from .exception import StatusSesiError

class Siswa(User):
    def __init__(self, id_user, nama, email, password, noHp, jenjang, saldo=0):
        super().__init__(id_user, nama, email, password, noHp, saldo)
        self.jenjang = jenjang

    def getRole(self): return "Siswa"

    def ringkasan(self):
        return f"[Siswa] {self.id} | {self.nama} | Jenjang {self.jenjang} | HP {self.noHp} | Saldo {rp(self.saldo)}"

    def bayar(self, sesi) -> int:
        if sesi.siswa is not self: raise StatusSesiError("Ini bukan sesi milik Anda.")
        if sesi.status != APPROVED: raise StatusSesiError(f"Sesi berstatus {sesi.status}; hanya sesi APPROVED yang bisa dibayar.")
        if sesi.lunas: raise StatusSesiError("Sesi ini sudah dibayar.")

        biaya = sesi.hitung_biaya()
        self.potong_saldo(biaya)
        try:
            sesi.tutor.tambah_saldo(biaya)
            sesi.lunas = True
        except Exception:
            self._saldo += biaya
            raise
        return biaya