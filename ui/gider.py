"""Gider ekleme sayfası — ortak IslemFormuSayfasi'nın ince sarmalayıcısı."""

from ui import tema
from ui.islem_formu import IslemFormuSayfasi

# Varsayılan gider kategorileri (dashboard düzenleme penceresi de kullanır)
VARSAYILAN_GIDER_KATEGORILER = [
    "Market",
    "Kira",
    "Fatura",
    "Yakıt",
    "Yemek",
    "Sağlık",
    "Eğlence",
    "Diğer",
]


class GiderSayfasi(IslemFormuSayfasi):
    def __init__(self, parent, db, dashboard_callback=None):
        super().__init__(
            parent, db, "Gider",
            kategoriler=VARSAYILAN_GIDER_KATEGORILER,
            varsayilan_kategori="Market",
            renk="#c0392b",
            kart_renk=tema.GIDER_KART,
            dashboard_callback=dashboard_callback,
        )
