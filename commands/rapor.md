---
description: TEYDEB dönemsel Gelişme Raporu (AGY301) veya Sonuç Raporu taslağını izleyici/hakem gözüyle değerlendirir (donem-raporu-kontrolu skill'ini çalıştırır)
argument-hint: [rapor taslağı ve onaylı proje planı, veya dosya yolları]
---

`donem-raporu-kontrolu` skill'indeki kurallara göre çalış: önce onaylı proje planını (AGY101/iş paketleri/takvim/bütçe) iste, sonra rapor taslağını iş paketi/hedef bazında planla karşılaştır. Her hedef için somut kanıt olup olmadığını kontrol et, "çalışmalar devam etmektedir" gibi belirsiz ifadeleri işaretle, takvim/bütçe/kapsam sapmalarının gerekçelendirilip gerekçelendirilmediğini değerlendir ve bir sonraki dönem planının tutarlılığını incele. Kesinti/red öngörme, kanıt uydurma, raporu kendi adına yazma.

Rapor taslağı / proje planı: $ARGUMENTS

Yukarıda dosya yolu verildiyse önce o dosyaları oku. Hiçbir şey verilmediyse, kullanıcıdan hem onaylı proje planını hem de değerlendirilecek dönem/gelişme/sonuç raporu taslağını iste.
