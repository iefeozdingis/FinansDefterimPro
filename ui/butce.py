from datetime import datetime
from tkinter import messagebox

import customtkinter as ctk

from ui import tema
from ui.utils import para_formatla, tutar_bind, tutar_oku


class ButceSayfasi(ctk.CTkFrame):
    def __init__(self, parent, db, dashboard_callback=None):
        super().__init__(parent)
        self.db = db
        self.dashboard_callback = dashboard_callback
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(3, weight=1)

        ctk.CTkLabel(
            self, text="📅 Bütçe Yönetimi", font=("Segoe UI", 28, "bold"),
            text_color=tema.METIN_TEAL,
        ).grid(row=0, column=0, pady=(20, 10), sticky="w", padx=20)

        # Ekleme formu
        form = ctk.CTkFrame(self, fg_color=tema.KART, corner_radius=12)
        form.grid(row=1, column=0, sticky="ew", padx=20, pady=(0, 10))

        simdi = datetime.now()
        self.ay = ctk.CTkEntry(form, width=70, placeholder_text="Ay")
        self.ay.insert(0, str(simdi.month))
        self.ay.pack(side="left", padx=(12, 4), pady=10)

        self.yil = ctk.CTkEntry(form, width=90, placeholder_text="Yıl")
        self.yil.insert(0, str(simdi.year))
        self.yil.pack(side="left", padx=4, pady=10)

        self.kategori = ctk.CTkComboBox(form, width=150, values=self._kategori_listesi())
        self.kategori.set("Market")
        self.kategori.pack(side="left", padx=4, pady=10)

        self.tutar = ctk.CTkEntry(form, width=120, placeholder_text="Bütçe Tutarı")
        self.tutar.pack(side="left", padx=4, pady=10)
        tutar_bind(self.tutar)
        self.tutar.bind("<Return>", lambda e: self.kaydet())

        ctk.CTkButton(
            form, text="💾 Kaydet", width=90, fg_color="#0d9488", command=self.kaydet
        ).pack(side="left", padx=4, pady=10)

        # Kontrol barı
        bar = ctk.CTkFrame(self, fg_color="transparent")
        bar.grid(row=2, column=0, sticky="ew", padx=20, pady=(0, 5))
        ctk.CTkButton(
            bar, text="🔄 Göster", width=90, height=28, fg_color="#475569",
            command=self.goster,
        ).pack(side="left", padx=(0, 6))
        ctk.CTkButton(
            bar, text="📝 Önceki Aydan Kopyala", width=180, height=28,
            fg_color="#0ea5e9", command=self._onceki_aydan_kopyala,
        ).pack(side="left")

        # İlerleme çubukları alanı (dashboard'la aynı görsel dil)
        self.liste = ctk.CTkScrollableFrame(self, fg_color=tema.KART, corner_radius=12)
        self.liste.grid(row=3, column=0, sticky="nsew", padx=20, pady=(5, 15))
        self.liste.grid_columnconfigure(0, weight=1)
        self.goster()

    def _kategori_listesi(self) -> list:
        varsayilan = [
            "Maaş", "Prim", "Ek İş", "Faiz", "Yatırım", "Market", "Kira",
            "Fatura", "Yakıt", "Yemek", "Sağlık", "Eğlence", "Diğer",
        ]
        ozel_gelir = self.db.kategorileri_getir("Gelir")
        ozel_gider = self.db.kategorileri_getir("Gider")
        return list(dict.fromkeys(varsayilan + ozel_gelir + ozel_gider))

    def _ay_yil(self):
        try:
            return int(self.ay.get()), int(self.yil.get())
        except ValueError:
            return None, None

    def kaydet(self):
        ay, yil = self._ay_yil()
        if ay is None or not (1 <= ay <= 12):
            messagebox.showerror("Hata", "Ay 1-12 arasında olmalıdır.")
            return
        if not (2000 <= yil <= 2100):
            messagebox.showerror("Hata", "Geçerli bir yıl giriniz (2000-2100).")
            return
        try:
            tutar = tutar_oku(self.tutar)
        except ValueError:
            messagebox.showerror("Hata", "Geçerli bir tutar giriniz.")
            return
        if tutar <= 0:
            messagebox.showerror("Hata", "Bütçe tutarı sıfırdan büyük olmalıdır.")
            return
        self.db.kaydet_butce(ay, yil, self.kategori.get(), tutar)
        self.tutar.delete(0, "end")
        self.goster()
        if self.dashboard_callback:
            self.dashboard_callback()

    def _onceki_aydan_kopyala(self):
        ay, yil = self._ay_yil()
        if ay is None:
            messagebox.showerror("Hata", "Geçerli ay/yıl giriniz.")
            return
        onceki_ay, onceki_yil = (12, yil - 1) if ay == 1 else (ay - 1, yil)
        n = self.db.butce_kopyala(onceki_ay, onceki_yil, ay, yil)
        if n == 0:
            messagebox.showinfo(
                "Bilgi", f"{onceki_ay:02d}.{onceki_yil} için bütçe bulunamadı."
            )
        else:
            messagebox.showinfo("Başarılı", f"{n} kategori bu aya kopyalandı.")
            self.goster()

    def _sil(self, kategori):
        ay, yil = self._ay_yil()
        if ay is None:
            return
        if messagebox.askyesno("Sil", f"'{kategori}' bütçesi silinsin mi?"):
            self.db.butce_sil(ay, yil, kategori)
            self.goster()
            if self.dashboard_callback:
                self.dashboard_callback()

    def goster(self):
        for w in self.liste.winfo_children():
            w.destroy()
        ay, yil = self._ay_yil()
        if ay is None:
            ctk.CTkLabel(
                self.liste, text="Geçerli bir ay ve yıl girin.",
                text_color="#94a3b8",
            ).pack(pady=20)
            return

        durumlar = self.db.butce_durumu(ay, yil)
        if not durumlar:
            # Boş durum — eyleme çağır
            ctk.CTkLabel(
                self.liste, text="Bu ay için henüz bütçe tanımlanmadı.",
                font=("Segoe UI", 14, "bold"), text_color=tema.METIN_TEAL,
            ).pack(pady=(20, 4))
            ctk.CTkLabel(
                self.liste,
                text="Yukarıdan kategori + tutar girerek başla ya da önceki "
                "aydan kopyala.",
                font=("Segoe UI", 12), text_color="#94a3b8",
            ).pack(pady=(0, 20))
            return

        for b in durumlar:
            oran = min(b["harcanan"] / b["butce"] * 100, 100) if b["butce"] > 0 else 0
            renk = "#ef4444" if oran > 90 else "#f59e0b" if oran > 70 else "#22c55e"

            satir = ctk.CTkFrame(self.liste, fg_color="transparent")
            satir.pack(fill="x", padx=12, pady=6)

            ust = ctk.CTkFrame(satir, fg_color="transparent")
            ust.pack(fill="x")
            ctk.CTkLabel(
                ust, text=b["kategori"], font=("Segoe UI", 13, "bold"),
            ).pack(side="left")
            durum = "🔴 Aşıldı" if b["kalan"] < 0 else (
                "🟡 Yaklaşıyor" if b["kalan"] < b["butce"] * 0.1 else "✅"
            )
            ctk.CTkLabel(
                ust, text=f"{durum}  %{int(oran)}",
                font=("Segoe UI", 12), text_color=renk,
            ).pack(side="right")
            ctk.CTkButton(
                ust, text="🗑", width=32, height=24, fg_color="#c0392b",
                command=lambda k=b["kategori"]: self._sil(k),
            ).pack(side="right", padx=(0, 8))

            bar_bg = ctk.CTkFrame(satir, height=14, fg_color="#1e293b", corner_radius=7)
            bar_bg.pack(fill="x", pady=3)
            bar_fill = ctk.CTkFrame(bar_bg, height=14, fg_color=renk, corner_radius=7)
            bar_fill.place(relx=0, rely=0, relheight=1, relwidth=min(oran / 100, 1))

            ctk.CTkLabel(
                satir,
                text=f"Harcanan {para_formatla(b['harcanan'])} / "
                f"Bütçe {para_formatla(b['butce'])} / "
                f"Kalan {para_formatla(b['kalan'])}",
                font=("Segoe UI", 10), text_color="#94a3b8",
            ).pack(anchor="w")
