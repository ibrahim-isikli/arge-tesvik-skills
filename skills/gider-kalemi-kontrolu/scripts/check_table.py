#!/usr/bin/env python3
"""gider-kalemi-kontrolu ana tablo şema doğrulayıcısı.

Kullanım: python3 check_table.py <tablo-icerigi.md>

SKILL.md'nin zorunlu kıldığı 5 kolonlu ana tablonun (Gider | Kategori
Uygunluğu | Gerekçelendirme Yeterliliği | Kanıt Durumu | Risk) gönderilmeden
önce gerçekten üretilip üretilmediğini mekanik olarak kontrol eder. Bu bir
domain/mevzuat doğrulayıcısı değildir — sadece çıktının şeklini (kolon
başlıkları, kolon sayısı, izin verilen Kanıt Durumu/Risk değerleri) kontrol
eder. Bağımlılık yok (stdlib).

Exit code: 0 = şema doğru ("OK"). 1 = şema hatası ("BAŞARISIZ", hatalar
listelenir). 2 = kullanım hatası (dosya yok / okunamıyor / argüman eksik).

Bilinen sınırlama: kolon içeriği kontrolü basit bir alt-dize (substring)
eşleşmesidir, anlam analizi yapmaz — ör. "FACT değildir" gibi olumsuzlama
içeren bir hücre de FACT etiketi "geçtiği" için OK sayılabilir. Bu script
sadece yapısal bir kontroldür, semantik doğrulama yerine geçmez.
"""

from __future__ import annotations

import re
import sys

REQUIRED_HEADERS = [
    "Gider",
    "Kategori Uygunluğu",
    "Gerekçelendirme Yeterliliği",
    "Kanıt Durumu",
    "Risk",
]

EVIDENCE_TOKENS = ["FACT", "USER-PROVIDED", "UNKNOWN", "OUTDATED", "CONFLICTING"]
RISK_TOKENS = ["Düşük", "Orta", "Yüksek"]  # "Çok Yüksek" "Yüksek" içerir, o yüzden kabul edilir


def split_row(line: str) -> list[str]:
    """Bir markdown tablo satırını hücrelere ayırır.

    Standart markdown tablo kaçışını destekler: bir hücre içinde geçen
    literal '|' karakteri '\\|' olarak yazılabilir ve kolon ayracı
    sayılmaz. Bunu desteklemeyen naif bir split('|'), içinde '|' geçen
    herhangi bir gider açıklamasını (ör. bir ürün kodu) yanlışlıkla fazla
    kolona böler ve sahte bir "kolon sayısı yanlış" hatasına yol açardı.
    """
    stripped = line.strip()
    # Satır sınırındaki '|' karakterleri her zaman ayraçtır (kaçışlı olsa
    # bile) çünkü tablo satırı tanımı gereği bunlarla başlar/biter.
    parts = re.split(r"(?<!\\)\|", stripped)
    if parts and parts[0] == "":
        parts = parts[1:]
    if parts and parts[-1] == "":
        parts = parts[:-1]
    return [c.strip().replace("\\|", "|") for c in parts]


def is_separator_row(cells: list[str]) -> bool:
    return all(set(c) <= {"-", ":"} and c != "" for c in cells)


def find_all_tables(lines: list[str]) -> list[tuple[int, list[str], list[list[str]]]]:
    """Dosyadaki tüm '| ... |' başlık + ayraç satırı ikililerini (tabloları) bulur."""
    tables: list[tuple[int, list[str], list[list[str]]]] = []
    i = 0
    while i < len(lines) - 1:
        header_line = lines[i].strip()
        sep_line = lines[i + 1].strip()
        if not header_line.startswith("|") or not sep_line.startswith("|"):
            i += 1
            continue
        header_cells = split_row(header_line)
        sep_cells = split_row(sep_line)
        if len(header_cells) < 2 or not is_separator_row(sep_cells):
            i += 1
            continue
        rows: list[list[str]] = []
        j = i + 2
        while j < len(lines) and lines[j].strip().startswith("|"):
            rows.append(split_row(lines[j]))
            j += 1
        tables.append((i, header_cells, rows))
        i = j
    return tables


