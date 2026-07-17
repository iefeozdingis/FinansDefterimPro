"""Merkezi renk paleti — CustomTkinter (light, dark) tuple'ları.

Önceden yüzeyler tek bir koyu hex ile sabitlenmişti (ör. fg_color="#134e4a");
bu yüzden Aydınlık temada sayfalar "koyu adacıklar" halinde kalıyordu. Buradaki
renkler (açık, koyu) çifti olarak verilir; CustomTkinter aktif temaya göre
doğru olanı seçer. Tek doğruluk kaynağı budur.
"""

# Teal ana yüzey (kartlar, çerçeveler)
KART = ("#d5efec", "#134e4a")
# Koyu panel (tasarruf kartı, admin liste, widget)
PANEL = ("#e6ebf2", "#0f172a")
# Gelir kartı (yeşil tonu)
GELIR_KART = ("#e3f4e8", "#0d2818")
# Gider kartı (kırmızı tonu)
GIDER_KART = ("#fbe9e7", "#2d0f0f")
# Giriş/vurgu yüzeyi
VURGU = ("#0d9488", "#0f766e")

# Metin renkleri
METIN = ("#1a1a1a", "#ffffff")
METIN_SOLUK = ("#475569", "#94a3b8")
METIN_TEAL = ("#0f766e", "#5eead4")

# İkincil ayraç
AYRAC = ("#cbd5e1", "#334155")
