# 💎 FINEding — Akıllı Kişisel Finans Yönetimi

<div align="center">

**Python + CustomTkinter ile geliştirilmiş, şık ve güçlü bir masaüstü finans takip uygulaması.**

<sub>🌍 A local-first, privacy-focused personal finance desktop app (Turkish UI). All data stays on your machine — no cloud, no accounts, no tracking. Income/expense tracking, budgets, debts, savings goals, charts, CSV/Excel/PDF.</sub>

[![Python](https://img.shields.io/badge/Python-3.10%2B-blue)](https://python.org)
[![Tests](https://img.shields.io/badge/Tests-103%2F103%20✅-green)](tests/)
[![License](https://img.shields.io/badge/License-MIT-yellow)](LICENSE)
[![GitHub issues](https://img.shields.io/github/issues/iefeozdingis/FINEding)](https://github.com/iefeozdingis/FINEding/issues)

</div>

---

## 🎯 Neden FINEding?

Harcamalarını kontrol etmek, bütçeni yönetmek ve finansal hedeflerine ulaşmak ister misin?  
FINEding, tüm gelir-gider takibini **tek bir şık arayüzde**, **ücretsiz** ve **reklamsız** olarak sunar.

> 💡 *"Paranı yönet, hayatını yönet."*

---

## ✨ Tüm Özellikler

### 📊 Dashboard
- **4 özet kartı**: Toplam Gelir, Gider, Bakiye, İşlem Sayısı
- **Bütçe ilerleme çubukları**: Kategori bazlı renkli progress bar (🟢🟡🔴)
- **Akıllı uyarılar**: Bütçe aşımı ve yaklaşan limit bildirimleri
- **Hızlı işlem**: 💰 +Gelir / 💸 +Gider popup (tutar yaz, Enter'la)
- **Günlük/Haftalık filtre**: "Bugün", "Bu Hafta", "Tümü" butonları
- **Arama & filtreleme**: Kategori, açıklama, etiket veya tutara göre anlık arama
- **🔍 Global arama**: Ctrl+F ile tüm işlem ve borç/alacaklarda anında ara
- **Dışa aktar**: Tek tıkla CSV 📄, Excel 📗, PDF 📕
- **📥 İçe aktar**: CSV veya Excel dosyasından toplu işlem yükle

### 💰 Gelir & Gider Yönetimi
- Gelir/gider kaydı ekle, düzenle, sil, geri al
- Kategori bazlı işlem takibi (özel kategori eklenebilir)
- 🏷️ İşlemlere serbest etiket ekleme (virgülle ayrılmış), etikete göre arama
- Toplu silme (Ctrl+seçim)
- Tarih otomatik formatlama (GG.AA.YYYY)

### 📅 Bütçe & Planlama
- **Aylık bütçe**: Kategori başına limit belirle
- **Bütçe ilerleme çubukları**: Dashboard'da görsel takip
- **Aylık planlama**: Gelecek ay gelir/gider tahmini
- **Borç & Alacak takibi**: Kimden, ne kadar, vadesi ne zaman?
- **🔄 Tekrarlayan işlemler**: Kira, fatura gibi düzenli ödemeleri her ay otomatik ekler
- **🎯 Tasarruf hedefleri**: Hedef tutar/tarih belirle, katkı ekle, renkli ilerleme çubuğuyla takip et

### 📈 Grafikler & Analiz
- **Aylık gelir/gider çubuk grafiği**
- **Kategori dağılımı pasta grafikleri** (Gelir + Gider)
- **📊 Bu Ay vs Geçen Ay** karşılaştırma grafiği
- **📆 Yıllık Karşılaştırma** — yıl bazında gelir/gider trendi
- Matplotlib ile profesyonel görselleştirme

### 🔐 Çok Kullanıcılı Sistem
- Her kullanıcı kendi hesabıyla giriş yapar
- **Admin paneli**: Kullanıcı yönetimi, şifre sıfırlama, kullanıcı silme
- Şifreler bcrypt ile hash'lenir (her kullanıcı için ayrı tuz)
- "Beni Hatırla" özelliği

### 🎨 Arayüz
- **🌓 Aydınlık/Karanlık tema**: Sidebar'dan tek tıkla değiştir
- CustomTkinter ile modern, responsive tasarım
- Teal ( #0f766e ) renk teması
- Klavye kısayolları (Ctrl+D Dashboard, Ctrl+N Gelir, vb.)
- Emoji ikonları ile zengin görsel deneyim

### 🛡️ Sistem Özellikleri
- **🔔 Masaüstü bildirimleri**: Borç vadesi yaklaşınca uyarı
- **⬇️ Sistem tepsisi**: Kapatınca arka planda çalışır
- **💾 Otomatik yedekleme**: Uygulama kapanırken `backups/` altına yedekler (son 10 tutulur)
- **🗂 Manuel yedekleme**: İstediğin zaman yedek al, geri yükle
- HMAC-SHA256 imzası ile yedek bütünlük/kurcalama kontrolü

---

## 🚀 Hızlı Başlangıç

### Gereksinimler
- **Python 3.10+** ([python.org](https://python.org))
- **Windows 10/11**

### Tek Tıkla Kurulum (Yeni Kullanıcılar)
```bash
# Projeyi indir, KURULUM.bat'a çift tıkla — her şeyi otomatik yapar!
```

### ⚡ Tek Dosya İndir (En Kolay)
**[📥 FINEding.exe İndir](https://github.com/iefeozdingis/FINEding/releases/latest)**  
Python kurmaya gerek yok! Tek `.exe` dosyası, çift tıkla çalışır (~216 MB).

### Manuel Kurulum
```bash
git clone https://github.com/iefeozdingis/FINEding.git
cd FINEding
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
python main.py
```

### İlk Giriş
Uygulama ilk açıldığında **kendi hesabını oluşturursun** — önceden tanımlı
bir `admin/12345` hesabı yoktur. İlk kaydolan kullanıcı otomatik olarak admin
olur. Şifreler bcrypt ile hash'lenir ve en az 8 karakter olmalıdır.

> ⚠️ Eski sürümlerde belgelenmiş `admin/12345` gibi varsayılan bir hesap
> kullanıyorsan, **ilk fırsatta Ayarlar → Şifre Değiştir** ile güçlü bir
> şifre belirle.

---

## ⌨️ Klavye Kısayolları

| Kısayol | Sayfa |
|---------|-------|
| `Ctrl+F` | 🔍 Tüm Uygulamada Ara |
| `Ctrl+D` | Dashboard |
| `Ctrl+N` | Gelir Ekle |
| `Ctrl+Shift+N` | Gider Ekle |
| `Ctrl+Shift+G` | Grafikler |
| `Ctrl+B` | Bütçe |
| `Ctrl+P` | Planlama |
| `Ctrl+,` | Ayarlar |
| `Ctrl+Q` | Kapat (tepsi açıksa arka plana küçültür) |

---

## 🧪 Testler

```bash
python -m unittest discover -s tests -v
```

3 test dosyası, toplam **103 test** (hepsi yeşil):

| Dosya | Kapsam |
|---|---|
| `tests/test_database.py` | Veri katmanı: işlem/bütçe/borç/tasarruf, kullanıcı izolasyonu, migrasyon, yedek |
| `tests/test_para.py` | Para ayrıştırma/biçimlendirme, bütçe eşikleri, tarih biçimleme (Tk gerektirmez) |
| `tests/test_utils.py` | Tarih formatlama widget davranışı |

> CI, koşan test sayısı 103'ün altına düşerse veya çok fazla test atlanırsa başarısız olur — testlerin sessizce atlanmasını engeller.

---

## 🗂 Proje Yapısı

```
FINEding/
├── main.py              # Uygulama ana giriş + tema + menü
├── database.py           # SQLite veritabanı katmanı
├── requirements.txt      # Bağımlılıklar
├── KURULUM.bat           # 🆕 Tek tıkla kurulum
├── run_finans_defterim.bat  # Başlatıcı
├── version.py            # Sürüm — tek kaynak
├── ui/
│   ├── dashboard.py      # Ana dashboard (kartlar + tablo + filtre + dışa aktar)
│   ├── gelir.py / gider.py  # Gelir/gider ekleme sayfaları
│   ├── islem_formu.py    # Ortak işlem formu
│   ├── butce.py          # Bütçe yönetimi
│   ├── planlama.py       # Planlama + borç/alacak + tekrarlayan + tasarruf
│   ├── grafikler.py      # Grafikler ve aylık karşılaştırma
│   ├── global_arama.py   # Ctrl+F ile tüm uygulamada arama
│   ├── ayarlar.py        # Ayarlar + admin paneli
│   ├── giris.py          # Giriş/kayıt ekranı
│   ├── hakkinda.py       # Hakkında sayfası
│   ├── money.py          # Para/eşik saf fonksiyonları (GUI-bağımsız)
│   └── utils.py          # Tarih/para/modal yardımcıları
├── tests/                # 3 dosya, 103 test
├── database/             # SQLite veritabanı (.gitignore)
├── backups/              # Otomatik yedekler
├── logs/                 # Uygulama logları
└── assets/               # İkon ve tema dosyaları
```

---

## 🛠 Teknoloji Stack'i

| Katman | Teknoloji |
|--------|----------|
| Arayüz | CustomTkinter |
| Grafik | Matplotlib |
| Veritabanı | SQLite3 |
| Rapor | ReportLab (PDF), openpyxl (Excel) |
| Bildirim | Plyer |
| Sistem Tepsisi | Pystray |

---

## 🩹 Son Düzeltmeler (2026-07-12)

- **⚠️ Eski (SHA-256) şifreler artık doğrulanamıyordu:** bcrypt eklendikten sonra, bcrypt öncesi oluşturulmuş hesapların şifreleri hiçbir zaman eşleşmiyordu — bu hesaplar kilitli kalıyordu. Eski hash formatı için ayrı doğrulama yolu eklendi.
- **⚠️ Manuel yedekleme veri kaybediyordu:** `Yedek Oluştur` butonu, WAL modundaki veritabanını checkpoint yapmadan kopyalıyordu — uygulama kapatılmadan alınan yedekler tabloları bile içermeyebiliyordu. Artık kopyalamadan önce checkpoint zorlanıyor.
- **"Geri Al" işlemi etiketleri siliyordu:** silinen bir işlem geri alındığında etiket/not bilgisi kayboluyordu; artık korunuyor.
- **X'e basınca tepsi simgesi yoksa uygulama arka planda takılı kalıyordu:** tepsi desteği olmayan/başarısız olan durumlarda artık gerçekten kapanıyor.
- **Yedek temizliğinde `.sha256` dosyaları birikiyordu:** eski yedekler silinirken eşlik eden checksum dosyaları artık birlikte siliniyor.
- **Tema tercihi kalıcı değildi:** uygulama her açılışta koyu temayla başlıyordu; artık son seçilen tema hatırlanıyor.
- **Admin şifre sıfırlama diyalogunda yeni şifre açık metin görünüyordu:** maskelendi.
- Kullanılmayan `ui/raporlar.py` (ölü kod) kaldırıldı.
- Planlama → Tekrarlayan sekmesi açılmıyordu, Bütçe sayfası tema hatası veriyordu, Bakiye widget'ı hiç görünmüyordu — hepsi çözüldü.
- Tüm sayfalar hatasız açılıyor; tüm testler yeşil.

## 📝 Geliştirici Notları

- **Commit Convention:** `fix:`, `feat:`, `chore:`, `style:`, `test:`
- **Issue sistemi:** Bug bildirimi ve özellik isteği şablonları mevcut
- **CI/CD:** GitHub Actions ile otomatik test + lint
- **Auto-issue:** CI başarısız olursa otomatik bug issue'su oluşturur

---

## 🤝 Katkı & Güvenlik

- Katkı vermek istersen: [CONTRIBUTING.md](CONTRIBUTING.md) (kod dışı katkılar da dahil)
- Sürüm geçmişi: [CHANGELOG.md](CHANGELOG.md)
- Güvenlik açığı bildirimi: [SECURITY.md](SECURITY.md)

---

## 📄 Lisans

[MIT](LICENSE) — Dilediğin gibi kullan, değiştir, paylaş.

---

**FINEding** — Finansal geleceğini planla, kontrol et! 💎

<div align="center">

**⭐ Bu projeyi beğendiysen yıldız vermeyi unutma!**

[![Star History Chart](https://img.shields.io/github/stars/iefeozdingis/FINEding?style=social)](https://github.com/iefeozdingis/FINEding)

</div>
