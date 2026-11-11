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

- **Mensagem:** falha ao carregar o livro `rebornstorage:rs_book`.
- **Estado:** pendente.
- **Ainda não determinado:** se o recurso está ausente, malformado, incompatível ou se o erro é apenas de conteúdo/documentação.

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

## Tinkers' Construct — material stats não registrados

- **Materiais citados:** `allthemodium:unobtainium`, `allthemodium:allthemodium`, `allthemodium:vibranium`
- **Mensagem:** `Skipping unregistered material stat type 'tconstruct:extra'`
- **Estado:** pendente.
- **Hipótese:** incompatibilidade ou integração incompleta entre dados de materiais e Tinkers' Construct. Ainda não confirmada.

## ComputerCraft / Advanced Peripherals — métodos de integração

Foram observadas mensagens indicando que métodos de integração não possuem os parâmetros esperados, incluindo:

- `ReactorIntegration.getName`
- `EnergyCellIntegration.getName`
- `FurnatorIntegration.getName`

**Estado:** pendente de identificar as versões envolvidas e verificar se a integração está funcionalmente afetada.

## Aviso de configuração Mixin

- **Mensagem:** `ftbxaerocompat.mixins.json does not specify "minVersion" property`
- **Estado:** aviso de configuração/qualidade; sem falha funcional confirmada.
- **Ação:** nenhuma alteração aplicada.

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
