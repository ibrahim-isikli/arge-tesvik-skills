#!/usr/bin/env python3
"""arge-tesvik-skills marketplace — çoklu-plugin statik doğrulayıcı.

Bağımlılık yok (yalnızca stdlib). Kaynak/mevzuat doğruluğunu kontrol etmez —
sadece marketplace.json'da listelenen her plugin'in skill/command dosyalarının
yapısal olarak Claude Code'un beklediği formata uyup uymadığını denetler.
CI'da veya commit öncesi `python3 scripts/validate.py` ile çalıştırılabilir.
"""

from __future__ import annotations

import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
ERRORS: list[str] = []
WARNINGS: list[str] = []

NAME_RE = re.compile(r"^[a-z0-9-]+$")
RESERVED_WORDS = {"anthropic", "claude"}
SEMVER_RE = re.compile(r"^\d+\.\d+\.\d+$")


def error(msg: str) -> None:
    ERRORS.append(msg)


def warn(msg: str) -> None:
    WARNINGS.append(msg)


def load_json(path: Path) -> dict | None:
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except FileNotFoundError:
        error(f"{path.relative_to(ROOT)}: dosya bulunamadı")
    except json.JSONDecodeError as e:
        error(f"{path.relative_to(ROOT)}: geçersiz JSON — {e}")
    return None


def parse_frontmatter(text: str, path: Path) -> dict[str, str]:
    m = re.match(r"^---\n(.*?)\n---\n", text, re.S)
    if not m:
        error(f"{path.relative_to(ROOT)}: YAML frontmatter (--- ... ---) bulunamadı")
        return {}
    fm: dict[str, str] = {}
    current_key = None
    for line in m.group(1).splitlines():
        kv = re.match(r"^([a-zA-Z_-]+):\s*(.*)$", line)
        if kv:
            current_key = kv.group(1)
            fm[current_key] = kv.group(2)
        elif current_key:
            fm[current_key] += " " + line.strip()
    return fm


def validate_plugin_manifest(data: dict | None, plugin_dir: Path) -> str | None:
    if data is None:
        return None

    rel = plugin_dir.relative_to(ROOT) if plugin_dir != ROOT else Path(".")

    for required in ("name", "version", "description"):
        if not data.get(required):
            error(f"{rel}/.claude-plugin/plugin.json: zorunlu alan eksik veya boş: '{required}'")

    version = data.get("version", "")
    if version and not SEMVER_RE.match(version):
        error(f"{rel}/.claude-plugin/plugin.json: version '{version}' semantic versioning (x.y.z) formatında değil")

    if "author" in data:
        if not isinstance(data["author"], dict):
            error(f"{rel}/.claude-plugin/plugin.json: 'author' bir obje olmalı")
        elif not data["author"].get("name"):
            error(f"{rel}/.claude-plugin/plugin.json: 'author.name' eksik")

    if "keywords" in data and not isinstance(data["keywords"], list):
        error(f"{rel}/.claude-plugin/plugin.json: 'keywords' bir liste olmalı")

    if "repository" not in data:
        warn(f"{rel}/.claude-plugin/plugin.json: 'repository' alanı yok (opsiyonel ama önerilir)")

    if "mcpServers" in data:
        if not isinstance(data["mcpServers"], dict):
            error(f"{rel}/.claude-plugin/plugin.json: 'mcpServers' bir obje olmalı")
        else:
            for server_name, cfg in data["mcpServers"].items():
                if not isinstance(cfg, dict) or "type" not in cfg:
                    error(f"{rel}/.claude-plugin/plugin.json: mcpServers.{server_name} 'type' alanı eksik")

    return data.get("name")


def load_marketplace() -> list[dict]:
    """marketplace.json'ı doğrular ve içindeki plugin girdilerini döner."""
    path = ROOT / ".claude-plugin" / "marketplace.json"
    data = load_json(path)
    if data is None:
        return []

    for required in ("name", "owner", "plugins"):
        if required not in data:
            error(f"marketplace.json: zorunlu alan eksik: '{required}'")

    plugins = data.get("plugins", [])
    if not isinstance(plugins, list) or not plugins:
        error("marketplace.json: 'plugins' boş olmayan bir liste olmalı")
        return []

    for p in plugins:
        if not p.get("name") or not p.get("source"):
            error(f"marketplace.json: her plugin girdisi 'name' ve 'source' içermeli — hatalı girdi: {p}")

    return plugins


def resolve_source(source: str) -> Path:
    return (ROOT / source).resolve()


