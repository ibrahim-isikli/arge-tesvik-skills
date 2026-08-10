---
description: Aynı projeye ait birden fazla belge (proje planı, bütçe, iş paketleri, hakem raporu, dönem raporu vb.) arasında süre/bütçe/personel/hedef gibi alanlarda çelişki arar (proje-tutarlilik-kontrolu skill'ini çalıştırır)
argument-hint: [karşılaştırılacak iki veya daha fazla belge/dosya yolu]
---

`proje-tutarlilik-kontrolu` skill'indeki kurallara göre çalış: en az iki belge olmadan çelişki aranamayacağını unutma, her belgeden süre/bütçe/personel/iş paketleri/TRL/ticarileşme tarihi gibi alanları çıkar, farklı belgelerde farklı değer varsa çelişki olarak işaretle, hangi değerin doğru olduğuna karar verme, tutarlı bulunan alanları da raporla.

Belgeler: $ARGUMENTS

Yukarıda dosya yolları verildiyse önce onları oku. İki belgeden azı verildiyse, kullanıcıdan karşılaştırılacak ikinci (veya daha fazla) belgeyi iste.
