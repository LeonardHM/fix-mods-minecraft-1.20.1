# Runbook de comandos — correções reaplicáveis

Este documento reúne somente comandos recuperados do histórico com segurança suficiente para reprodução. Quando o histórico confirma uma correção, mas não preserva o comando literal ou o conteúdo final do arquivo, isso é indicado explicitamente. Não substitua essa lacuna por um comando presumido.

**Diretório de trabalho do servidor em 10–11/11/2026:**

```bash
cd /var/opt/minecraft/crafty/crafty-4/servers/1a528e4d-a48e-4989-a7fd-115760b0012b
```

Execute alterações em arquivos do servidor com o servidor parado, salvo quando o procedimento indicar expressamente `/reload`.

## 1. SGJourney — backup, gravação e validação

Caminho corrigido:

```bash
FILE="kubejs/data/overworld_cartouches/sgjourney/address_table/cartouche_overworld.json"
```

O comando de backup usado foi:

```bash
cp -a "$FILE" "$FILE.bak"
```

O arquivo foi regravado como JSON com o campo `address` estruturado como objeto contendo `dimension` e `galaxy`, em vez de uma string simples. A gravação foi feita por heredoc; devido a uma falha de permissão na tentativa com redirecionamento comum, foi usada a variante com `sudo tee`:

```bash
sudo tee "$FILE" > /dev/null <<'EOF'
[INSERIR AQUI O JSON CORRIGIDO PRESERVADO NO BACKUP/NO HISTÓRICO LOCAL]
EOF
```

Validação executada:

```bash
python3 -m json.tool "$FILE"
ls -l "$FILE"
```

O usuário confirmou JSON válido e proprietário `crafty:crafty`. **O conteúdo JSON integral não está preservado neste registro**; não use o marcador acima como conteúdo literal. Para reaplicar depois de atualização, recuperar o JSON corrigido do backup versionado/arquivo de referência e conferir os valores de `dimension` e `galaxy` antes de gravar.

## 2. MegaCells — override vazio da EMC Interface

Comando literal recuperado:

```bash
sudo install -d -o crafty -g crafty -m 755 kubejs/data/megacells/loot_tables/blocks
printf '%s\n' '{"type":"minecraft:block","pools":[]}' | sudo tee kubejs/data/megacells/loot_tables/blocks/mega_emc_interface.json > /dev/null
sudo chown crafty:crafty kubejs/data/megacells/loot_tables/blocks/mega_emc_interface.json
sudo chmod 644 kubejs/data/megacells/loot_tables/blocks/mega_emc_interface.json
python3 -m json.tool kubejs/data/megacells/loot_tables/blocks/mega_emc_interface.json
```

O override suprime drops para essa loot table. Ele não corrige o JAR do MegaCells. O erro correspondente deixou de aparecer após reinicialização.

## 3. ResourcefulLib — criar diretório home esperado

Comando literal executado:

```bash
sudo install -d -o crafty -g crafty -m 0750 /home/crafty
```

Isso cria o diretório com proprietário/grupo `crafty` e permissão `0750`. A exceção `AccessDeniedException` deixou de aparecer após reinicialização.

## 4. Correções confirmadas cujo comando integral não foi recuperado

As correções abaixo constam do histórico e foram validadas, mas a revisão do histórico não recuperou os comandos exatos nem todos os conteúdos finais. Não inventar comandos de reaplicação.

| Correção | Estado do registro de comandos |
|---|---|
| Naturalist — override `kubejs/data/naturalist/loot_tables/entities/tortoise.json` usando `minecraft:scute` | Conteúdo/validação conhecidos; comando de criação integral não recuperado |
| ExtendedAE — override vazio `kubejs/data/expatternprovider/loot_tables/blocks/ex_emc_interface.json` | Conteúdo do override conhecido; comando integral não recuperado |
| Occultism — remoção de `kubejs/data/occultism/recipes/miner/ores/thorium_ore.json` (arquivo de 0 bytes) | A remoção foi confirmada; comando literal não recuperado |
| Citadel — conversão de 12 entradas de livros para NBT compatível com 1.20.1 no datapack `compat_loot_fixes` | Transformação confirmada; script/comandos e lista dos 12 arquivos não recuperados |
| SFM — override vazio da loot table `sfm:blocks/buffer` no datapack `compat_loot_fixes` | Resultado e validação por `/reload` confirmados; comando integral não recuperado |
| Crypt Loot — correção do campo `value` para `name` no datapack `compat_loot_fixes` | Correção e validação por `/reload` confirmadas; comando/script integral não recuperado |

