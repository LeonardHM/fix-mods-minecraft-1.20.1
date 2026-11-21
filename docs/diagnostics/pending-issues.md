# Diagnósticos pendentes

**Ambiente de referência:** Arclight / Forge 1.20.1, Forge 47.4.10, Java 17 (Amazon Corretto)  
**Última revisão registrada:** 2026-11-21

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
| SOB — `sob:get_prickly_pear` | `sob:prickly_pear` (**resolvido em 2026-11-21**: override removido junto com os mods Delight; ver `docs/fixes/delight-mods-removal-leftovers.md`) |
| Supplementaries — `supplementaries:recipes/planter_rich` | `farmersdelight:rich_soil` (mod removido; vem do JAR do Supplementaries, afeta só o advancement que desbloqueia a receita) |
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

Confirmado pelos nomes das classes: as três pertencem à integração do Advanced Peripherals com o Powah (`advancedperipherals.common.addons.powah`).

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

## Avisos observados em 2026-11-20/21 (sem correção aplicada)

Itens abaixo foram vistos nos logs desta sessão. Salvo indicação, a causa **não foi confirmada**.

- **Mixins do `ae2cs`:** `ClassNotFoundException` para cinco classes do pacote `io.github.lounode.ae2cs` (`CircuitEtcherBlockEntity`, `CrystalPulverizerBlockEntity`, `CrystalAggregatorBlockEntity`, `EntropyVariationReactionChamberBlockEntity`, `EnergyComponent`). Hipótese: incompatibilidade de versão entre um addon do AE2 e o mod alvo. O JAR de origem ainda não foi identificado.
- **Cataclysm 3.31 — `azure_seastone_brick_stair_from_stonecutting`:** `ItemStack 'result' can't be empty!`. **Causa confirmada:** a receita aponta para `cataclysm:azure_seastone_brick_stair` (singular), mas o item real é `azure_seastone_brick_stairs`. A receita correta (`..._stairs_from_stonecutting`) existe no mesmo JAR e não gera erro. Sem perda funcional; nenhuma ação necessária.
- **Productive Bees:** receita `honeycomb_hyper_experience` com `Invalid empty fluid 'create_enchantment_industry:hyper_experience'`. O fluido não está registrado na versão instalada do Create Enchantment Industry; versões não verificadas.
- **AllTheModium:** receita de fundição `vibranium_allthemodium_alloy_ingot` com o fluido `allthemodium:molten_atmvib` não registrado. Está na mesma área da correção do Tinkers' Construct, mas não há relação confirmada.
- **Theurgy:** `lava_from_crystallized_lava` sem as chaves `evaporant` e `evaporantAmount`.
- **Caupona:** `cooking/fish_chowder` com erro `null` e sem detalhe; precisa do stack trace.
- **GregTech CEu:** dezenas de `failed to add recipe from staging into lookup DB` para receitas de smelting de vários mods. Causa não investigada.
- **Curios / Thermal:** `Duplicate Capability Key: curios:item` aparece nos mesmos milissegundos da consulta do Thermal ao combustível de `mekanism:hdpe_elytra`. A relação é sugerida pelo horário, não confirmada. O Thermal informa que o item deve funcionar como combustível.
- **Deeper and Darker — `PhantomRendererMixin`:** mixin de classe de cliente (`PhantomRenderer`) carregado no servidor; aviso esperado em servidor dedicado. Candidato ao tratamento descrito em `docs/fixes/client-only-mixins.md`, se o log precisar ser limpo.
