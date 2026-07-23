"""Para ayrıştırma ve biçimlendirme — GUI bağımsız, saf fonksiyonlar.

Bu modül bilinçli olarak tkinter/customtkinter'a bağımlı değildir; böylece
para mantığı headless ortamda (CI dahil) test edilebilir.
"""

from typing import Optional

# Desteklenen para birimleri — hepsi 2 ondalıklı (minör birim = 100 kuruş/cent).
# 'TRY' temel/raporlama birimidir; yabancı işlemler girişte TL'ye çevrilerek
# saklanır (bkz. database.gelir_ekle) ama orijinal tutar+birim de korunur.
PARA_BIRIMLERI = {
    "TRY": {"sembol": "₺", "ad": "Türk Lirası"},
    "USD": {"sembol": "$", "ad": "ABD Doları"},
    "EUR": {"sembol": "€", "ad": "Euro"},
    "GBP": {"sembol": "£", "ad": "İngiliz Sterlini"},
}


def para_sembol(para_birimi: str) -> str:
    """Para birimi kodunun sembolünü döner; bilinmeyen kod kendini döner."""
    return PARA_BIRIMLERI.get(para_birimi, {}).get("sembol", para_birimi)


def para_parse(metin: str) -> float:
    """Kullanıcı girdisindeki tutarı güvenle float'a çevirir.

    Noktayı koşulsuz binlik ayraç saymak, "12.5" gibi ondalık-noktalı
    girişleri 125'e, "1500.50"yi 150050'ye çeviriyordu (10x-100x hata).
    Türk (1.234,56), ABD (1,234.56) ve sade (12.5 / 12,5) yazımlarının
    hepsi doğru yorumlanır.
    """
    ham = (metin or "").strip().replace("₺", "").replace(" ", "")
    negatif = ham.startswith("-")
    if negatif:
        ham = ham[1:]
    if not ham or any(c not in "0123456789.," for c in ham):
        raise ValueError(f"Geçersiz tutar: {metin!r}")

    son_nokta = ham.rfind(".")
    son_virgul = ham.rfind(",")
    ondalik: Optional[str]
    if son_nokta != -1 and son_virgul != -1:
        # İki ayraç da varsa sonda olan ondalık ayracıdır
        ondalik = "." if son_nokta > son_virgul else ","
    elif son_virgul != -1:
        # Tek virgül + 1-2 hane → ondalık (12,5); aksi halde binlik (1,500)
        ondalik = (
            "," if ham.count(",") == 1 and len(ham) - son_virgul - 1 in (1, 2)
            else None
        )
    elif son_nokta != -1:
        # Tek nokta + 1-2 hane → ondalık (12.5); aksi halde binlik (1.500)
        ondalik = (
            "." if ham.count(".") == 1 and len(ham) - son_nokta - 1 in (1, 2)
            else None
        )
    else:
        ondalik = None

    if ondalik:
        binlik = "," if ondalik == "." else "."
        tam, _, kusur = ham.rpartition(ondalik)
        tam = tam.replace(binlik, "")
        if (tam and not tam.isdigit()) or not kusur.isdigit():
            raise ValueError(f"Geçersiz tutar: {metin!r}")
        deger = float(f"{tam or '0'}.{kusur}")
    else:
        temiz = ham.replace(".", "").replace(",", "")
        if not temiz.isdigit():
            raise ValueError(f"Geçersiz tutar: {metin!r}")
        deger = float(temiz)
    return -deger if negatif else deger


def butce_durum_etiketi(harcanan: float, butce: float) -> tuple:
    """Bütçe kullanım oranını, durum etiketini ve renk kodunu döner.

    (oran_yuzde, durum_metni, renk) döner. Bu eşikler (>%90 kırmızı,
    kalan < bütçenin %10'u -> "Yaklaşıyor") birer İŞ KURALI'dır; önceden
    doğrudan render fonksiyonunun içine gömülüydü ve hiçbir test onları
    korumuyordu — eşik yanlışlıkla değişse kimse fark etmezdi.
    """
    if butce > 0:
        oran = min(harcanan / butce * 100, 100)
    else:
        oran = 0.0
    kalan = butce - harcanan

    if oran > 90:
        renk = "#ef4444"
    elif oran > 70:
        renk = "#f59e0b"
    else:
        renk = "#22c55e"

    if kalan < 0:
        durum = "🔴 Aşıldı"
    elif kalan < butce * 0.1:
        durum = "🟡 Yaklaşıyor"
    else:
        durum = "✅"
    return oran, durum, renk


def para_formatla(
    deger: float, sembol: bool = True, ondalik: int = 2,
    para_birimi: str = "TRY",
) -> str:
    """Tutarı Türk sayı formatında döner: 1.234,56 ₺ (negatif: -1.234,56 ₺).

    para_birimi ile sembol değişir (USD→$, EUR→€, GBP→£); varsayılan TRY→₺
    olduğundan mevcut tüm çağrılar değişmeden çalışır. Sayı biçimi (binlik ".",
    ondalık ",") her birim için aynı kalır; yalnızca sembol farklıdır.
    """
    metin = f"{abs(deger):,.{ondalik}f}"
    metin = metin.replace(",", "X").replace(".", ",").replace("X", ".")
    isaret = "-" if deger < 0 else ""
    if not sembol:
        return f"{isaret}{metin}"
    return f"{isaret}{metin} {para_sembol(para_birimi)}"
