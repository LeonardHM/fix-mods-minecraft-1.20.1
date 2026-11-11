# Changelog

Alterações relevantes na documentação e nas correções registradas neste repositório.

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
