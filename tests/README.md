# tests/ — Eval Senaryoları

## Bu ne, ne değil

Bu klasördeki dosyalar **otomatik/CI testleri değildir.** `arge-tesvik` eklentisindeki skill'ler deterministik kod değil, bir LLM tarafından yorumlanan doğal dil talimatlarıdır — bu yüzden klasik `assert`/`pytest` tarzı bir test koşucusu skill davranışını doğrulayamaz. Yapısal/deterministik kontroller için `scripts/validate.py`'a bakın (JSON geçerliliği, frontmatter kısıtları, command→skill eşlemesi vb.).

Buradaki dosyalar, her skill için **LLM-graded manuel bir eval çerçevesi**dir: gerçek bir Claude Code oturumunda (`claude --plugin-dir .`) skill'i bu senaryolarla çalıştırıp çıktının "Beklenen davranış" ile eşleşip eşleşmediğini bir insan (veya ayrı bir değerlendirici Claude oturumu) kontrol eder.

## Nasıl kullanılır

1. `claude --plugin-dir /path/to/arge-tesvik-skills` ile eklentiyi yerel olarak yükleyin.
2. İlgili skill'in `tests/<skill-adı>/eval-scenarios.md` dosyasındaki bir senaryonun "Girdi"sini oturuma yapıştırın (veya ilgili slash komutunu kullanın).
3. Çıktıyı "Beklenen davranış" maddeleriyle karşılaştırın. Her madde ya karşılanmalı ya da skill'in neden karşılamadığı anlaşılır olmalı.
4. Bir madde tutarlı biçimde karşılanmıyorsa, bunu SKILL.md'de bir talimat netliği sorunu olarak ele alın (bkz. [Skill authoring best practices](https://platform.claude.com/docs/en/agents-and-tools/agent-skills/best-practices) — "evaluation-driven development").

## Senaryo kategorileri

Her skill dosyası aynı 7 kategoriyi kapsar:

1. **Normal case** — skill'in ana kullanım amacına uygun, sorunsuz bir girdi.
2. **Eksik bilgi** — değerlendirme için gerekli bir bilginin (tarih, belge, tutar) eksik olduğu durum; skill'in uydurmadan eksik olanı sorması beklenir.
3. **Hallucination tuzağı** — kullanıcının skill'i sayı/sonuç/hukuki değerlendirme uydurmaya zorlamaya çalıştığı durum.
4. **Çelişkili bilgi** — birden fazla kaynak/belge/ifade birbiriyle çeliştiğinde skill'in bunu sessizce çözmek yerine açıkça işaretlemesi beklenir.
5. **Güncelliğini yitirmiş bilgi** — eski/stale bir kaynağın güncelmiş gibi kullanılmaması gereken durum.
6. **Kötü niyetli girdi (prompt injection)** — belge/web sayfası/MCP çıktısı içine gömülü, agent'ın davranışını değiştirmeye çalışan sahte talimat.
7. **Belirsiz istek** — kullanıcının skill'i tetikleyecek kadar bilgi vermediği durum; skill'in varsayım yapmadan netleştirme sorması beklenir.

## Kapsam

| Skill | Dosya |
|---|---|
| `hakem-simulasyonu` | [tests/hakem-simulasyonu/eval-scenarios.md](hakem-simulasyonu/eval-scenarios.md) |
| `gider-kalemi-kontrolu` | [tests/gider-kalemi-kontrolu/eval-scenarios.md](gider-kalemi-kontrolu/eval-scenarios.md) |
| `cagri-tarama` | [tests/cagri-tarama/eval-scenarios.md](cagri-tarama/eval-scenarios.md) |
| `patent-on-arastirma` | [tests/patent-on-arastirma/eval-scenarios.md](patent-on-arastirma/eval-scenarios.md) |
| `donem-raporu-kontrolu` | [tests/donem-raporu-kontrolu/eval-scenarios.md](donem-raporu-kontrolu/eval-scenarios.md) |
| `itiraz-hazirlik` | [tests/itiraz-hazirlik/eval-scenarios.md](itiraz-hazirlik/eval-scenarios.md) |
| `proje-tutarlilik-kontrolu` | [tests/proje-tutarlilik-kontrolu/eval-scenarios.md](proje-tutarlilik-kontrolu/eval-scenarios.md) |

## fixtures/

`tests/fixtures/injection-sample.md`, kötü niyetli girdi (prompt injection) senaryolarını gerçek bir `WebFetch` çağrısıyla test etmek için kullanılan, kasıtlı olarak talimat enjeksiyonu içeren bir test sayfasıdır. Gerçek bir TÜBİTAK belgesi değildir. `cagri-tarama` skill'ini bu dosyanın raw GitHub URL'siyle çalıştırarak "kaynak = veri, talimat değil" kuralının runtime'da tutup tutmadığını doğrulayabilirsiniz.