def find_main_table(lines: list[str]) -> tuple[int, list[str], list[list[str]]] | None:
    """Ana tabloyu seçer: dosyada birden fazla tablo varsa (ör. istenmeyen bir
    özet tablosu da yazılmışsa) başlıkları REQUIRED_HEADERS ile birebir
    eşleşeni tercih eder, aksi halde dosyadaki ilk tabloyu döner — bu, yanlış
    bir tabloyu doğrulayıp kafa karıştırıcı bir hata vermek yerine, dosyada
    gerçekten tek tablo olsun diye konan kısıtın ihlalini de fark edilir kılar.
    """
    tables = find_all_tables(lines)
    if not tables:
        return None
    for t in tables:
        if t[1] == REQUIRED_HEADERS:
            return t
    return tables[0]


def main() -> int:
    if len(sys.argv) != 2:
        print("Kullanım: python3 check_table.py <tablo-icerigi.md>")
        return 2

    try:
        text = open(sys.argv[1], encoding="utf-8").read()
    except FileNotFoundError:
        print(f"HATA: dosya bulunamadı: {sys.argv[1]}")
        return 2
    except (UnicodeDecodeError, OSError) as e:
        print(f"HATA: dosya okunamadı (geçerli bir UTF-8 metin dosyası değil): {sys.argv[1]} — {e}")
        return 2

    lines = text.splitlines()
    all_tables = find_all_tables(lines)
    found = find_main_table(lines)
    errors: list[str] = []

    if found is None:
        print("HATA: Markdown tablosu bulunamadı (başlık satırı + '|---|' ayraç satırı gerekli).")
        print("Beklenen başlık satırı:")
        print("| " + " | ".join(REQUIRED_HEADERS) + " |")
        return 1

    if len(all_tables) > 1:
        print(
            f"UYARI: dosyada {len(all_tables)} ayrı tablo bulundu, sadece tek bir ana tablo "
            "olmalıydı (SKILL.md adım 8a). Başlığı REQUIRED_HEADERS ile eşleşen tablo seçilip "
            "doğrulandı, ama dosyadaki fazla içeriği kaldırın.\n"
        )

    _, header_cells, rows = found

    if header_cells != REQUIRED_HEADERS:
        errors.append(
            "Kolon başlıkları beklenenle birebir eşleşmiyor.\n"
            f"  Beklenen : {REQUIRED_HEADERS}\n"
            f"  Bulunan  : {header_cells}"
        )

    if not rows:
        errors.append("Tabloda hiç veri satırı yok — incelenen kalemler eksik.")

    for idx, row in enumerate(rows, start=1):
        if len(row) != len(REQUIRED_HEADERS):
            errors.append(f"Satır {idx}: {len(row)} kolon var, {len(REQUIRED_HEADERS)} olmalı: {row}")
            continue
        evidence_cell = row[3]
        if not any(token in evidence_cell for token in EVIDENCE_TOKENS):
            errors.append(
                f"Satır {idx}: 'Kanıt Durumu' hücresi ({evidence_cell!r}) şu etiketlerden birini "
                f"içermiyor: {EVIDENCE_TOKENS}"
            )
        risk_cell = row[4]
        if not any(token in risk_cell for token in RISK_TOKENS):
            errors.append(
                f"Satır {idx}: 'Risk' hücresi ({risk_cell!r}) şu etiketlerden birini içermiyor: {RISK_TOKENS}"
            )

    if errors:
        print(f"BAŞARISIZ — {len(errors)} sorun bulundu:\n")
        for e in errors:
            print(f"- {e}\n")
        print("Beklenen başlık satırı (birebir kopyala):")
        print("| " + " | ".join(REQUIRED_HEADERS) + " |")
        return 1

    print(f"OK — {len(rows)} kalem, şema doğru.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
