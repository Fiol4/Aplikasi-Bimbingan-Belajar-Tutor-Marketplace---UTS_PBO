from datetime import timedelta
from .constants import PENDING, APPROVED, REJECTED, ONGOING, COMPLETED, STATUS_AKTIF
from .exception import StatusSesiError, rp

class Sesi:
    def __init__(self, idSesi, siswa, tutor, mapel, waktu, durasi):
        self.idSesi = idSesi
        self.siswa = siswa
        self.tutor = tutor
        self.mapel = mapel
        self.waktu = waktu
        self.durasi = durasi
        self.tarif = tutor.get_tarif(mapel)
        self.status = PENDING
        self.lunas = False
        self.materi = ""

    @property
    def waktu_selesai(self): return self.waktu + timedelta(hours=self.durasi)
    @property
    def aktif(self): return self.status in STATUS_AKTIF
    def hitung_biaya(self) -> int: return round(self.durasi * self.tarif)
    def bentrok(self, mulai, selesai) -> bool: return mulai < self.waktu_selesai and selesai > self.waktu

    def _pindah(self, dari, ke):
        if self.status != dari: raise StatusSesiError(f"Aksi tidak valid: status sesi {self.status}, seharusnya {dari}.")
        self.status = ke

    def setujui(self): self._pindah(PENDING, APPROVED)
    def tolak(self): self._pindah(PENDING, REJECTED)

    def mulai(self):
        if self.status == APPROVED and not self.lunas: raise StatusSesiError("Siswa belum membayar sesi ini.")
        self._pindah(APPROVED, ONGOING)

    def selesaikan(self, materi):
        if not materi.strip(): raise ValueError("Catatan materi tidak boleh kosong!")
        self._pindah(ONGOING, COMPLETED)
        self.materi = materi.strip()

    def __str__(self):
        teks = (f"[{self.idSesi}] {self.status:<9} | {self.mapel} | {self.waktu:%Y-%m-%d %H:%M} "
                f"({self.durasi:g} jam) | {rp(self.hitung_biaya())} ({'Lunas' if self.lunas else 'Belum bayar'})")
        return teks + (f" | Materi: {self.materi}" if self.materi else "")