### Como completar essas receitas de manutenção

Quando os comandos originais ou arquivos finais forem recuperados, acrescentar para cada item:
1. caminho completo do arquivo;
2. comando de backup;
3. comando/heredoc ou script completo;
4. validação JSON/NBT;
5. comando de recarga ou reinicialização;
6. trecho de log que confirmou a ausência do erro.

Não copiar um override de uma versão antiga do mod sem comparar o recurso original da versão nova.

## 6. Relacionamento com os demais runbooks

- Fixação da versão Forge no JAR Arclight: [Arclight — inicialização e fixação do Forge](../maintenance/arclight-forge-version-pinning.md).
- Correções de Mixins client-only: [client-only-mixins.md](../fixes/client-only-mixins.md).
- Correções de dados e loot tables: [data-and-loot-table-fixes.md](../fixes/data-and-loot-table-fixes.md).

## 7. Regra para atualização de mods

Uma atualização pode substituir recursos internos dos JARs e invalidar overrides. Antes de reaplicar:
- compare o recurso da versão nova com o recurso que motivou a correção;
- confirme se o mod já corrigiu o problema upstream;
- preserve o arquivo atual antes de editar;
- reaplique apenas o ajuste ainda necessário;
- valide sintaxe e inicialização;
- teste no jogo quando a correção afetar drops, receitas, livros ou progressão.


## 5. Advancements — Industrial Foregoing, Delightful e Legendary Monsters

Os overrides abaixo foram criados a partir dos JSONs originais dos JARs. O script faz backup de um override anterior, quando existir, e altera somente o campo necessário. Execute na raiz do servidor:

```bash
sudo python3 <<'PY'
import json
import zipfile
from pathlib import Path

fixes = [
    {
        "jar": Path("mods/industrial-foregoing-1.20.1-3.5.22.jar"),
        "source": "data/industrialforegoing/advancements/recipes/misc/simulated_hydroponic_bed.json",
        "target": Path("kubejs/data/industrialforegoing/advancements/recipes/misc/simulated_hydroponic_bed.json"),
        "tag_predicate": True,
    },
    {
        "jar": Path("mods/Delightful-1.20.1-3.8.1.jar"),
        "source": "data/sob/advancements/get_prickly_pear.json",
        "target": Path("kubejs/data/sob/advancements/get_prickly_pear.json"),
        "icon": "minecraft:apple",
    },
    {
        "jar": Path("mods/legendarymonsters-2.2.4 MC 1.20.1.jar"),
        "source": "data/legendary_monsters/advancements/defeat_ambusher.json",
        "target": Path("kubejs/data/legendary_monsters/advancements/defeat_ambusher.json"),
        "icon": "legendary_monsters:chiseled_ancient_dripstone_shard",
    },
]

for fix in fixes:
    with zipfile.ZipFile(fix["jar"]) as jar:
        data = json.loads(jar.read(fix["source"]))
    target = fix["target"]
    target.parent.mkdir(parents=True, exist_ok=True)
    if target.exists():
        target.with_suffix(target.suffix + ".bak").write_bytes(target.read_bytes())
    if fix.get("tag_predicate"):
        predicate = data["criteria"]["has_item"]["conditions"]["items"][0]
        predicate.pop("items", None)
        predicate["tag"] = "forge:plastic"
    else:
        data["display"]["icon"]["item"] = fix["icon"]
    target.write_text(json.dumps(data, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(f"Criado: {target}")
PY

sudo chown -R crafty:crafty kubejs/data/industrialforegoing kubejs/data/sob kubejs/data/legendary_monsters
```

