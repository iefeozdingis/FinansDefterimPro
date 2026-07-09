"""Otomatik formatlama yardımcıları — tarih ve para girişi için."""


def tarih_formatla(event=None):
    """CTkEntry içinde GG.AA.YYYY formatını otomatik uygular."""
    widget = event.widget

    # Backspace/Delete ise formatlama yapma, kullanıcının silmesine izin ver
    if event and event.keysym in (
        "BackSpace",
        "Delete",
        "Left",
        "Right",
        "Home",
        "End",
        "Tab",
    ):
        return

    metin = "".join(c for c in widget.get() if c.isdigit())
    if not metin:
        # Sadece noktalar varsa tamamen temizle
        if widget.get().replace(".", "").strip() == "":
            widget.delete(0, "end")
        return

    eski_pos = widget.index("insert")

    if len(metin) <= 2:
        yeni = metin
    elif len(metin) <= 4:
        yeni = f"{metin[:2]}.{metin[2:]}"
    else:
        yeni = f"{metin[:2]}.{metin[2:4]}.{metin[4:8]}"

    widget.delete(0, "end")
    widget.insert(0, yeni)

    # Cursor'ı mümkün olduğunca eski yerine yakın tut
    dot_sayisi_eski = widget.get()[:eski_pos].count(".")
    yeni_pos = eski_pos
    if dot_sayisi_eski < yeni[:eski_pos].count("."):
        yeni_pos += 1
    widget.icursor(min(yeni_pos, len(yeni)))


def tutar_formatla(event=None):
    """CTkEntry içinde para formatını otomatik uygular (1.500,75 gibi)."""
    widget = event.widget

    # Navigation tuşlarında formatlama yapma
    if event and event.keysym in ("Left", "Right", "Home", "End", "Tab"):
        return

    ham = widget.get().strip()
    if not ham:
        return

    eski_pos = widget.index("insert")

    if "," in ham:
        parts = ham.split(",")
        kurus = "".join(c for c in parts[-1] if c.isdigit())[:3]
        tam_kisim = "".join(c for c in ",".join(parts[:-1]) if c.isdigit())
    else:
        kurus = None
        tam_kisim = "".join(c for c in ham if c.isdigit())

    if not tam_kisim:
        if kurus:
            widget.delete(0, "end")
            widget.insert(0, f"0,{kurus}")
        return

    # Binlik ayraç ekle
    sayi = int(tam_kisim)
    tam_formatli = f"{sayi:,}".replace(",", ".")

    if kurus is not None:
        yeni = f"{tam_formatli},{kurus}"
    else:
        yeni = tam_formatli

    # Cursor pozisyonunu koru: nokta eklendiyse cursor'ı 1 ilerlet
    eski_nokta = widget.get()[:eski_pos].count(".")
    widget.delete(0, "end")
    widget.insert(0, yeni)
    yeni_nokta = yeni[:eski_pos].count(".")
    yeni_pos = eski_pos + (yeni_nokta - eski_nokta)
    widget.icursor(min(yeni_pos, len(yeni)))


def tarih_bind(widget):
    """Widget'a tarih formatlama binding'i ekle."""
    widget.bind("<KeyRelease>", tarih_formatla)


def tutar_bind(widget):
    """Widget'a para formatlama binding'i ekle."""
    widget.bind("<KeyRelease>", tutar_formatla)


def tutar_oku(widget) -> float:
    """Formatlı tutar widget'ından float değer okur."""
    ham = widget.get().strip()
    # Noktaları kaldır, virgülü noktaya çevir
    temiz = ham.replace(".", "").replace(",", ".")
    return float(temiz)
