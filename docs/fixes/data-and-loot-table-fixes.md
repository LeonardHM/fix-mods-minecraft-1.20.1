# Correções de dados, loot tables e inicialização

**Janela revisada:** 2026-11-10 10:17 até 2026-11-11 02:53 (America/Sao_Paulo)  
**Ambiente:** servidor Minecraft 1.20.1 em Arclight / Forge; versão Forge ativa confirmada: 47.4.10.  
**Critério:** este documento registra somente alterações com evidência de execução e/ou validação no log. Itens sem confirmação suficiente ficam identificados como pendentes.

## 1. SGJourney — corrigir estrutura JSON da tabela de endereços

- **Arquivo sobrescrito via KubeJS:** `kubejs/data/overworld_cartouches/sgjourney/address_table/cartouche_overworld.json`
- **Erro:** `Not a JSON object: "sgjourney:abydos"`
- **Causa:** entradas do campo `address` estavam em formato incompatível com o formato esperado pelo mod.
- **Correção:** ajustar `address` para ser um objeto contendo `dimension` e `galaxy`, em vez de uma string simples.
- **Backup:** arquivo original preservado com sufixo `.bak`.
- **Validação:** `python3 -m json.tool "$FILE"` passou. Na inicialização posterior, os erros de parsing do SGJourney não reapareceram.

## 2. Naturalist — loot table da tartaruga

- **JAR:** `mods/naturalist-5.0pre2+forge-1.20.1.jar`
- **Recurso original:** `data/naturalist/loot_tables/entities/tortoise.json`
- **Problema:** a loot table fazia referência a `minecraft:turtle_scute`, ID que não era reconhecido nesse contexto/versão.
- **Override criado:** `kubejs/data/naturalist/loot_tables/entities/tortoise.json`
- **Conteúdo funcional registrado:** loot table substituta contendo somente `minecraft:scute`.
- **Permissões:** diretório/arquivo criados com proprietário `crafty:crafty`; diretório com modo 0755.
- **Validação:** JSON validado; após reiniciar, a mensagem relacionada a `turtle_scute` não reapareceu.

## 3. MegaCells — EMC Interface

- **JAR:** `mods/megacells-forge-2.4.6-1.20.1.jar`
- **Recurso sobrescrito:** `data/megacells/loot_tables/blocks/mega_emc_interface.json`
- **Problema:** loot table fazia referência ao bloco `megacells:mega_emc_interface`, cujo registro depende da integração opcional AppliedE. As receitas relacionadas usam condição `forge:mod_loaded` para `appliede`, mas a loot table não tinha a condição equivalente; isso gerava erro de item desconhecido quando AppliedE não estava carregado.
- **Override KubeJS:** `kubejs/data/megacells/loot_tables/blocks/mega_emc_interface.json`
- **Conteúdo:**
  ```json
  {"type":"minecraft:block","pools":[]}
  ```
- **Validação:** após reiniciar, o erro da loot table EMC do MegaCells não reapareceu.

## 4. ExtendedAE — EMC Interface

- **Recurso sobrescrito:** `data/expatternprovider/loot_tables/blocks/ex_emc_interface.json`
- **Bloco:** `expatternprovider:ex_emc_interface`
- **Problema:** mesmo padrão da integração opcional/loot table sem condição adequada, resultando em referência a item desconhecido.
- **Override KubeJS:** `kubejs/data/expatternprovider/loot_tables/blocks/ex_emc_interface.json`
- **Conteúdo:**
  ```json
  {"type":"minecraft:block","pools":[]}
  ```
- **Validação:** após reiniciar, o erro da loot table EMC do ExtendedAE não reapareceu.

> Os overrides vazios evitam que o sistema tente resolver uma loot table para um bloco opcional que não está registrado. Não representam uma correção no JAR original.

## 5. Occultism — arquivo de receita Thorium com tamanho zero

- **Arquivo removido:** `kubejs/data/occultism/recipes/miner/ores/thorium_ore.json`
- **Problema:** arquivo override KubeJS de 0 bytes provocava erro de parsing/EOF.
- **Verificação:** o JSON original dentro do JAR do Occultism estava íntegro.
- **Correção:** remover somente o override vazio de KubeJS, permitindo que o recurso original do mod seja utilizado.
- **Validação:** após reiniciar, o erro de parsing/EOF da receita de thorium não reapareceu.

## 6. ResourcefulLib — diretório de home ausente

