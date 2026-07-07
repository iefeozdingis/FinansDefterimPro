import csv
import shutil
import sqlite3
from pathlib import Path
import hashlib
from datetime import datetime
from typing import Any, Optional, List, Tuple, Dict

# ==========================
# Veritabanı Ayarları
# ==========================

DB_FOLDER = Path("database")
DB_FOLDER.mkdir(exist_ok=True)

DB_PATH = DB_FOLDER / "finans.db"


def normalize_date(tarih_str: str) -> str:
    """Normalize a date string to ISO YYYY-MM-DD.

    Accepts DD.MM.YYYY or YYYY-MM-DD and returns YYYY-MM-DD.
    Raises ValueError on invalid formats.
    """
    if not isinstance(tarih_str, str):
        raise ValueError("Tarih string olmalidir")

    tarih_str = tarih_str.strip()
    # DD.MM.YYYY
    try:
        if "." in tarih_str:
            dt = datetime.strptime(tarih_str, "%d.%m.%Y")
            return dt.strftime("%Y-%m-%d")
        # YYYY-MM-DD
        dt = datetime.strptime(tarih_str, "%Y-%m-%d")
        return dt.strftime("%Y-%m-%d")
    except Exception as e:
        raise ValueError(f"Geçersiz tarih formatı: {tarih_str}") from e


