# Diagnósticos pendentes

**Ambiente de referência:** Arclight / Forge 1.20.1, Forge 47.4.10, Java 17 (Amazon Corretto)  
**Última revisão registrada:** 2026-11-11

Este documento separa mensagens observadas no log de causas já comprovadas. Uma mensagem de erro não significa, por si só, que exista impacto funcional no jogo.

## Industrial Foregoing — advancement com item desconhecido

- **Mod/JAR:** `industrial-foregoing-1.20.1-3.5.22.jar`
- **Registro:** advancement `industrialforegoing:recipes/misc/simulated_hydroponic_bed`
- **Mensagem:** `Unknown item id 'forge:plastic'`
- **Estado:** pendente de inspeção do JSON do advancement.
- **Contexto observado:** Almost Unified registrou que modificou a tag `#forge:plastic`, adicionando `pneumaticcraft:plastic`.
- **Hipótese a confirmar:** o advancement pode estar usando `forge:plastic` em um campo que espera um ID de item, e não uma tag. Ainda não foi confirmado sem inspecionar o JSON dentro do JAR.
- **Próxima verificação:**
  ```bash
  unzip -p mods/industrial-foregoing-1.20.1-3.5.22.jar data/industrialforegoing/advancements/recipes/misc/simulated_hydroponic_bed.json
  ```

Não alterar o JAR ou datapack até conferir o conteúdo e a estrutura desse JSON.

## GregTech CEu — Rhino não consegue resolver classes client-only

- **Mensagens observadas:** `NoClassDefFoundError: net/minecraft/client/color/item/ItemColor`
- **Classes citadas:** `GTMaterialBlocks` e `GTMaterialItems`
- **Estado:** investigação adiada deliberadamente.
- **Observação:** o erro aparece durante a tentativa do Rhino de obter métodos declarados. Ainda não foi determinado se é apenas uma limitação de introspecção, um problema de carregamento no servidor dedicado ou algo com impacto funcional.

Também foram observados avisos/erros relacionados a receitas do GregTech CEu. Devem ser analisados em conjunto, com o trecho completo do log e as versões exatas das dependências.

## Patchouli — livro de Reborn Storage

- **Mensagem:** falha ao carregar o livro `rebornstorage:rs_book` (`use_resource_pack set to false. This behaviour was removed in 1.20`).
- **Causa confirmada:** o `book.json` do Reborn Storage 5.0.7 não declara `use_resource_pack` e o conteúdo está em `data/`; o Patchouli 1.20.1 não aceita isso.
- **Estado:** corrigido **somente no servidor** (erro sumiu do log); clientes seguem com o erro e sem o livro. Ver `docs/fixes/rebornstorage-patchouli-book.md`.
- **Pendente:** correção completa (mod atualizado ou JAR alterado também nos clientes), não aplicada.

## PneumaticCraft — consulta de receitas sem mundo

- **Mensagem:** o mod detectou uma consulta de receitas sem um mundo disponível e retornou uma lista vazia.
- **Estado:** pendente de avaliação de impacto.
- **Observação:** não há evidência registrada de que isso interrompa uma receita normal durante o jogo.

## Tags de estruturas — Rats / Towns and Towers

- **Tag:** `totw_modded:has_structure/ratlantis_tower`
- **Referência ausente:** `rats:ratlantis`
- **Estado:** pendente.
- **Observação:** verificar se o datapack/mod que deveria registrar essa estrutura está instalado e se a referência é esperada nessa combinação de versões.

## Tags de conteúdo — CTOV / Wares

Foram registradas referências ausentes:
- `wares:sealed_delivery_agreement`
- `wares:cardboard_box`

**Estado:** pendente de verificar compatibilidade entre as versões dos mods e os datapacks que declaram essas tags.

## Advancements com IDs desconhecidos

Foram observados os seguintes registros:

| Advancement | ID desconhecido |
|---|---|
| Industrial Foregoing — `industrialforegoing:recipes/misc/simulated_hydroponic_bed` | `forge:plastic` |
| SOB — `sob:get_prickly_pear` | `sob:prickly_pear` |
| Legendary Monsters | `legendary_monsters:ancient_dripstone_shard` |

**Estado:** pendente de verificar se são referências obsoletas, itens removidos/renomeados ou dados incompatíveis entre versões. O caso do Industrial Foregoing está descrito separadamente acima.

## Coremod `field_to_method.js` — campo `Biome.climateSettings` público (Voidscape)

- **Mod/JAR:** `Voidscape-1.20.1-1.5.389.jar`
- **Mensagem (2 ocorrências no log de 11/11/2026):**
  ```
  Error occurred applying transform of coremod coremods/field_to_method.js function biome
  java.lang.IllegalStateException: Field f_47437_ is not private and an instance field
  ```
- **Causa confirmada:** o Access Transformer do Voidscape (`META-INF/accesstransformer.cfg`, linha 15) torna o campo público:
  ```
  public net.minecraft.world.level.biome.Biome f_47437_ # climateSettings
  ```
  A mensagem do coremod indica que ele exige que o campo seja privado.
- **Como o mod foi identificado:**
  ```bash
  for j in mods/*.jar; do
    unzip -p "$j" META-INF/accesstransformer.cfg 2>/dev/null | grep -qE 'f_47437_|climateSettings' && echo "$j"
  done
  ```
- **Estado:** causa confirmada; **nenhuma alteração aplicada** (decisão de manter). O servidor inicia; o impacto funcional não foi avaliado.
- **Possível solução:** versão do Voidscape que não torne o campo público, se existir. Não verificado se há versão posterior à 1.5.389.

> A correção do Tinkers' Construct x AllTheModium (`tconstruct:extra`), antes listada aqui, foi aplicada: ver `docs/fixes/allthemodium-tconstruct-material-stats.md`.

## ComputerCraft / Advanced Peripherals — métodos de integração

Foram observadas mensagens indicando que métodos de integração não possuem os parâmetros esperados, incluindo:

- `ReactorIntegration.getName`
- `EnergyCellIntegration.getName`
- `FurnatorIntegration.getName`

**Estado:** pendente de identificar as versões envolvidas e verificar se a integração está funcionalmente afetada.

## Critério para encerrar um diagnóstico

Antes de marcar qualquer item como corrigido, registrar:
1. trecho completo da mensagem original;
2. versões exatas dos mods envolvidos;
3. causa confirmada (não apenas hipótese);
4. alteração realizada e backup, quando aplicável;
5. validação após reiniciar e, quando pertinente, teste funcional no jogo.


## Mixins — BufferBuilder / ImmediatelyFast / ModernFix

- Durante a análise de Mixins client-only, referências a `BufferBuilder` também apareceram em CreateBetterFPS, ImmediatelyFast e ModernFix.
- CreateBetterFPS foi corrigido e validado conforme `docs/fixes/client-only-mixins.md`.
- O histórico disponível não confirma alteração aplicada em ImmediatelyFast nem em ModernFix. Não desativar nem mover Mixins desses mods sem identificar a classe, o JSON exato e validar o efeito.
- A identificação “ImmediatelyFast 1.20.4” foi esclarecida pelo usuário como apenas o nome do pacote; não deve ser tratada como evidência de que o servidor use Minecraft 1.20.4.
