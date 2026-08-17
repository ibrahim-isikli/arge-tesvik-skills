---
description: Bir taslaktaki atıf/kaynakça tutarlılığını ve şüpheli kaynakları kontrol eder (atif-butunluk-kontrolu skill'ini çalıştırır)
argument-hint: [taslak dosya yolu veya yapıştırılmış metin, + varsa atıf stili]
---

Aşağıdaki taslağı `atif-butunluk-kontrolu` skill'indeki kurallara göre kontrol et: metin-içi atıf ↔ kaynakça eşleşmesini çıkar, format tutarlılığını denetle, kaynakçadan riskli görünen bir örneklemi canlı arama ile doğrulamaya çalış (DOĞRULANDI/BULUNAMADI/UYUŞMAZLIK etiketleriyle), aşırı iddialı dili ve yapay zeka açıklaması eksikliğini işaretle. "Bulunamadı" sonucunu asla "uydurma kaynak" ile eş tutma.

Taslak: $ARGUMENTS

Eğer yukarıda bir dosya yolu verildiyse önce o dosyayı oku. Hiçbir taslak verilmediyse, kullanıcıdan kontrol edilecek metni/kaynakçayı ve atıf stilini iste.
