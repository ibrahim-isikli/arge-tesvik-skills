# Skill Akış Şemaları

Bu doküman, `arge-tesvik` ve `akademik-arastirma` eklentilerindeki her skill'in karar noktalarını, döngülerini ve hata yollarını görselleştirir. Bir bug-arama turunun (2026-10-30) parçası olarak hazırlandı — amacı dokümantasyon kadar, **her karar noktasının gerçekten ele alındığını, bir kenarın unutulmadığını** göstermektir. SKILL.md dosyalarının yerini tutmaz, onların bir okuma yardımcısıdır; SKILL.md değişirse bu dosya da güncellenmeli.

Her bölümün sonunda, akışı okurken/test ederken bulunan gerçek riskler **"⚠ Bulunan riskler"** altında ayrıca listelenir (bulgu yoksa bu başlık atlanır).

---

## arge-tesvik eklentisi

### hakem-simulasyonu

```mermaid
flowchart TD
    A[Başla] --> B{Taslak metni var mı?}
    B -- Hayır --> B1[Taslağı iste] --> Z[Bitir]
    B -- Evet --> C[Taslağı oku]
    C --> D["3 boyutu sırayla işle:<br/>1) Ar-Ge niteliği/yenilik<br/>2) Proje planı/yapılabilirlik<br/>3) Ticarileşme potansiyeli (en ağırlıklı)"]
    D --> E[Her boyut: taslaktan alıntı + somut gerekçe + düzeltme yönü]
    E --> F[Genel Değerlendirme — puan/kabul-ret tahmini YOK]
    F --> G[Zorunlu uyarı bloğu: gizlilik + ÜYZ beyanı + nihai sorumluluk]
    G --> Z2[Nihai yanıt]
```

Kenar şartları (SKILL.md "Kesinlikle yapma"): puan uydurma yok, kabul garantisi yok, taslağı kendi adına yeniden yazma yok. Bütçeyi satır satır incelemek gerekirse `gider-kalemi-kontrolu`'na yönlendirir (içinde çalıştırmaz, sadece önerir).

---

### gider-kalemi-kontrolu

En karmaşık akış — tek skill içinde gerçek bir kod döngüsü (`scripts/check_table.py`) var, bu yüzden en çok bug yüzeyine sahip.

```mermaid
flowchart TD
    A[Başla] --> B{Bütçe/gider dökümü var mı?}
    B -- Hayır --> Z1[İste]
    B -- Evet --> C["Her kalemi 5 kategoriden birine ata<br/>(net oturmuyorsa 'belirsiz')"]
    C --> D[Kategoriye özgü bilinen ret kalıplarını kontrol et]
    D --> E["Uygunluk VE Gerekçelendirmeyi AYRI değerlendir<br/>(tek yargıda birleştirme)"]
    E --> F{Sayısal sınır (üst limit/tavan) soruluyor mu?}
    F -- Evet --> F1["Hafızadan yazma →<br/>cagri-tarama öner ya da<br/>doğrulanamıyorsa UNKNOWN"]
    F -- Hayır --> G
    F1 --> G["Ana tabloyu dosyaya yaz<br/>(5 kolon: Gider/Kategori Uygunluğu/<br/>Gerekçelendirme/Kanıt Durumu/Risk)"]
    G --> H["Bash: check_table.py çalıştır"]
    H --> I{Bash izni var mı?}
    I -- Hayır --> I1["Elle kontrol et +<br/>'DOĞRULAMA: script çalıştırılamadı' notu<br/>(2026-10-30'da eklendi)"] --> M
    I -- Evet --> J{Script çıktısı}
    J -- BAŞARISIZ --> K[Hataları düzelt, dosyayı güncelle] --> G
    J -- OK --> M[Nihai yanıt: tablo + açıklama]
    M --> N[Zorunlu uyarı bloğu]
    N --> Z2[Bitir]
```

