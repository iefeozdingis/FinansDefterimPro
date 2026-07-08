# csv import removed (unused) to satisfy flake8 F401
import tkinter as tk
from datetime import datetime
from tkinter import filedialog, messagebox

import customtkinter as ctk
from openpyxl import Workbook
from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.units import mm

from ui.utils import tarih_bind


class RaporlarSayfasi(ctk.CTkFrame):
    def __init__(self, parent, db, dashboard_callback=None):
        super().__init__(parent)
        self.db = db
        self.dashboard_callback = dashboard_callback
        self.grid_columnconfigure(0, weight=1)

        ctk.CTkLabel(self, text="📄 Raporlar", font=("Segoe UI", 28, "bold")).pack(
            pady=20
        )

        simdi = datetime.now()
        ctk.CTkLabel(self, text="Başlangıç Tarihi", font=("Segoe UI", 14)).pack()
        self.baslangic = ctk.CTkEntry(self, width=300, placeholder_text="GG.AA.YYYY")
        self.baslangic.insert(0, simdi.strftime("%d.%m.%Y"))
        self.baslangic.pack(pady=6)
        tarih_bind(self.baslangic)

        ctk.CTkLabel(self, text="Bitiş Tarihi", font=("Segoe UI", 14)).pack()
        self.bitis = ctk.CTkEntry(self, width=300, placeholder_text="GG.AA.YYYY")
        self.bitis.insert(0, simdi.strftime("%d.%m.%Y"))
        self.bitis.pack(pady=6)
        tarih_bind(self.bitis)

        ctk.CTkButton(
            self, text="📊 Raporu Göster", width=220, command=self.goster
        ).pack(pady=16)
        ctk.CTkButton(
            self, text="⬇️ CSV Olarak Dışa Aktar", width=240, command=self.disa_aktar
        ).pack(pady=8)
        ctk.CTkButton(
            self, text="📗 Excel Olarak Dışa Aktar", width=240, command=self.excel_aktar
        ).pack(pady=8)
        ctk.CTkButton(
            self, text="📥 CSV'den İçe Aktar", width=240, command=self.ice_aktar,
            fg_color="#2e7d32", hover_color="#1b5e20"
        ).pack(pady=8)
        ctk.CTkButton(
            self, text="📕 PDF Olarak Dışa Aktar", width=240, command=self.pdf_aktar,
            fg_color="#c0392b", hover_color="#962d22"
        ).pack(pady=8)

        self.ozet = ctk.CTkTextbox(self, height=220)
        self.ozet.pack(fill="both", expand=True, padx=20, pady=10)

    def goster(self):
        try:
            gelir = self.db.toplam_gelir_aralik(self.baslangic.get(), self.bitis.get())
            gider = self.db.toplam_gider_aralik(self.baslangic.get(), self.bitis.get())
            bakiye = gelir - gider
            self.ozet.delete("1.0", tk.END)
            self.ozet.insert(tk.END, f"Başlangıç: {self.baslangic.get()}\n")
            self.ozet.insert(tk.END, f"Bitiş: {self.bitis.get()}\n")
            self.ozet.insert(tk.END, f"Toplam Gelir: {gelir:,.2f} ₺\n")
            self.ozet.insert(tk.END, f"Toplam Gider: {gider:,.2f} ₺\n")
            self.ozet.insert(tk.END, f"Net Bakiye: {bakiye:,.2f} ₺\n")
        except Exception as hata:
            messagebox.showerror("Hata", str(hata))

    def disa_aktar(self):
        yol = filedialog.asksaveasfilename(
            defaultextension=".csv", filetypes=[("CSV Dosyası", "*.csv")]
        )
        if yol:
            self.db.export_csv(yol)
            messagebox.showinfo("Başarılı", f"Rapor dışa aktarıldı: {yol}")

    def excel_aktar(self):
        yol = filedialog.asksaveasfilename(
            defaultextension=".xlsx", filetypes=[("Excel Dosyası", "*.xlsx")]
        )
        if not yol:
            return

        wb = Workbook()
        ws = wb.active
        ws.title = "İşlemler"
        ws.append(["id", "tarih", "tur", "kategori", "aciklama", "tutar"])
        for satir in self.db.tum_islemler():
            ws.append(satir)
        wb.save(yol)
        messagebox.showinfo("Başarılı", f"Excel raporu kaydedildi: {yol}")

    def ice_aktar(self):
        yol = filedialog.askopenfilename(
            defaultextension=".csv", filetypes=[("CSV Dosyası", "*.csv")]
        )
        if not yol:
            return
        try:
            eklenen = self.db.import_csv(yol)
            messagebox.showinfo("Başarılı", f"{eklenen} işlem içe aktarıldı.")
            if self.dashboard_callback:
                self.dashboard_callback()
        except Exception as hata:
            messagebox.showerror("Hata", str(hata))

    def pdf_aktar(self):
        yol = filedialog.asksaveasfilename(
            defaultextension=".pdf", filetypes=[("PDF Dosyası", "*.pdf")]
        )
        if not yol:
            return

        try:
            gelir = self.db.toplam_gelir_aralik(self.baslangic.get(), self.bitis.get())
            gider = self.db.toplam_gider_aralik(self.baslangic.get(), self.bitis.get())
            bakiye = gelir - gider
            islemler = self.db.islemler_aralik(self.baslangic.get(), self.bitis.get())

            doc = SimpleDocTemplate(yol, pagesize=A4, topMargin=20 * mm)
            styles = getSampleStyleSheet()
            elements = []

            # Başlık
            title = Paragraph(
                f"<b>Fineding - Finansal Rapor</b>",
                styles["Title"],
            )
            elements.append(title)
            elements.append(Spacer(1, 6 * mm))

            # Tarih aralığı
            elements.append(Paragraph(
                f"Rapor Dönemi: {self.baslangic.get()} - {self.bitis.get()}",
                styles["Normal"],
            ))
            elements.append(Paragraph(
                f"Oluşturma Tarihi: {datetime.now().strftime('%d.%m.%Y %H:%M')}",
                styles["Normal"],
            ))
            elements.append(Spacer(1, 6 * mm))

            # Özet
            ozet_data = [
                ["Özet", "Tutar"],
                ["Toplam Gelir", f"{gelir:,.2f} ₺"],
                ["Toplam Gider", f"{gider:,.2f} ₺"],
                ["Net Bakiye", f"{bakiye:,.2f} ₺"],
            ]
            ozet_tablo = Table(ozet_data, colWidths=[80 * mm, 60 * mm])
            ozet_tablo.setStyle(TableStyle([
                ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#2e8b57")),
                ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
                ("ALIGN", (0, 0), (-1, -1), "CENTER"),
                ("GRID", (0, 0), (-1, -1), 0.5, colors.grey),
                ("FONTSIZE", (0, 0), (-1, -1), 10),
                ("BACKGROUND", (0, 1), (-1, 1), colors.HexColor("#e8f5e9")),
                ("BACKGROUND", (0, 2), (-1, 2), colors.HexColor("#fce4ec")),
                ("BACKGROUND", (0, 3), (-1, 3), colors.HexColor("#e3f2fd")),
            ]))
            elements.append(ozet_tablo)
            elements.append(Spacer(1, 10 * mm))

            # İşlemler tablosu
            if islemler:
                elements.append(Paragraph("<b>İşlem Detayları</b>", styles["Heading2"]))
                elements.append(Spacer(1, 3 * mm))
                tablo_data = [["ID", "Tarih", "Tür", "Kategori", "Açıklama", "Tutar"]]
                for satir in islemler:
                    tablo_data.append([
                        str(satir[0]),
                        str(satir[1]),
                        str(satir[2]),
                        str(satir[3]),
                        str(satir[4] or ""),
                        f"{float(satir[5]):,.2f} ₺",
                    ])
                tablo = Table(tablo_data, colWidths=[12 * mm, 23 * mm, 17 * mm, 30 * mm, 42 * mm, 25 * mm])
                tablo.setStyle(TableStyle([
                    ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#333333")),
                    ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
                    ("ALIGN", (0, 0), (-1, -1), "CENTER"),
                    ("ALIGN", (3, 0), (3, -1), "LEFT"),
                    ("GRID", (0, 0), (-1, -1), 0.3, colors.grey),
                    ("FONTSIZE", (0, 0), (-1, -1), 7),
                    ("ROWBACKGROUNDS", (0, 1), (-1, -1), [colors.white, colors.HexColor("#f5f5f5")]),
                ]))
                elements.append(tablo)
            else:
                elements.append(Paragraph(
                    "<i>Bu tarih aralığında işlem bulunamadı.</i>", styles["Normal"]
                ))

            doc.build(elements)
            messagebox.showinfo("Başarılı", f"PDF raporu kaydedildi: {yol}")
        except Exception as hata:
            messagebox.showerror("Hata", str(hata))
