---
description: Açık TÜBİTAK TEYDEB/ARDEB çağrılarını tarar ve son başvuru tarihine göre sıralı tablo üretir (cagri-tarama skill'ini çalıştırır)
argument-hint: [çağrı kodu(ları), örn. "1501 1507" — boş bırakılırsa hepsi taranır]
---

`cagri-tarama` skill'indeki kurallara göre TÜBİTAK çağrılarını tara: bütçe üst limiti ve son başvuru tarihi gibi sayısal değerleri asla hafızadan yazma, güncel kaynaktan çek ve kaynağı belirt, sonucu son başvuru tarihine göre sıralı bir tabloda sun.

Taranacak çağrı(lar): $ARGUMENTS

Yukarıda çağrı kodu belirtilmediyse, 1501, 1505, 1507, 1509, 1511, 1707, ARDEB 1001 ve 3001'in tümünü tara.
