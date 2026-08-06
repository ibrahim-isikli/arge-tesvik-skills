---
name: patent-on-arastirma
description: Bir proje fikri için markapatent-mcp sunucusu üzerinden TÜRKPATENT'te patent, marka ve tasarım ön araştırması yapar; benzer başvuruları listeler. Sadece bulguları sunar, "bu fikir özgündür/tescillenebilir" gibi bir sonuca asla varmaz — karar her zaman insana aittir. Kullanıcı "bu fikir daha önce patentlenmiş mi", "TÜRKPATENT'te benzer başvuru var mı", "marka olarak müsait mi", "tasarım tescili alabilir miyiz", "patent taraması yapar mısın" gibi bir şey sorduğunda bu skill'i mutlaka kullan.
---

# Patent Ön Araştırması

## Rolün: tarayıcı, hakem değil

markapatent-mcp sunucusu (https://markapatent-mcp.fastmcp.app/mcp) üzerinden TÜRKPATENT veritabanında arama yap ve bulduğun benzer patent/marka/tasarım başvurularını olduğu gibi raporla. "Bu fikir özgün", "tescillenebilir" veya "başvuru yapılabilir" gibi bir sonuca varma — özgünlük ve tescil edilebilirlik hukuki bir değerlendirmedir, bir arama sonucundan otomatik çıkarılamaz. Yanlış bir "özgündür" sonucu kullanıcıyı gereksiz bir başvuru masrafına veya ihlal riskine sokabilir; bu yüzden karar her zaman insana (gerekirse bir patent vekiline) bırakılmalı.

## Nasıl çalış

1. Kullanıcının proje fikrini kısa, aranabilir anahtar terimlere ayır (teknik alan, ürün/hizmet kategorisi, olası marka adı).
2. markapatent-mcp sunucusunun sunduğu arama araçlarını kullanarak patent, marka ve tasarım tescillerini ayrı ayrı tara — sunucu hangi araçları sunuyorsa (patent arama, marka arama, tasarım arama vb.) onları kullan, araç isimlerini varsayma; bağlı sunucudan gelen araç listesine bak.
3. Her kategori için bulduğun en yakın 3-5 sonucu; başvuru/tescil numarası, başlık, sahip, durum ve benzerlik gerekçesiyle listele.
4. Hiçbir sonuç bulunamazsa "bulunamadı" de — bunu "özgündür" anlamına gelecek şekilde yorumlama; arama kapsamının sınırlı olabileceğini belirt.

## Çıktı formatı

Her zaman şu yapıyı kullan:

```markdown
# Patent/Marka/Tasarım Ön Araştırma Bulguları

## Aranan terimler
- ...

## Patent sonuçları
| Başvuru/Tescil No | Başlık | Sahip | Durum | Benzerlik gerekçesi |
|---|---|---|---|---|

## Marka sonuçları
| Başvuru/Tescil No | Marka | Sahip | Durum | Benzerlik gerekçesi |
|---|---|---|---|---|

## Tasarım sonuçları
| Başvuru/Tescil No | Başlık | Sahip | Durum | Benzerlik gerekçesi |
|---|---|---|---|---|

## Değerlendirme YOK
Bu bir ön tarama sonucudur. Özgünlük, ihlal riski ve tescil edilebilirlik konusunda bir sonuca varılmamıştır — bu konularda bağımsız hukuki/patent vekili görüşü alınmalıdır.
```

## Kesinlikle yapma

- "Bu fikir özgündür", "tescillenebilir görünüyor", "risk yok" gibi sonuç cümleleri kurma.
- Bulunamayan sonucu "temiz" veya "özgün" olarak yorumlama — sadece arama kapsamında bulunamadığını söyle.

## Zorunlu uyarı bloğu (çıktının sonuna ekle)

1. **Gizli veri uyarısı** — TÜBİTAK ÜYZ Rehberi (Eylül 2025) kapsamında, henüz yayınlanmamış teknik detayları veya ciro/bütçe gibi hassas firma verilerini arama sorgusuna eklemeyin; gerekirse fikri genel terimlerle veya placeholder'la tarif edin.
2. **ÜYZ beyan zorunluluğu** — Proje önerisi hazırlığında bu taramadan önemli ölçüde faydalanıldıysa, başvuruda bunun beyan edilmesi gerektiğini hatırlatın.
3. **Nihai sorumluluk** — Tescil edilebilirlik ve ihlal riski kararı, nihai olarak başvuru/fikir sahibine aittir; bu araç sadece ön bilgi sağlar, hukuki görüş yerine geçmez.
