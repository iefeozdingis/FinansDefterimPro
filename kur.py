"""Döviz kuru — TCMB günlük kuru çekme, önbellek ve elle geçersiz kılma.

Uygulama yerel-önceliklidir; ağ çağrısı yalnızca kullanıcı isteğiyle ("TCMB'den
Güncelle") veya açılışta arka planda (sessiz, en iyi çaba) yapılır. İşlem formu
HER ZAMAN önbellekten okur ve ağı beklemez — çevrimdışıyken son çekilen ya da
elle girilen kur kullanılır.

Kaynak: TCMB today.xml, ForexSelling (döviz satış). Yeni bağımlılık yok —
urllib + xml.etree (stdlib). Önbellek ve elle kurlar `ayarlar` tablosunda JSON
olarak saklanır (ayrı tabloya gerek yok).
"""
from __future__ import annotations

import json
import urllib.request
import xml.etree.ElementTree as ET
from typing import Any, Dict, Optional

TCMB_URL = "https://www.tcmb.gov.tr/kurlar/today.xml"

# ayarlar tablosundaki anahtarlar
_ONBELLEK_ANAHTAR = "kur_onbellek"   # {"tarih": "YYYY-MM-DD", "kurlar": {...}}
_ELLE_ANAHTAR = "kur_elle"           # {"USD": 34.5, ...} kullanıcı override

# TRY temel birimdir (kur=1); yalnızca yabancılar için kur gerekir.
DESTEKLENEN = ("USD", "EUR", "GBP")


def tcmb_xml_parse(
    xml_metin: str, kodlar: tuple = DESTEKLENEN
) -> Dict[str, float]:
    """TCMB kur XML'inden {kod: 1 birimin TL karşılığı} döner.

    Saf/ağsız — sample XML ile test edilebilir. ForexSelling yoksa
    BanknoteSelling'e düşer. Unit alanı dikkate alınır (bazı birimler 100
    üzerinden kote edilir; USD/EUR/GBP için Unit=1).
    """
    kok = ET.fromstring(xml_metin)
    sonuc: Dict[str, float] = {}
    for cur in kok.findall("Currency"):
        kod = cur.get("Kod") or cur.get("CurrencyCode")
        if not kod or kod not in kodlar:
            continue
        satis = cur.findtext("ForexSelling") or cur.findtext("BanknoteSelling")
        birim = cur.findtext("Unit") or "1"
        if not satis or not satis.strip():
            continue
        try:
            deger = float(satis.replace(",", ".")) / float(birim)
        except (ValueError, ZeroDivisionError):
            continue
        if deger > 0:
            sonuc[kod] = deger
    return sonuc


def tcmb_getir(timeout: float = 6.0) -> Dict[str, float]:
    """TCMB today.xml'i çeker ve parse eder. Ağ/parse hatasında yükseltir.

    Bu fonksiyon ağ I/O yapar — ASLA ana thread'den doğrudan çağırma; worker
    thread'de çağır (bkz. ui.ayarlar 'TCMB'den Güncelle')."""
    istek = urllib.request.Request(
        TCMB_URL, headers={"User-Agent": "FINEding/1.0"}
    )
    with urllib.request.urlopen(istek, timeout=timeout) as yanit:  # noqa: S310
        ham = yanit.read().decode("iso-8859-9", errors="replace")
    return tcmb_xml_parse(ham)


# ==========================
# ÖNBELLEK / ELLE KURLAR (ayarlar tablosu)
# ==========================

def _json_oku(db: Any, anahtar: str) -> dict:
    ham = db.ayar_oku(anahtar, "") or ""
    if not ham:
        return {}
    try:
        veri = json.loads(ham)
        return veri if isinstance(veri, dict) else {}
    except (ValueError, TypeError):
        return {}


def onbellek_oku(db: Any) -> dict:
    """Son çekilen TCMB önbelleğini döner: {'tarih':..., 'kurlar':{...}}."""
    return _json_oku(db, _ONBELLEK_ANAHTAR)


def onbellek_kaydet(db: Any, kurlar: Dict[str, float], tarih: str) -> None:
    db.ayar_kaydet(
        _ONBELLEK_ANAHTAR, json.dumps({"tarih": tarih, "kurlar": kurlar})
    )


def elle_kurlar(db: Any) -> Dict[str, float]:
    """Kullanıcının elle girdiği kur override'larını döner."""
    return {k: float(v) for k, v in _json_oku(db, _ELLE_ANAHTAR).items()}


def elle_kur_ayarla(db: Any, kod: str, deger: Optional[float]) -> None:
    """Bir para birimi için elle kur ayarlar; deger None ise override'ı siler."""
    mevcut = elle_kurlar(db)
    if deger is None:
        mevcut.pop(kod, None)
    else:
        mevcut[kod] = float(deger)
    db.ayar_kaydet(_ELLE_ANAHTAR, json.dumps(mevcut))


def guncel_kur(db: Any, para_birimi: str) -> Optional[float]:
    """1 birim `para_birimi` kaç TL — çözümleme sırası: TRY=1 → elle → önbellek.

    Bulunamazsa None döner (çağıran uyarır; yabancı işlem kaydını engeller).
    Elle kur, TCMB önbelleğinin önüne geçer (kullanıcının bilinçli tercihi).
    """
    if para_birimi == "TRY":
        return 1.0
    elle = elle_kurlar(db)
    if para_birimi in elle:
        return elle[para_birimi]
    onb = onbellek_oku(db).get("kurlar", {})
    if para_birimi in onb:
        try:
            return float(onb[para_birimi])
        except (ValueError, TypeError):
            return None
    return None


def kur_kaynagi(db: Any, para_birimi: str) -> str:
    """guncel_kur'un hangi kaynaktan geldiğini açıklar (UI ipucu için)."""
    if para_birimi == "TRY":
        return "temel"
    if para_birimi in elle_kurlar(db):
        return "elle"
    if para_birimi in onbellek_oku(db).get("kurlar", {}):
        onb = onbellek_oku(db)
        return f"TCMB {onb.get('tarih', '')}".strip()
    return "yok"
