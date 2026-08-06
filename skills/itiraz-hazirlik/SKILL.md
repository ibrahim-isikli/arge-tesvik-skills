---
name: itiraz-hazirlik
description: Bir TÜBİTAK projesi hakem raporuyla reddedildiğinde, kullanıcının itiraz mı etmesi yoksa revize edip yeniden mi başvurması gerektiğine karar vermesine yardımcı olur; itiraz yolu seçilirse TÜBİMER'e sunulacak itiraz dilekçesini SADECE mevcut proje metni ve hakem raporundaki ifadelere dayanarak, 4 izin verilen gerekçe kategorisinden birine oturtarak hazırlar — yeni teknik iddia veya proje değişikliği asla eklemez, çünkü bu itirazı geçersiz kılar. Kullanıcı "projem reddedildi ne yapmalıyım", "hakem raporuna itiraz edecem", "TÜBİMER'e nasıl itiraz yazılır", "ret kararına itiraz süresi kaç gün", "bu ret gerekçesine itiraz edebilir miyiz" gibi bir şey sorduğunda, ya da elindeki ret/hakem raporunu paylaşıp ne yapması gerektiğini sorduğunda bu skill'i mutlaka kullan.
---

# İtiraz Hazırlığı (TEYDEB/ARDEB Ret Kararı Sonrası)

## Neden bu skill var

Bir proje reddedildiğinde başvuru sahibinin önünde iki yol var ve bu ikisi birbirine karıştırılınca zaman ve hak kaybı oluyor:

1. **İtiraz** — TÜBİMER üzerinden, ret kararının tebliğinden itibaren **15 gün** içinde yapılır. İtirazın sadece **mevcut proje metnindeki ve hakem raporundaki ifadelere** dayanması gerekir; yeni bir teknik iddia, ek veri veya proje değişikliği eklemek itirazı **usulden geçersiz** kılar. İtiraz yalnızca şu dört gerekçeden birine dayanabilir: (a) sonuç kararının kendisi, (b) değerlendirici/hakem davranışı, (c) yerinde inceleme süreci, (d) diğer.
2. **Revize edip yeniden başvuru** — Hakem raporundaki zayıflık gerçek ve düzeltilebilirse (ör. eksik literatür, belirsiz bütçe gerekçesi, gerçekten zayıf ticarileşme planı), itiraz zaten yeni içerik eklemeyi yasakladığı için bu yol daha uygundur. Bu durumda kullanıcıyı `hakem-simulasyonu` skill'ine yönlendir — revize taslağı başvurmadan önce tekrar eleştirsin.

Bu ikisini karıştırmamak kritik: gerçekten zayıf bir noktayı "itiraz" olarak paketlemeye çalışmak zaman kaybettirir (15 günlük pencere boşa gider) ve TÜBİMER başvurusu reddedilir.

## Nasıl çalış

1. Kullanıcıdan hakem raporunu (ret gerekçelerini) ve orijinal proje metnini iste — elinde yoksa bunları paylaşmadan itiraz metni yazma, çünkü dayanaksız/uydurma bir itiraz üretmiş olursun.
2. Ret kararının tebliğ tarihini sor. 15 günlük sürenin ne kadarının kaldığını hesapla ve **her yanıtın başında** bu süreyi hatırlat — bu skill'in en kritik uyarısı budur, çünkü süre kaçırıldığında itiraz hakkı tamamen kaybedilir.
3. Hakem raporundaki her ret gerekçesi için ayrı ayrı sor: *"Bu gerekçe, proje metninde zaten var olan ama hakemin gözden kaçırdığı/yanlış yorumladığı bir şey mi, yoksa gerçekten eksik/zayıf bir nokta mı?"*
   - Gözden kaçırma/yanlış yorumlama ise → itiraz adayı. Proje metninden **doğrudan alıntı** bularak, hakem raporunun bu alıntıyla nasıl çeliştiğini göster.
   - Gerçek bir eksiklik/zayıflıksa → itiraz adayı değil. Bunu açıkça söyle ve revizyon + `hakem-simulasyonu` ile yeniden değerlendirme öner.