class Database:
    def __init__(self) -> None:
        self.conn = sqlite3.connect(DB_PATH)
        self.cursor = self.conn.cursor()
        self.create_tables()

    # ==========================
    # Tablolar
    # ==========================

    def create_tables(self) -> None:
        self.cursor.execute(
            """
        CREATE TABLE IF NOT EXISTS islemler(

            id INTEGER PRIMARY KEY AUTOINCREMENT,

            tarih TEXT NOT NULL,

            tur TEXT NOT NULL,

            kategori TEXT NOT NULL,

            aciklama TEXT,

            tutar REAL NOT NULL

        )
        """
        )

        self.cursor.execute(
            """
        CREATE TABLE IF NOT EXISTS butceler(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            ay INTEGER NOT NULL,
            yil INTEGER NOT NULL,
            kategori TEXT NOT NULL,
            tutar REAL NOT NULL,
            UNIQUE(ay, yil, kategori)
        )
        """
        )

        self.cursor.execute(
            """
        CREATE TABLE IF NOT EXISTS ayarlar(
            anahtar TEXT PRIMARY KEY,
            deger TEXT
        )
        """
        )

        self.conn.commit()
    # ==========================
    # GELİR EKLE
    # ==========================

    def gelir_ekle(self, tarih: str, kategori: str, aciklama: Optional[str], tutar: float) -> None:
        tarih_iso = normalize_date(tarih)
        self.cursor.execute(
            """
        INSERT INTO islemler
        (tarih,tur,kategori,aciklama,tutar)

        VALUES (?,?,?,?,?)

        """,
            (tarih_iso, "Gelir", kategori, aciklama, tutar),
        )

        self.conn.commit()

    # ==========================
    # GİDER EKLE
    # ==========================

    def gider_ekle(self, tarih: str, kategori: str, aciklama: Optional[str], tutar: float) -> None:
        tarih_iso = normalize_date(tarih)
        self.cursor.execute(
            """
        INSERT INTO islemler
        (tarih,tur,kategori,aciklama,tutar)

        VALUES (?,?,?,?,?)

        """,
            (tarih_iso, "Gider", kategori, aciklama, tutar),
        )

        self.conn.commit()

    # ==========================
    # TÜM İŞLEMLER
    # ==========================

    def tum_islemler(self) -> List[Tuple[Any, ...]]:
        self.cursor.execute(
            """
        SELECT *

        FROM islemler

        ORDER BY id DESC
        """
        )

        return self.cursor.fetchall()

    def guncelle_islem(
        self,
        id: int,
        tarih: str,
        tur: str,
        kategori: str,
        aciklama: Optional[str],
        tutar: float,
    ) -> None:
        tarih_iso = normalize_date(tarih)
        self.cursor.execute(
            """
        UPDATE islemler
        SET tarih=?, tur=?, kategori=?, aciklama=?, tutar=?
        WHERE id=?
        """,
            (tarih_iso, tur, kategori, aciklama, tutar, id),
        )
        self.conn.commit()

    def islemler_aralik(self, baslangic: str, bitis: str) -> List[Tuple[Any, ...]]:
        bas_iso = normalize_date(baslangic)
        bit_iso = normalize_date(bitis)
        self.cursor.execute(
            """
        SELECT *
        FROM islemler
        WHERE tarih BETWEEN ? AND ?
        ORDER BY id DESC
        """,
            (bas_iso, bit_iso),
        )
        return self.cursor.fetchall()

    def toplam_gelir_aralik(self, baslangic: str, bitis: str) -> float:
        bas_iso = normalize_date(baslangic)
        bit_iso = normalize_date(bitis)
        self.cursor.execute(
            """
        SELECT IFNULL(SUM(tutar),0)
        FROM islemler
        WHERE tur='Gelir' AND tarih BETWEEN ? AND ?
        """,
            (bas_iso, bit_iso),
        )
        row = self.cursor.fetchone()
        val = row[0] if row and row[0] is not None else 0.0
        return float(val)

    def toplam_gider_aralik(self, baslangic: str, bitis: str) -> float:
        bas_iso = normalize_date(baslangic)
        bit_iso = normalize_date(bitis)
        self.cursor.execute(
            """
        SELECT IFNULL(SUM(tutar),0)
        FROM islemler
        WHERE tur='Gider' AND tarih BETWEEN ? AND ?
        """,
            (bas_iso, bit_iso),
        )
        row = self.cursor.fetchone()
        val = row[0] if row and row[0] is not None else 0.0
        return float(val)

    def kategori_toplamlari(self, tur: Optional[str] = None) -> List[Tuple[str, float]]:
        sorgu = "SELECT kategori, SUM(tutar) FROM islemler"
        kosullar = []
        if tur:
            sorgu += " WHERE tur=?"
            kosullar.append(tur)
        sorgu += " GROUP BY kategori ORDER BY SUM(tutar) DESC"
        if kosullar:
            self.cursor.execute(sorgu, tuple(kosullar))
        else:
            self.cursor.execute(sorgu)
        return self.cursor.fetchall()

    def export_csv(self, path: str) -> None:
        with open(path, "w", newline="", encoding="utf-8") as dosya:
            writer = csv.writer(dosya)
            writer.writerow(["id", "tarih", "tur", "kategori", "aciklama", "tutar"])
            for satir in self.tum_islemler():
                writer.writerow(satir)

    def kaydet_butce(self, ay: int, yil: int, kategori: str, tutar: float) -> None:
        self.cursor.execute(
            """
        INSERT INTO butceler (ay, yil, kategori, tutar)
        VALUES (?, ?, ?, ?)
        ON CONFLICT(ay, yil, kategori) DO UPDATE SET tutar=excluded.tutar
        """,
            (ay, yil, kategori, tutar),
        )
        self.conn.commit()

    def butce_listele(self, ay: int, yil: int) -> List[Tuple[str, float]]:
        self.cursor.execute(
            """
        SELECT kategori, tutar FROM butceler
        WHERE ay=? AND yil=?
        ORDER BY kategori
        """,
            (ay, yil),
        )
        return self.cursor.fetchall()

    def butce_durumu(self, ay: int, yil: int) -> List[Dict[str, Any]]:
        self.cursor.execute(
            """
        SELECT
            b.kategori,
            b.tutar AS butce,
            COALESCE(
                SUM(CASE WHEN i.tur='Gider' THEN i.tutar ELSE 0 END),
                0
            ) AS harcanan
        FROM butceler b
        LEFT JOIN islemler i ON i.kategori = b.kategori
        AND strftime('%m', i.tarih) = printf('%02d', b.ay)
        AND strftime('%Y', i.tarih) = b.yil
        WHERE b.ay=? AND b.yil=?
        GROUP BY b.kategori, b.tutar
        ORDER BY b.kategori
        """,
            (ay, yil),
        )
        sonuc = []
        for kategori, butce, harcanan in self.cursor.fetchall():
            sonuc.append(
                {
                    "kategori": kategori,
                    "butce": float(butce),
                    "harcanan": float(harcanan),
                    "kalan": float(butce) - float(harcanan),
                }
            )
        return sonuc

    def ayar_kaydet(self, anahtar: str, deger: str) -> None:
        self.cursor.execute(
            """
        INSERT INTO ayarlar (anahtar, deger)
        VALUES (?, ?)
        ON CONFLICT(anahtar) DO UPDATE SET deger=excluded.deger
        """,
            (anahtar, deger),
        )
        self.conn.commit()

    def yedekle(self, hedef_yol: str) -> None:
        shutil.copy2(DB_PATH, hedef_yol)
        # create checksum file next to backup
        h = hashlib.sha256()
        with open(hedef_yol, "rb") as f:
            for chunk in iter(lambda: f.read(8192), b""):
                h.update(chunk)
        checksum_path = str(hedef_yol) + ".sha256"
        with open(checksum_path, "w", encoding="utf-8") as cf:
            cf.write(h.hexdigest())

    def geri_yukle(self, kaynak_yol: str) -> None:
        # verify checksum if present
        checksum_path = str(kaynak_yol) + ".sha256"
        if Path(checksum_path).exists():
            h = hashlib.sha256()
            with open(kaynak_yol, "rb") as f:
                for chunk in iter(lambda: f.read(8192), b""):
                    h.update(chunk)
            with open(checksum_path, "r", encoding="utf-8") as cf:
                expected = cf.read().strip()
            if h.hexdigest() != expected:
                raise ValueError("Yedek bütünlük kontrolü başarısız.")

        shutil.copy2(kaynak_yol, DB_PATH)
        self.conn.close()
        self.conn = sqlite3.connect(DB_PATH)
        self.cursor = self.conn.cursor()

    def ayar_oku(self, anahtar: str, varsayilan: Optional[str] = None) -> Optional[str]:
        self.cursor.execute("SELECT deger FROM ayarlar WHERE anahtar=?", (anahtar,))
        sonuc = self.cursor.fetchone()
        if not sonuc:
            return varsayilan
        value: Any = sonuc[0]
        if value is None:
            return varsayilan
        return str(value)

    # ==========================
    # TOPLAM GELİR
    # ==========================

    def toplam_gelir(self) -> float:
        self.cursor.execute(
            """
        SELECT IFNULL(SUM(tutar),0)

        FROM islemler

        WHERE tur='Gelir'
        """
        )

        row = self.cursor.fetchone()
        val = row[0] if row and row[0] is not None else 0.0
        return float(val)

    # ==========================
    # TOPLAM GİDER
    # ==========================

    def toplam_gider(self) -> float:
        self.cursor.execute(
            """
        SELECT IFNULL(SUM(tutar),0)

        FROM islemler

        WHERE tur='Gider'
        """
        )

        row = self.cursor.fetchone()
        val = row[0] if row and row[0] is not None else 0.0
        return float(val)

    # ==========================
    # BAKİYE
    # ==========================

    def bakiye(self) -> float:
        return self.toplam_gelir() - self.toplam_gider()

    # ==========================
    # İŞLEM SİL
    # ==========================

    def sil(self, id: int) -> None:
        self.cursor.execute("DELETE FROM islemler WHERE id=?", (id,))

        self.conn.commit()

    # ==========================
    # KAPAT
    # ==========================

    def close(self) -> None:
        self.conn.close()
