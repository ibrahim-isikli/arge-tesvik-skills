---
description: TEYDEB bütçe kalemlerini 5 resmi gider kategorisine oturtur ve bilinen ret kalıplarına göre işaretler (gider-kalemi-kontrolu skill'ini çalıştırır)
argument-hint: [bütçe/gider dökümü veya dosya yolu]
---

`gider-kalemi-kontrolu` skill'indeki kurallara göre çalış: her kalemi personel/seyahat/hizmet alımı/alet-teçhizat-yazılım-yayın/malzeme-sarf kategorilerinden birine ata, bilinen ret kalıplarına (fazla mesai-prim gibi uygun olmayan personel ödemeleri, business class seyahat, "altyapı yatırımı" görünümlü alımlar, gerekçesiz dış hizmet alımı, piyasadan kopuk malzeme tahmini vb.) göre işaretle, güncel bütçe üst limitini hafızandan yazma. Hiçbir kalemi "kesin kabul edilir" diye onaylama.

Bütçe/gider dökümü: $ARGUMENTS

Yukarıda bir dosya yolu verildiyse önce o dosyayı oku. Hiçbir şey verilmediyse, kullanıcıdan gider kalemi dökümünü iste.