def validate_skills(plugin_dir: Path) -> set[str]:
    skills_dir = plugin_dir / "skills"
    rel_plugin = plugin_dir.relative_to(ROOT) if plugin_dir != ROOT else Path(".")
    if not skills_dir.is_dir():
        error(f"{rel_plugin}/skills/ dizini bulunamadı")
        return set()

    skill_names: set[str] = set()
    for skill_dir in sorted(skills_dir.iterdir()):
        if not skill_dir.is_dir():
            continue
        skill_md = skill_dir / "SKILL.md"
        if not skill_md.exists():
            error(f"{rel_plugin}/skills/{skill_dir.name}/: SKILL.md eksik")
            continue

        text = skill_md.read_text(encoding="utf-8")
        fm = parse_frontmatter(text, skill_md)
        rel = skill_md.relative_to(ROOT)

        name = fm.get("name", "").strip()
        if not name:
            error(f"{rel}: frontmatter 'name' eksik")
        else:
            skill_names.add(name)
            if name != skill_dir.name:
                error(f"{rel}: frontmatter name ('{name}') klasör adıyla ('{skill_dir.name}') eşleşmiyor")
            if len(name) > 64:
                error(f"{rel}: name 64 karakterden uzun ({len(name)})")
            if not NAME_RE.match(name):
                error(f"{rel}: name sadece küçük harf/rakam/tire içermeli: '{name}'")
            if name in RESERVED_WORDS:
                error(f"{rel}: name rezerve kelime olamaz: '{name}'")

        description = fm.get("description", "").strip()
        if not description:
            error(f"{rel}: frontmatter 'description' eksik veya boş")
        else:
            if len(description) > 1024:
                error(f"{rel}: description 1024 karakterden uzun ({len(description)})")
            if "<" in description or ">" in description:
                warn(f"{rel}: description XML/HTML etiketi gibi görünen karakter içeriyor")
            lowered = description.lower()
            for word in RESERVED_WORDS:
                if word in lowered:
                    warn(f"{rel}: description rezerve kelime içeriyor: '{word}'")

        line_count = text.count("\n") + 1
        if line_count > 500:
            warn(f"{rel}: {line_count} satır — 500 satır sınırını aşıyor, dosyayı bölmeyi düşünün")

    return skill_names


def validate_commands(plugin_dir: Path, skill_names: set[str]) -> None:
    commands_dir = plugin_dir / "commands"
    rel_plugin = plugin_dir.relative_to(ROOT) if plugin_dir != ROOT else Path(".")
    if not commands_dir.is_dir():
        warn(f"{rel_plugin}/commands/ dizini bulunamadı")
        return

    for cmd_path in sorted(commands_dir.glob("*.md")):
        text = cmd_path.read_text(encoding="utf-8")
        fm = parse_frontmatter(text, cmd_path)
        rel = cmd_path.relative_to(ROOT)

        if not fm.get("description", "").strip():
            error(f"{rel}: frontmatter 'description' eksik veya boş")

        referenced = set(re.findall(r"`([a-z0-9-]+)`", text)) & skill_names
        if not referenced:
            error(
                f"{rel}: metin içinde bilinen bir skill adına (backtick içinde) referans bulunamadı "
                f"— kırık bir cross-reference olabilir (skill adı yanlış yazılmış veya skill kaldırılmış)"
            )


def validate_version_consistency(plugin_dir: Path, version: str | None) -> None:
    rel_plugin = plugin_dir.relative_to(ROOT) if plugin_dir != ROOT else Path(".")
    changelog = plugin_dir / "CHANGELOG.md"
    if not version or not changelog.exists():
        return
    text = changelog.read_text(encoding="utf-8")
    m = re.search(r"^##\s+(\d+\.\d+\.\d+)", text, re.M)
    if not m:
        warn(f"{rel_plugin}/CHANGELOG.md: semver formatında bir '## x.y.z' başlığı bulunamadı")
        return
    top_version = m.group(1)
    if top_version != version:
        error(
            f"{rel_plugin}/CHANGELOG.md'deki en üst sürüm ('{top_version}') "
            f"plugin.json'daki version ('{version}') ile eşleşmiyor"
        )


def main() -> int:
    plugins = load_marketplace()

    for entry in plugins:
        name = entry.get("name")
        source = entry.get("source")
        if not source:
            continue
        plugin_dir = resolve_source(source)
        rel_plugin = plugin_dir.relative_to(ROOT) if plugin_dir != ROOT else Path(".")

        if not plugin_dir.is_dir():
            error(f"marketplace.json: plugin '{name}' için source dizini bulunamadı: {rel_plugin}")
            continue

        plugin_manifest_path = plugin_dir / ".claude-plugin" / "plugin.json"
        plugin_data = load_json(plugin_manifest_path)
        plugin_name = validate_plugin_manifest(plugin_data, plugin_dir)
        plugin_version = (plugin_data or {}).get("version")

        if plugin_name and name and plugin_name != name:
            error(
                f"{rel_plugin}/.claude-plugin/plugin.json: name ('{plugin_name}') "
                f"marketplace.json'daki plugin adıyla ('{name}') eşleşmiyor"
            )

        skill_names = validate_skills(plugin_dir)
        validate_commands(plugin_dir, skill_names)
        validate_version_consistency(plugin_dir, plugin_version)

    if not plugins:
        pass  # load_marketplace() zaten uygun hatayı ekledi

    if WARNINGS:
        print(f"UYARI ({len(WARNINGS)}):")
        for w in WARNINGS:
            print(f"  - {w}")
    if ERRORS:
        print(f"\nHATA ({len(ERRORS)}):")
        for e in ERRORS:
            print(f"  - {e}")
        print(f"\nValidasyon BAŞARISIZ: {len(ERRORS)} hata, {len(WARNINGS)} uyarı.")
        return 1

    print(f"Validasyon BAŞARILI ({len(plugins)} plugin, {len(WARNINGS)} uyarı).")
    return 0


if __name__ == "__main__":
    sys.exit(main())
