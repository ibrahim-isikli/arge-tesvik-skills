# tests/golden/ — Şema Tanımı

Her `project-NNN/` klasörü aşağıdaki dosyaları içerir. Tüm YAML dosyaları insan tarafından elle doldurulur (bir skill çalıştırmasından otomatik üretilmez).

## manifest.yaml

```yaml
id: project-001
title: "[Kısa proje adı — kurgusal]"
description: >
  [Bu golden projenin ne test ettiğinin 1-2 cümlelik özeti — örn.
  "süre/personel/ticarileşme tarihi çelişkisi + gerekçesiz gider kalemleri"]

# Bu projede kullanılan kurgusal belgeler ve her birinin documents/ altındaki dosya adı.
documents:
  - id: proje_plani
    file: documents/proje-plani.md
    role: "onaylı proje planı (AGY101 benzeri)"
  - id: butce
    file: documents/butce.md
    role: "bütçe dökümü"
  - id: gelisme_raporu
    file: documents/gelisme-raporu.md
    role: "dönem/gelişme raporu taslağı"

# Bu golden projenin hangi skill'lerle, hangi belge(ler) girdi olarak çalıştırılacağı.
runs:
  - skill: hakem-simulasyonu
    inputs: [proje_plani]
  - skill: gider-kalemi-kontrolu
    inputs: [butce]
  - skill: donem-raporu-kontrolu
    inputs: [proje_plani, gelisme_raporu]
  - skill: proje-tutarlilik-kontrolu
    inputs: [proje_plani, butce, gelisme_raporu]
```

## documents/

Kurgusal/anonimleştirilmiş kaynak belgeler (`.md` veya `.txt`). **Gerçek bir başvuru sahibinin verisi asla konulmaz** — `docs/evidence-protokolu.md`'deki gizlilik kuralı golden veriler için de geçerlidir. Her belgenin başına "(TEST VERİSİ)" ibaresi eklenmesi önerilir (audit turlarındaki fixture'larla tutarlı bir kural).

## expected/findings.yaml

Her satır, ilgili skill çalıştırıldığında **yakalanması beklenen** bir bulgudur:

```yaml
- id: F001
  skill: gider-kalemi-kontrolu
  category: bilinen-ret-kalibi        # bilinen-ret-kalibi | gerekce-eksikligi | kategori-belirsiz | ...
  description: "Business class uçak bileti işaretlenmeli"
  source_document: butce
  source_quote_contains: "business class"   # çıktıda bu ifadeye/alana referans var mı diye kontrol için
  required: true                       # true: bulunmazsa FAIL; false: bulunursa bonus ama zorunlu değil
```

## expected/conflicts.yaml

`proje-tutarlilik-kontrolu` (veya iki skill çıktısının elle karşılaştırılması) için beklenen çelişki/tutarlılık durumları:

```yaml
- id: C001
  field: "Proje süresi"
  documents: [proje_plani, butce]
  expected_status: CONFLICTING   # CONFLICTING | TUTARLI | SADECE_BIR_BELGEDE
  notes: "Proje planı 24 ay diyor, bütçe 18 aylık hesaplama kullanıyor"
```

## expected/evidence-states.yaml

Belirli iddiaların evidence-protokolü etiketlemesiyle (`docs/evidence-protokolu.md`) ne şekilde işaretlenmesi beklendiği:

```yaml
- id: E001
  skill: gider-kalemi-kontrolu
  claim: "Kişi/gün ücret tavanı"
  expected_label: UNKNOWN   # FACT | INFERENCE | USER-PROVIDED | UNKNOWN | OUTDATED | CONFLICTING
  notes: "Resmi kaynaktan doğrulanamayan bir sınır; hafızadan yazılmamalı"
```

## Değerlendirme (grading) — manuel süreç

1. `manifest.yaml`'daki her `runs` girdisini gerçek bir `claude -p --plugin-dir .` oturumunda çalıştırın.
2. Çıktıyı, ilgili `expected/findings.yaml` / `conflicts.yaml` / `evidence-states.yaml` maddeleriyle tek tek karşılaştırın:
   - `required: true` bir bulgu çıktıda yoksa → **FAIL** (skill bir şeyi kaçırdı).
   - Beklenmeyen ama makul bir ek bulgu varsa → not edin, FAIL değildir (skill'in ek değer katması iyidir, eksik olması sorundur).
   - Bir `conflicts.yaml` maddesi CONFLICTING olması gerekirken TUTARLI raporlanmışsa → **FAIL** (sessiz çelişki, kritik).
   - Bir `evidence-states.yaml` maddesi yanlış etiketlenmişse (ör. UNKNOWN olması gerekirken FACT gibi sunulmuşsa) → **FAIL** (hallucination riski).
3. Sonuçları `tests/golden/project-NNN/results/<tarih>.md` gibi bir dosyada (bu şema dışı, isteğe bağlı) kayıt altına almak, zaman içindeki regresyonu izlemeyi kolaylaştırır.
