from datetime import datetime
from models import BimbelError, rp
from models.constants import PENDING, APPROVED, ONGOING, MAX_DURASI
from utils import (tanya, v_dalam, v_angka, v_level, v_tidak_kosong, v_tanggal, 
                   v_jam, v_waktu, pilih_mapel, pilih_sesi)

def siswa_booking(app, siswa):
    mapel = pilih_mapel()
    level = tanya(f"Level (SD/SMP/SMA) [Enter = {siswa.jenjang}]: ", v_level(siswa.jenjang))
    hasil = app.cari_tutor(mapel, level)
    if not hasil:
        print(f"[INFO] Belum ada tutor {mapel} untuk level {level}."); return
    print(f"\nTutor {mapel} level {level}:")
    for t in hasil:
        slot = "; ".join(f"{m:%Y-%m-%d %H:%M}-{s:%H:%M}" for m, s in t.jadwal_mendatang()[:3]) or "belum ada jadwal"
        print(f"  [{t.id}] {t.nama} | {rp(t.get_tarif(mapel))}/jam\n        Jadwal buka: {slot}")
    tutor = tanya("ID Tutor (0 = batal): ", v_dalam({t.id: t for t in hasil}, "ID tutor tidak ada di daftar!"))

    while True:
        waktu = tanya("Waktu mulai (YYYY-MM-DD HH:MM): ", v_waktu)
        durasi = tanya(f"Durasi (jam, maks {MAX_DURASI}): ", v_angka(0.5, MAX_DURASI, float))
        try:
            sesi = app.buat_booking(siswa, tutor, mapel, waktu, durasi)
            break
        except (BimbelError, ValueError) as e:
            print(f"[GAGAL] {e}\n        Coba waktu/durasi lain, atau ketik 0 untuk batal.")
    print(f"[SUKSES] Booking dibuat. ID: {sesi.idSesi} | Total biaya {rp(sesi.hitung_biaya())} ({durasi:g} jam x {rp(sesi.tarif)}). Menunggu persetujuan tutor.")

def tutor_jadwal(app, tutor):
    print("\nJadwal tersedia saat ini:")
    slot = tutor.jadwal_mendatang()
    for m, s in slot: print(f"  {m:%Y-%m-%d %H:%M} - {s:%H:%M}")
    if not slot: print("  (belum ada)")
    tgl = tanya("Tanggal (YYYY-MM-DD): ", v_tanggal)
    mulai = tanya("Jam mulai (HH:MM): ", v_jam)
    selesai = tanya("Jam selesai (HH:MM): ", v_jam)
    tutor.set_jadwal(datetime.combine(tgl, mulai), datetime.combine(tgl, selesai))
    app.simpan()
    print("[SUKSES] Jadwal ditambahkan.")

def tutor_persetujuan(app, tutor):
    pending = [s for s in tutor.riwayat_sesi if s.status == PENDING]
    sesi = pilih_sesi(pending, tutor, "PERSETUJUAN BOOKING", "Tidak ada booking PENDING.")
    if not sesi: return
    aksi = tanya("Setujui atau Tolak? (S/T, 0 = batal): ", v_dalam({"S": sesi.setujui, "T": sesi.tolak}, "Ketik S atau T!"))
    aksi()
    app.simpan()
    print(f"[SUKSES] Sesi {sesi.idSesi} sekarang berstatus {sesi.status}.")

def tutor_mulai(app, tutor):
    approved = [s for s in tutor.riwayat_sesi if s.status == APPROVED]
    sesi = pilih_sesi(approved, tutor, "MULAI SESI", "Tidak ada sesi APPROVED.")
    if not sesi: return
    sesi.mulai()
    app.simpan()
    print(f"[SUKSES] Sesi {sesi.idSesi} dimulai.")

def tutor_selesai(app, tutor):
    berjalan = [s for s in tutor.riwayat_sesi if s.status == ONGOING]
    sesi = pilih_sesi(berjalan, tutor, "SELESAIKAN SESI", "Tidak ada sesi yang sedang berjalan (mulai sesi dulu).")
    if not sesi: return
    sesi.selesaikan(tanya("Catatan materi yang diajarkan: ", v_tidak_kosong))
    app.simpan()
    print(f"[SUKSES] Sesi {sesi.idSesi} selesai. Saldo Anda: {rp(tutor.saldo)}")