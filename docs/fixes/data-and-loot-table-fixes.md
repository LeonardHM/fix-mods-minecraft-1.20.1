# Correções de dados, loot tables e inicialização

**Janela revisada:** 2026-11-10 10:17 até 2026-11-11 02:15 (America/Sao_Paulo)  
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

## 9. Erros de loot table que permaneceram após as correções

Na inicialização de validação, ainda foram reportados IDs de itens desconhecidos nas seguintes loot tables:

| Mod/recurso | Referência |
|---|---|
| Maiden's Merry Making | `maidensmerrymaking:blocks/roof_bamboo_stairs` |
| SFM | `sfm:blocks/buffer` |
| Advanced Generators | `advgenerators:blocks/eu_output_iv`, `eu_output_hv`, `eu_output_ev`, `eu_output_mv`, `eu_output_lv` |

Mensagem observada: `Expected name to be an item, was unknown string ...`

Esses erros **não foram corrigidos** nessa janela. Devem permanecer na lista de diagnósticos pendentes.

## Resultado consolidado da inicialização

Após as alterações, o servidor chegou à inicialização dos mundos. Na validação do log, não reapareceram os erros anteriormente associados a:

- SGJourney — parsing da tabela de endereços;
- Naturalist — `minecraft:turtle_scute`;
- MegaCells e ExtendedAE — loot tables das interfaces EMC;
- Occultism — receita Thorium com erro EOF;
- ResourcefulLib — `AccessDeniedException` em `/home/crafty`.

A ausência dessas mensagens após reinicialização confirma a correção do erro de inicialização correspondente; não substitui testes funcionais específicos dentro do jogo.
