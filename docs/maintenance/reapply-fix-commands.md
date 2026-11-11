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

## 5. Relacionamento com os demais runbooks

- Fixação da versão Forge no JAR Arclight: [Arclight — inicialização e fixação do Forge](../maintenance/arclight-forge-version-pinning.md).
- Correções de Mixins client-only: [client-only-mixins.md](../fixes/client-only-mixins.md).
- Correções de dados e loot tables: [data-and-loot-table-fixes.md](../fixes/data-and-loot-table-fixes.md).

## 6. Regra para atualização de mods

Uma atualização pode substituir recursos internos dos JARs e invalidar overrides. Antes de reaplicar:
- compare o recurso da versão nova com o recurso que motivou a correção;
- confirme se o mod já corrigiu o problema upstream;
- preserve o arquivo atual antes de editar;
- reaplique apenas o ajuste ainda necessário;
- valide sintaxe e inicialização;
- teste no jogo quando a correção afetar drops, receitas, livros ou progressão.