Valide os três JSONs:

```bash
python3 -m json.tool kubejs/data/industrialforegoing/advancements/recipes/misc/simulated_hydroponic_bed.json > /dev/null
python3 -m json.tool kubejs/data/sob/advancements/get_prickly_pear.json > /dev/null
python3 -m json.tool kubejs/data/legendary_monsters/advancements/defeat_ambusher.json > /dev/null
```

No console do servidor, execute `/reload`. Depois confira o log:

```bash
grep -iE 'get_prickly_pear|defeat_ambusher|simulated_hydroponic_bed|Parsing error loading custom advancement|Unknown item id' logs/latest.log | tail -n 30
```

A validação registrada em 11/11/2026 não retornou linhas para essa busca. Isso confirma a ausência dos erros de carregamento correspondentes, não o desbloqueio funcional das conquistas.


## 8. AllTheModium — `tconstruct:extra` → `tconstruct:binding` no JAR

Correção documentada em [allthemodium-tconstruct-material-stats.md](../fixes/allthemodium-tconstruct-material-stats.md). Execute na raiz do servidor, com o servidor parado.

O comando executado originalmente foi um heredoc Python equivalente; o script abaixo é a forma reutilizável (testada apenas em JAR sintético). Veja primeiro o que seria alterado:

```bash
sudo python3 scripts/patch_allthemodium_stats.py --dry-run mods/allthemodium-1.20.1-47.1.25-2.5.8.jar
```

Aplicar (cria `mods/allthemodium-1.20.1-47.1.25-2.5.8.jar.original` se ainda não existir):

```bash
sudo python3 scripts/patch_allthemodium_stats.py mods/allthemodium-1.20.1-47.1.25-2.5.8.jar
```

Validar o JAR:

```bash
for m in unobtainium vibranium allthemodium; do
  unzip -p mods/allthemodium-1.20.1-47.1.25-2.5.8.jar data/allthemodium/tinkering/materials/stats/$m.json | grep -c 'tconstruct:extra'
done   # esperado: 0 em cada linha
```

Depois de reiniciar:

```bash
grep -c 'tconstruct:extra' logs/latest.log   # esperado: 0
```

Rollback: com o servidor parado, restaurar o `.original` sobre o JAR. Em uma atualização do AllTheModium ou do Tinkers' Construct, aplicar a regra da seção 7 antes de reaplicar.


## 9. Reborn Storage — `use_resource_pack` no `book.json` (somente servidor)

Correção documentada em [rebornstorage-patchouli-book.md](../fixes/rebornstorage-patchouli-book.md). Execute na raiz do servidor, com o servidor parado. Comando executado:

```bash
J=mods/rebornstorage-1.20.1-5.0.7.jar
sudo cp -a $J $J.original
sudo python3 - "$J" <<'EOF'
import sys, json, shutil, tempfile, os, zipfile
jar = sys.argv[1]
name = "data/rebornstorage/patchouli_books/rs_book/book.json"
tmp = os.path.join(tempfile.mkdtemp(), "new.jar")
with zipfile.ZipFile(jar) as zin, zipfile.ZipFile(tmp, "w", zipfile.ZIP_DEFLATED) as zout:
    for i in zin.infolist():
        data = zin.read(i.filename)
        if i.filename == name:
            d = json.loads(data); d["use_resource_pack"] = True
            data = (json.dumps(d, indent=2) + "\n").encode()
        zout.writestr(i, data)
shutil.copyfile(tmp, jar)
EOF
unzip -p $J data/rebornstorage/patchouli_books/rs_book/book.json
```

A saída deve conter `"use_resource_pack": true`. Depois de reiniciar:

```bash
grep -c 'rebornstorage:rs_book' logs/latest.log   # esperado: 0
```

Rollback: com o servidor parado, restaurar o `.original` sobre o JAR. Não altera os clientes. Em atualização do mod, aplicar a regra da seção 7.
