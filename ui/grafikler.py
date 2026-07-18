from datetime import datetime

import customtkinter as ctk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure

from ui.utils import para_formatla, tema_renkleri


class GrafiklerSayfasi(ctk.CTkFrame):
    def __init__(self, parent, db, dashboard_callback=None):
        super().__init__(parent)
        self.db = db
        self.dashboard_callback = dashboard_callback
        self.grid_columnconfigure(0, weight=1)

        ctk.CTkLabel(self, text="📊 Grafikler", font=("Segoe UI", 28, "bold")).pack(
            pady=(20, 5)
        )

        btn_frame = ctk.CTkFrame(self, fg_color="transparent")
        btn_frame.pack(pady=(0, 10))
        ctk.CTkButton(
            btn_frame,
            text="🔄 Grafikleri Yenile",
            width=200,
            fg_color="#0d9488",
            command=self._grafik_ciz,
        ).pack(side="left", padx=5)

        ctk.CTkButton(
            btn_frame,
            text="📊 Bu Ay vs Geçen Ay",
            width=180,
            fg_color="#6366f1",
            command=self._aylik_karsilastirma_ciz,
        ).pack(side="left", padx=5)

        ctk.CTkButton(
            btn_frame,
            text="📆 Yıllık Karşılaştırma",
            width=180,
            fg_color="#9333ea",
            command=self._yillik_karsilastirma_ciz,
        ).pack(side="left", padx=5)

        self._grafik_frame = ctk.CTkFrame(self, fg_color="transparent")
        self._grafik_frame.pack(fill="both", expand=True, padx=20, pady=10)
        # Açık matplotlib canvas/figure'larını takip et; yeniden çizimden önce
        # açıkça temizlenmezlerse Agg buffer'ları GC'ye kalıp RSS büyütüyordu.
        self._canvaslar = []
        self._grafik_ciz()

    def _grafikleri_temizle(self):
        """Önceki figure/canvas'ları serbest bırakır (bellek sızıntısını önler)."""
        for canvas in getattr(self, "_canvaslar", []):
            try:
                canvas.get_tk_widget().destroy()
            except Exception:
                pass
            try:
                canvas.figure.clf()
            except Exception:
                pass
        self._canvaslar = []
        for widget in self._grafik_frame.winfo_children():
            widget.destroy()

    def _grafik_stil_uygula(self, fig, *eksenler, pasta_metinler=()):
        """Figure/axes'i mevcut aydınlık/karanlık temaya göre boyar.

        matplotlib varsayılan olarak her zaman beyaz arka plan çizer;
        bu yüzden karanlık modda grafikler tema dışı kalıyordu.
        """
        renk = tema_renkleri()
        fig.patch.set_facecolor(renk["arka_plan"])
        for ax in eksenler:
            ax.set_facecolor(renk["arka_plan"])
            ax.tick_params(colors=renk["metin"])
            ax.xaxis.label.set_color(renk["metin"])
            ax.yaxis.label.set_color(renk["metin"])
            ax.title.set_color(renk["metin"])
            for spine in ax.spines.values():
                spine.set_color(renk["izgara"])
            legend = ax.get_legend()
            if legend:
                legend.get_frame().set_facecolor(renk["arka_plan"])
                legend.get_frame().set_edgecolor(renk["izgara"])
                for text in legend.get_texts():
                    text.set_color(renk["metin"])
        for metin_grubu in pasta_metinler:
            for text in metin_grubu:
                text.set_color(renk["metin"])

    def _grafik_ciz(self):
        self._grafikleri_temizle()

        fig = Figure(figsize=(8, 6), dpi=100)
        ax1 = fig.add_subplot(211)
        ax2 = fig.add_subplot(212)

        aylik = self._aylik_veri()
        aylar = list(aylik["Gelir"].keys())
        if len(aylar) < 2:
            aylar = [datetime.now().strftime("%Y-%m")]

        gelir_deger = [aylik["Gelir"].get(ay, 0) for ay in aylar]
        gider_deger = [aylik["Gider"].get(ay, 0) for ay in aylar]
        ax1.bar(aylar, gelir_deger, color="#2e8b57", label="Gelir")
        ax1.bar(aylar, [-x for x in gider_deger], color="#c0392b", label="Gider")
        ax1.set_title("Aylık Gelir / Gider")
        ax1.set_ylabel("₺")
        ax1.legend()

        renk = tema_renkleri()
        pasta_metinler = []

        gelirler = self.db.kategori_toplamlari("Gelir")
        if gelirler:
            labels, values = self._diger_grupla(gelirler)
            _, metin1, autometin1 = ax2.pie(values, labels=labels, autopct="%1.1f%%")
            pasta_metinler.append(metin1)
            pasta_metinler.append(autometin1)
            ax2.set_title("Gelir Kategori Dağılımı")
        else:
            ax2.text(0.5, 0.5, "Henüz gelir verisi yok", ha="center", va="center", color=renk["metin"])
            ax2.set_title("Gelir Kategori Dağılımı")

        # Gider pasta grafiği (yeni)
        fig2 = Figure(figsize=(4, 3), dpi=100)
        ax3 = fig2.add_subplot(111)
        giderler = self.db.kategori_toplamlari("Gider")
        if giderler:
            labels2, values2 = self._diger_grupla(giderler)
            _, metin2, autometin2 = ax3.pie(
                values2,
                labels=labels2,
                autopct="%1.1f%%",
                colors=["#c0392b", "#e74c3c", "#e67e22", "#f39c12", "#d35400", "#7f8c8d"],
            )
            pasta_metinler.append(metin2)
            pasta_metinler.append(autometin2)
            ax3.set_title("Gider Kategori Dağılımı")
        else:
            ax3.text(0.5, 0.5, "Henüz gider verisi yok", ha="center", va="center", color=renk["metin"])
            ax3.set_title("Gider Kategori Dağılımı")

        self._grafik_stil_uygula(fig, ax1, ax2, pasta_metinler=pasta_metinler[:2])
        self._grafik_stil_uygula(fig2, ax3, pasta_metinler=pasta_metinler[2:])

        # ÖNCE ana figür (aylık bar + gelir pastası), SONRA gider pastası.
        # Ters sırada paketlemek küçük gider pastasını en üste koyuyor, asıl
        # grafik altta kalıyordu; kullanıcı hangisinin ana grafik olduğunu
        # çözemiyordu.
        fig.tight_layout()
        canvas = FigureCanvasTkAgg(fig, master=self._grafik_frame)
        canvas.draw()
        canvas.get_tk_widget().pack(fill="both", expand=True)
        self._canvaslar.append(canvas)

        fig2.tight_layout()
        canvas2 = FigureCanvasTkAgg(fig2, master=self._grafik_frame)
        canvas2.draw()
        canvas2.get_tk_widget().pack(fill="both", expand=True, pady=(10, 0))
        self._canvaslar.append(canvas2)

    @staticmethod
    def _diger_grupla(kategoriler, ilk=5):
        """İlk N kategoriyi tutar, kalanları 'Diğer' diliminde toplar.

        Önceden yalnızca ilk 5 çiziliyor, kalanlar sessizce atılıyordu;
        bu yüzden yüzdeler yanıltıcıydı (toplam %100 değil). Artık tüm
        kategoriler temsil edilir.
        """
        temiz = [(str(k), float(v)) for k, v in kategoriler if v]
        ilk_kisim = temiz[:ilk]
        kalan = temiz[ilk:]
        labels = [k for k, _ in ilk_kisim]
        values = [v for _, v in ilk_kisim]
        if kalan:
            labels.append("Diğer")
            values.append(sum(v for _, v in kalan))
        return labels, values

    def _aylik_veri(self):
        """SQL tabanlı aylık özet — tüm veriyi RAM'e çekmez."""
        data = {"Gelir": {}, "Gider": {}}
        for ay, gelir, gider in self.db.aylik_ozet():
            data["Gelir"][ay] = gelir
            data["Gider"][ay] = gider
        return data

    def _aylik_karsilastirma_ciz(self):
        """Bu ay vs geçen ay karşılaştırma grafiği."""
        self._grafikleri_temizle()

        kars = self.db.aylik_karsilastirma()
        bu = kars["bu_ay"]
        gecen = kars["gecen_ay"]

        fig = Figure(figsize=(8, 5), dpi=100)
        ax = fig.add_subplot(111)

        kategoriler = ["Gelir", "Gider"]
        bu_deger = [bu["gelir"], bu["gider"]]
        gecen_deger = [gecen["gelir"], gecen["gider"]]

        x = range(len(kategoriler))
        w = 0.35
        ax.bar([i - w / 2 for i in x], bu_deger, w, color="#14b8a6", label=f"Bu Ay ({bu['ay']:02d}/{bu['yil']})")
        ax.bar([i + w / 2 for i in x], gecen_deger, w, color="#475569", label=f"Geçen Ay ({gecen['ay']:02d}/{gecen['yil']})")
        ax.set_xticks(x)
        ax.set_xticklabels(kategoriler)
        ax.set_ylabel("₺")
        ax.set_title("📊 Bu Ay vs Geçen Ay")
        ax.legend()

        renk = tema_renkleri()
        # Değerleri barların üstüne yaz
        for i, v in enumerate(bu_deger):
            ax.text(i - w / 2, v + 50, para_formatla(v, sembol=False, ondalik=0), ha="center", fontsize=9, color=renk["metin"])
        for i, v in enumerate(gecen_deger):
            ax.text(i + w / 2, v + 50, para_formatla(v, sembol=False, ondalik=0), ha="center", fontsize=9, color=renk["metin"])

        self._grafik_stil_uygula(fig, ax)

        fig.tight_layout()
        canvas = FigureCanvasTkAgg(fig, master=self._grafik_frame)
        canvas.draw()
        canvas.get_tk_widget().pack(fill="both", expand=True)
        self._canvaslar.append(canvas)

    def _yillik_karsilastirma_ciz(self):
        """Yıl bazında gelir/gider karşılaştırma grafiği."""
        self._grafikleri_temizle()

        veri = self.db.yillik_karsilastirma()
        if not veri:
            veri = [(str(datetime.now().year), 0.0, 0.0)]

        yillar = [v[0] for v in veri]
        gelirler = [v[1] for v in veri]
        giderler = [v[2] for v in veri]

        fig = Figure(figsize=(8, 5), dpi=100)
        ax = fig.add_subplot(111)

        x = range(len(yillar))
        w = 0.35
        ax.bar([i - w / 2 for i in x], gelirler, w, color="#2e8b57", label="Gelir")
        ax.bar([i + w / 2 for i in x], giderler, w, color="#c0392b", label="Gider")
        ax.set_xticks(x)
        ax.set_xticklabels(yillar)
        ax.set_ylabel("₺")
        ax.set_title("📆 Yıllık Gelir / Gider Karşılaştırması")
        ax.legend()

        renk = tema_renkleri()
        for i, v in enumerate(gelirler):
            ax.text(i - w / 2, v, para_formatla(v, sembol=False, ondalik=0), ha="center", va="bottom", fontsize=9, color=renk["metin"])
        for i, v in enumerate(giderler):
            ax.text(i + w / 2, v, para_formatla(v, sembol=False, ondalik=0), ha="center", va="bottom", fontsize=9, color=renk["metin"])

        self._grafik_stil_uygula(fig, ax)

        fig.tight_layout()
        canvas = FigureCanvasTkAgg(fig, master=self._grafik_frame)
        canvas.draw()
        canvas.get_tk_widget().pack(fill="both", expand=True)
        self._canvaslar.append(canvas)
