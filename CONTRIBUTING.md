# Katkı Rehberi

FINEding'e katkın için teşekkürler! 🎉 Bu proje **yerel-öncelikli, gizlilik-dostu,
Türkçe** bir kişisel finans uygulamasıdır. Her boyutta katkı değerlidir.

## Kod dışı katkılar da değerli

Python bilmesen de yardımcı olabilirsin:

- 🐛 **Hata bildir** — Issues → "Bug bildirimi" şablonu
- 💡 **Özellik öner** — Issues → "Özellik isteği" şablonu
- 📖 **Dokümantasyon** — README/CHANGELOG düzeltmeleri, çeviri
- 🎨 **Tasarım** — ekran görüntüsü, ikon, arayüz önerisi
- 🧪 **Test et** — yeni sürümü dene, geri bildirim ver

## Geliştirme ortamı

```bash
git clone https://github.com/iefeozdingis/FINEding.git
cd FINEding
python -m venv .venv
.venv\Scripts\activate          # Windows
pip install -r requirements.txt
pip install -r dev-requirements.txt
python main.py
```

## Kalite kapıları (PR açmadan önce üçü de geçmeli)

CI bunları zorunlu tutar; yerelde de çalıştır:

```bash
python -m unittest discover -s tests    # tüm testler, atlanmadan
flake8 --config .flake8 .               # stil
mypy .                                  # tip denetimi
```

- **Yeni veritabanı/iş mantığı → test ekle.** İş mantığını mümkünse UI'dan
  ayrı, saf fonksiyona koy (bkz. `ui/money.py`) — Tk gerektirmeden test edilir.
- **Şema değişikliği → migrasyon yaz.** `database.py`'deki numaralı
  `_migrate_*` desenini izle ve `SCHEMA_VERSION`'ı artır; eski veritabanlarını
  veri kaybı olmadan yükselt.
- **Para → `ui.money.para_parse`/`para_formatla` kullan**, elle `float()` yok.

## Commit kuralı

Türkçe, açıklayıcı, önekli:

- `fix:` hata düzeltme · `feat:` yeni özellik · `refactor:` davranış
  değiştirmeyen düzenleme · `ci:` CI/CD · `chore:` bakım · `test:` test

## Mimari (kısa)

- `database.py` — SQLite veri katmanı (izolasyon `kullanici_id` ile)
- `ui/` — CustomTkinter sayfaları; `ui/money.py` & `ui/utils.py` saf yardımcılar
- `main.py` — uygulama kabuğu, menü, periyodik kontroller
- `tests/` — `test_database.py` (veri), `test_para.py` & `test_utils.py` (Tk'siz)

Büyük bir değişikliğe başlamadan önce bir **issue açıp tartışman** önerilir.