- **Versão:** ResourcefulLib 2.1.29.
- **Erro:** `AccessDeniedException` ao acessar `/home/crafty`.
- **Causa observada:** o diretório esperado pelo mod/serviço não existia.
- **Correção executada:**
  ```bash
  sudo install -d -o crafty -g crafty -m 0750 /home/crafty
  ```
- **Resultado:** diretório criado com proprietário `crafty:crafty` e permissão 0750.
- **Validação:** após reiniciar, a exceção `AccessDeniedException` do ResourcefulLib não reapareceu.

## 7. Forge / Arclight — versão ativa confirmada

- **JAR ativo:** `arclight-forge-1.20.1-1.0.6-SNAPSHOT-5dc8683.jar`
- **Forge:** 47.4.10
- **Hash registrado:** `237c5a17d941bfe793ff5780a4f330914d2c9f57`
- **Arquivos preservados:** cópia `.jar.original` e arquivo de teste `.jar.test`.
- **Permissões registradas:** `crafty:crafty`, modo 644.
- **Observação:** o ambiente de diagnóstico posterior também confirmou Forge 47.4.10. Não inferir que outras versões/servidores citados em conversas antigas correspondam a este ambiente.

## 8. Radium / Arclight — ajuste investigativo, não correção concluída

- Foi identificado conflito provável entre `ChunkMapMixin_Optimize` do Radium e o gerenciamento de chunks/portais do Arclight.
- Foi configurado `mixin.world.player_chunk_tick=false` em `config/lithium.properties`.
- **Radium não foi desinstalado** no registro disponível.
- **Não há evidência suficiente de backup nem de validação após reinicialização** para declarar esse item corrigido.
- Portanto, manter como investigação/mitigação pendente, não como correção confirmada.

## 9. Erros de loot table que permaneceram após a primeira rodada

Na inicialização de validação da primeira rodada, ainda foram reportados IDs de itens desconhecidos nas seguintes loot tables:

| Mod/recurso | Referência |
|---|---|
| Maiden's Merry Making | `maidensmerrymaking:blocks/roof_bamboo_stairs` |
| Advanced Generators | `advgenerators:blocks/eu_output_iv`, `eu_output_hv`, `eu_output_ev`, `eu_output_mv`, `eu_output_lv` |

Mensagem observada: `Expected name to be an item, was unknown string ...`

Esses erros permaneceram sem correção confirmada no registro desta revisão. **SFM não está incluído nesta lista:** sua loot table foi corrigida posteriormente no datapack `compat_loot_fixes`, conforme a seção seguinte, e o erro deixou de aparecer após `/reload`.


## 10. Datapack `compat_loot_fixes` — correções de loot tables

Durante a rodada de correções com datapack, três grupos de erros foram tratados. As alterações foram recarregadas com `/reload`; os três erros correspondentes deixaram de aparecer no log.

### Citadel — livros com formato NBT incompatível

- **Escopo:** 12 entradas de livros nas loot tables do Citadel.
- **Problema:** os dados dos livros estavam em formato incompatível com a versão 1.20.1.
- **Correção:** converter os dados das 12 entradas para o formato NBT esperado pelo Minecraft 1.20.1.
- **Validação:** após `/reload`, o erro do Citadel não reapareceu.
- **Limite do registro:** o histórico disponível confirma a quantidade e a conversão, mas não preserva aqui os nomes individuais dos 12 arquivos. Não inventar nomes nem caminhos.

### SFM — loot table do bloco Buffer

- **Recurso corrigido no datapack:** `sfm:blocks/buffer` (arquivo `buffer.json`).
- **Problema:** a loot table fazia referência a um recurso/ID inválido para a configuração ativa.
- **Correção:** substituir a loot table por uma tabela vazia no datapack `compat_loot_fixes`.
- **Validação:** após `/reload`, o erro de SFM não reapareceu.
- **Observação:** o override vazio suprime drops dessa loot table; não altera o JAR do mod.

### Crypt Loot — chave de campo incorreta

- **Recurso:** loot table do datapack/mod identificado como `crypt_loot`.
- **Problema:** campo `value` estava sendo usado onde o formato esperava `name`.
- **Correção:** substituir a chave `value` por `name`, preservando o conteúdo restante da tabela.
- **Validação:** após `/reload`, o erro correspondente não reapareceu.

