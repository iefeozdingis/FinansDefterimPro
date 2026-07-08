# 💎 FINEding — Kişisel Finans Yönetimi

Modern ve kullanıcı dostu bir kişisel gelir-gider takip uygulaması.  
CustomTkinter ile geliştirilmiş, karanlık tema destekli masaüstü uygulaması.

---

## ✨ Özellikler

| Kategori | Detay |
|---|---|
| 💰 **Gelir & Gider** | Gelir ve gider kayıtlarını ekle, düzenle, sil |
| 📊 **Dashboard** | Toplam gelir, gider, bakiye ve işlem sayısını tek ekranda gör |
| 📅 **Bütçe Yönetimi** | Kategori bazlı aylık bütçe belirle, aşım uyarıları al |
| 📋 **Planlama** | Gelecek ay planlaması, borç & alacak takibi |
| 📈 **Grafikler** | Aylık gelir/gider grafikleri, pasta grafiklerle kategori dağılımı |
| 📄 **Raporlar** | CSV, Excel ve PDF formatında dışa aktarım |
| 🔐 **Çok Kullanıcılı** | Her kullanıcı kendi hesabıyla giriş yapar |
| 👑 **Admin Paneli** | Admin kullanıcıları yönetir, şifre sıfırlar |
| 🔔 **Bildirimler** | Borç vadesi yaklaşınca masaüstü bildirimi |
| ⬇️ **Sistem Tepsisi** | Kapatınca arka planda çalışır, tepsi simgesinden eriş |
| 🗂 **Yedekleme** | Veritabanı yedekleme ve geri yükleme |

---

## 🚀 Kurulum

### Gereksinimler
- Python 3.10+
- Windows işletim sistemi

### Adımlar

```bash
# 1. Projeyi klonla
git clone https://github.com/kullanici/FINEding.git
cd FINEding

# 2. Sanal ortam oluştur
python -m venv .venv

# 3. Sanal ortamı aktif et
.venv\Scripts\activate

# 4. Bağımlılıkları kur
pip install -r requirements.txt

# 5. Uygulamayı başlat
python main.py
```

### Tek Tıkla Çalıştırma
`run_finans_defterim.bat` dosyasına çift tıklayarak uygulamayı doğrudan başlatabilirsin.

---

## 🎯 İlk Kullanım

1. Uygulama ilk açıldığında giriş ekranı gelir
2. **"📝 Yeni Hesap Oluştur"** butonuna tıkla
3. Ad soyad, kullanıcı adı ve şifreni belirle
4. **İlk oluşturulan hesap otomatik olarak 👑 Admin olur**
5. Giriş yap ve kullanmaya başla!

> ℹ️ Veritabanı dosyası (`database/finans.db`) `.gitignore`'a eklenmiştir.  
> GitHub'dan indiren herkes sıfırdan kendi hesabını oluşturur.

---

## 👑 Admin Özellikleri

İlk kayıt olan kullanıcı (ID: 1) admin yetkilerine sahiptir:

- **Kullanıcı Listesi**: Tüm kayıtlı kullanıcıları görüntüle
- **Şifre Sıfırlama**: Herhangi bir kullanıcının şifresini değiştir
- **Kullanıcı Silme**: İstenmeyen hesapları kalıcı olarak sil

Admin paneline **Ayarlar** sayfasının en altından ulaşılır.

---

## 🛠 Teknoloji

| Teknoloji | Kullanım |
|---|---|
| Python 3.10+ | Ana dil |
| CustomTkinter | Modern masaüstü arayüzü |
| SQLite3 | Yerel veritabanı |
| Matplotlib | Grafik ve görselleştirme |
| Pillow (PIL) | Görüntü işleme |
| Plyer | Masaüstü bildirimleri |
| PyStray | Sistem tepsisi entegrasyonu |
| OpenPyXL | Excel dışa aktarım |
| ReportLab | PDF dışa aktarım |

---

## 📁 Proje Yapısı

```
FINEding/
├── main.py              # Uygulama giriş noktası
├── database.py          # Veritabanı işlemleri
├── requirements.txt     # Python bağımlılıkları
├── run_finans_defterim.bat  # Tek tıkla başlatma
├── run_finans_defterim.vbs  # Sessiz başlatma
├── assets/              # Logo ve tema dosyaları
├── database/            # SQLite veritabanı (.gitignore)
├── exports/             # Dışa aktarılan raporlar
├── logs/                # Uygulama logları
├── tests/               # Test dosyaları
└── ui/                  # Arayüz modülleri
    ├── dashboard.py     # Ana gösterge paneli
    ├── gelir.py         # Gelir ekleme sayfası
    ├── gider.py         # Gider ekleme sayfası
    ├── giris.py         # Giriş ekranı
    ├── grafikler.py     # Grafikler sayfası
    ├── butce.py         # Bütçe yönetimi
    ├── planlama.py      # Planlama & borç takibi
    ├── raporlar.py      # Rapor dışa aktarım
    ├── ayarlar.py       # Ayarlar & admin paneli
    ├── hakkinda.py      # Hakkında sayfası
    └── utils.py         # Yardımcı fonksiyonlar
```

---

## 🧪 Test

```bash
python -m unittest discover -s tests -v
```

---

## 📝 Lisans

MIT License — Dilediğin gibi kullan, değiştir, paylaş.

---

**FINEding** — Finansal geleceğini planla, kontrol et! 💎
