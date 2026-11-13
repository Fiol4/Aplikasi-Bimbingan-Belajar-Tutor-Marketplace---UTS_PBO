from abc import ABC, abstractmethod
import hashlib
import secrets
from .exception import SaldoTidakCukupError, rp

class User(ABC):
    def __init__(self, id_user, nama, email, password, noHp, saldo=0):
        self._id = id_user
        self.nama = nama
        self._email = email
        self._noHp = noHp
        self._saldo = saldo
        self._salt = secrets.token_hex(16)
        self._password_hash = self._hash(password)
        self.riwayat_sesi = []

    def _hash(self, password):
        return hashlib.pbkdf2_hmac("sha256", password.encode(), self._salt.encode(), 100_000).hex()

    def verifikasi_password(self, password) -> bool:
        return secrets.compare_digest(self._hash(password), self._password_hash)

    def ganti_password(self, password):
        self._salt = secrets.token_hex(16)
        self._password_hash = self._hash(password)

    @property
    def id(self): return self._id
    @property
    def email(self): return self._email
    @property
    def noHp(self): return self._noHp
    @property
    def saldo(self): return self._saldo

    def tambah_saldo(self, jumlah) -> None:
        if jumlah <= 0: raise ValueError("Jumlah saldo harus lebih besar dari 0!")
        self._saldo += jumlah

    def potong_saldo(self, jumlah) -> None:
        if jumlah > self._saldo:
            raise SaldoTidakCukupError(f"Saldo {rp(self._saldo)} tidak cukup untuk biaya {rp(jumlah)}. Silakan isi saldo dulu.")
        self._saldo -= jumlah

    def ada_bentrok(self, mulai, selesai) -> bool:
        return any(s.aktif and s.bentrok(mulai, selesai) for s in self.riwayat_sesi)

    @abstractmethod
    def getRole(self) -> str: ...
    @abstractmethod
    def ringkasan(self) -> str: ...