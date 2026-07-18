"""para_parse / para_formatla birim testleri — Tk gerektirmez."""

import unittest

from ui.money import butce_durum_etiketi, para_formatla, para_parse
from ui.utils import tarih_bicimle


class TestParaParse(unittest.TestCase):
    def test_sade_tam_sayi(self):
        self.assertEqual(para_parse("1500"), 1500.0)

    def test_nokta_ondalik_kucuk(self):
        # "12.5" binlik değil ondalık olmalı (10x hata düzeltmesi)
        self.assertEqual(para_parse("12.5"), 12.5)

    def test_nokta_ondalik_iki_hane(self):
        self.assertEqual(para_parse("1500.50"), 1500.50)

    def test_virgul_ondalik(self):
        self.assertEqual(para_parse("12,5"), 12.5)

    def test_turk_format(self):
        self.assertEqual(para_parse("1.234,56"), 1234.56)

    def test_turk_format_buyuk(self):
        self.assertEqual(para_parse("1.500.000,00"), 1500000.0)

    def test_abd_format(self):
        self.assertEqual(para_parse("1,234.56"), 1234.56)

    def test_binlik_nokta_ondalik_yok(self):
        # "1.500" → 1500 (binlik ayraç), 1.5 değil
        self.assertEqual(para_parse("1.500"), 1500.0)

    def test_binlik_virgul_ondalik_yok(self):
        self.assertEqual(para_parse("1,500"), 1500.0)

    def test_negatif(self):
        self.assertEqual(para_parse("-1.234,56"), -1234.56)

    def test_sembol_ve_bosluk(self):
        self.assertEqual(para_parse("1.234,56 ₺"), 1234.56)

    def test_gecersiz(self):
        for kotu in ("", "abc", "12.34.56,78,9", "1.2.3,4,5", "12,3.4,5"):
            with self.assertRaises(ValueError):
                para_parse(kotu)


class TestParaFormatla(unittest.TestCase):
    def test_temel(self):
        self.assertEqual(para_formatla(1234.56), "1.234,56 ₺")

    def test_negatif(self):
        self.assertEqual(para_formatla(-1234.56), "-1.234,56 ₺")

    def test_sembolsuz(self):
        self.assertEqual(para_formatla(1234.56, sembol=False), "1.234,56")

    def test_ondalik_sifir(self):
        self.assertEqual(para_formatla(1500, ondalik=0), "1.500 ₺")

    def test_roundtrip(self):
        # format → parse → aynı değer
        for deger in (0.0, 12.5, 1234.56, 1500000.0, -99.99):
            self.assertAlmostEqual(
                para_parse(para_formatla(deger, sembol=False)), deger, places=2
            )


class TestButceDurumEtiketi(unittest.TestCase):
    """Bütçe eşikleri artık render'a gömülü değil, saf fonksiyonda."""

    def test_normal_kullanim_yesil(self):
        oran, durum, renk = butce_durum_etiketi(harcanan=300, butce=1000)
        self.assertEqual(oran, 30.0)
        self.assertEqual(durum, "✅")
        self.assertEqual(renk, "#22c55e")

    def test_yetmis_ustu_sari(self):
        _, _, renk = butce_durum_etiketi(harcanan=750, butce=1000)
        self.assertEqual(renk, "#f59e0b")

    def test_doksan_ustu_kirmizi(self):
        _, _, renk = butce_durum_etiketi(harcanan=950, butce=1000)
        self.assertEqual(renk, "#ef4444")

    def test_kalan_yuzde_ondan_az_yaklasiyor(self):
        # kalan 50 < butce*0.1 (100) → "Yaklaşıyor"
        _, durum, _ = butce_durum_etiketi(harcanan=950, butce=1000)
        self.assertEqual(durum, "🟡 Yaklaşıyor")

    def test_asilan_butce(self):
        oran, durum, _ = butce_durum_etiketi(harcanan=1200, butce=1000)
        self.assertEqual(durum, "🔴 Aşıldı")
        self.assertEqual(oran, 100.0, "Oran %100'de kırpılmalı")

    def test_sifir_butce_bolme_hatasi_vermez(self):
        oran, _, _ = butce_durum_etiketi(harcanan=500, butce=0)
        self.assertEqual(oran, 0.0)


class TestTarihBicimle(unittest.TestCase):
    """Tarih biçimlendirme mantığı artık Tk gerektirmiyor."""

    def test_gun(self):
        self.assertEqual(tarih_bicimle("0"), "0")
        self.assertEqual(tarih_bicimle("01"), "01")

    def test_gun_ay(self):
        self.assertEqual(tarih_bicimle("017"), "01.7")
        self.assertEqual(tarih_bicimle("0107"), "01.07")

    def test_tam_tarih(self):
        self.assertEqual(tarih_bicimle("01072026"), "01.07.2026")

    def test_kismi_yil(self):
        self.assertEqual(tarih_bicimle("010720"), "01.07.20")

    def test_fazla_hane_yok_sayilir(self):
        self.assertEqual(tarih_bicimle("010720269999"), "01.07.2026")

    def test_rakam_disi_karakterler_atilir(self):
        self.assertEqual(tarih_bicimle("01.07.2026"), "01.07.2026")
        self.assertEqual(tarih_bicimle("abc01x07y2026"), "01.07.2026")

    def test_bos(self):
        self.assertEqual(tarih_bicimle(""), "")
        self.assertEqual(tarih_bicimle("..."), "")


if __name__ == "__main__":
    unittest.main()
