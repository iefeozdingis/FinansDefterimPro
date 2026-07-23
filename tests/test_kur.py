"""kur modülü testleri — TCMB XML parse, önbellek/elle kur, çözümleme.

Ağ çekimi (tcmb_getir) TEST EDİLMEZ: tcmb_xml_parse saf/ağsız olarak örnek
XML ile doğrulanır; önbellek/override yolları temp DB'nin ayarlar tablosuyla.
"""
import tempfile
import unittest
from pathlib import Path

import database as db_module
import kur

# Gerçek TCMB today.xml biçimini taklit eden örnek (kısaltılmış).
SAMPLE_XML = """<?xml version="1.0" encoding="ISO-8859-9"?>
<Tarih_Date Tarih="23.07.2026" Date="07/23/2026">
  <Currency CrossOrder="0" Kod="USD" CurrencyCode="USD">
    <Unit>1</Unit><Isim>ABD DOLARI</Isim><CurrencyName>US DOLLAR</CurrencyName>
    <ForexBuying>34.1000</ForexBuying><ForexSelling>34.2000</ForexSelling>
    <BanknoteBuying>34.0500</BanknoteBuying><BanknoteSelling>34.2500</BanknoteSelling>
  </Currency>
  <Currency CrossOrder="9" Kod="EUR" CurrencyCode="EUR">
    <Unit>1</Unit><Isim>EURO</Isim><CurrencyName>EURO</CurrencyName>
    <ForexBuying>37.0000</ForexBuying><ForexSelling>37.1500</ForexSelling>
    <BanknoteBuying>36.9000</BanknoteBuying><BanknoteSelling>37.2000</BanknoteSelling>
  </Currency>
  <Currency CrossOrder="12" Kod="JPY" CurrencyCode="JPY">
    <Unit>100</Unit><Isim>JAPON YENI</Isim><CurrencyName>JAPANESE YEN</CurrencyName>
    <ForexBuying>22.0000</ForexBuying><ForexSelling>22.1000</ForexSelling>
    <BanknoteBuying>21.9000</BanknoteBuying><BanknoteSelling>22.3000</BanknoteSelling>
  </Currency>
</Tarih_Date>"""


class KurParseTests(unittest.TestCase):
    def test_forex_selling_okur(self):
        k = kur.tcmb_xml_parse(SAMPLE_XML)
        self.assertAlmostEqual(k["USD"], 34.20)
        self.assertAlmostEqual(k["EUR"], 37.15)

    def test_desteklenmeyen_haric(self):
        k = kur.tcmb_xml_parse(SAMPLE_XML)
        self.assertNotIn("JPY", k)  # DESTEKLENEN dışı (varsayılan USD/EUR/GBP)
        self.assertNotIn("GBP", k)  # örnek XML'de yok

    def test_unit_bolme(self):
        # JPY 100 birim üzerinden kote: 22.10 / 100 = 0.221
        k = kur.tcmb_xml_parse(SAMPLE_XML, kodlar=("JPY",))
        self.assertAlmostEqual(k["JPY"], 0.221)

    def test_bos_xml(self):
        bos = '<?xml version="1.0"?><Tarih_Date></Tarih_Date>'
        self.assertEqual(kur.tcmb_xml_parse(bos), {})


class KurCozumlemeTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        db_module.DB_FOLDER = Path(self.temp.name)
        db_module.DB_PATH = db_module.DB_FOLDER / "test_kur.db"
        self.db = db_module.Database()

    def tearDown(self):
        self.db.close()
        self.temp.cleanup()

    def test_try_daima_bir(self):
        self.assertEqual(kur.guncel_kur(self.db, "TRY"), 1.0)
        self.assertEqual(kur.kur_kaynagi(self.db, "TRY"), "temel")

    def test_kur_yoksa_none(self):
        self.assertIsNone(kur.guncel_kur(self.db, "USD"))
        self.assertEqual(kur.kur_kaynagi(self.db, "USD"), "yok")

    def test_onbellek(self):
        kur.onbellek_kaydet(self.db, {"USD": 34.20, "EUR": 37.15}, "2026-07-23")
        self.assertAlmostEqual(kur.guncel_kur(self.db, "USD"), 34.20)
        self.assertIn("TCMB", kur.kur_kaynagi(self.db, "USD"))
        self.assertIn("2026-07-23", kur.kur_kaynagi(self.db, "USD"))

    def test_elle_kur_onbellegin_onune_gecer(self):
        kur.onbellek_kaydet(self.db, {"USD": 34.20}, "2026-07-23")
        kur.elle_kur_ayarla(self.db, "USD", 35.50)
        self.assertEqual(kur.guncel_kur(self.db, "USD"), 35.50)
        self.assertEqual(kur.kur_kaynagi(self.db, "USD"), "elle")
        # Elle kur silinince önbelleğe geri düşer
        kur.elle_kur_ayarla(self.db, "USD", None)
        self.assertAlmostEqual(kur.guncel_kur(self.db, "USD"), 34.20)

    def test_elle_kur_kalici(self):
        kur.elle_kur_ayarla(self.db, "EUR", 37.00)
        # Aynı DB'yi yeni bir Database ile açınca (ayarlar tablosundan) korunur
        self.db.close()
        db2 = db_module.Database()
        try:
            self.assertEqual(kur.guncel_kur(db2, "EUR"), 37.00)
        finally:
            db2.close()


if __name__ == "__main__":
    unittest.main()
