# Güvenlik Politikası

FINEding kişisel finans verisi tutar; güvenliği ciddiye alıyoruz.

## Zafiyet bildirimi

Bir güvenlik açığı bulduysan **herkese açık issue AÇMA.** Bunun yerine
GitHub'ın **[Security Advisories](https://github.com/iefeozdingis/FINEding/security/advisories/new)**
(özel bildirim) özelliğini kullan. Makul sürede yanıt vermeye çalışırız.

Lütfen şunları paylaş: etkilenen sürüm, yeniden üretme adımları, olası etki.

## Mevcut güvenlik duruşu

- **Yerel-öncelikli:** Tüm veri kullanıcının makinesinde kalır. Bulut yok,
  hesap yok, telemetri yok.
- **Şifreler:** bcrypt ile hash'lenir (kullanıcıya özel tuz). bcrypt yoksa
  uygulama zayıf hash üretmek yerine hata verir.
- **Yedekler:** HMAC-SHA256 imzasıyla bütünlük/kurcalama kontrolü.
- **İzolasyon:** Çok kullanıcılı kurulumda her kullanıcının verisi
  `kullanici_id` ile ayrılır.
- **Dışa aktarım:** CSV/Excel formül enjeksiyonuna karşı hücreler temizlenir.

## Bilinen sınırlamalar (yol haritasında)

- **At-rest şifreleme yok:** Veritabanı ve yedekler diskte düz metindir.
  Diske fiziksel erişimi olan biri (çalınan cihaz, paylaşılan hesap) finans
  geçmişini ve parola hash'lerini okuyabilir. SQLCipher + OS anahtar deposu
  değerlendiriliyor.
- **Uzaktan erişim yok:** Uygulama yalnızca yerel çalışır; ağ saldırı yüzeyi
  bulunmaz. İleride mobil/web erişimi eklenirse kimlik doğrulama + TLS zorunlu
  olacaktır.

## Desteklenen sürümler

En son yayınlanan sürüm desteklenir. Güncel sürümü kullanman önerilir.
