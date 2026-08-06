---
description: TÜBİTAK ret kararı sonrası itiraz mı yoksa revizyon mu uygun karar verir, itiraz yolu için TÜBİMER dilekçe taslağı hazırlar (itiraz-hazirlik skill'ini çalıştırır)
argument-hint: [hakem raporu / ret gerekçesi metni veya dosya yolu]
---

`itiraz-hazirlik` skill'indeki kurallara göre çalış: önce ret kararının tebliğ tarihini ve kalan 15 günlük itiraz süresini netleştir, sonra her ret gerekçesini itiraz adayı mı yoksa revizyon konusu mu diye ayır. İtiraz adayı maddeler için dilekçe taslağını SADECE mevcut proje metnine/hakem raporuna dayanarak yaz, yeni teknik iddia ekleme. Revizyon önerilen maddeler için kullanıcıyı `hakem-simulasyonu` skill'ine yönlendir.

Hakem raporu / ret gerekçesi: $ARGUMENTS

Yukarıda bir dosya yolu verildiyse önce o dosyayı oku. Hiçbir şey verilmediyse, kullanıcıdan hakem raporunu (veya ret gerekçelerini), orijinal proje metnini ve ret kararının tebliğ tarihini iste.
