#!/usr/bin/env python3
"""gider-kalemi-kontrolu ana tablo şema doğrulayıcısı.

Kullanım: python3 check_table.py <tablo-icerigi.md>

SKILL.md'nin zorunlu kıldığı 5 kolonlu ana tablonun (Gider | Kategori
Uygunluğu | Gerekçelendirme Yeterliliği | Kanıt Durumu | Risk) gönderilmeden
önce gerçekten üretilip üretilmediğini mekanik olarak kontrol eder. Bu bir
domain/mevzuat doğrulayıcısı değildir — sadece çıktının şeklini (kolon
başlıkları, kolon sayısı, izin verilen Kanıt Durumu/Risk değerleri) kontrol
eder. Bağımlılık yok (stdlib).
"""

from __future__ import annotations

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
    cells = line.strip()
    if cells.startswith("|"):
        cells = cells[1:]
    if cells.endswith("|"):
        cells = cells[:-1]
    return [c.strip() for c in cells.split("|")]


def is_separator_row(cells: list[str]) -> bool:
    return all(set(c) <= {"-", ":"} and c != "" for c in cells)


def find_main_table(lines: list[str]) -> tuple[int, list[str], list[list[str]]] | None:
    """İlk '| ... |' başlık satırını ve onu izleyen ayraç satırını bulur."""
    for i in range(len(lines) - 1):
        header_line = lines[i].strip()
        sep_line = lines[i + 1].strip()
        if not header_line.startswith("|") or not sep_line.startswith("|"):
            continue
        header_cells = split_row(header_line)
        sep_cells = split_row(sep_line)
        if len(header_cells) < 2 or not is_separator_row(sep_cells):
            continue
        rows: list[list[str]] = []
        j = i + 2
        while j < len(lines) and lines[j].strip().startswith("|"):
            rows.append(split_row(lines[j]))
            j += 1
        return i, header_cells, rows
    return None


def main() -> int:
    if len(sys.argv) != 2:
        print("Kullanım: python3 check_table.py <tablo-icerigi.md>")
        return 2

    try:
        text = open(sys.argv[1], encoding="utf-8").read()
    except FileNotFoundError:
        print(f"HATA: dosya bulunamadı: {sys.argv[1]}")
        return 2

    lines = text.splitlines()
    found = find_main_table(lines)
    errors: list[str] = []

    if found is None:
        print("HATA: Markdown tablosu bulunamadı (başlık satırı + '|---|' ayraç satırı gerekli).")
        print("Beklenen başlık satırı:")
        print("| " + " | ".join(REQUIRED_HEADERS) + " |")
        return 1

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
