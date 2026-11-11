#!/usr/bin/env python3
"""Troca `tconstruct:extra` por `tconstruct:binding` ({}) nos stats de materiais de um JAR.

Motivo: o Tinkers' Construct 3.12 não registra mais o tipo de stat `tconstruct:extra`.
Veja docs/fixes/allthemodium-tconstruct-material-stats.md.

Uso (com o servidor parado, na pasta do servidor):
    sudo python3 scripts/patch_allthemodium_stats.py mods/allthemodium-1.20.1-47.1.25-2.5.8.jar
    sudo python3 scripts/patch_allthemodium_stats.py --dry-run mods/allthemodium-1.20.1-47.1.25-2.5.8.jar

- Cria `<jar>.original` ao lado do JAR, se ainda não existir (nunca sobrescreve um backup).
- Só altera arquivos em `*/tinkering/materials/stats/*.json` que tenham `tconstruct:extra`.
- É idempotente: numa segunda execução não altera nada.
- Grava sobre o JAR existente, preservando dono e permissões.
"""
import argparse
import json
import os
import shutil
import sys
import tempfile
import zipfile

STATS_DIR = "tinkering/materials/stats/"
OLD_KEY = "tconstruct:extra"
NEW_KEY = "tconstruct:binding"


def patch(jar: str, dry_run: bool) -> int:
    patched = []
    workdir = tempfile.mkdtemp(prefix="atm_patch_")
    try:
        new_jar = os.path.join(workdir, "new.jar")
        with zipfile.ZipFile(jar) as zin, zipfile.ZipFile(new_jar, "w", zipfile.ZIP_DEFLATED) as zout:
            for info in zin.infolist():
                data = zin.read(info.filename)
                if STATS_DIR in info.filename and info.filename.endswith(".json"):
                    doc = json.loads(data)
                    stats = doc.get("stats", {})
                    if OLD_KEY in stats:
                        stats.pop(OLD_KEY)
                        stats.setdefault(NEW_KEY, {})
                        data = (json.dumps(doc, indent=2) + "\n").encode()
                        patched.append(info.filename)
                zout.writestr(info, data)

        for name in patched:
            print(("seria alterado: " if dry_run else "alterado: ") + name)
        print(f"{len(patched)} arquivo(s) {'a alterar' if dry_run else 'alterado(s)'}")

        if dry_run or not patched:
            return 0

        backup = jar + ".original"
        if not os.path.exists(backup):
            shutil.copy2(jar, backup)
            print(f"backup criado: {backup}")
        else:
            print(f"backup já existe, mantido: {backup}")
        shutil.copyfile(new_jar, jar)  # preserva dono/permissões do JAR original
        return 0
    finally:
        shutil.rmtree(workdir, ignore_errors=True)


if __name__ == "__main__":
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("jar")
    ap.add_argument("--dry-run", action="store_true", help="só mostra o que seria alterado")
    args = ap.parse_args()
    sys.exit(patch(args.jar, args.dry_run))
