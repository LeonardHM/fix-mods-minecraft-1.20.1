# Deeper and Darker — receitas de Ferramentas de Resonarium na Smithing Table

**Status:** aplicada no servidor e validada pelo log (teste funcional no jogo não registrado)  
**Ambiente:** Minecraft 1.20.1, Forge/Arclight, Deeper and Darker Forge 1.20.1-1.3.3 (`deeperdarker-forge-1.20.1-1.3.3.jar`), KubeJS  
**Data do registro:** 2026-11-20

## 1. Erro original

Durante o carregamento das receitas, nove receitas de transformação de ferraria falham com:

```
Failed to parse recipe 'deeperdarker:resonarium_*_smithing[minecraft:smithing_transform]'!
Falling back to vanilla: Ingredient 'template' can't be empty!
```

A inspeção do arquivo original dentro do JAR do mod confirmou que a receita contém `"template": []`:

```json
{
  "type": "minecraft:smithing_transform",
  "addition": { "item": "deeperdarker:resonarium_plate" },
  "base": { "item": "minecraft:iron_pickaxe" },
  "result": { "item": "deeperdarker:resonarium_pickaxe" },
  "template": []
}
```

## 2. Causa

Confirmada: o mod distribui as nove receitas com o campo `template` como lista vazia, e o KubeJS rejeita o ingrediente vazio ao ler o JSON original. O erro vem da receita do próprio mod, não de script do servidor. Não foi encontrada atualização do Deeper and Darker que resolva isso na versão usada.

## 3. Receitas afetadas

`deeperdarker:resonarium_<peça>_smithing`, para `axe`, `boots`, `chestplate`, `helmet`, `hoe`, `leggings`, `pickaxe`, `shovel` e `sword`.

## 4. Tentativa 1: script KubeJS (não resolveu o aviso)

Foi instalado `kubejs/server_scripts/deeperdarker_resonarium.js`, que removia cada receita por ID e a recriava com `event.smithing(...)` usando `minecraft:netherite_upgrade_smithing_template`. O log mostra o script carregado (`Loaded script server_scripts:deeperdarker_resonarium.js`) e, mesmo assim, as nove mensagens `Ingredient 'template' can't be empty!` continuaram aparecendo.

Explicação: o aviso é emitido ao fazer o parse da receita original, antes de o evento do script rodar. O script não consegue impedir esse parse; apenas substitui a receita depois.

## 5. Solução aplicada: override por datapack

Foram criados nove JSONs em `kubejs/data/deeperdarker/recipes/`, com o mesmo nome dos originais (`resonarium_<peça>_smithing.json`), que substituem os arquivos do mod. Com isso a receita original (`template: []`) deixa de ser lida.

Conteúdo (exemplo: picareta):

```json
{
  "type": "minecraft:smithing_transform",
  "template": { "item": "minecraft:netherite_upgrade_smithing_template" },
  "base": { "item": "minecraft:iron_pickaxe" },
  "addition": { "item": "deeperdarker:resonarium_plate" },
  "result": { "item": "deeperdarker:resonarium_pickaxe" }
}
```

| Slot | Item |
|---|---|
| Template | `minecraft:netherite_upgrade_smithing_template` |
| Base | Ferramenta/armadura de ferro correspondente |
| Addition | `deeperdarker:resonarium_plate` |
| Resultado | Peça de Resonarium correspondente |

Comandos: [runbook, seção 12](../maintenance/reapply-fix-commands.md).

O script `.js` da tentativa 1 foi desativado renomeando-o para `kubejs/server_scripts/deeperdarker_resonarium.js.disabled` (o KubeJS só carrega `.js`). Os dois métodos não devem ficar ativos ao mesmo tempo, pois definiriam a mesma receita.

### Efeito da alteração

- As nove receitas continuam na Smithing Table e mantêm os mesmos IDs.
- **Mudança de balanceamento:** o jogador passa a precisar de um Netherite Upgrade Smithing Template em cada transformação. O mod original não exigia template (era justamente o campo vazio).
- O JAR do Deeper and Darker não é modificado.

## 6. Backup

Não há backup, pois nenhum arquivo existente foi alterado: os JSONs são novos e o script foi apenas renomeado (o próprio `.disabled` é o backup).

## 7. Validação

Após aplicar os JSONs, desativar o script e recarregar:

```bash
grep -i 'Failed to parse recipe.*deeperdarker' logs/latest.log   # sem saída (0 ocorrências)
```

Resultado: o comando não retornou nada; os nove avisos deixaram de aparecer.

Limites da validação:

- Confirma o desaparecimento do erro de parsing. **Não foi registrado** teste de crafting no jogo (template de netherite + ferramenta de ferro + Resonarium Plate na Smithing Table). Fazer ao menos um teste antes de considerar a receita funcionalmente confirmada.
- O método de recarga usado (`/reload` ou reinício) não foi registrado.

## 8. Avisos que continuam no log e não têm relação

Na mesma busca apareceram outros avisos que não fazem parte desta correção e permanecem sem tratamento:

- `GregTechCEu ... failed to add recipe from staging into lookup DB` para `deeperdarker:copper_ingot_from_smelting_gloomslate_copper_ore` e `deeperdarker:lapis_lazuli_from_smelting_gloomslate_lapis_ore` (receitas de fundição; não investigado).
- `mixins.deeperdarker.json:PhantomRendererMixin`: o alvo `net.minecraft.client.renderer.entity.PhantomRenderer` é classe de cliente e não existe no servidor (aviso esperado em servidor dedicado).

## 9. Rollback

Com o servidor parado, remover os nove JSONs de override:

```bash
sudo rm kubejs/data/deeperdarker/recipes/resonarium_*_smithing.json
```

Sem eles, as receitas originais com `template: []` voltam a ser lidas e o aviso reaparece. Se também quiser restaurar o script da tentativa 1: `sudo mv kubejs/server_scripts/deeperdarker_resonarium.js.disabled kubejs/server_scripts/deeperdarker_resonarium.js`.

## 10. Atenção a atualizações

Se o Deeper and Darker for atualizado, conferir se a receita original ainda tem `template: []`. Se o mod corrigir o campo, o override deixa de ser necessário e pode ser removido (o override prevalece sobre o mod e manteria o template de netherite como exigência).