**⚠ Bulunan riskler (bu turda düzeltildi):**
1. `split_row()` escape edilmiş pipe (`\|`) karakterini kolon ayracı sanıyordu — hücre içinde `|` geçen herhangi bir gider açıklaması (ürün kodu vb.) sahte bir "kolon sayısı yanlış" hatasına yol açıyordu, bu da G→H→J(BAŞARISIZ)→K→G döngüsünü asla "OK" ile bitiremeyecek bir duruma sokabilirdi. **Düzeltildi** (regex tabanlı, kaçış-farkında split).
2. `find_main_table()` dosyadaki **ilk** tabloyu alıyordu — dosyada istenmeyen ikinci bir tablo varsa (adım G'nin "sadece tablo" kuralı ihlal edilirse) yanlış tabloyu doğrulayıp kafa karıştırıcı bir hata veriyordu. **Düzeltildi** (başlığı REQUIRED_HEADERS ile eşleşen tablo tercih ediliyor artık + birden fazla tablo varsa uyarı).
3. **I düğümü (Bash izni yoksa) daha önce SKILL.md'de hiç tanımlı değildi** — canlı testte (bkz. bu turun test kaydı) model kendi inisiyatifiyle şeffaf davrandı ama bu garanti değildi; skill'in kendi "atlanamaz" kuralını sessizce ihlal etme riski vardı. **Düzeltildi** (adım 8e eklendi, `docs/evidence-protokolu.md`'deki UNAVAILABLE/DEGRADED şeffaflık mantığıyla tutarlı).

**Teorik, düşük öncelikli not:** G→K→G döngüsü teorik olarak sınırsız tekrar edebilir (script hep BAŞARISIZ derse) — script'in kuralları net olduğu ve LLM'in kendi ürettiği tabloyu düzeltmesi beklendiği için pratikte düşük risk, ama bir üst sınır (ör. "3 denemeden sonra kullanıcıya bildir") SKILL.md'de yok.

---

### cagri-tarama

```mermaid
flowchart TD
    A[Başla] --> B{Kullanıcı belirli kod(lar) mı istiyor?}
    B -- Hayır --> B1["Tümünü tara:<br/>1501,1505,1507,1509,1511,1707,1001,3001"]
    B -- Evet --> B2[Sadece istenenleri tara]
    B1 --> C
    B2 --> C[Her kod için tubitak.gov.tr kaynağını ara/aç]
    C --> D{"Sayfa içeriğinde talimat-benzeri<br/>ifade var mı? (prompt injection)"}
    D -- Evet --> D1["Veri olarak işle,<br/>komut olarak uygulama,<br/>kullanıcıyı bilgilendir"] --> E
    D -- Hayır --> E{Resmi kaynak bulundu mu?}
    E -- Hayır --> E1["Üçüncü taraf kaynak<br/>'resmi olmayan' etiketiyle"] --> F
    E -- Evet --> F[Son tarih/durum/bütçe üst limiti çıkar]
    F --> G{Değer sayfada var mı?}
    G -- Hayır --> G1["'Bulunamadı' yaz — tahmin etme"]
    G -- Evet --> G2[FACT etiketiyle kaydet]
    G1 --> H
    G2 --> H[Tüm kodlar bitti mi?] -- Hayır --> C
    H -- Evet --> I[Son başvuru tarihine göre sırala, açık çağrılar önce]
    I --> J[Tarama tarihi notu + zorunlu uyarı bloğu]
    J --> Z[Bitir]
```

`tests/fixtures/injection-sample.md` ile D düğümü bu turda canlı test edildi (bkz. aşağıdaki "Test kayıtları") — enjekte talimat (sahte 01.01.2020 tarihi, "sınırsız" bütçe) uygulanmadı, sahte değerler doğru olarak reddedildi.

---

### patent-on-arastirma

Çift kaynaklı (genel patent veritabanı + opsiyonel markapatent-mcp) olduğu için `cagri-tarama`'dan daha fazla dallanma içerir.

```mermaid
flowchart TD
    A[Başla] --> B[Fikri aranabilir anahtar terimlere ayır]
    B --> C{WebSearch/WebFetch bağlı mı?}
    C -- Hayır --> C1[UNAVAILABLE bildir] --> H
    C -- Evet --> D["Google Patents/Espacenet'te ara<br/>(VARSAYILAN — her zaman çalışır)"]
    D --> E{Detay sayfası açılabiliyor mu? 403/503?}
    E -- Engelleniyor --> E1["'bulunamadı — sayfa erişimi<br/>engelliyor' diye işaretle"] --> F
    E -- Açık --> F["Kaynak: Genel patent veritabanı<br/>etiketiyle kaydet"]
    F --> G{"Kullanıcı TÜRKPATENT'e özel istedi MI<br/>VEYA marka/tasarım istiyor mu?"}
    G -- Hayır --> H[markapatent-mcp'yi HİÇ deneme]
    G -- Evet --> G1[markapatent-mcp araç listesine bak]
    G1 --> G2{Sunucuya bağlanılabiliyor mu?}
    G2 -- Hayır --> G3[UNAVAILABLE markapatent-mcp] --> H
    G2 -- Evet --> G4{Sorgu hatasız/eksiksiz mi?}
    G4 -- Hayır/kısmi --> G5[DEGRADED markapatent-mcp] --> H
    G4 -- Evet --> G6["Kaynak: TÜRKPATENT (markapatent-mcp)<br/>ayrı satırlarda kaydet"] --> H
    H --> I{Sonuç sayısı çok mu? 20+}
    I -- Evet --> I1[En alakalı 5-10'u seç, toplamı belirt]
    I -- Hayır --> J
    I1 --> J[Aynı patent ailesinin tekrarlarını birleştir]
    J --> K{Her iki kaynak da UNAVAILABLE mı?}
    K -- Evet --> K1["Var olmayan bir servis UYDURMA —<br/>gerçek alternatifleri sun<br/>(manuel TÜRKPATENT/Google Patents, patent vekili)"]
    K -- Hayır --> L["Durum satırı + tablo + 'Değerlendirme YOK' notu"]
    K1 --> L
    L --> M[Zorunlu uyarı bloğu]
    M --> Z[Bitir]
```

**Not:** `docs/automation-readiness.md`'ye göre markapatent-mcp daha önceki bir audit turunda gerçekten üretimde bozuk bulunmuş (Capsolver bakiye hatası) — bu, G2/G4 dallarının UNAVAILABLE/DEGRADED yollarının **teorik değil, gerçek runtime'da karşılaşılmış** yollar olduğu anlamına gelir; bu yüzden H öncesi dallanmanın doğru çalışması (varsayılan akışın markapatent-mcp'ye hiç bağımlı olmaması) kritik — tasarım bunu doğru yapıyor.

---

### itiraz-hazirlik

```mermaid
flowchart TD
    A[Başla] --> B{Hakem raporu + proje metni var mı?}
    B -- Hayır --> B1["İste — bunlar olmadan<br/>itiraz metni YAZMA"] --> Z
    B -- Evet --> C[Tebliğ tarihini sor]
    C --> D["15 günlük süreyi hesapla —<br/>HER yanıtın başında hatırlat"]
    D --> E[Her ret gerekçesi için ayrı ayrı değerlendir]
    E --> F{"Gözden kaçırma/yanlış yorumlama mı,<br/>yoksa gerçek eksiklik mi?"}
    F -- Gerçek eksiklik --> F1["İtiraz adayı DEĞİL →<br/>revizyon + hakem-simulasyonu öner"]
    F -- Gözden kaçırma --> F2["İtiraz adayı → 4 kategoriden<br/>birine ata (sonuç/davranış/<br/>yerinde inceleme/diğer)"]
    F2 --> G["Proje metninden doğrudan alıntıyla<br/>dilekçe taslağı yaz"]
    G --> H{"Kendi kendini denetle:<br/>yeni iddia/veri sızdı mı?"}
    H -- Evet --> H1[Sızan cümleyi çıkar, kullanıcıyı uyar] --> I
    H -- Hayır --> I[Sonraki ret gerekçesi var mı?]
    I -- Evet --> E
    I -- Hayır --> J[TÜBİMER ücretini hatırlat — UNKNOWN uygula]
    F1 --> I
    J --> K[Zorunlu uyarı bloğu]
    K --> Z2[Bitir]
```

**Tasarım notu:** `donem-raporu-kontrolu`'nun aksine, bu skill destekleyici belge olmadan **tamamen reddeder** (B1) — iki skill'in aynı "belge eksikse ne yap" sorusuna kasıtlı olarak farklı cevap verdiği, dokümante edilmiş bir tasarım kararı (bkz. aşağıdaki not).

---

### donem-raporu-kontrolu

```mermaid
flowchart TD
    A[Başla] --> B{Rapor taslağı var mı?}
    B -- Hayır --> B1[İste] --> Z
    B -- Evet --> C{Onaylı proje planı var mı?}
    C -- Hayır --> C1["Reddetme — 'Önemli kısıtlama' notuyla<br/>sadece raporun iç tutarlılığını<br/>değerlendirmeye devam et"]
    C -- Evet --> D[İş paketi/hedef bazında planla karşılaştır]
    C1 --> D2[Sadece iç tutarlılık/kanıt yeterliliği üzerinden değerlendir]
    D --> E{Her hedef için somut kanıt var mı?}
    E -- Hayır/belirsiz ifade --> E1["'Çalışmalar devam etmektedir' gibi<br/>belirsiz ifadeleri işaretle"] --> F
    E -- Evet --> F[Takvim/bütçe/kapsam sapması var mı?]
    F --> G{Sapma gerekçelendirilmiş mi?}
    G -- Hayır (sessiz sapma) --> G1[Zayıf nokta olarak işaretle]
    G -- Evet --> H
    G1 --> H["Bütçe satır bazlı kontrol gerekiyorsa<br/>gider-kalemi-kontrolu öner"]
    D2 --> H
    H --> I["Sonraki dönem planı mevcut<br/>durumdan gerçekçi türetilmiş mi?"]
    I --> J{Sonuç Raporu mu?}
    J -- Evet --> J1["Ek: Ar-Ge/yenilik iddiası<br/>nihai çıktıyla karşılandı mı?"] --> K
    J -- Hayır --> K[Zorunlu uyarı bloğu]
    J1 --> K
    K --> Z2[Bitir]
```

**⚠ Tasarım tutarlılığı notu (bug değil, kasıtlı farklılık — ama dokümante edilmesi gereken bir nokta):** `itiraz-hazirlik` destekleyici belge eksikse tamamen reddederken, bu skill eksik planla kısıtlı modda devam ediyor (C1). İkisi de SKILL.md'de gerekçelendirilmiş, ama bir kullanıcı iki skill'i art arda kullanırsa bu davranış farkı şaşırtıcı gelebilir — `docs/evidence-protokolu.md`'ye bu farkı açıklayan bir not eklemek faydalı olabilir (bu turda eklenmedi, sadece kaydedildi).

---

### proje-tutarlilik-kontrolu

```mermaid
flowchart TD
    A[Başla] --> B{En az 2 belge var mı?}
    B -- Hayır --> B1["Çelişki aranamaz — ikinci belgeyi iste.<br/>Tek belgeyle 'kontrol yapılmış' gibi davranma"] --> Z
    B -- Evet --> C[Her belgeden 8 alanı çıkar: süre/bütçe/personel/<br/>iş paketleri/TRL/ticarileşme/KPI/kapsam]
    C --> D{Alan kaç belgede geçiyor?}
    D -- "0 belgede (yok)" --> D0[Karşılaştırma dışı bırak — uydurma]
    D -- "1 belgede" --> D1["'Sadece bir belgede var' —<br/>otomatik çelişki SAYMA"]
    D -- "2+ belgede, değerler eşit" --> D2[Tutarlı]
    D -- "2+ belgede, değerler farklı" --> D3[CONFLICTING olarak işaretle]
    D0 --> E
    D1 --> E[Sonraki alan var mı?] -- Evet --> C
    D2 --> E
    D3 --> E
    E -- Hayır --> F{Hangi değer doğru karar verilsin mi?}
    F -- "HAYIR (kural)" --> F1["En fazla nötr gözlem<br/>('X daha güncel görünüyor') —<br/>kesin hüküm verme"]
    F1 --> G["Çelişkinin niteliğine göre yönlendir:<br/>gider-kalemi-kontrolu / hakem-simulasyonu / donem-raporu-kontrolu"]
    G --> H[Tutarlı bulunan alanları da listele — sadece sorunları gösterme]
    H --> I[Zorunlu uyarı bloğu]
    I --> Z2[Bitir]
```

---

### fikir-uretimi

En çok cross-skill orkestrasyon içeren akış — `cagri-tarama` ve `patent-on-arastirma`'yı kendi içinden çağırır.

```mermaid
flowchart TD
    A[Başla] --> B{Alan/bağlam belli mi?}
    B -- Hayır --> B1[Sohbet bağlamına bak]
    B1 --> B2{Hâlâ belirsiz mi?}
    B2 -- Evet --> B3["references/ notuna bak"]
    B3 --> B4{Hâlâ belirsiz mi?}
    B4 -- Evet --> B5["TAHMİN ETME — sor"] --> Z
    B4 -- Hayır --> C
    B2 -- Hayır --> C
    B -- Evet --> C["cagri-tarama çalıştır<br/>(+ enerji/emisyon alanıysa 1832'yi ayrıca ara)"]
    C --> D["TÜBİTAK öncelikli alan listesini<br/>CANLI doğrula (hafızadan değil)"]
    D --> E[3-5 aday fikir üret — her biri farklı teknik yaklaşım]
    E --> F["Her aday: Problem/İhtiyaç alanını<br/>GENERATED veya USER-PROVIDED etiketle"]
    F --> G["Her adayı 4 unsura göre ele:<br/>teknik belirsizlik / yenilik /<br/>sistematik çalışma / yaygın etki"]
    G --> H{Dört unsurun hepsi karşılanıyor mu?}
    H -- Hayır --> H1[Elenenler listesine ekle, gerekçeyle]
    H -- Evet --> I["patent-on-arastirma çalıştır<br/>(hayatta kalan HER aday için ayrı ayrı)"]
    I --> J["Sonucu olduğu gibi ekle —<br/>UNAVAILABLE/DEGRADED dahil, atlama"]
    J --> K{Sayısal fayda biliniyor mu?}
    K -- Hayır --> K1["'[%…]' placeholder bırak — uydurma"]
    K -- Evet --> K2[Kaynağıyla INFERENCE etiketle]
    H1 --> L
    K1 --> L[Sonraki aday var mı?] 
    K2 --> L
    L -- Evet --> F
    L -- Hayır --> M["En güçlü 1-2 adayı forma dök,<br/>elenenleri de kısa listele"]
    M --> N["Paylaşma/ifşa UYARISI<br/>(herkese açık depo/sayfa/3. tarafa gönderme)"]
    N --> O["Zorunlu uyarı bloğu +<br/>ifşa/patentlenebilirlik uyarısı (4. madde)"]
    O --> Z2[Bitir]
```

**⚠ Performans/maliyet notu (doğruluk bug'ı değil):** I adımı, hayatta kalan **her** aday için ayrı ayrı `patent-on-arastirma`'yı tetikliyor — 3-5 aday × (WebSearch + opsiyonel markapatent-mcp) demek, tek bir `fikir-uretimi` çağrısının toplamda çok sayıda alt-araç çağrısına ve uzun bir yanıt süresine/yüksek token maliyetine yol açabileceği anlamına gelir. SKILL.md bunun için bir üst sınır (ör. "en fazla N adayda dene") tanımlamıyor. Fonksiyonel bir bug değil ama kullanıcı deneyimi/maliyet açısından not edilmeye değer.

---

## akademik-arastirma eklentisi

Bu dört skill, `arge-tesvik`'teki desenlerin akademik alana uyarlanmış halidir — akışları daha az dallanır, bu yüzden daha kısa gösterilmiştir.

### akademik-hakem-simulasyonu

`hakem-simulasyonu` ile izomorfik, tek fark boyut sayısı ve içeriği:

```mermaid
flowchart TD
    A[Başla] --> B{Taslak var mı?} -- Hayır --> B1[İste] 
    B -- Evet --> C["4 boyutu işle: araştırma sorusu/katkı,<br/>yöntem sağlamlığı, bulgu-tartışma tutarlılığı,<br/>literatüre yerleşim"]
    C --> D[Her boyut: alıntı + gerekçe + düzeltme yönü]
    D --> E[Genel Değerlendirme — puan/kabul-ret YOK]
    E --> F[Zorunlu uyarı bloğu]
```

### literatur-taramasi

```mermaid
flowchart TD
    A[Başla] --> B{Araştırma sorusu net mi?}
    B -- Hayır --> B1[Daraltıcı sorular sor: disiplin/coğrafya/dönem/tür]
    B -- Evet --> C["Çoklu kaynakta CANLI ara:<br/>Scholar/DergiPark/TR Dizin/YÖK Tez Merkezi"]
    B1 --> C
    C --> D{Abonelik gerektiren kaynak mı? Scopus/WoS}
    D -- Evet --> D1["'Erişimim yok' de —<br/>taradığını iddia etme"] --> E
    D -- Hayır --> E[Her kaynağı alaka/güncellik/tür açısından etiketle]
    E --> F{Sistematik derleme mi isteniyor?}
    F -- Evet --> F1[PRISMA-benzeri akışla say/filtrele/raporla]
    F -- Hayır --> G
    F1 --> G[Olası boşluk gözlemi — KESİN iddia değil]
    G --> H[Taramanın sınırları + zorunlu uyarı bloğu]
```

### atif-butunluk-kontrolu

```mermaid
flowchart TD
    A[Başla] --> B{Taslak + atıf stili var mı?}
    B -- Stil yok --> B1[Taslaktan çıkarmaya çalış, olmuyorsa sor]
    B -- Var --> C
    B1 --> C[Metin-içi atıf ↔ kaynakça eşleştirme tablosu]
    C --> D["Format tutarlılığını kontrol et<br/>(APA7/Chicago/IEEE/Vancouver/MLA)"]
    D --> E["Riskli görünen bir örneklem seç<br/>(küçük listede tümü)"]
    E --> F["Canlı ara (WebSearch/WebFetch)"]
    F --> G{Sonuç}
    G -- Bulundu+eşleşti --> G1[DOĞRULANDI]
    G -- Bulunamadı --> G2["BULUNAMADI —<br/>'uydurma' ile EŞ TUTMA"]
    G -- Bulundu+çelişiyor --> G3[UYUŞMAZLIK]
    G1 --> H
    G2 --> H[Aşırı iddialı dil tara]
    G3 --> H
    H --> I[AI kullanım beyanı eksik mi kontrol et]
    I --> J[Zorunlu uyarı bloğu]
```

### makale-yazim-rehberligi

```mermaid
flowchart TD
    A[Başla] --> B{Kullanıcı taslak paylaştı mı?}
    B -- Evet --> C["Mod 3: Taslak eleştirisi —<br/>önce tür/hedef kitleyi teyit et"]
    B -- Hayır --> D["Mod 1: Sokratik yapı planlama —<br/>tek seferde 1-2 soru sor"]
    D --> E{Kullanıcı 'sen karar ver' dedi mi?}
    E -- Evet --> E1["Yine de nihai kararı kullanıcıya bırak —<br/>seçenek sun, gerekçelendir"]
    E -- Hayır --> F
    E1 --> F[Mod 2: İskelet/başlık ağacı üret]
    C --> G{Atıf/kaynak sorunu fark edildi mi?}
    G -- Evet --> G1["Derinlemesine işleme —<br/>atif-butunluk-kontrolu öner"] --> H
    G -- Hayır --> H["Mod 4: Argüman tutarlılığı<br/>(istenirse)"]
    F --> H
    H --> I["ASLA paragraf/cümle yazma —<br/>sadece işlev tanımı/eleştiri"]
    I --> J[Zorunlu uyarı bloğu]
```

---

## Komut → Skill eşlemesi (deterministik, `scripts/validate.py` tarafından da kontrol edilir)

```mermaid
flowchart LR
    subgraph arge-tesvik
    c1["/arge-tesvik:degerlendir"] --> s1[hakem-simulasyonu]
    c2["/arge-tesvik:gider"] --> s2[gider-kalemi-kontrolu]
    c3["/arge-tesvik:tara"] --> s3[cagri-tarama]
    c4["/arge-tesvik:itiraz"] --> s4[itiraz-hazirlik]
    c5["/arge-tesvik:rapor"] --> s5[donem-raporu-kontrolu]
    c6["/arge-tesvik:tutarlilik"] --> s6[proje-tutarlilik-kontrolu]
    c7["/arge-tesvik:uret"] --> s7[fikir-uretimi]
    end
    subgraph akademik-arastirma
    c8["/akademik-arastirma:hakem"] --> s8[akademik-hakem-simulasyonu]
    c9["/akademik-arastirma:atif"] --> s9[atif-butunluk-kontrolu]
    c10["/akademik-arastirma:tara"] --> s10[literatur-taramasi]
    c11["/akademik-arastirma:planla"] --> s11[makale-yazim-rehberligi]
    end
```

`patent-on-arastirma`'nın doğrudan bir komutu yok — `hakem-simulasyonu`/`gider-kalemi-kontrolu`/`fikir-uretimi`'nin açıklamasından veya doğal dil tetiklemesinden çağrılır; `scripts/validate.py` bu yüzden ona bir komut eksikliği hatası vermiyor (komut zorunluluğu yok, sadece varsa skill adına referans kontrolü yapıyor).

---

## Bu turda test edilen akışlar (canlı `claude --plugin-dir .` koşuları)

| Akış | Yöntem | Sonuç |
|---|---|---|
| `gider-kalemi-kontrolu` — Bash izni YOK senaryosu | Gerçek koşu, izin verilmemiş | Model şeffaf davrandı (beklenenden iyi), ama SKILL.md'de garanti yoktu → **adım 8e eklendi** |
| `gider-kalemi-kontrolu` — Bash izni VAR, tam döngü | Gerçek koşu, `Skill,Write,Bash,Read` izinli | Script gerçekten çalıştı, "OK" ile sonuçlandı, düzeltmelerim regresyon yaratmadı |
| `cagri-tarama` / genel "kaynak=veri" kuralı | `tests/fixtures/injection-sample.md`'nin raw GitHub URL'si gerçekten WebFetch edildi | Enjekte talimat (sahte tarih/bütçe, sistem promptu ifşası) uygulanmadı |
| `check_table.py` — escaped pipe, çoklu tablo, em-dash ayraç | Script doğrudan, 4 sentetik girdiyle | 2 gerçek bug bulundu ve düzeltildi (yukarıya bakın) |

Test edilmeyen ama flowchart'ı çıkarılan akışlar (`hakem-simulasyonu`, `itiraz-hazirlik`, `donem-raporu-kontrolu`, `proje-tutarlilik-kontrolu`, `fikir-uretimi`, `patent-on-arastirma`'nın markapatent-mcp dalı, ve `akademik-arastirma`'nın 4 skill'i) için `tests/*/eval-scenarios.md` dosyalarındaki senaryolar zaten mevcut — bu dosya onların yerini almaz, sadece karar yapısını görselleştirir.
