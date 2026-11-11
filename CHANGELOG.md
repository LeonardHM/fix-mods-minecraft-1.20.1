## 2026-11-11 — correções de advancements

- Industrial Foregoing 3.5.22: corrigido o predicado do advancement `simulated_hydroponic_bed`, usando `tag: forge:plastic` em vez de tratar a tag como ID de item.
- Delightful 3.8.1: corrigido o ícone inválido de `sob:get_prickly_pear` para `minecraft:apple`, preservando o critério original baseado na tag de frutas.
- Legendary Monsters 2.2.4: corrigido o ícone inválido de `defeat_ambusher` para `legendary_monsters:chiseled_ancient_dripstone_shard`, preservando o critério de morte do Ambusher.
- As três correções foram aplicadas por overrides KubeJS e validadas por `/reload`; a busca posterior no `latest.log` não retornou os erros correspondentes.
- Documentadas as correções e o procedimento de reaplicação no guia de dados/loot tables e no runbook.

# Changelog

Alterações relevantes na documentação e nas correções registradas neste repositório.

## 2026-11-11 — ModernFix `dynamic_dfu` x Structurize

- Corrigido o aviso do Structurize `Invalid DataFixer detected, schematics might not paste correctly!` (`org.embeddedt.modernfix.dfu.LazyDataFixer`) desligando `mixin.perf.dynamic_dfu` em `config/modernfix-mixins.properties`. Validado por reinicialização: 0 ocorrências do aviso e de `Bypassed Mojang DFU`.
- Colagem de schematics não testada; custo da otimização desligada não medido. Versões: ModernFix 5.27.91, Structurize 1.0.825-snapshot. Seção 11 adicionada ao runbook de reaplicação.

## 2026-11-11 — minVersion do Mixin do ftbxaerocompat (somente servidor)

- ftbxaerocompat 1.4.0: corrigido `Mixin config ftbxaerocompat.mixins.json does not specify "minVersion" property` acrescentando `"minVersion": "0.8"` ao JSON dentro do JAR do servidor. Validado por reinicialização: 0 ocorrências de erro no log.
- Clientes não alterados. Item removido dos diagnósticos pendentes; seção 10 adicionada ao runbook de reaplicação.

## 2026-11-11 — livro do Patchouli do Reborn Storage (somente servidor)

- Reborn Storage 5.0.7 / Patchouli 1.20.1-85: corrigido `Failed to load book rebornstorage:rs_book` (`use_resource_pack set to false`) acrescentando `"use_resource_pack": true` ao `book.json` no JAR do servidor. Validado por reinicialização: 0 ocorrências no log.
- Os clientes não foram alterados e continuam sem o livro; a correção completa não foi aplicada nem testada.
- Item Patchouli atualizado nos diagnósticos pendentes (causa confirmada, estado parcial); seção 9 adicionada ao runbook de reaplicação.

## 2026-11-11 — Tinkers' Construct x AllTheModium

- AllTheModium 2.5.8 / Tinkers' Construct 3.12.1.231: corrigido `Skipping unregistered material stat type 'tconstruct:extra'` (unobtainium, vibranium e allthemodium), trocando `tconstruct:extra` por `tconstruct:binding` vazio nos JSONs de stats dentro do JAR do AllTheModium. Validado por reinicialização: 0 ocorrências no log.
- Registrada a tentativa com datapack `atm_fix`: foi carregado, mas o erro persistiu; removido.
- Adicionados `scripts/patch_allthemodium_stats.py` (testado apenas em JAR sintético) e a seção 8 do runbook de reaplicação.
- Removido o item Tinkers' Construct dos diagnósticos pendentes. Registrado como pendente, sem correção aplicada, o erro do coremod `field_to_method.js` causado pelo Access Transformer do Voidscape 1.5.389.

## 2026-11-11 — consolidação da documentação

- Expandido o README com um resumo das correções confirmadas e seus respectivos documentos de referência.
- Corrigida a seção de erros remanescentes de loot tables: SFM foi removido da lista de pendências porque sua loot table foi corrigida posteriormente no datapack `compat_loot_fixes` e validada por `/reload`.
- Mantidos como pendentes Maiden's Merry Making e Advanced Generators, sem presumir correções não confirmadas.
- Reforçada a distinção entre validação de carregamento e teste funcional dentro do jogo.

## 2026-11-11

- Criado o registro das quatro correções de Mixins client-only: CreateBetterFPS, CoFH Core, AdvancedAE e Legendary Monsters.
- Registrados os principais avisos e erros ainda pendentes de investigação.
- Documentado o ambiente de referência Arclight / Forge 1.20.1, Forge 47.4.10 e Java 17.


## 2026-11-11 — revisão histórica adicional

- Registradas as correções de SGJourney, Naturalist, MegaCells, ExtendedAE, Occultism e ResourcefulLib.
- Incluídas as correções do datapack `compat_loot_fixes`: 12 livros do Citadel, loot table `sfm:blocks/buffer` e campo `value`→`name` em `crypt_loot`.
- Atualizado o diagnóstico: SFM removido da lista de pendências após validação por `/reload`.
- Mantidas como pendentes as referências de loot table de Maiden's Merry Making e Advanced Generators, além dos demais avisos ainda não investigados.


## 2026-11-11 — runbooks de manutenção

- Documentado como o Crafty inicia diretamente o JAR Arclight e como a versão Forge 47.4.10 foi fixada em `META-INF/installer.json`.
- Incluídos comandos de backup, geração de JAR de teste, instalação, validação e rollback.
- Criado runbook de comandos reaplicáveis para as correções de SGJourney, MegaCells e ResourcefulLib.
- Identificadas explicitamente as correções cujo comando original/conteúdo integral não foi recuperado, evitando instruções presumidas.
