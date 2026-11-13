from models import rp
from models.constants import APPROVED
from utils import tanya, v_dalam, v_angka, pilih_sesi

def siswa_bayar(app, siswa):
    daftar = [s for s in siswa.riwayat_sesi if s.status == APPROVED and not s.lunas]
    sesi = pilih_sesi(daftar, siswa, "SESI MENUNGGU PEMBAYARAN", "Tidak ada sesi yang perlu dibayar (sesi harus disetujui tutor dulu).")
    if not sesi: return
    print(f"Biaya: {rp(sesi.hitung_biaya())} | Saldo Anda: {rp(siswa.saldo)}")
    tanya("Bayar sekarang? (1=Ya, 0=Batal): ", v_dalam({"1": True}, "Ketik 1 untuk bayar atau 0 untuk batal!"))
    biaya = siswa.bayar(sesi)
    app.simpan()
    print(f"[SUKSES] Pembayaran {rp(biaya)} berhasil. Sisa saldo: {rp(siswa.saldo)}")

def siswa_isi_saldo(app, siswa):
    print(f"Saldo saat ini: {rp(siswa.saldo)}")
    siswa.tambah_saldo(tanya("Jumlah isi saldo (Rp, 0 = batal): ", v_angka(1, 100_000_000)))
    app.simpan()
    print(f"[SUKSES] Saldo sekarang: {rp(siswa.saldo)}")