class BimbelError(Exception): pass
class TutorNotAvailableException(BimbelError):
    def __init__(self, pesan="Tutor tidak tersedia pada jadwal tersebut"):
        super().__init__(pesan)
class JadwalBentrokError(BimbelError): pass
class SaldoTidakCukupError(BimbelError): pass
class StatusSesiError(BimbelError): pass
class Batal(Exception): pass

def rp(n) -> str:
    return "Rp" + f"{n:,.0f}".replace(",", ".")