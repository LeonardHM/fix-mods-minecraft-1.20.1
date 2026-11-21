# Remoção dos mods Delight — sobras em datapacks, KubeJS e dados

**Status:** correções aplicadas e validadas pelo log; comportamento em jogo não testado  
**Ambiente:** Minecraft 1.20.1, Forge/Arclight, KubeJS, Hostile Neural Networks, GregTech CEu  
**Data do registro:** 2026-11-21

## Contexto

Todos os mods com "delight" no ID foram removidos do servidor (`ls mods | grep -i delight` sem resultado). Mods citados nos arquivos tratados: Farmer's Delight, Delightful, Twilight Delight, Ocean's Delight, End's Delight e Nether's Delight. Arquivos de datapack e scripts continuaram referenciando itens e advancements desses mods, gerando erros no log. Todos os backups ficaram em `~/backups/`, fora das pastas carregadas pelo jogo.

## Correções aplicadas

### 1. Datapack `compat_twilightdelight_no_neapolitan`

- **Erro:** `Couldn't load tag farmersdelight:snacks` (e `farmersdelight:sweets`, `diet:sugars`) `as it is missing following references: twilightdelight:torchberry_cookie (from file/compat_twilightdelight_no_neapolitan)`.
- **Causa:** o datapack em `world/datapacks/` só existia para o Twilight Delight. No 1.20.1, uma tag com referência obrigatória ausente costuma ser descartada inteira.
- **Ação:** pasta movida para `~/backups/` (servidor parado).
- **Validação:** as três mensagens deixaram de aparecer.

### 2. Pasta de backup dentro dos dados ativos do Hostile Neural Networks

- **Erro:** oito mensagens `Failed parsing data_models file hostilenetworks:backup_before_delight_cleanup/<modelo>`.
- **Causa:** a pasta `kubejs/data/hostilenetworks/data_models/backup_before_delight_cleanup/` (cópia feita antes de uma limpeza anterior) estava no caminho carregado como dado do jogo.
- **Ação:** pasta movida para `~/backups/`.
- **Validação:** as mensagens da pasta de backup deixaram de aparecer.

### 3. Modelos `pig`, `hoglin` e `endermite`

- **Erro:** `Failed parsing data_models file hostilenetworks:pig` (e `hoglin`, `endermite`), com `JsonParseException: Failed to read non-optional item farmersdelight:ham` no caso do `pig`.
- **Causa:** `kubejs/data/hostilenetworks/data_models/{pig,hoglin}.json` citam `farmersdelight:ham` e `endermite.json` cita `endersdelight:mite_crust`.
- **Ação:** troca de item (decisão do usuário, não o comportamento original): `farmersdelight:ham` → `minecraft:porkchop` e `endersdelight:mite_crust` → `minecraft:chorus_fruit`. Backup em `~/backups/hostilenetworks/`.
- **Validação:** `grep -c 'Failed parsing data_models' logs/latest.log` → `0`.
- **Efeito:** a Loot Fabricator desses três modelos passa a produzir os itens substitutos.

### 4. Override `sob:get_prickly_pear`

- **Erro:** `Couldn't load advancement sob:get_prickly_pear` com pai `farmersdelight:main/get_fd_seed`.
- **Causa:** o override em `kubejs/data/sob/advancements/get_prickly_pear.json` (criado na correção do Delightful, seção 11 de [data-and-loot-table-fixes.md](data-and-loot-table-fixes.md)) tem como pai um advancement do Farmer's Delight. Com os dois mods removidos, a correção do ícone ficou obsoleta.
- **Ação:** arquivo movido para `~/backups/`.
- **Validação:** `grep -c 'sob:get' logs/latest.log` → `0`.

### 5. Script da estufa (`greenhouse_recipes.js`)

- **Erro:** `Error in 'ServerEvents.recipes': Invalid or empty chanced output item (recipe ID: kubejs:greenhouse/gtceu/greenhouse/quark/oak_hedge)`.
- **Causa confirmada:** a receita do Botany Pots `quark/crop/oak_hedge.json` tem um segundo drop, `delightful:acorn` (chance 0,5). O script já ignorava drops sem campo `item`, mas não drops de item inexistente. As demais plantas dos Delight são filtradas pelo `bookshelf:load_conditions` do próprio Botany Pots.
- **Ação:** em `kubejs/server_scripts/mods/gtceu/greenhouse_recipes.js`, a guarda das duas ocorrências passou a ser `if (!drop.output || !drop.output.item || !Item.exists(drop.output.item)) return;`. Backup: `~/backups/greenhouse_recipes.js.original`.
- **Validação:** `grep -c 'oak_hedge' logs/latest.log` → `0`.
- **Efeito:** a receita de estufa do `oak_hedge` continua existindo, sem o drop da bolota.

### 6. Script do Neural Node (`neural_node_recipes.js`)

- **Erro:** `Invalid or empty output item (recipe ID: kubejs:neural_node/elder_guardian)`, seguido de `No key duration in MapLike[{"type":"gtceu:neural_node",...}]`.
- **Causa confirmada:** a saída do `elder_guardian` incluía `8x oceansdelight:elder_guardian_slab`. A falha deixa a receita sem saídas e sem `duration`, o que gera a segunda mensagem. Linhas do script com itens de mods Delight: 50, 52, 56, 64, 66, 76, 84 e 94 (Ocean's, End's, Nether's, Farmer's Delight e Delightful).
- **Inferência (não verificada):** a primeira falha interrompe o resto do script, o que explica por que só o `elder_guardian` foi registrado no log.
- **Ação:** no auxiliar `neural_node(...)`, `.itemOutputs(outputs)` virou `.itemOutputs(outputs.filter(o => !Item.of(o).isEmpty()))`. Backup: `~/backups/neural_node_recipes.js.original`.
- **Validação:** as duas mensagens deixaram de aparecer no boot seguinte.
- **Efeito:** as saídas com itens dos Delight desaparecem dessas receitas.

## Referências encontradas e deixadas como estão

Sem erro correspondente no log; comportamento em jogo não verificado:

- `kubejs/server_scripts/modpack/att_items.js` (linha 9): `ends_delight:non_hatchable_dragon_egg`.
- `kubejs/server_scripts/mods/farmingforblockheads/marketitems.json`: sementes de Twilight, Farmer's, Corn e Nether's Delight.
- `kubejs/data/modpack/loot_modifiers/ender_dragon_{wannabee,drygmy}.json`: `ends_delight:dragon_tooth` e `ends_delight:dragon_leg`.
- `supplementaries:recipes/planter_rich` (no JAR do Supplementaries): `farmersdelight:rich_soil` — o erro `Unknown item id` continua no log; afeta só o advancement que desbloqueia a receita.
- `config/{farmersdelight,ends_delight,delightful}-common.toml`, `world/advancements/` e `world/stats/`: configurações e progresso de jogadores, inertes.

## Limites da validação

A validação é por log. Não foram testados no jogo: receitas do Neural Node, modelos e Loot Fabricator do Hostile Neural Networks e receita de estufa do `oak_hedge`.

## Rollback

Restaurar os arquivos de `~/backups/` para os caminhos originais (servidor parado). Em particular, não devolver `backup_before_delight_cleanup/` para dentro de `kubejs/data/`.

## Observação para varreduras futuras

Ao procurar sobras com `grep -r` em `kubejs/`, não excluir diretórios chamados `mods`: existe `kubejs/server_scripts/mods/`, que contém scripts de integração. A primeira varredura desta limpeza fez isso e deixou de listar o `neural_node_recipes.js`.
