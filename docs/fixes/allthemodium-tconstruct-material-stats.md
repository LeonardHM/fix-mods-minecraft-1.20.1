# Correção: stats de materiais do AllTheModium incompatíveis com o Tinkers' Construct

**Status:** aplicada e validada após reinicialização (uso no jogo não testado)  
**Ambiente:** Arclight / Forge 1.20.1, Forge 47.4.10, Java 17 (Amazon Corretto)  
**Data do registro:** 2026-11-11

## Erro original

```
[main/ERROR] [slimeknights.tconstruct.library.materials.stats.MaterialStatsManager/]: Skipping unregistered material stat type 'tconstruct:extra' for material 'allthemodium:unobtainium'. This likely indicates a broken mod or datapack.
[main/ERROR] [slimeknights.tconstruct.library.materials.stats.MaterialStatsManager/]: Skipping unregistered material stat type 'tconstruct:extra' for material 'allthemodium:allthemodium'. This likely indicates a broken mod or datapack.
[main/ERROR] [slimeknights.tconstruct.library.materials.stats.MaterialStatsManager/]: Skipping unregistered material stat type 'tconstruct:extra' for material 'allthemodium:vibranium'. This likely indicates a broken mod or datapack.
```

## Mods e versões

| Mod | Arquivo |
|---|---|
| AllTheModium (alterado) | `allthemodium-1.20.1-47.1.25-2.5.8.jar` |
| Tinkers' Construct | `TConstruct-1.20.1-3.12.1.231.jar` |
| Tinkers' Levelling Addon (presente, não envolvido) | `TinkersLevellingAddon-1.20.1-1.5.0.jar` |

## Causa

Confirmado:

- O AllTheModium define os stats dos três materiais em `data/allthemodium/tinkering/materials/stats/{unobtainium,vibranium,allthemodium}.json`, e os três declaram `tconstruct:extra`. Valores vistos: unobtainium `extra.durability` = 2450, vibranium = 2050; o valor em `allthemodium.json` não foi registrado.
- O Tinkers' Construct 3.12.1.231 informa, no próprio log, que `tconstruct:extra` não é um tipo de stat registrado e ignora a entrada.

Inferência (não confirmada em changelog do Tinkers): o tipo passou a se chamar `tconstruct:binding`. Indício: em `data/tconstruct/tinkering/materials/stats/cobalt.json` do JAR do Tinkers aparece `"tconstruct:binding": {}` e não há `tconstruct:extra`.

Consequência: antes da correção o Tinkers já descartava essas entradas; o erro era o aviso desse descarte.

## Solução aplicada

Nos três JSONs de stats **dentro do JAR do AllTheModium**, remover `tconstruct:extra` e acrescentar `"tconstruct:binding": {}` (vazio, como no `cobalt.json`). Os demais stats (`head`, `handle`) ficaram como estavam. A durabilidade que estava em `extra` deixa de constar.

Comandos: [runbook, seção 8](../maintenance/reapply-fix-commands.md) e `scripts/patch_allthemodium_stats.py`.

> O que foi executado originalmente no servidor foi um heredoc Python equivalente. O script do repositório foi escrito depois, com a mesma lógica; foi testado apenas em um JAR sintético, não no JAR real do AllTheModium.

## Tentativa que não funcionou

Datapack `world/datapacks/atm_fix` com os mesmos JSONs corrigidos em `data/allthemodium/tinkering/materials/stats/`.

- O datapack foi carregado (`Found new data pack file/atm_fix, loading it automatically`).
- Mesmo assim, as três mensagens de `tconstruct:extra` continuaram no log da mesma inicialização.
- A causa de o override não ter efeito **não foi confirmada**. Hipótese: o Tinkers combina os stats de todas as fontes em vez de substituir o arquivo do JAR.
- O datapack foi removido (`sudo rm -rf world/datapacks/atm_fix`).

## Backup

Cópia do JAR original antes da alteração: `~/allthemodium-2.5.8.jar.bak` (diretório home de quem executou o comando, no servidor). O script do repositório cria `<jar>.original` ao lado do JAR.

## Validação

Após reiniciar o servidor:

```bash
grep -c 'tconstruct:extra' logs/latest.log
```

Resultado: `0` (antes da correção: 3 linhas, uma por material).

Limites da validação:

- Confirma o desaparecimento do erro de carregamento. Não houve teste dentro do jogo.
- Não testado: se os materiais unobtainium, vibranium e allthemodium passam a poder ser usados em partes `binding` no Tinkers, e se isso é desejado.
- A saída do comando de alteração do JAR (linhas `patched`) não foi registrada; a validação é a busca no log.

## Atenção a atualizações

A alteração está dentro do JAR do AllTheModium. Atualizar o mod a desfaz. Antes de reaplicar, abrir os JSONs de stats da versão nova e conferir se ainda usam `tconstruct:extra`; se o mod já foi corrigido upstream, não reaplicar. Se o Tinkers' Construct for atualizado, conferir também se `tconstruct:binding` continua sendo o nome do tipo.