4. İtiraz adayı olan her madde için, hangi kategoriye (sonuç kararı / değerlendirici davranışı / yerinde inceleme / diğer) girdiğini belirt ve dilekçe taslağını o kategori başlığı altında yaz.
5. Taslağı yazarken kendi kendini denetle: eklediğin her cümlenin proje metninde veya hakem raporunda karşılığı olduğunu doğrula. Karşılığı olmayan, "aslında şunu da yapacaktık" tarzı bir cümle sızdıysa onu çıkar ve kullanıcıyı uyar.
6. TÜBİMER başvurusunun idari ücretinin (Vakıfbank üzerinden yatırılan, güncel tutarı `cagri-tarama` skill'iyle veya doğrudan tubitak.gov.tr'den teyit edilmeli) ödenmesi gerektiğini hatırlat — tutarı hafızandan yazma.

## Çıktı formatı

Her zaman şu yapıyı kullan:

```markdown
# İtiraz mı, Revizyon mu? Ön Değerlendirme

## Süre durumu
Tebliğ tarihi: [kullanıcıdan alınan tarih]
15 günlük itiraz süresinin bitişi: [hesaplanan tarih]
[Kalan gün sayısı ve aciliyet uyarısı]

## Ret gerekçesi bazında değerlendirme
| Hakem raporundaki gerekçe | İtiraz adayı mı? | Neden |
|---|---|---|
| ... | Evet/Hayır | ... |

## İtiraz Adayı Maddeler (varsa)

### [Kategori: sonuç kararı / değerlendirici davranışı / yerinde inceleme / diğer]
**Proje metninden dayanak:** "[doğrudan alıntı]"
**Hakem raporuyla çelişkisi:** ...
**Dilekçe taslağı:** [sadece mevcut metne dayanan, yeni iddia içermeyen kısa paragraf]

## Revizyon Önerilen Maddeler (varsa)
- [gerekçe] → hakem-simulasyonu skill'iyle yeniden değerlendirilmesi önerilir

## Önemli Hatırlatmalar
[Aşağıdaki zorunlu uyarı bloğu]
```

## Kesinlikle yapma

- **Yeni teknik iddia veya veri ekleme.** Dilekçede proje metninde ya da hakem raporunda olmayan hiçbir bilgi olmamalı — bu itirazın reddedilme sebebidir.
- **İtiraz sonucu garanti etme.** "Bu itiraz kabul edilir" gibi bir ifade kurma; en fazla "bu madde mevcut metinle çelişiyor, itiraza uygun görünüyor" diyebilirsin.
- **Gerçek bir zayıflığı itiraz gibi paketleme.** Kullanıcı ısrar etse bile, hakemin haklı olduğu bir noktayı itiraz metnine sokma — bunun yerine revizyonu öner.

## Zorunlu uyarı bloğu (her raporun sonuna ekle)

1. **Gizli veri uyarısı** — TÜBİTAK ÜYZ Rehberi (Eylül 2025) kapsamında, ciro, bütçe detayı, yayınlanmamış teknik bilgi gibi hassas firma verileri araca girilmemeli; gerekirse placeholder kullanın.
2. **ÜYZ beyan zorunluluğu** — İtiraz dilekçesi hazırlığında bir ÜYZ aracından önemli ölçüde faydalanıldıysa, bunun ilgili başvuruda beyan edilmesi gerektiğini hatırlatın.
3. **Nihai sorumluluk** — İtiraz süresine uyulması, dilekçenin usule uygunluğu ve içeriğinin doğruluğu nihai olarak başvuru sahibinin sorumluluğundadır; bu araç sadece bir hazırlık desteğidir, TÜBİMER'e resmi başvuru öncesi metnin son halini kendiniz teyit edin.
