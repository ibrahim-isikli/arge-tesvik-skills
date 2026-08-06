---
name: gider-kalemi-kontrolu
description: Bir TEYDEB proje bütçesindeki gider kalemlerini (personel, seyahat, hizmet alımı, alet/teçhizat/yazılım/yayın alımı, malzeme/sarf) 5 resmi kategoriye oturtur ve her kalemi hakemlerin sık sık uygunsuz/orantısız bulduğu somut kalıplara (fazla mesai-prim-yol-yemek gibi uygun olmayan personel ödemeleri, business class seyahat, "altyapı yatırımı" gibi görünen genel yazılım/donanım alımları, gerekçesiz dış hizmet alımı vb.) göre işaretler. Bütçe üst limiti gibi sayısal değerleri asla hafızadan yazmaz. Kullanıcı "bu bütçe kalemi geçer mi", "gider kalemlerimizi kontrol eder misin", "bu harcamayı proje bütçesine yazabilir miyiz", "hakem bütçeyi neden reddeder", "TEYDEB'de hangi giderler kabul ediliyor" gibi bir şey sorduğunda, ya da bir bütçe/gider dökümü paylaştığında bu skill'i mutlaka kullan.
---

# Gider Kalemi Kontrolü

## Neden bu skill var

Hakem raporlarında en sık tekrar eden ret gerekçelerinden biri bütçe: kalemin gerekçesi zayıf, proje faaliyetiyle bağlantısı belirsiz veya kategoriye uymuyor. `hakem-simulasyonu` skill'i bütçeyi genel bir "proje planı ve yapılabilirlik" başlığı altında ele alır; bu skill ise sadece bütçe kalemlerine odaklanıp her satırı tek tek, bilinen ret kalıplarıyla karşılaştırır. İkisi birbirinin yerine geçmez — bütçe satırlarını didik didik incelemek istiyorsan bu skill'i, tüm öneriyi bütünsel değerlendirmek istiyorsan `hakem-simulasyonu`'nu kullan (ikisini art arda çalıştırmak da makul).

## 5 resmi gider kategorisi

TEYDEB projelerinde desteklenen gider kalemleri şu 5 kategoriden birine girer; bunun dışında bir kategori uydurma:

1. **Personel giderleri** — Ücretli personel ve burslu araştırmacılar.
2. **Seyahat giderleri** — Proje faaliyetiyle doğrudan ilgili yurt içi/yurt dışı seyahatler.
3. **Hizmet alım giderleri** — Ar-Ge ve test hizmetleri, danışmanlık gibi dışarıdan alınan hizmetler.
4. **Alet, teçhizat, yazılım ve yayın alım giderleri**.
5. **Malzeme ve sarf giderleri**.

## Kategori bazlı bilinen ret kalıpları

Her kalemi ilgili kategoriye oturttuktan sonra, aşağıdaki kalıplardan herhangi birine uyup uymadığını kontrol et. Bunlar TEYDEB uygulama esaslarının birebir metni değil, hakem raporlarında ve başvuru sahiplerinin deneyimlerinde sık görülen kırmızı bayraklardır — kesin kural olarak değil, "bunu incele" sinyali olarak kullan.

- **Personel**: Fazla mesai, prim, yol, yemek, yakacak gibi ek ödemeler genelde personel gideri kapsamında kabul edilmez. Proje ekibinde ilgili eğitime sahip en az bir kişi (genelde lisans mezunu) bulunmalı. KOBİ/orta ölçekli firma sahibinin kendine maaş yazması sorun çıkarır. İş planındaki faaliyetlerle personel saatleri tutarsızsa hakem bunu fark eder.
- **Seyahat**: Sadece ekonomi sınıfı uçak bileti kabul edilir; business/premium sınıf talepleri işaretlenir. Proje takvimi veya faaliyetleriyle ilişkisi kurulamayan seyahatler reddedilir.
- **Alet/teçhizat/yazılım/yayın**: Genel amaçlı kurumsal yazılım (ör. ERP) veya "önce altyapı kurup sonra kullanırız" mantığıyla istenen alımlar, hakem tarafından proje özelinde değil "altyapı yatırımı" olarak görülüp reddedilir. Ekip başına orantısız sayıda cihaz istenmesi ve alımın hangi faaliyete hizmet ettiğinin net kurulamaması da sık görülen sorun.
- **Hizmet alımı**: Başvuru sahibinin kendi Ar-Ge katkısını göstermesi gereken işin dışarıya verilmesi hakemde "bu firma ne yapıyor o zaman" sorusunu doğurur. Akademisyen/firma arası sözleşme belgesi eksikse, ya da dış uzmanlığın neden gerekli olduğu açıklanmamışsa işaretle.
- **Malzeme/sarf**: Piyasa koşullarından kopuk, gerekçesiz maliyet tahminleri; erken aşama bir projede prototipleme gerekçesinin zayıf olması; ithal malzemede kur riskinin hiç değerlendirilmemiş olması sık rastlanan sorunlar.
- **Genel örüntü**: Hakemler tutarlı biçimde, gider kaleminin "proje faaliyetiyle ilişkisi" net kurulmamış bütçeleri reddeder — kategori doğru olsa bile gerekçe zayıfsa işaretle.

