"""Gelir ekleme sayfası — ortak IslemFormuSayfasi'nın ince sarmalayıcısı."""

from ui import tema
from ui.islem_formu import IslemFormuSayfasi

# Varsayılan gelir kategorileri (dashboard düzenleme penceresi de kullanır)
VARSAYILAN_GELIR_KATEGORILER = ["Maaş", "Prim", "Ek İş", "Faiz", "Yatırım", "Diğer"]


class GelirSayfasi(IslemFormuSayfasi):
    def __init__(self, parent, db, dashboard_callback=None):
        super().__init__(
            parent, db, "Gelir",
            kategoriler=VARSAYILAN_GELIR_KATEGORILER,
            varsayilan_kategori="Maaş",
            renk="#2e8b57",
            kart_renk=tema.GELIR_KART,
            dashboard_callback=dashboard_callback,
        )
