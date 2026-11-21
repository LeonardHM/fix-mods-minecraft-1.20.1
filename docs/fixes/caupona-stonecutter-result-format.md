# Caupona — receitas de stonecutter com `result` no formato de versões novas

**Status:** aplicada no servidor e validada pelo log (teste de crafting na pedra de corte não registrado)  
**Ambiente:** Minecraft 1.20.1, Forge/Arclight, KubeJS  
**Mod:** `caupona-1.20.1-0.4.14.jar`  
**Data do registro:** 2026-11-21

## Erro original

```
Failed to parse recipe 'caupona:stonecutter/sandstone_road_remove_curb[stonecutting]'! Falling back to vanilla: ItemStack 'result' can't be empty!
Failed to parse recipe 'caupona:stonecutter/stone_road_remove_curb[stonecutting]'! Falling back to vanilla: ItemStack 'result' can't be empty!
Failed to parse recipe 'caupona:stonecutter/felsic_tuff_road_remove_curb[stonecutting]'! Falling back to vanilla: ItemStack 'result' can't be empty!
```

## Causa

Confirmada pela inspeção dos três JSONs dentro do JAR: o campo `result` é um objeto com `id`, formato usado por versões mais novas do Minecraft (1.20.5+):

```json
{
  "type": "stonecutting",
  "ingredient": { "item": "caupona:stone_road_side" },
  "result": { "id": "caupona:stone_road" },
  "count": 1
}
```

A 1.20.1 espera uma string (`"result": "caupona:stone_road"`). O KubeJS lê o resultado como vazio e a receita não é carregada. É um defeito do próprio JAR do mod.

## Solução aplicada

Override por datapack em `kubejs/data/caupona/recipes/stonecutter/`, com os mesmos nomes dos originais, usando `result` como string:

| Arquivo | Ingrediente | Resultado |
|---|---|---|
| `stone_road_remove_curb.json` | `caupona:stone_road_side` | `caupona:stone_road` |
| `sandstone_road_remove_curb.json` | `caupona:sandstone_road_side` | `caupona:sandstone_road` |
| `felsic_tuff_road_remove_curb.json` | `caupona:felsic_tuff_road_side` | `caupona:felsic_tuff_road` |

```json
{
  "type": "minecraft:stonecutting",
  "ingredient": { "item": "caupona:stone_road_side" },
  "result": "caupona:stone_road",
  "count": 1
}
```

Comandos: [runbook, seção 13](../maintenance/reapply-fix-commands.md).

## Backup

Não há: os três arquivos são novos e nenhum arquivo existente foi alterado.

## Validação

Após `/reload` ou reinicialização:

```bash
grep -i 'Failed to parse recipe.*caupona' logs/latest.log   # sem saída
```

Resultado: sem saída nos boots seguintes à criação dos arquivos.

Limites da validação:

- Confirma só que o erro de parsing deixou de aparecer. **Não** houve teste de conversão na pedra de corte.
- A existência dos itens `*_road` e `*_road_side` não foi verificada diretamente; como não há erro de resultado vazio, presume-se que existam.
- Efeito no jogo: receitas que antes não carregavam passam a existir.

## Rollback

```bash
sudo rm kubejs/data/caupona/recipes/stonecutter/*_road_remove_curb.json
```

## Atenção a atualizações

Se uma versão futura do Caupona corrigir o formato do `result`, os overrides deixam de ser necessários e podem ser removidos.