> O histórico recuperado confirma que essas três correções foram aplicadas no datapack `compat_loot_fixes` e validadas por `/reload`. Como não temos nesta revisão o conteúdo integral dos arquivos finais, não reproduzir JSONs completos nem supor caminhos específicos que não estejam preservados.

## Resultado consolidado da inicialização

Após as alterações, o servidor chegou à inicialização dos mundos. Na validação do log, não reapareceram os erros anteriormente associados a:

- SGJourney — parsing da tabela de endereços;
- Naturalist — `minecraft:turtle_scute`;
- MegaCells e ExtendedAE — loot tables das interfaces EMC;
- Occultism — receita Thorium com erro EOF;
- ResourcefulLib — `AccessDeniedException` em `/home/crafty`.

A ausência dessas mensagens após reinicialização confirma a correção do erro de inicialização correspondente; não substitui testes funcionais específicos dentro do jogo.


## 11. Advancements — Industrial Foregoing, Delightful e Legendary Monsters

As três correções abaixo foram aplicadas por overrides em `kubejs/data/` e verificadas com `/reload`. A consulta posterior ao `logs/latest.log` não retornou ocorrências dos três advancements nem das mensagens `Parsing error loading custom advancement` ou `Unknown item id` associadas a eles.

### Industrial Foregoing 3.5.22 — tag de plástico no predicado

- **Recurso original:** `data/industrialforegoing/advancements/recipes/misc/simulated_hydroponic_bed.json`, extraído de `industrial-foregoing-1.20.1-3.5.22.jar`.
- **Erro original:** `Unknown item id 'forge:plastic'`.
- **Causa:** o advancement usava `forge:plastic` como se fosse um ID de item no campo `items`. Trata-se de uma tag de itens.
- **Override:** `kubejs/data/industrialforegoing/advancements/recipes/misc/simulated_hydroponic_bed.json`.
- **Correção:** no predicado `criteria.has_item.conditions.items[0]`, substituir a propriedade `items` pela propriedade `tag`, com valor `forge:plastic`:
  ```json
  {
    "tag": "forge:plastic"
  }
  ```
- **Validação:** após `/reload`, a busca por `simulated_hydroponic_bed`, `Unknown item id` e erros de parsing de advancements não retornou mensagens correspondentes.

### Delightful 3.8.1 — ícone inexistente em `sob:get_prickly_pear`

- **Recurso original:** `data/sob/advancements/get_prickly_pear.json`, dentro de `Delightful-1.20.1-3.8.1.jar`.
- **Erro original:** `Expected item to be an item, was unknown string 'sob:prickly_pear'`.
- **Causa:** o campo `display.icon.item` apontava para `sob:prickly_pear`, que não está registrado pelo JAR. A tag `forge:fruits/prickly_pear` contém `ecologics:prickly_pear` como valor opcional (`required: false`).
- **Override:** `kubejs/data/sob/advancements/get_prickly_pear.json`.
- **Correção:** alterar somente `display.icon.item` para `minecraft:apple`. O critério original, que verifica a tag `forge:fruits/prickly_pear`, foi preservado.
- **Validação:** após `/reload`, a busca por `get_prickly_pear` e erros de parsing de advancements não retornou mensagens correspondentes.

### Legendary Monsters 2.2.4 — ícone inexistente em `defeat_ambusher`

- **Recurso original:** `data/legendary_monsters/advancements/defeat_ambusher.json`, dentro de `legendarymonsters-2.2.4 MC 1.20.1.jar`.
- **Erro original:** `Expected item to be an item, was unknown string 'legendary_monsters:ancient_dripstone_shard'`.
- **Causa:** o advancement referenciava um ID inexistente no campo `display.icon.item`. O JAR contém o item `legendary_monsters:chiseled_ancient_dripstone_shard`, confirmado pelo modelo do item e pela loot table do Ambusher.
- **Override:** `kubejs/data/legendary_monsters/advancements/defeat_ambusher.json`.
- **Correção:** alterar somente `display.icon.item` para `legendary_monsters:chiseled_ancient_dripstone_shard`. O critério original `minecraft:player_killed_entity` para `legendary_monsters:ambusher` foi preservado.
- **Validação:** após `/reload`, a busca por `defeat_ambusher` e erros de parsing de advancements não retornou mensagens correspondentes.

> **Limite da validação:** a ausência dos erros confirma que os três advancements foram aceitos pelo carregador após `/reload`. Não foi registrado teste dentro do jogo para confirmar o desbloqueio de cada conquista. Os arquivos originais dos JARs não foram modificados.
