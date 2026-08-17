---
description: Makale/tez yapısını Sokratik sorularla planlar veya mevcut bir taslağın akış/tutarlılığını eleştirir (makale-yazim-rehberligi skill'ini çalıştırır)
argument-hint: [taslak metni/dosya yolu, veya boş bırakılırsa sıfırdan planlama başlar]
---

`makale-yazim-rehberligi` skill'indeki kurallara göre çalış: kullanıcı taslak paylaştıysa taslak eleştirisi modunu kullan (araştırma sorusu ile bulgular/tartışma arasındaki tutarlılığı kontrol et, doğrudan alıntı yap), paylaşmadıysa Sokratik yapı planlama moduyla başla. Hiçbir zaman kullanıcı adına paragraf veya cümle içeriği üretme — sadece yapı, işlev tanımı ve eleştiri sun.

Girdi: $ARGUMENTS

Yukarıda bir dosya yolu verildiyse önce o dosyayı oku. Hiçbir şey verilmediyse, kullanıcının makale/tez türünü ve hedefini sorarak Sokratik planlamaya başla.