## Nasıl çalış

1. Kullanıcının paylaştığı bütçe/gider dökümündeki her kalemi yukarıdaki 5 kategoriden birine ata. Hiçbirine net oturmuyorsa bunu ayrıca belirt, kategori uydurma.
2. Her kalem için ilgili kategorinin bilinen ret kalıplarını kontrol et ve eşleşme varsa somut olarak göster: *"Bu kalem [X], çünkü [gerekçe]."*
3. Kalemin proje faaliyetleriyle bağlantısını taslakta/açıklamada bulamıyorsan bunu ayrı bir bulgu olarak işaretle — kategori ve tutar doğru olsa bile bağlantı kurulmamışsa hakem sorar.
4. Bütçe üst limiti, kişi/gün ücret tavanı gibi güncel sayısal sınırlar soruluyorsa hafızandan yazma; `cagri-tarama` skill'ini çalıştırmasını öner ya da doğrudan resmi kaynağı tara.
5. Hiçbir kalemi "bu kesin kabul edilir" diye onaylama — en fazla "bilinen ret kalıplarından hiçbirine uymuyor" diyebilirsin.

## Çıktı formatı

Her zaman şu tabloyu kullan:

```markdown
# Gider Kalemi Kontrolü

| Kalem | Kategori | Bulgu | Gerekçe |
|---|---|---|---|
| ... | Personel / Seyahat / Hizmet Alımı / Alet-Teçhizat-Yazılım-Yayın / Malzeme-Sarf | Uygun görünüyor / Şüpheli / Kategorisi belirsiz | ... |

## Genel örüntü
[Bütçenin genelinde tekrar eden bir sorun varsa buraya]

## Önemli Hatırlatmalar
[Aşağıdaki zorunlu uyarı bloğu]
```

## Kesinlikle yapma

- **Güncel bütçe üst limitini, kişi/gün ücret tavanını veya yüzde sınırlarını hafızadan yazma.** Bunlar sık değişir; kaynağa yönlendir.
- **"Bu kalem kesin kabul edilir" gibi bir garanti verme.** Bilinen ret kalıplarına uymaması, hakemin kabul edeceği anlamına gelmez.
- **Kategori uydurma.** Bir kalem 5 kategoriden hiçbirine net oturmuyorsa bunu belirsiz olarak işaretle, zorla bir kategoriye sokma.

## Zorunlu uyarı bloğu (çıktının sonuna ekle)

1. **Gizli veri uyarısı** — TÜBİTAK ÜYZ Rehberi (Eylül 2025) kapsamında, gerçek tutarlar, tedarikçi/firma isimleri gibi hassas bilgileri araca girmeyin; gerekirse placeholder ile (`[TUTAR]`, `[TEDARİKÇİ]`) kontrol ettirin.
2. **ÜYZ beyan zorunluluğu** — Bütçe hazırlığında bir ÜYZ aracından önemli ölçüde faydalanıldıysa, bunun başvuruda beyan edilmesi gerektiğini hatırlatın.
3. **Nihai sorumluluk** — Gider kalemlerinin uygunluğuna ve tutarlarının doğruluğuna nihai olarak başvuru sahibi karar verir; bu kontrol bilinen kalıplara dayanan bir ön tarama sağlar, resmi kabul/red garantisi vermez.
